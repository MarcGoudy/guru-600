/* Captures des écrans 3D (HOME, ENV, LFO, FILTER) et du MENU > DISPLAY > 3D dans Felucca construit pour l'hôte.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/g3_cost tests/g3_cost.c -lm
 *   build/g3_cost OUTDIR */
#include "felucca_web.c"

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
static void turn(uint32_t role, int32_t n) { int32_t i; for (i = 0; i < (n < 0 ? -n : n); i++) { web_enc(role, n < 0 ? -1 : 1); run(150); } run(300); }
#include <time.h>
static double cost(uint32_t kind)
{
    clock_t t0 = clock();
    uint32_t i;
    for (i = 0; i < 2000u; i++) {
        cv_begin(240, H_GRAPH, T_BG);
        cv_rrect(3, 0, 234, H_GRAPH, 5, T_SURF, T_BG);
        g3_draw(kind);
    }
    return (double)(clock() - t0) / CLOCKS_PER_SEC / 2000.0 * 1e6;
}
static double cost2d(void)
{
    clock_t t0 = clock();
    uint32_t i;
    for (i = 0; i < 2000u; i++) {
        cv_begin(240, H_GRAPH, T_BG);
        cv_rrect(3, 0, 234, H_GRAPH, 5, T_SURF, T_BG);
        graph_scope(ACC);
    }
    return (double)(clock() - t0) / CLOCKS_PER_SEC / 2000.0 * 1e6;
}
int main(int argc, char **argv)
{
    web_nor_erase();
    web_boot();
    run(7000);
    web_midi(0x90, 48, 100);
    run(300);
    printf("2D scope %.1f us\n", cost2d());
    printf("scope %.1f us\n", cost(G3_SCOPE));
    tap(B_ENV); printf("env %.1f us\n", cost(G3_ENV));
    tap(B_LFO); printf("lfo %.1f us\n", cost(G3_LFO));
    tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); printf("flt %.1f us\n", cost(G3_FLT));
    return 0;
}
