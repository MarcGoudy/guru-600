/* Captures des pages du P600 dans Felucca construit pour l'hôte (web/emu/felucca_web.c) : allumage, puis des appuis
 * sur ENV, LFO et EDIT ; un PPM 240 x 240 de l'écran après chaque appui.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/p600_ui_shot tests/p600_ui_shot.c -lm
 *   build/p600_ui_shot OUTDIR */
#include "felucca_web.c"

static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static void shot(const char *dir, const char *name)
{
    char path[512];
    FILE *f;
    uint32_t i;
    snprintf(path, sizeof path, "%s/%s.ppm", dir, name);
    f = fopen(path, "wb");
    fprintf(f, "P6\n240 240\n255\n");
    for (i = 0; i < 240u * 240u; i++) {
        uint16_t v = web_fb[i];
        v = (uint16_t)((v >> 8) | (v << 8));          /* the panel's byte order */
        fputc(((v >> 11) & 31) * 255 / 31, f);
        fputc(((v >> 5) & 63) * 255 / 63, f);
        fputc((v & 31) * 255 / 31, f);
    }
    fclose(f);
}
static void press(uint32_t b)
{
    web_buttons(1u << b);
    run(80);
    web_buttons(0);
    run(400);
}
int main(int argc, char **argv)
{
    static const struct { uint32_t b; const char *n; } SEQ[] = {
        {B_EDIT, "edit1"}, {B_EDIT, "edit2"}, {B_EDIT, "edit3"}, {B_EDIT, "edit4"}, {B_EDIT, "edit5"},
        {B_EDIT, "edit6"}, {B_EDIT, "edit7"}, {B_EDIT, "edit8"}, {B_EDIT, "edit9"}, {B_ENV, "env1"}, {B_ENV, "env2"}, {B_LFO, "lfo1"}, {B_LFO, "lfo2"},
        {B_LFO, "lfo3"}, {B_HOME, "home"},
    };
    uint32_t i;
    if (argc < 2)
        return 2;
    web_nor_erase();
    web_boot();
    run(7000);
    shot(argv[1], "boot");
    for (i = 0; i < NELEM(SEQ); i++) {
        press(SEQ[i].b);
        shot(argv[1], SEQ[i].n);
    }
    return 0;
}
