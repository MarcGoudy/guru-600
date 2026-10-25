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
    uint32_t a = argc > 3 ? (uint32_t)atoi(argv[2]) : 0, b = argc > 3 ? (uint32_t)atoi(argv[3]) : 99, k, i;
    static const uint8_t CHORD[] = {48, 55, 60, 64}, PHRASE[] = {36, 48, 43, 55, 60, 67, 72, 60};
    char path[512];
    if (argc < 2)
        return 2;
    buf = malloc(sizeof(float) * 2 * 44100 * 12);
    web_nor_erase();
    web_boot();
    render(300);
    for (k = a; k <= b; k++) {
        track_t *t = &trk[0];
        double peak = 0, sum = 0, dc = 0, cpu;
        clock_t c0;
        int bad = 0;
        set_engine_of(t, getenv("ENG") ? (uint32_t)atoi(getenv("ENG")) : ENGI_P600);
        apply_preset_to(t, k);
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
        printf("%2u %-8s peak %.3f rms %.4f dc %+.4f cpu %.3f %s\n", k, ENGINES[t->eng_req]->presets[k].name, peak,
               sqrt(sum / (2 * nbuf)), dc / (2 * nbuf), cpu, bad ? "NaN!" : "");
        snprintf(path, sizeof path, "%s/P600_%02u.wav", argv[1], k);
        wav(path);
    }
    return 0;
}
