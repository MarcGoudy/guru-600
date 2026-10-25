/* La mémoire de l'application Guru-600 (flash.bin) et la sauvegarde de l'éditeur : ce que le firmware lui-même y lit.
 *   flash_capture make IMG          une mémoire remplie (places, banque FM6, découpes SLICE, son USER, projet), dans IMG
 *   flash_capture list IMG [JSON]   IMG au démarrage du firmware : la sauvegarde qu'il en fait (id, taille, CRC), et
 *                                   dans JSON le fichier que l'éditeur en tirerait
 *   (backup.rs, l'export et l'import de l'application, se compare à ces deux-là : p600/tests/app_backup_check.sh)
 *   cc -O1 -w -IFelucca/build/gen -IFelucca/firmware/src -IFelucca/web/emu -o p600/build/flash_capture \
 *      p600/tests/flash_capture.c -lm   (depuis ~/Documents/FM-1) */
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
static uint32_t call(uint32_t cmd, const uint8_t *a, uint32_t n)
{
    rep_n = 0;
    ed_backup_handle(cmd, a, n);
    return rep_n;
}
static void put32(uint8_t *a, uint32_t v) { for (uint32_t i = 0; i < 5u; i++) a[i] = (uint8_t)((v >> (7u * i)) & 127u); }

/* the archive: each object's bytes, as captureBackup takes them */
static uint8_t obj[64][0x14000];                     /* (a sample slot each, at most) */
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

static const char B64[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static void b64(FILE *f, const uint8_t *p, uint32_t n)
{
    uint32_t i;
    for (i = 0; i < n; i += 3) {
        uint32_t v = (uint32_t)p[i] << 16 | (i + 1 < n ? (uint32_t)p[i + 1] << 8 : 0) | (i + 2 < n ? p[i + 2] : 0);
        fputc(B64[v >> 18 & 63], f); fputc(B64[v >> 12 & 63], f);
        fputc(i + 1 < n ? B64[v >> 6 & 63] : '=', f); fputc(i + 2 < n ? B64[v & 63] : '=', f);
    }
}
int main(int argc, char **argv)
{
    uint32_t i, k;
    if (argc < 3) return 2;
    if (!strcmp(argv[1], "make")) {
        uint8_t pk[FM6_PACKED];
        uint32_t c = 0xFFFFFFFFu;
        FILE *f;
        web_nor_erase();
        web_boot();
        run(8000);
        for (i = 0; i < 3u; i++) {                         /* three places */
            p6imp_t *m = &p6_imp[i];
            memset(m, 0, sizeof *m);
            m->dest = (uint8_t)(i == 0 ? 6u : i == 1 ? 150u : 210u);
            m->used = 1;
            for (k = 0; k < 8u; k++) m->e[k] = (int8_t)(10 + i * 20 + k);
            for (k = 0; k < 4u; k++) m->env[k] = (uint8_t)(30 + i + k);
            snprintf(m->name, sizeof m->name, "APP %u", i + 1u);
        }
        p600_apply();
        p6_dirty = 1; p6_dirty_ms = fm1_ms;
        run(3000);
        fvb_begin();                                       /* a voice bank: voices 2 and 9 */
        for (k = 0; k < FM6_NBANK; k++)
            if (k == 1 || k == 8) {
                for (i = 0; i < FM6_PACKED; i++) pk[i] = (uint8_t)((i * 5u + k * 11u) & 127u);
                fvb_write(k, pk);
                c = st_crc32_add(c, pk, FM6_PACKED);
            }
        if (fvb_end((const uint8_t *)"APPBANK   ", ~c)) return 3;
        {                                                  /* a loop in user slot 2, its MAN slices kept */
            uint8_t *sl = nor + SMP_USER_BASE + SMP_USER_SIZE;
            slc_man_t *m;
            if (load("Felucca/build/slice_demo/loop.hdr", sl, SMP_USER_DATA) != (long)sizeof(smp_user_hdr_t) ||
                load("Felucca/build/slice_demo/loop.bin", sl + SMP_USER_DATA, SLC_REC_OFF - SMP_USER_DATA) <= 0) return 4;
            smp_user_scan(1);
            m = slc_man_begin(1);
            if (m->n > 4u) m->n = 4u;
            slc_man_commit(1);
            if (slc_store_write(1) != 3) return 5;
        }
        trk[0].step[2] = (step_t){{67}, 1, ST_NOTE, 0, 90, 0, 0};
        if (up_store(4, "APP SOUND")) return 6;            /* a USER sound in U05 */
        project_save(2);                                   /* a project in C */
        run(15000);                                        /* (the autosave: 10 s after the last change) */
        f = fopen(argv[2], "wb");
        fwrite(nor, 1, sizeof nor, f);
        fclose(f);
        return 0;
    }
    if (!strcmp(argv[1], "list")) {
        FILE *f = fopen(argv[2], "rb");
        if (!f || fread(nor, 1, sizeof nor, f) != sizeof nor) return 2;
        fclose(f);
        web_boot();
        run(8000);
        if (capture()) return 3;
        for (i = 0; i < obj_n; i++) {
            uint32_t len = obj_len[i];
            if (obj_id[i] >= 32u) {                        /* (the samples: their slot as the editor reads it) */
                const smp_user_hdr_t *h = (const smp_user_hdr_t *)smp_user_xip(obj_id[i] - 32u);
                len = usr_nz[obj_id[i] - 32u] ? SMP_USER_DATA + h->data_len : 0u;
                memcpy(obj[i], smp_user_xip(obj_id[i] - 32u), len);
                obj_len[i] = len;
            }
            printf("%u %u %u\n", obj_id[i], len, len ? st_crc32(obj[i], len) : 0u);
        }
        if (argc > 3) {
            f = fopen(argv[3], "w");
            fprintf(f, "{\"format\":\"felucca-backup\",\"version\":1,\"firmware\":\"host\",\"objects\":[");
            for (i = 0; i < obj_n; i++) {
                fprintf(f, "%s{\"id\":%u,\"size\":%u,\"crc\":%u,\"data\":\"", i ? "," : "", obj_id[i], obj_len[i],
                        obj_len[i] ? st_crc32(obj[i], obj_len[i]) : 0u);
                b64(f, obj[i], obj_len[i]);
                fprintf(f, "\"}");
            }
            fprintf(f, "]}\n");
            fclose(f);
        }
        return 0;
    }
    return 2;
}
