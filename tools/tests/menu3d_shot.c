/* Captures du MENU > DISPLAY (Guru-600 : la ligne 3D, l'ascenseur) dans Felucca construit pour l'hôte.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/menu3d_shot tests/menu3d_shot.c -lm
 *   build/menu3d_shot OUTDIR */
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
    web_buttons(1u << B_HOME); run(1200); web_buttons(0); run(400);
    shot("menu_display");
    turn(EN_PRESET, 7); shot("menu_home");
    turn(EN_PRESET, 1); shot("menu_3d");
    tap(B_OCTDN); shot("menu_3d_off");
    turn(EN_ALGO, 1); shot("menu_control");
    turn(EN_ALGO, 3); shot("menu_system");
    return 0;
}
