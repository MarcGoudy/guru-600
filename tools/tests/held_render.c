/* Sons de démonstration pour les maquettes des écrans 3D : quelques sons du Guru-600, mono puis avec effets,
 * à la suite dans un WAV stéréo (les courbes y réagissent). Construit comme held_render.c (Felucca construit pour l'hôte, comme web/emu/native_check.c) :
 * un accord tenu puis relâché, et une phrase, par programme ; un WAV par programme et une ligne de mesures.
 *   cc -O2 -ffp-contract=off -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu \
 *      -o build/held_render tests/held_render.c -lm
 *   build/held_render OUTDIR [premier dernier] */
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
    static const uint8_t N[5] = {36, 48, 60, 72, 84};   /* C2 .. C6, each held 2.5 s */
    uint32_t k;
    track_t *t = &trk[0];
    buf = malloc(sizeof(float) * 2 * 44100 * 40);
    web_nor_erase();
    web_boot();
    render(300);
    set_engine_of(t, ENGI_P600);
    apply_preset_to(t, 0);                            /* 1 ORGAN I */
    render(30);
    nbuf = 0;
    render(500);
    for (k = 0; k < 5u; k++) {
        trk_note_on(t, N[k], 100);
        render(2500);
        trk_note_off(t, N[k]);
        render(300);
    }
    render(1200);
    wav(argv[1]);
    return 0;
}
