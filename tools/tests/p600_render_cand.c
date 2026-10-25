/* (p600_render_cand.c : la même chose pour des sons candidats lus dans un fichier texte, une ligne chacun :
 *  e0..e7 env0..3 fenv0..3 pw0 pw1 fine sync pm0 pm1 pm2 kbd lfo0 lfo1 lfod0 lfod1 lfod2 glide unison lfoamp vel
 *  detune wheel mono ; build/p600_render_cand OUTDIR FICHIER) */
/* Rend les programmes d'usine du moteur P600 (Felucca construit pour l'hôte, comme web/emu/native_check.c) :
 * un accord tenu puis relâché, et une phrase, par programme ; un WAV par programme et une ligne de mesures.
 *   cc -O2 -ffp-contract=off -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu \
 *      -o build/p600_render tests/p600_render.c -lm
 *   build/p600_render OUTDIR [premier dernier] */
#include "felucca_web.c"
#include <math.h>
#include <time.h>

static float *buf;
static uint32_t nbuf;
static void render(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k, i;
    for (k = 0; k < n; k += 128u) {
        uint32_t m = n - k < 128u ? n - k : 128u;
        web_render(m);
        for (i = 0; i < m; i++) {
            buf[2 * nbuf] = out_l[i];
            buf[2 * nbuf + 1] = out_r[i];
            nbuf++;
        }
    }
}
static void wav(const char *path)
{
    FILE *f = fopen(path, "wb");
    uint32_t i, bytes = nbuf * 4u, v;
    uint16_t h;
    fwrite("RIFF", 1, 4, f); v = 36 + bytes; fwrite(&v, 4, 1, f); fwrite("WAVEfmt ", 1, 8, f);
    v = 16; fwrite(&v, 4, 1, f); h = 1; fwrite(&h, 2, 1, f); h = 2; fwrite(&h, 2, 1, f);
    v = 44100; fwrite(&v, 4, 1, f); v = 44100 * 4; fwrite(&v, 4, 1, f); h = 4; fwrite(&h, 2, 1, f);
    h = 16; fwrite(&h, 2, 1, f); fwrite("data", 1, 4, f); fwrite(&bytes, 4, 1, f);
    for (i = 0; i < 2 * nbuf; i++) {
        float s = buf[i] * 32767.0f;
        int16_t q = (int16_t)(s > 32767 ? 32767 : s < -32768 ? -32768 : s);
        fwrite(&q, 2, 1, f);
    }
    fclose(f);
}

int main(int argc, char **argv)
{
    uint32_t k, i;
    static const uint8_t CHORD[] = {48, 55, 60, 64}, PHRASE[] = {36, 48, 43, 55, 60, 67, 72, 60};
    char path[512];
    if (argc < 2)
        return 2;
    buf = malloc(sizeof(float) * 2 * 44100 * 12);
    web_nor_erase();
    web_boot();
    render(300);
    FILE *cf = fopen(argv[2], "r");
    static p6imp_t cm;
    int v[40];
    for (k = 0; ; k++) {
        track_t *t = &trk[0];
        uint32_t j;
        for (j = 0; j < 36u; j++) if (fscanf(cf, "%d", &v[j]) != 1) break;
        if (j < 36u) break;
        memset(&cm, 0, sizeof cm);
        for (j = 0; j < 8u; j++) cm.e[j] = (int8_t)v[j];
        for (j = 0; j < 4u; j++) { cm.env[j] = (uint8_t)v[8 + j]; cm.x.fenv[j] = (uint8_t)v[12 + j]; }
        cm.x.pw[0] = (uint8_t)v[16]; cm.x.pw[1] = (uint8_t)v[17]; cm.x.fine = (uint8_t)v[18]; cm.x.sync = (uint8_t)v[19];
        cm.x.pm[0] = (uint8_t)v[20]; cm.x.pm[1] = (uint8_t)v[21]; cm.x.pm[2] = (uint8_t)v[22]; cm.x.kbd = (uint8_t)v[23];
        cm.x.lfo[0] = (uint8_t)v[24]; cm.x.lfo[1] = (uint8_t)v[25];
        cm.x.lfod[0] = (int8_t)v[26]; cm.x.lfod[1] = (int8_t)v[27]; cm.x.lfod[2] = (int8_t)v[28];
        cm.x.glide = (uint8_t)v[29]; cm.x.unison = (uint8_t)v[30]; cm.x.lfoamp = (uint8_t)v[31]; cm.x.vel = (uint8_t)v[32];
        cm.x.detune = (uint8_t)v[33]; cm.x.wheel = (uint8_t)v[34];
        str_cpy(cm.name, "CAND", 16);
        (void)p6_put(254, &cm);
        double peak = 0, sum = 0, dc = 0, cpu;
        clock_t c0;
        int bad = 0;
        set_engine_of(t, ENGI_P600);
        apply_preset_to(t, 254);
        if (v[35]) t->p[P_VOICE] = V_LEGATO;
        if (getenv("OVR")) {                          /* OVR="id=val,id=val": a parameter set after the preset */
            const char *o = getenv("OVR");
            while (*o) {
                int id = atoi(o), val;
                while (*o && *o != '=') o++;
                val = atoi(++o);
                t->p[id] = (int16_t)val;
                while (*o && *o != ',') o++;
                if (*o) o++;
            }
        }
        render(50);
        if (getenv("DBG"))
            fprintf(stderr, "P_FM4_ATK=%d P_FM4_DEC=%d P_FM3_ATK=%d P_E0=%d\n", P_FM4_ATK, P_FM4_DEC, P_FM3_ATK, P_E0);
        nbuf = 0;
        c0 = clock();
        for (i = 0; i < sizeof CHORD; i++)
            trk_note_on(t, CHORD[i], 100);
        render(2000);
        for (i = 0; i < sizeof CHORD; i++)
            trk_note_off(t, CHORD[i]);
        render(1500);
        for (i = 0; i < sizeof PHRASE; i++) {
            trk_note_on(t, PHRASE[i], 100);
            render(220);
            trk_note_off(t, PHRASE[i]);
            render(30);
        }
        render(1500);
        cpu = (double)(clock() - c0) / CLOCKS_PER_SEC / (nbuf / 44100.0);
        for (i = 0; i < 2 * nbuf; i++) {
            double s = buf[i];
            if (s != s) bad = 1;
            if (fabs(s) > peak) peak = fabs(s);
            sum += s * s;
            dc += s;
        }
        printf("%3u peak %.3f rms %.4f dc %+.4f cpu %.3f %s\n", k, peak,
               sqrt(sum / (2 * nbuf)), dc / (2 * nbuf), cpu, bad ? "NaN!" : "");
        snprintf(path, sizeof path, "%s/C_%03u.wav", argv[1], k);
        wav(path);
    }
    return 0;
}
