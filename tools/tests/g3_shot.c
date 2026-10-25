/* Captures des écrans 3D (HOME, ENV, LFO, FILTER) et du MENU > DISPLAY > 3D dans Felucca construit pour l'hôte.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/g3_shot tests/g3_shot.c -lm
 *   build/g3_shot OUTDIR */
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
int main(int argc, char **argv)
{
    out = argv[1];
    web_nor_erase();
    web_boot();
    run(7000);
    web_midi(0x90, 48, 100); web_midi(0x90, 55, 100); web_midi(0x90, 64, 100);
    run(600); shot("g3_home");
    run(500); shot("g3_home2");
    tap(B_ENV); run(300); shot("g3_env");
    run(1500); shot("g3_env2");
    tap(B_LFO); run(300); shot("g3_lfo");
    run(250); shot("g3_lfo2");
    tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); tap(B_EDIT); shot("g3_flt");
    turn(EN_K1, 12); run(100); shot("g3_flt_turn");
    turn(EN_K2, 20); run(1200); shot("g3_flt_res");
    return 0;
}
