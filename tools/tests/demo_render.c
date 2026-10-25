/* Sons de démonstration pour les maquettes des écrans 3D : quelques sons du Guru-600, mono puis avec effets,
 * à la suite dans un WAV stéréo (les courbes y réagissent). Construit comme demo_render.c (Felucca construit pour l'hôte, comme web/emu/native_check.c) :
 * un accord tenu puis relâché, et une phrase, par programme ; un WAV par programme et une ligne de mesures.
 *   cc -O2 -ffp-contract=off -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu \
 *      -o build/demo_render tests/demo_render.c -lm
 *   build/demo_render OUTDIR [premier dernier] */
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
    static const struct { uint32_t k; uint8_t notes[8]; uint32_t n, hold_ms, phrase; } S[] = {
        {0,   {48, 55, 60, 64}, 4, 2600, 0},          /* 1 ORGAN I: dry, mono */
        {249, {48, 55, 60, 67}, 4, 2600, 0},          /* 250 CHIME PAD: chorus + reverb */
        {228, {36, 48, 43, 36, 48, 51, 36, 55}, 8, 0, 1},   /* 229 ACID SEQ 1: delay */
        {242, {29}, 1, 3200, 0},                      /* 243 WOBBLE BASS: the LFO on the filter */
        {231, {45, 52}, 2, 2600, 0},                  /* 232 GONG: reverb */
    };
    uint32_t s, i, r;
    buf = malloc(sizeof(float) * 2 * 44100 * 40);
    web_nor_erase();
    web_boot();
    render(300);
    nbuf = 0;
    for (s = 0; s < NELEM(S); s++) {
        track_t *t = &trk[0];
        uint32_t n0 = nbuf;
        set_engine_of(t, ENGI_P600);
        apply_preset_to(t, S[s].k);
        render(30);
        nbuf = n0;
        if (S[s].phrase) {
            for (r = 0; r < 2u; r++)
                for (i = 0; i < S[s].n; i++) {
                    trk_note_on(t, S[s].notes[i], 100);
                    render(170);
                    trk_note_off(t, S[s].notes[i]);
                    render(30);
                }
        } else {
            for (i = 0; i < S[s].n; i++)
                trk_note_on(t, S[s].notes[i], 100);
            render(S[s].hold_ms);
            for (i = 0; i < S[s].n; i++)
                trk_note_off(t, S[s].notes[i]);
        }
        render(1300);
        fprintf(stderr, "%u %s %.2f s\n", S[s].k + 1, ENGINES[t->eng_req]->presets[S[s].k].name, (nbuf - n0) / 44100.0);
    }
    wav(argv[1]);
    return 0;
}
