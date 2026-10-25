/* L'écran d'accueil à 4,5 s (le logo affiché), en PPM.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/splash_shot tests/splash_shot.c -lm */
#include "felucca_web.c"
int main(int argc, char **argv)
{
    uint32_t i, n = (uint32_t)(4500 * 44.1), k;
    FILE *f;
    web_nor_erase(); web_boot();
    (void)n; (void)k;
    lcd_fill(0, 0, 240, 240, SPL_BG);
    for (k = 0; k <= 4500u; k += 15u) splash_anim(k);   /* main.c: the animation, frame by frame, to 4.5 s */
    f = fopen(argv[1], "wb");
    fprintf(f, "P6\n240 240\n255\n");
    for (i = 0; i < 240u * 240u; i++) {
        uint16_t v = web_fb[i];
        v = (uint16_t)((v >> 8) | (v << 8));
        fputc(((v >> 11) & 31) * 255 / 31, f); fputc(((v >> 5) & 63) * 255 / 63, f); fputc((v & 31) * 255 / 31, f);
    }
    fclose(f);
    return 0;
}
