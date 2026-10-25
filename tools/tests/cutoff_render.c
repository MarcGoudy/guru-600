/* Sons de démonstration pour les maquettes des écrans 3D : quelques sons du Guru-600, mono puis avec effets,
 * à la suite dans un WAV stéréo (les courbes y réagissent). Construit comme cutoff_render.c (Felucca construit pour l'hôte, comme web/emu/native_check.c) :
 * un accord tenu puis relâché, et une phrase, par programme ; un WAV par programme et une ligne de mesures.
 *   cc -O2 -ffp-contract=off -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu \
 *      -o build/cutoff_render tests/cutoff_render.c -lm
 *   build/cutoff_render OUTDIR [premier dernier] */
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
    static const uint8_t CH[3] = {48, 55, 60};
    uint32_t k, i;
    track_t *t = &trk[0];
    FILE *cf = fopen(argv[2], "w");                   /* the cutoff every 40 ms (a video frame), for the mock-up */
    buf = malloc(sizeof(float) * 2 * 44100 * 40);
    web_nor_erase();
    web_boot();
    render(300);
    set_engine_of(t, ENGI_P600);
    apply_preset_to(t, 201);                          /* 202 SAW LOFI */
    t->p[P_E5] = 80;                                  /* RESONANCE ~ 63 % */
    t->p[P_E4] = 10;
    render(30);
    nbuf = 0;
    for (i = 0; i < 3u; i++)
        trk_note_on(t, CH[i], 100);
    for (k = 0; k < 350u; k++) {                      /* 14 s: closed, opens to the top, closes, opens half way */
        double u = k / 350.0, c;
        if (u < 0.4) c = 10 + 115 * (u / 0.4);
        else if (u < 0.75) c = 125 - 110 * ((u - 0.4) / 0.35);
        else c = 15 + 60 * ((u - 0.75) / 0.25);
        t->p[P_E4] = (int16_t)(c + 0.5);
        fprintf(cf, "%d\n", t->p[P_E4]);
        render(40);
    }
    for (i = 0; i < 3u; i++)
        trk_note_off(t, CH[i]);
    for (k = 0; k < 30u; k++) { fprintf(cf, "%d\n", t->p[P_E4]); render(40); }
    fclose(cf);
    wav(argv[1]);
    return 0;
}
