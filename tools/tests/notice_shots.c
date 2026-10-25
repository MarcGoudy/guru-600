/* Captures d'écran pour la notice : chaque page, le MENU, la liste des sons, l'enregistrement d'un son.
 *   build/notice_shots OUTDIR */
#include "felucca_web.c"

static const char *dir;
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
    snprintf(path, sizeof path, "%s/%s.ppm", dir, name);
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
static void tap(uint32_t b) { web_buttons(1u << b); run(80); web_buttons(0); run(700); }
static void hold(uint32_t b, double ms) { web_buttons(1u << b); run(ms); }
static void let(void) { web_buttons(0); run(300); }
static void turn(uint32_t role, int32_t n) { web_enc(role, n); run(500); }
int main(int argc, char **argv)
{
    uint32_t i;
    dir = argv[1];
    web_nor_erase();
    web_boot();
    run(9000);
    for (i = 0; i < 4u; i++)                           /* (a chord held: the 3D screens show a sound) */
        trk_note_on(&trk[0], (uint8_t[4]){48, 55, 60, 64}[i], 100);
    run(1500);
    shot("home");
    turn(EN_PRESET, 1); shot("presets_turn"); turn(EN_PRESET, -1);
    for (i = 0; i < 4u; i++)                           /* (the sound changed: the chord again) */
        trk_note_on(&trk[0], (uint8_t[4]){48, 55, 60, 64}[i], 100);
    run(1500);
    for (i = 0; i < 10u; i++) { char n[16]; tap(B_EDIT); snprintf(n, sizeof n, "edit%u", i + 1); shot(n); }
    tap(B_ENV); shot("env1"); tap(B_ENV); shot("env2");
    tap(B_LFO); shot("lfo1"); tap(B_LFO); shot("lfo2"); tap(B_LFO); shot("lfo3"); tap(B_LFO); shot("lfo4");
    tap(B_FX); shot("fx1"); tap(B_FX); shot("fx2");
    tap(B_SCL); shot("scl1");
    tap(B_ARP); shot("arp1"); tap(B_ARP); shot("arp2");
    tap(B_SEQ); shot("seq1");
    tap(B_GLO); shot("glo1");
    tap(B_HOME); run(500); shot("home2");
    tap(B_SAVE); shot("save_user"); tap(B_SAVE); shot("save_presets"); tap(B_SAVE); shot("save_phrases");
    tap(B_SAVE); shot("save_project"); tap(B_SAVE); shot("save_tools");
    tap(B_HOME); run(500);
    hold(B_EDIT, 900); shot("layer_edit"); let();
    hold(B_HOME, 1200); let(); shot("menu");
    for (i = 0; i < 4u; i++) turn(EN_ALGO, 1);
    shot("menu_system");
    for (i = 0; i < 3u; i++) turn(EN_PRESET, 1);     /* (Guru-600: no USB SERIAL, RESET SOUNDS one row up) */
    shot("menu_system_rows");
    turn(EN_PRESET, 1); shot("menu_p600reset");
    tap(B_HOME); run(500);
    {                                                  /* the pages with their own animation, on a stereo sound */
        static const char *const PG[11] = {"REVERB", "CHORUS", "DLY", "ARP 2", "ENV DEST", "CLOCK", "ARP", "OSC 2",
                                           "POLY MOD", "LFO 2", "MIXER"};
        static const char *const ST[11] = {"style_cell", "style_walls", "style_tunnel", "style_sparks", "style_waves",
                                           "style_flower", "style_blocks", "style_cascade", "style_ribbon", "style_helix",
                                           "style_tracks"};
        static const uint8_t UP[6] = {36, 48, 55, 64, 72, 84};
        uint32_t s2, q, k;
        for (q = 0; q < 128u; q++)
            trk_note_off(&trk[0], q);
        apply_preset_to(&trk[0], 249);                 /* 250 CHIME PAD */
        run(100);
        for (q = 0; q < 4u; q++)
            trk_note_on(&trk[0], (uint8_t[4]){48, 55, 60, 67}[q], 100);
        for (s2 = 0; s2 < 11u; s2++) {
            for (k = 0; k < NPAGES; k++)
                if (str_eq(PAGES[k].title, PG[s2])) {
                    ui.page = (uint8_t)k;
                    break;
                }
            ui.home = 0;
            ui.force = 1;
            if (s2 == 3u)
                for (q = 0; q < 6u; q++) {
                    trk_note_on(&trk[0], UP[q], 110);
                    run(700);
                    trk_note_off(&trk[0], UP[q]);
                }
            run(2000);
            shot(ST[s2]);
        }
    }
    return 0;
}
