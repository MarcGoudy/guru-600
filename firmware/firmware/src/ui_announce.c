/* SPDX-License-Identifier: GPL-3.0-only */
/* Guru-600 1.1: the screen reader (João Durães, Discussion #2): what the screen shows, for the FM-1 Screen Reader on
 * the computer (Charles Vestal's fm1-reader: its page speaks it, or hands it to the computer's own screen reader).
 * The protocol is announce.c's (fm1-base, MPL-2.0, as it is): SysEx F0 7D 53 52 over USB-MIDI; nothing is built or
 * sent while no reader listens (a DAW on the port never sees a byte), and nothing changes on the screen.
 * ui_draw notes each card it draws (ann_col: label, value, unit), then ann_ui says:
 *   a new place (a page, HOME, a MENU tab, a dialog, NAME, a layer): its title, then its four cards, at once (cutting
 *     off what was being said);
 *   a knob turned (the card just turned, ui.hot_col): its label and value once it has settled (300 ms);
 *   the track's sound when it changes (PRESETS, a MIDI program change, MORPH);
 *   the banner's messages (ui_say): as they come, heard whole (ANN_KEEP).
 * The reader's WHERE says the whole screen again. editor.c ed_service hands it the reader's frames and ticks it.
 * MENU > SCREEN OFF: nothing is drawn, so nothing is said until the screen wakes. */
static struct {
    char col[4][40];                                    /* the cards drawn this frame */
    uint8_t drawn, hot;                                 /* their mask; the menu's row (always "turned") */
    uint32_t where, knob[4], sound;                     /* hashes of what was said */
} annc;                                                 /* (.bss, zero at start; main loop only) */

/* ui_draw.c (draw_column, draw_column_tall, draw_act_column, the P600 panel's knobs): card c shows label, value, unit */
static void ann_col(uint32_t c, const char *label, const char *val, const char *unit)
{
    char *s;
    if (!ann_on() || c > 3u)
        return;
    s = annc.col[c];
    s[0] = 0;
    ann_cat(s, sizeof annc.col[c], label);
    ann_cat(s, sizeof annc.col[c], val);
    if (unit && !str_eq(unit, label ? label : ""))
        ann_cat(s, sizeof annc.col[c], unit);
    annc.drawn |= (uint8_t)(1u << c);
}

/* the place the screen shows: its words in s (what a new one says first) */
static void ann_place(char *s, uint32_t cap)
{
    char a[48], b[48];
    s[0] = 0;
    annc.hot = 0;
    if (ui.menu) {
        if (ui.menu != 1u) {
            ann_cat(s, cap, ui.menu == 3 ? "INFO" : "ABOUT");
            return;
        }
        ann_cat(s, cap, "MENU");
        ann_cat(s, cap, MTAB_NAME[menu_tab()]);
        annc.col[0][0] = 0;                             /* the row: as a card turned */
        ann_cat(annc.col[0], sizeof annc.col[0], MI_NAME[ui.menu_sel]);
        if (menu_valued(ui.menu_sel))
            ann_cat(annc.col[0], sizeof annc.col[0], menu_vname(ui.menu_sel, menu_get(ui.menu_sel)));
        annc.drawn = 1;
        annc.hot = 1;
        return;
    }
    if (ui.confirm) {
        confirm_text(a, b);
        ann_cat(s, cap, a);
        ann_cat(s, cap, b);
        ann_cat(s, cap, ". OCT+ YES, OCT- NO");
        return;
    }
    if (name_on()) {
        ann_cat(s, cap, "NAME");
        annc.col[0][0] = 0;
        ann_cat(annc.col[0], sizeof annc.col[0], nm.s[0] ? nm.s : "EMPTY");
        annc.drawn = 1;
        annc.hot = 1;
        return;
    }
    if (ui.layer) {
        const page_t *lp = ly_page(ui.layer);
        ann_cat(s, cap, "LAYER");
        ann_cat(s, cap, lp ? lp->title : "");
        return;
    }
    if (ui.home) {
        ann_cat(s, cap, "HOME");
        return;
    }
#if FELUCCA_P600
    if (p6ui_page()) {
        ann_cat(s, cap, p6ui_page()->title);
        return;
    }
#endif
    page_title(a);
    ann_cat(s, cap, a);
}

/* after each frame (ui_draw) */
static void ann_ui(void)
{
    char s[ANN_MAX + 1u], pn[24];
    uint32_t c, h, hs, w;
    if (!ann_on()) {
        annc.drawn = 0;
        return;
    }
    ann_place(s, sizeof s);
    h = str_hash(ui.menu * 7u + ui.confirm * 131u + ui.layer * 1009u + ui.home, s);
    pn[0] = (char)('1' + song.sel);                     /* the track and its sound: "TRACK 1, 3 BRASS" */
    pn[1] = ',';
    pn[2] = ' ';
    sound_name(TSEL, pn + 3);
    hs = str_hash(7u, pn);
    w = (uint32_t)ann_where();
    if (w || h != annc.where) {                         /* a new place: its title and its cards (the track and its
                                                         * sound too when they changed, or the reader asked) */
        annc.where = h;
        if (!ui.menu && !ui.confirm && !name_on() && (w || hs != annc.sound)) {
            ann_cat(s, sizeof s, ",");
            ann_cat(s, sizeof s, "TRACK");
            ann_cat(s, sizeof s, pn);
        }
        annc.sound = hs;
        for (c = 0; c < 4u; c++)
            if ((annc.drawn >> c) & 1u) {
                ann_cat(s, sizeof s, ",");
                ann_cat(s, sizeof s, annc.col[c]);
                annc.knob[c] = str_hash(c, annc.col[c]);
            }
        ann_say(s, 0, ANN_NOW);
    } else {
        for (c = 0; c < 4u; c++) {                      /* a knob turned: once it settles */
            if (!((annc.drawn >> c) & 1u) || str_hash(c, annc.col[c]) == annc.knob[c])
                continue;
            annc.knob[c] = str_hash(c, annc.col[c]);
            if (annc.hot || (c == ui.hot_col && ui.hot_t))
                ann_later(annc.col[c], ANN_NOW, 300u, fm1_ms);
        }
        if (hs != annc.sound && !ui.menu && !ui.confirm && !name_on()) {
            annc.sound = hs;
            s[0] = 0;
            ann_cat(s, sizeof s, "TRACK");
            ann_cat(s, sizeof s, pn);
            ann_later(s, ANN_NOW, 300u, fm1_ms);
        }
    }
    annc.drawn = 0;
}
