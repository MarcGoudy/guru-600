/* Captures des écrans 3D v2 dans Felucca construit pour l'hôte : un son joué (accord tenu), chaque style de HOME,
 * puis ENV, FLT ENV, LFO, FILTER ; et le coût de dessin de chaque écran (µs sur l'hôte).
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/g3v2_shot tests/g3v2_shot.c -lm
 *   build/g3v2_shot OUTDIR */
#include "felucca_web.c"
#include <time.h>

static const char *out;
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static void shot(const char *name)
{
    char path[512];
    FILE *f;
    uint32_t i;
    snprintf(path, sizeof path, "%s/%s.ppm", out, name);
    f = fopen(path, "wb");
    fprintf(f, "P6\n240 240\n255\n");
    for (i = 0; i < 240u * 240u; i++) {
        uint16_t v = web_fb[i];
        v = (uint16_t)((v >> 8) | (v << 8));
        fputc(((v >> 11) & 31) * 255 / 31, f);
        fputc(((v >> 5) & 63) * 255 / 63, f);
        fputc((v & 31) * 255 / 31, f);
    }
    fclose(f);
}
static void tap(uint32_t b) { web_buttons(1u << b); run(80); web_buttons(0); run(500); }
static double cost(uint32_t kind)
{
    clock_t t0 = clock();
    uint32_t i;
    for (i = 0; i < 200u; i++) {
        cv_begin(240, H_GRAPH, T_BG);
        cv_rrect(3, 0, 234, H_GRAPH, 5, T_SURF, T_BG);
        g3_draw(kind);
    }
    return (double)(clock() - t0) / CLOCKS_PER_SEC / 200.0 * 1e6;
}
static void sound(uint32_t k, const uint8_t *notes, uint32_t n)
{
    track_t *t = &trk[0];
    uint32_t i;
    for (i = 0; i < 128u; i++)
        trk_note_off(t, i);
    set_engine_of(t, ENGI_P600);
    apply_preset_to(t, k);
    run(50);
    for (i = 0; i < n; i++)
        trk_note_on(t, notes[i], 100);
}
int main(int argc, char **argv)
{
    static const char *const NAMES[7] = {"disc", "walls", "tunnel", "cell", "waves", "sparks", "flower"};
    static const uint8_t CH[4] = {48, 55, 60, 67}, BASS[1] = {29};
    uint32_t s;
    out = argv[1];
    web_nor_erase();
    web_boot();
    run(7000);
    sound(249, CH, 4);                                 /* 250 CHIME PAD: stereo, reverb */
    run(800);
    for (s = 0; s < 7u; s++) {
        char n[32];
        ui_prefs3 = (uint8_t)(s == 0 ? 0 : s + 2);
        ui.home = 1;
        ui.force = 1;
        if (s == 5u) {                                 /* (SPARKS: a few notes struck, up the keyboard) */
            static const uint8_t UP[6] = {36, 48, 55, 64, 72, 84};
            uint32_t q;
            for (q = 0; q < 6u; q++) {
                trk_note_on(&trk[0], UP[q], 110);
                run(250);
                trk_note_off(&trk[0], UP[q]);
            }
        }
        run(1500);
        snprintf(n, sizeof n, "home_%u_%s", s, NAMES[s]);
        shot(n);
        printf("%-8s %7.0f us\n", NAMES[s], cost(G3_HOME));
    }
    ui_prefs3 = 0;
    tap(B_ENV); run(1500); shot("env"); printf("env      %7.0f us\n", cost(G3_ENV));
    tap(B_LFO); run(800); shot("lfo"); printf("lfo      %7.0f us\n", cost(G3_LFO));
    sound(242, BASS, 1);                               /* 243 WOBBLE BASS */
    tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); run(1500); shot("filter"); printf("filter   %7.0f us\n", cost(G3_FLT));
    tap(B_EDIT); run(1500); shot("fltenv"); printf("fltenv   %7.0f us\n", cost(G3_FENV));
    return 0;
}
