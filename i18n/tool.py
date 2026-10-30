#!/usr/bin/env python3
"""Translation maintenance tool for the Simplified-Chinese UxPlay fork.

Usage (from the repository root):

    python3 i18n/tool.py build    # i18n/catalog.jsonl -> lib/i18n_zh.inc
    python3 i18n/tool.py check    # report msgids used in the sources but missing
                                  # from the catalog (and stale catalog entries)
    python3 i18n/tool.py extract  # dump every translatable msgid as JSON lines

The runtime lookup table lib/i18n_zh.inc must be sorted by the bytes of the
English msgid (lib/i18n.c uses bsearch on strcmp order); `build` sorts it and
verifies that the result really is strictly increasing.

Only the directory / file layout of this repository is assumed, so the tool
keeps working after `git merge upstream/master`.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                     # repository root
CATALOG = os.path.join(HERE, "catalog.jsonl")
IGNORED = os.path.join(HERE, "untranslated.jsonl")
OUT = os.path.join(ROOT, "lib", "i18n_zh.inc")

SPEC_RE = re.compile(
    r"%(?:%|[-+ #0']*(?:\d+|\*)?(?:\.(?:\d+|\*))?(?:hh|h|ll|l|j|z|t|L)?[diouxXeEfgGaAcsp])")
IDENT_RE = re.compile(r"[A-Za-z_]\w*")
SRC_GLOBS = ["uxplay.cpp", "lib/*.c", "renderers/*.c", "lib/*.cpp"]
PRINTF_FNS = {"printf", "fprintf", "sprintf", "snprintf", "vprintf", "vfprintf",
              "g_print", "g_printerr"}
LOG_MACROS = {"LOGD", "LOGI", "LOGW", "LOGE"}
DEBUG_RE = re.compile(r"LOGGER_DEBUG|DEBUG_DATA|\bDEBUG\b")

ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'",
           "a": "\a", "b": "\b", "f": "\f", "v": "\v", "?": "?", "0": "\0"}


def unescape(raw):
    """Decode a C string literal body (as written between the quotes)."""
    out, i, n = [], 0, len(raw)
    while i < n:
        c = raw[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:
            break
        c = raw[i]
        if c == "x":
            m = re.match(r"[0-9A-Fa-f]+", raw[i + 1:])
            if m:
                out.append(chr(int(m.group(0), 16) & 0x10FFFF))
                i += 1 + len(m.group(0))
                continue
        if c in "01234567":
            m = re.match(r"[0-7]{1,3}", raw[i:])
            out.append(chr(int(m.group(0), 8)))
            i += len(m.group(0))
            continue
        if c == "u":
            out.append(chr(int(raw[i + 1:i + 5], 16)))
            i += 5
            continue
        if c == "U":
            out.append(chr(int(raw[i + 1:i + 9], 16)))
            i += 9
            continue
        if c in ESCAPES:
            out.append(ESCAPES[c])
        else:
            out.append(c)
        i += 1
    return "".join(out)


def skip_string(s, i):
    """i points at the opening quote; return the index just past the closing quote."""
    i += 1
    while i < len(s):
        if s[i] == "\\":
            i += 2
            continue
        if s[i] == '"':
            return i + 1
        i += 1
    return i


def read_literals(s, i):
    """Read a (possibly concatenated) C string literal starting at i.

    Returns (end, [raw parts]) or (i, []) when s[i] does not start a literal.
    """
    parts, n = [], len(s)
    while True:
        j = i
        while j < n and s[j] in " \t\r\n":
            j += 1
        while j < n and s[j] == "\\" and j + 1 < n and s[j + 1] == "\n":
            j += 2                                   # backslash-newline splice
            while j < n and s[j] in " \t\r":
                j += 1
        if j < n and s[j] == '"':
            k = skip_string(s, j)
            parts.append(s[j + 1:k - 1])
            i = k
        else:
            return i, parts


def split_args(s, i):
    """i points at '('; return ([(start, end)], index_after_close_paren)."""
    assert s[i] == "(", s[i - 20:i + 20]
    n, depth, start, args = len(s), 0, i + 1, []
    i += 1
    while i < n:
        c = s[i]
        if c == '"':
            i = skip_string(s, i)
            continue
        if c == "'":
            i += 1
            while i < n and s[i] != "'":
                i += 2 if s[i] == "\\" else 1
            i += 1
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                args.append((start, i))
                return args, i + 1
            depth -= 1
        elif c == "," and depth == 0:
            args.append((start, i))
            start = i + 1
        i += 1
    return args, i


def literal_msgid(s, a, b):
    """If the source slice is nothing but C string literals, return the decoded text."""
    text = s[a:b]
    lead = len(text) - len(text.lstrip())
    end, parts = read_literals(text, lead)
    if not parts:
        return None
    if text[end:].strip():
        return None                                  # trailing expression -> not a pure literal
    return "".join(unescape(p) for p in parts)


SKIPPED = []          # calls whose format is not a pure literal (macro-built, e.g. "%"PRIu64)


def collect(paths):
    """Return {(msgid, is_debug)} -> [locations]."""
    found = {}
    del SKIPPED[:]
    for path in paths:
        src = open(path, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(path, ROOT)

        def loc(pos):
            return "%s:%d" % (rel, src.count("\n", 0, pos) + 1)

        # 1. explicit _("...") wrappers
        for m in re.finditer(r"(?<![\w>])_\(\s*", src):
            a = m.end()
            end, parts = read_literals(src, a)
            if parts:
                found.setdefault(("".join(unescape(p) for p in parts), False), []).append(loc(m.start()))
        # 2. printf family: first argument that is a pure literal
        for m in IDENT_RE.finditer(src):
            name = m.group(0)
            j = m.end()
            while j < len(src) and src[j] in " \t\r\n":
                j += 1
            if j >= len(src) or src[j] != "(":
                continue
            if name in PRINTF_FNS:
                args, _ = split_args(src, j)
                for a, b in args:
                    lit = literal_msgid(src, a, b)
                    if lit is None and src[a:b].lstrip().startswith('"'):
                        SKIPPED.append(loc(m.start()))
                    if lit is not None:
                        ctx = src[max(0, m.start() - 60):m.start()]
                        debug = "debug" in ctx.lower()
                        found.setdefault((lit, debug), []).append(loc(m.start()))
                        break
            elif name in LOG_MACROS:
                args, _ = split_args(src, j)
                if args:
                    lit = literal_msgid(src, *args[0])
                    if lit is not None:
                        found.setdefault((lit, name == "LOGD"), []).append(loc(m.start()))
            elif name == "logger_log":
                args, _ = split_args(src, j)
                if len(args) >= 3:
                    level = src[args[1][0]:args[1][1]]
                    lit = literal_msgid(src, *args[2])
                    if lit is None and src[args[2][0]:args[2][1]].lstrip().startswith('"'):
                        SKIPPED.append(loc(m.start()))
                    if lit is not None:
                        found.setdefault((lit, bool(DEBUG_RE.search(level))), []).append(loc(m.start()))
    return found


def sources():
    out = []
    for g in SRC_GLOBS:
        out += sorted(glob.glob(os.path.join(ROOT, g)))
    return out


def c_string(s):
    out = ['"']
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\r":
            out.append("\\r")
        elif ord(ch) < 0x20:
            out.append("\\%03o" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def load_catalog():
    entries, origin, errors = {}, {}, []
    with open(CATALOG, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append("catalog.jsonl:%d: bad json: %s" % (lineno, e))
                continue
            en, zh = obj.get("en"), obj.get("zh")
            if not en or not zh:
                errors.append("catalog.jsonl:%d: empty en or zh" % lineno)
                continue
            if SPEC_RE.findall(en) != SPEC_RE.findall(zh):
                errors.append("catalog.jsonl:%d: %% specifiers differ\n    en=%r\n    zh=%r"
                              % (lineno, en, zh))
                continue
            if en in entries and entries[en] != zh:
                errors.append("catalog.jsonl:%d: conflicting translation for %r" % (lineno, en))
                continue
            entries[en] = zh
            origin.setdefault(en, lineno)
    return entries, origin, errors


def cmd_build(args):
    entries, _, errors = load_catalog()
    if errors:
        print("ERRORS (%d):" % len(errors))
        for e in errors[:40]:
            print(" ", e)
        return 1
    items = sorted(entries.items(), key=lambda kv: kv[0].encode("utf-8"))
    prev = None
    for en, _ in items:
        if prev is not None and en.encode("utf-8") <= prev.encode("utf-8"):
            print("sortedness self-check failed at %r" % en)
            return 1
        prev = en
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("/* Generated by i18n/tool.py from i18n/catalog.jsonl -- do not edit.\n"
                " * %d entries.  Sorted by the bytes of the English text (strcmp order),\n"
                " * which is what the binary search in lib/i18n.c requires. */\n" % len(items))
        for en, zh in items:
            f.write("    { %s,\n      %s },\n" % (c_string(en), c_string(zh)))
    os.replace(tmp, OUT)
    print("wrote %s: %d entries" % (os.path.relpath(OUT, ROOT), len(items)))
    return 0


def load_ignored():
    """msgids that are deliberately kept in English (format fragments, caps names)."""
    out = {}
    if not os.path.exists(IGNORED):
        return out
    with open(IGNORED, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                obj = json.loads(line)
                out[obj["en"]] = obj.get("why", "")
    return out


def cmd_check(args):
    entries, _, errors = load_catalog()
    ignored = load_ignored()
    if errors:
        print("CATALOG ERRORS (%d):" % len(errors))
        for e in errors[:20]:
            print(" ", e)
        return 1
    found = collect(sources())
    visible = {m: l for (m, d), l in found.items() if not d}
    debug = {m: l for (m, d), l in found.items() if d}
    used = {m for m, _ in found}
    missing = sorted(m for m in visible if m not in entries and m not in ignored)
    debug_missing = sorted(m for m in debug if m not in entries)
    stale = sorted(en for en in entries if en not in used)
    ignored_used = sorted(m for m in ignored if m in used and m not in entries)
    ignored_covered = sorted(m for m in ignored if m in entries)
    ignored_unused = sorted(m for m in ignored if m not in used)
    print("sources: %d files, %d visible msgids, %d debug-only msgids"
          % (len(sources()), len(visible), len(debug)))
    print("catalog: %d entries" % len(entries))
    print("missing translations: %d visible, %d debug-only (debug is intentionally untranslated)"
          % (len(missing), len(debug_missing)))
    print("stale catalog entries: %d" % len(stale))
    print("skipped (format built from macros, cannot be looked up): %d at %s"
          % (len(SKIPPED), ", ".join(SKIPPED[:6]) or "-"))
    print("intentionally English: %d listed, %d used, %d unused, %d now translated"
          % (len(ignored), len(ignored_used), len(ignored_unused), len(ignored_covered)))
    for m in ignored_unused:
        print("  IGNORED-UNUSED %r" % m)
    for m in ignored_covered:
        print("  IGNORED-BUT-TRANSLATED %r" % m)
    for m in missing[:40]:
        print("  MISSING %r  at %s" % (m, ", ".join(visible[m][:3])))
    if len(missing) > 40:
        print("  ... and %d more" % (len(missing) - 40))
    for m in stale[:20]:
        print("  STALE   %r" % m)
    return 1 if (missing or stale or ignored_unused or ignored_covered) else 0


def cmd_extract(args):
    found = collect(sources())
    for msgid, is_debug in sorted(found, key=lambda k: k[0].encode("utf-8")):
        print(json.dumps({"en": msgid, "debug": is_debug, "at": found[(msgid, is_debug)][:3]},
                         ensure_ascii=False))
    return 0


def main(argv):
    table = {"build": cmd_build, "check": cmd_check, "extract": cmd_extract}
    if len(argv) != 2 or argv[1] not in table:
        print(__doc__)
        return 2
    return table[argv[1]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
