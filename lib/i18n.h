/**
 * UxPlay i18n (Chinese localization) -- 中文本地化支持
 *
 * Copyright (C) 2026 FoolishWiser
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * How it works:
 *   Every user-facing message is written in English in the source, wrapped in
 *   _("...")  (or passed through tr() by the logging helpers).  The Chinese
 *   translation of every message lives in lib/i18n_zh.inc, a sorted table of
 *   {english, chinese} pairs generated from i18n/catalog.jsonl by
 *   "python3 i18n/tool.py build".  When the language is Chinese, tr() looks the message
 *   up and returns the translation; otherwise (or when a message has not been
 *   translated yet) the original English text is returned unchanged.
 *
 * Language selection (highest priority first):
 *   1. command line option "-zh" / "--zh"  or  "-en" / "--en"
 *   2. environment variable UXPLAY_LANG=zh|en
 *   3. LC_ALL / LC_MESSAGES / LANG starting with "zh"
 */

#ifndef UXPLAY_I18N_H
#define UXPLAY_I18N_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    UXPLAY_LANG_AUTO = 0,   /* detect from the environment */
    UXPLAY_LANG_EN   = 1,
    UXPLAY_LANG_ZH   = 2
} uxplay_lang_t;

/* Initialise the language.  May be called again later (e.g. when "-zh" is
 * found on the command line); later calls simply override the setting. */
void i18n_init(uxplay_lang_t lang);

/* 1 when messages are shown in Chinese, 0 for English. */
int i18n_is_zh(void);

/* "zh" or "en" */
const char *i18n_lang_name(void);

/* Translate one message id (the English text) into the current language.
 * Returns the input pointer unchanged when no translation is available. */
const char *tr(const char *msgid);

/* Number of entries in the translation catalog (used by the self-test). */
size_t i18n_catalog_count(void);

/* Translation table entry access, for tools/tests. */
const char *i18n_catalog_en(size_t i);
const char *i18n_catalog_zh(size_t i);

#ifdef __cplusplus
}
#endif

/* Short marker used at the call sites:  printf(_("Usage: %s ...\n"), name); */
#ifndef _
#define _(msgid) tr(msgid)
#endif

#endif /* UXPLAY_I18N_H */
