/* La sauvegarde complète de l'éditeur (editor_backup.c) rend la machine telle qu'elle était, même après un autre
 * firmware qui aurait tout effacé (Felucca construit pour l'hôte : sa flash simulée, web/emu/felucca_web.c).
 * 1. allumage ; 2. trois places P600 remplies, gardées en flash ; une banque de voix FM6 (trois voix) ;
 * 3. sauvegarde (LIST puis GET de chaque objet) ; 4. « un autre firmware » : toute la flash effacée, la RAM reprise
 *    à l'allumage ; 5. restauration (PUT de chaque objet, dans l'ordre de l'éditeur : fm1backup.js restoreBackup) ;
 * 6. les places et la banque sont revenues, et le restent après un rallumage ; 7. une sauvegarde sans banque, rendue
 *    sur une machine qui en a une : la banque part.
 *   cc -O1 -w -IFelucca/build/gen -IFelucca/firmware/src -IFelucca/web/emu -o build/p600_backup_test \
 *      p600/tests/p600_backup_test.c -lm   (depuis ~/Documents/FM-1) */
#include "felucca_web.c"

/* what editor.c gives editor_backup.c (as Felucca's tests/backup_test.c) */
#undef __attribute__
#define __attribute__(x)                               /* (hostsim.c: no sections on the host) */
enum { ED_BACKUP_LIST = 65, ED_BACKUP_GET, ED_BACKUP_PUT };
static uint8_t rep[4096];
static uint32_t rep_n;
static void ed_b(uint32_t v) { if (rep_n < sizeof rep) rep[rep_n++] = (uint8_t)(v & 127u); }
static uint32_t ed_unpack7(const uint8_t *a, uint32_t na, uint8_t *out, uint32_t max)
{
    uint32_t n = 0;
    while (na && n < max) {
        uint32_t m = *a++, j;
        na--;
        uint32_t k = na > 7u ? 7u : na;
        if (!k || n + k > max || (m >> k))
            return 0;
        for (j = 0; j < k; j++, na--)
            out[n++] = (uint8_t)(*a++ | ((m >> j) & 1u) << 7);
    }
    return na ? 0u : n;
}
static uint8_t ed_smp_buf[512] __attribute__((aligned(4)));
static int ed_flash_stop(void) { return transport_busy(); }
#include "../../Felucca/firmware/src/editor_backup.c"

static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static int check(const char *what, int ok)
{
    printf("p600 backup: %-84s %s\n", what, ok ? "ok" : "FAIL");
    return !ok;
}
static uint32_t call(uint32_t cmd, const uint8_t *a, uint32_t n)
{
    rep_n = 0;
    ed_backup_handle(cmd, a, n);
    return rep_n;
}
static void put32(uint8_t *a, uint32_t v) { for (uint32_t i = 0; i < 5u; i++) a[i] = (uint8_t)((v >> (7u * i)) & 127u); }

/* the archive: each object's bytes, as captureBackup takes them */
static uint8_t obj[64][4096];
static uint32_t obj_len[64], obj_n;
static uint8_t obj_id[64];

