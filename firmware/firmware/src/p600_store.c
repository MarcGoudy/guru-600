/* SPDX-License-Identifier: GPL-3.0-only */
/* P600: the imported programs kept in flash (eng_p600.c p6_imp; storage.c OBJ_P600, A/B at 0xD9000 / 0xDA000, the 3rd
 * user sample slot's 18th and 19th sectors: eng_sample.c SMP_SLOT_END). Saved by st_save (a commit record and a CRC, the
 * copy that is not the current one: a power cut keeps the old set or the new one, never half of one), 1.5 s after the
 * last change and only while stopped (as the settings); read back once at power-on, before the first sound loads.
 * A 3rd sample slot written by an older build may run into those sectors: then nothing is kept (imports for the session
 * only) and the sample stays whole */
#define P6ST_STORE 1                                   /* (editor_backup.c: the places' object, OBJ_P600) */
_Static_assert(sizeof(p6st_t) <= ST_PAYLOAD_MAX, "the imports fit a sector");   /* (p6st_t, p6st: eng_p600.c) */
static uint8_t p6st_ok;                                /* the sectors are ours (not the 3rd sample's) */

static void p600_boot(void)
{
    const smp_user_hdr_t *h = (const smp_user_hdr_t *)smp_user_xip(2);
    uint32_t i;
    p6st_ok = !(h->magic == SMP_USER_MAGIC && h->data_len > SMP_SLOT_END(2u) - SMP_USER_DATA);
    if (p6st_ok && st_load(OBJ_P600, &p6st, sizeof p6st) == (int)sizeof p6st && p6st.magic == P6ST_MAGIC &&
        p6st.ver == 1u && p6st.n == P6_NIMP)       /* (read straight into the places: p6_imp is p6st.imp) */
        for (i = 0; i < P6_NIMP; i++) {
            p6_imp[i].name[15] = 0;
            if (p6_imp[i].dest > 254u || p6_imp[i].used > 1u)
                p6_imp[i].used = 0;
        }
    else
        memset(&p6st, 0, sizeof p6st);                 /* (none kept, or a partial read: no place) */
    p6_booted = 1;
    p6_dirty = 0;
    p600_apply();
}

static void p600_store_poll(void)                      /* main loop */
{
    if (!p6_dirty || fm1_ms - p6_dirty_ms < 1500u || song.playing || !p6st_ok)
        return;
    p6_dirty = 0;
    p6st.magic = P6ST_MAGIC;
    p6st.ver = 1u;
    p6st.n = P6_NIMP;
    if (st_save(OBJ_P600, &p6st, sizeof p6st))
        ui_message("P600: NOT SAVED");
}
