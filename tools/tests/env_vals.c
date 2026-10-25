/* Les réglages ATTACK DECAY SUSTAIN RELEASE (page ENV) de quelques sons, tels que l'écran les affiche.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/env_vals tests/env_vals.c -lm */
#include "felucca_web.c"
int main(void)
{
    static const uint32_t K[] = {0, 249, 228, 242, 231};
    uint32_t i, c;
    web_nor_erase();
    web_boot();
    for (i = 0; i < 5u; i++) {
        track_t *t = &trk[0];
        static const uint8_t ID[4] = {P_ATK, P_DEC, P_SUS, P_REL};
        set_engine_of(t, ENGI_P600);
        apply_preset_to(t, K[i]);
        printf("%u", K[i] + 1);
        for (c = 0; c < 4u; c++) {
            char val[24];
            const char *unit;
            const param_desc_t *d = &TP[ID[c]];
            param_format(d, t->p[ID[c]], val, &unit);
            printf(" | %d %s %s", t->p[ID[c]], val, unit);
        }
        printf("\n");
    }
    return 0;
}