static int capture(void)
{
    uint32_t i, off;
    call(ED_BACKUP_LIST, 0, 0);
    if (rep[0] != 1u || rep[1] || rep[2] != ED_BK_N)
        return -1;
    obj_n = rep[2];
    {
        static uint8_t man[512];
        memcpy(man, rep, rep_n);
        for (i = 0; i < obj_n; i++) {
            const uint8_t *o = man + 3 + i * 11u;
            obj_id[i] = o[0];
            obj_len[i] = ed_bk_r32(o + 1);
            if (o[0] >= 32u)                                  /* (the samples: none here, by their own commands) */
                continue;
            for (off = 0; off < obj_len[i]; off += 256u) {
                uint8_t a[8] = {o[0]};
                uint32_t c = obj_len[i] - off > 256u ? 256u : obj_len[i] - off;
                put32(a + 1, off);
                a[6] = (uint8_t)(c & 127u);
                a[7] = (uint8_t)(c >> 7);
                call(ED_BACKUP_GET, a, sizeof a);
                if (rep[1] || ed_unpack7(rep + 9, rep_n - 9u, obj[i] + off, c) != c)
                    return -2;
            }
            if (st_crc32(obj[i], obj_len[i]) != ed_bk_r32(o + 6))
                return -3;
        }
    }
    return 0;
}
static uint32_t put(uint32_t id, const uint8_t *p, uint32_t len)
{
    uint8_t a[16 + 300];
    uint32_t off, rc;
    a[0] = 0; a[1] = (uint8_t)id;
    put32(a + 2, len);
    put32(a + 7, st_crc32(p, len));
    call(ED_BACKUP_PUT, a, 12);
    if ((rc = rep[2]) != 0)
        return rc;
    for (off = 0; off < len; off += 256u) {
        uint32_t n = len - off > 256u ? 256u : len - off, k = 7, g, i, m;
        const uint8_t *q = p + off;
        a[0] = 1; a[1] = (uint8_t)id;
        put32(a + 2, off);
        while (n) {
            g = n > 7u ? 7u : n;
            for (m = 0, i = 0; i < g; i++) m |= (uint32_t)(q[i] >> 7) << i;
            a[k++] = (uint8_t)m;
            for (i = 0; i < g; i++) a[k++] = q[i] & 127u;
            q += g; n -= g;
        }
        call(ED_BACKUP_PUT, a, k);
        if ((rc = rep[2]) != 0)
            return rc;
    }
    a[0] = 2; a[1] = (uint8_t)id;
    call(ED_BACKUP_PUT, a, 2);
    return rep[2];
}
/* fm1backup.js restoreBackup's order: everything after the current music and the settings, then the settings, then
 * the music; the first failing rc */
static uint32_t restore(void)
{
    uint32_t i, rc;
    for (i = 2; i < obj_n; i++)
        if (obj_id[i] < 32u && (rc = put(obj_id[i], obj[i], obj_len[i])) != 0)
            return 100u + obj_id[i] * 10u + rc;
    if ((rc = put(obj_id[1], obj[1], obj_len[1])) != 0)
        return 110u + rc;
    return put(obj_id[0], obj[0], obj_len[0]);
}
static long load(const char *path, void *dst, long max)
{
    FILE *f = fopen(path, "rb");
    long n;
    if (!f) return -1;
    n = (long)fread(dst, 1, (size_t)max, f);
    fclose(f);
    return n;
}
static uint8_t slot0[SMP_USER_SIZE];                   /* the sample of user slot 1, as the editor's file holds it */
static void power_on_ram(void)                         /* the RAM as at power-on, from the flash as it is */
{
    memset(p6_imp, 0, sizeof p6_imp);
    p6_booted = 0;
    ENG_P600.presets = P600_PRESETS;
    ENG_P600.npresets = P600_NFIX;
    p600_boot();
    fvb_boot();
    memset(slc_man, 0, sizeof slc_man);
    slc_store_boot();
    smp_user_scan(0);
}

