/**
 * UxPlay i18n (Chinese localization) -- implementation
 *
 * Copyright (C) 2026 FoolishWiser
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * The translation table itself lives in lib/i18n_zh.inc, which is generated
 * from the JSONL files in locale/ by tools/gen_catalog.py.  Keeping it in a separate
 * generated include means translators never have to touch C code.
 */

#include <stdlib.h>
#include <string.h>

#include "i18n.h"

typedef struct {
    const char *en;
    const char *zh;
} i18n_entry_t;

static const i18n_entry_t i18n_catalog[] = {
#include "i18n_zh.inc"
};

#define I18N_CATALOG_COUNT (sizeof(i18n_catalog) / sizeof(i18n_catalog[0]))

static uxplay_lang_t current_lang = UXPLAY_LANG_AUTO;
static int lang_is_zh = 0;

/* Does an environment value select Chinese / English?  Returns
 * -1 when the value says nothing about it. */
static int lang_from_env_value(const char *value) {
    if (value == NULL || *value == '\0') return -1;
    if ((value[0] == 'z' || value[0] == 'Z') &&
        (value[1] == 'h' || value[1] == 'H')) return UXPLAY_LANG_ZH;
    if ((value[0] == 'e' || value[0] == 'E') &&
        (value[1] == 'n' || value[1] == 'N')) return UXPLAY_LANG_EN;
    return -1;
}

/* Decide the language when the caller did not force one. */
static uxplay_lang_t detect_lang(void) {
    int l = lang_from_env_value(getenv("UXPLAY_LANG"));
    if (l >= 0) return (uxplay_lang_t)l;

    static const char *const locale_vars[] = {"LC_ALL", "LC_MESSAGES", "LANG"};
    for (size_t i = 0; i < sizeof(locale_vars) / sizeof(locale_vars[0]); i++) {
        l = lang_from_env_value(getenv(locale_vars[i]));
        if (l >= 0) return (uxplay_lang_t)l;
    }
    return UXPLAY_LANG_EN;
}

void i18n_init(uxplay_lang_t lang) {
    if (lang == UXPLAY_LANG_AUTO) lang = detect_lang();
    if (lang != UXPLAY_LANG_EN && lang != UXPLAY_LANG_ZH) lang = UXPLAY_LANG_EN;
    current_lang = lang;
    lang_is_zh = (lang == UXPLAY_LANG_ZH);
}

int i18n_is_zh(void) {
    return lang_is_zh;
}

const char *i18n_lang_name(void) {
    return lang_is_zh ? "zh" : "en";
}

const char *tr(const char *msgid) {
    if (msgid == NULL || !lang_is_zh) return msgid;

    size_t lo = 0;
    size_t hi = I18N_CATALOG_COUNT;
    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;
        int c = strcmp(i18n_catalog[mid].en, msgid);
        if (c == 0) return i18n_catalog[mid].zh;
        if (c < 0) lo = mid + 1;
        else hi = mid;
    }
    /* not translated yet: keep the original English text */
    return msgid;
}

size_t i18n_catalog_count(void) {
    return I18N_CATALOG_COUNT;
}

const char *i18n_catalog_en(size_t i) {
    return (i < I18N_CATALOG_COUNT) ? i18n_catalog[i].en : NULL;
}

const char *i18n_catalog_zh(size_t i) {
    return (i < I18N_CATALOG_COUNT) ? i18n_catalog[i].zh : NULL;
}