int main(void)
{
    static p6imp_t want[P6_NIMP];
    static uint8_t bank[FVB_LEN];
    uint8_t pk[FM6_PACKED];
    uint32_t i, k, c = 0xFFFFFFFFu, used = 0, rc;
    int bad = 0;
    web_nor_erase();
    web_boot();
    run(8000);

    /* the places: three of them, with values of their own, kept in flash as the device keeps them */
    for (i = 0; i < 3u; i++) {
        p6imp_t *m = &p6_imp[i];
        memset(m, 0, sizeof *m);
        m->dest = (uint8_t)(i == 0 ? 6u : i == 1 ? 150u : 210u);
        m->used = 1;
        for (k = 0; k < 8u; k++) m->e[k] = (int8_t)(10 + i * 20 + k);
        for (k = 0; k < 4u; k++) m->env[k] = (uint8_t)(30 + i + k);
        snprintf(m->name, sizeof m->name, "BACKUP %u", i + 1u);
    }
    p600_apply();
    p6_dirty = 1;
    p6_dirty_ms = fm1_ms;
    run(3000);
    memcpy(want, p6_imp, sizeof want);
    bad += check("three places kept in flash", st_load(OBJ_P600, &p6st, sizeof p6st) == (int)sizeof p6st);

    /* the FM6 voice bank: voices 1, 6 and 32 */
    bad += check("an FM6 voice bank begins", fvb_begin() == 0);
    for (k = 0; k < FM6_NBANK; k++)
        if (k == 0 || k == 5 || k == 31) {
            for (i = 0; i < FM6_PACKED; i++) pk[i] = (uint8_t)((i * 7u + k * 13u) & 127u);
            fvb_write(k, pk);
            c = st_crc32_add(c, pk, FM6_PACKED);
            used |= 1u << k;
        }
    bad += check("the bank written (three voices)", fvb_end((const uint8_t *)"TESTBANK  ", ~c) == 0 && fm6_bank_used == used);
    st_read(FVB_HOME + FVB_INFO, bank, FVB_LEN);

    /* SLICE: a loop in user slot 1 (Felucca's build/slice_demo/loop), its MAN slices set and kept */
    {
        uint8_t *sl = nor + SMP_USER_BASE;
        long h = load("Felucca/build/slice_demo/loop.hdr", sl, SMP_USER_DATA);
        long d = load("Felucca/build/slice_demo/loop.bin", sl + SMP_USER_DATA, SLC_REC_OFF - SMP_USER_DATA);
        slc_man_t *m;
        bad += check("a loop in user slot 1", h == (long)sizeof(smp_user_hdr_t) && d > 0);
        smp_user_scan(0);
        m = slc_man_begin(0);                          /* (AUTO's slices) */
        if (m->n > 5u) m->n = 5u;
        slc_man_commit(0);
        bad += check("its MAN slices kept in the slot's last sector", usr_nz[0] && slc_rec_room(0) && slc_store_write(0) == 3);
        memcpy(slot0, sl, SLC_REC_OFF);                /* (the sample, without the record: the editor's file) */
    }
    slc_rec_t slw;
    slc_rec_make(0, &slw);

    /* and a project in slot B, the music of the moment */
    trk[0].step[3] = (step_t){{64}, 1, ST_NOTE, 0, 100, 0, 0};
    project_save(1);
    run(2000);
    {   /* every stored object's payload, to compare after the restore */
        static uint8_t pay[OBJ_COUNT][ST_PAYLOAD_MAX];
        static int plen[OBJ_COUNT];
        for (k = 0; k < OBJ_COUNT; k++)
            if (k != OBJ_AUTOSAVE && k != OBJ_FM6BANK)
                plen[k] = st_load(k, pay[k], ST_PAYLOAD_MAX);

    /* 3. the backup */
    rc = (uint32_t)-capture();
    bad += check("the backup: 16 objects, every one read back with its CRC", rc == 0 && obj_n == 16u);
    for (i = 0; i < obj_n; i++) {
        if (obj_id[i] == 10u) bad += check("id 10, the places: the whole table", obj_len[i] == sizeof(p6st_t));
        if (obj_id[i] == 11u) bad += check("id 11, the bank: its payload, byte for byte",
                                           obj_len[i] == FVB_LEN && !memcmp(obj[i], bank, FVB_LEN));
        if (obj_id[i] == 12u) bad += check("id 12, the slices: three records", obj_len[i] == 3u * sizeof(slc_rec_t));
    }

    /* 4. another firmware: the whole flash erased; the RAM as at power-on */
    memset(nor, 0xFF, sizeof nor);
    power_on_ram();
    bad += check("after the other firmware: no place, no bank", p6_find(6) < 0 && p6_find(150) < 0 && !fvb_info());

    /* 5. the restore, 6. the machine as it was (the sample first, as the editor's SMP commands write it) */
    memcpy(nor + SMP_USER_BASE, slot0, SLC_REC_OFF);
    smp_user_scan(0);
    bad += check("the sample is back without its slices", usr_nz[0] && !slc_man_of(slc_get(1)));
    {   /* this unit wired otherwise (its CALIBRATION): kept by the restore */
        uint8_t x = panel.btn[0];
        panel.btn[0] = panel.btn[1];
        panel.btn[1] = x;
    }
    panel_t mine = panel;
    rc = restore();
    bad += check("the restore: every object accepted", rc == 0);
    {
        persist_t ps;
        bad += check("the unit keeps its own CALIBRATION, in use and saved", !memcmp(&panel, &mine, sizeof mine) &&
                     st_load(OBJ_SETTINGS, &ps, sizeof ps) == (int)sizeof ps && !memcmp(&ps.panel, &mine, sizeof mine));
        panel = PANEL_DEFAULT;                         /* (the rest of the test: the backup's, as before) */
        ps.panel = panel;
        st_save(OBJ_SETTINGS, &ps, sizeof ps);
    }
    bad += check("the three places are back, byte for byte", !memcmp(p6_imp, want, sizeof want));
    bad += check("place 7 plays its kept sound again", !strcmp(ENG_P600.presets[6].name, "BACKUP 1") &&
                 ENG_P600.presets[6].e[0] == 10);
    bad += check("the bank is back: its voices and its name", fm6_bank_used == used && fvb_info() &&
                 !memcmp(fvb_info()->name, "TESTBANK  ", 10));
    st_read(FVB_HOME + FVB_INFO, pk, 0);
    {
        static uint8_t now[FVB_LEN];
        st_read(FVB_HOME + FVB_INFO, now, FVB_LEN);
        bad += check("the bank's payload in flash, byte for byte", !memcmp(now, bank, FVB_LEN));
    }
    {
        slc_rec_t now;
        slc_rec_make(0, &now);
        bad += check("the MAN slices are back, in use and in the slot's record",
                     slc_man_of(slc_get(1)) && !memcmp(&now, &slw, sizeof now) &&
                     !memcmp(nor + SMP_USER_BASE + SLC_REC_OFF, &slw, sizeof slw));
    }
    power_on_ram();
    bad += check("after a power-on: the slices are read back from the slot", slc_man_of(slc_get(1)) &&
                 slc_man_of(slc_get(1))->n == slw.n);
    bad += check("after a power-on: the places and the bank are still there",
                 !memcmp(p6_imp, want, sizeof want) && fm6_bank_used == used);
    {
        static uint8_t now[ST_PAYLOAD_MAX];
        int same = 1;
        for (k = 0; k < OBJ_COUNT; k++)
            if (k != OBJ_AUTOSAVE && k != OBJ_FM6BANK) {
                int n = st_load(k, now, ST_PAYLOAD_MAX);
                if (plen[k] <= 0 && (n <= 0 || k == OBJ_SETTINGS || k == OBJ_UPFM6))
                    continue;                          /* (none before: the defaults; now none, or the defaults written) */
                if (n != plen[k] || (n > 0 && memcmp(now, pay[k], (size_t)n))) { same = 0; printf("  object %u differs: %d then %d bytes\n", k, plen[k], n); }
            }
        bad += check("every stored object (settings, projects, user presets, FM6 patches, places) as before", same &&
                     plen[OBJ_PROJECT0 + 1] > 0);
        bad += check("the music of the moment: the step set before the backup", trk[0].step[3].note[0] == 64);
    }
    }

    /* 7. a backup without a bank (nor any place), restored onto a machine that has both: they go */
    memset(nor, 0xFF, sizeof nor);
    power_on_ram();
    bad += check("a fresh machine: a backup of it", capture() == 0);
    memcpy(p6_imp, want, sizeof want);
    p600_apply();
    p6_dirty = 1; p6_dirty_ms = fm1_ms;
    run(3000);
    fvb_begin();
    for (i = 0; i < FM6_PACKED; i++) pk[i] = (uint8_t)(i & 127u);
    fvb_write(3, pk);
    c = st_crc32_add(0xFFFFFFFFu, pk, FM6_PACKED);
    fvb_end((const uint8_t *)"OTHER     ", ~c);
    rc = restore();
    bad += check("restored: no place, no bank left", rc == 0 && p6_find(6) < 0 && !fvb_info() && !fm6_bank_used);
    power_on_ram();
    bad += check("after a power-on: still none", p6_find(6) < 0 && !fvb_info());

    printf(bad ? "P600 BACKUP TEST FAILED (%d)\n" : "p600 backup test passed\n", bad);
    return bad ? 1 : 0;
}
