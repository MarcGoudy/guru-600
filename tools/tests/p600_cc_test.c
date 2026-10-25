/* Guru-600 : la table CC du P600 (midi_control.c p6_cc) : chaque CC, sa commande.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/p600_cc_test tests/p600_cc_test.c -lm */
#include "felucca_web.c"
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
int main(void)
{
    static const struct { uint8_t cc, val; uint32_t id; const char *n; } C[] = {
        {16, 127, P_E0 + P6_A_FRQ, "FREQ A"}, {17, 0, P_E0 + P6_MIX, "OSC A level -> MIXER"}, {18, 0, P6_APW, "PW A"},
        {19, 0, P_E0 + P6_B_FRQ, "FREQ B"}, {20, 127, P_E0 + P6_MIX, "OSC B level -> MIXER"}, {21, 127, P6_BPW, "PW B"},
        {22, 127, P6_BFIN, "FINE B"}, {23, 0, P_E0 + P6_CUT, "CUTOFF"}, {24, 127, P_E0 + P6_RES, "RESONANCE"},
        {25, 127, P_E0 + P6_FENV, "ENV AMOUNT"}, {26, 127, P6_FREL, "FIL REL"}, {27, 0, P6_FSUS, "FIL SUS"},
        {28, 127, P6_FDEC, "FIL DEC"}, {29, 127, P6_FATK, "FIL ATK"}, {30, 127, P_REL, "AMP REL"}, {31, 0, P_SUS, "AMP SUS"},
        {32, 127, P_DEC, "AMP DEC"}, {33, 127, P_ATK, "AMP ATK"}, {34, 127, P6_PMENV, "PM FIL ENV"}, {35, 127, P6_PMB, "PM OSC B"},
        {36, 0, P_LRATE, "LFO FREQ"}, {37, 127, P_M4AMT, "LFO INITIAL AMOUNT"}, {40, 127, P_M3AMT, "VEL > FLT"},
        {44, 127, P_DETUNE, "DETUNE"}, {48, 127, P_E0 + P6_A_WAV, "A SAW on"}, {50, 0, P_E0 + P6_A_WAV, "A PULSE off"},
        {52, 127, P_E0 + P6_B_WAV, "B TRI on"}, {54, 0, P6_SYNC, "SYNC off"}, {55, 127, P6_PMDST, "PM FREQ A on"},
        {56, 127, P6_PMDST, "PM FILTER on"}, {57, 127, P_LWAVE, "LFO SQR"}, {60, 64, P6_KBD, "KBD HALF"},
        {66, 127, P_VOICE, "UNISON"}, {113, 127, P_LD_PIT, "LFO FREQ A-B"}, {114, 127, P_LD_SHP, "LFO PW A-B"},
        {115, 0, P_LD_FLT, "LFO FILTER off"}, {116, 127, P6_VINT, "VINTAGE"},
    };
    uint32_t i, ok = 0;
    web_nor_erase(); web_boot(); run(7000);
    apply_preset_to(TSEL, 0);                                  /* 1 ORGAN I, track 1, channel 1 */
    for (i = 0; i < sizeof C / sizeof C[0]; i++) {
        int before = TSEL->p[C[i].id];
        midi_control(0, C[i].cc, C[i].val);
        printf("CC%-3u = %3u  %-20s %4d -> %4d%s\n", C[i].cc, C[i].val, C[i].n, before, TSEL->p[C[i].id],
               before == TSEL->p[C[i].id] ? "   (inchangé)" : "");
        ok += before != TSEL->p[C[i].id];
    }
    printf("%u / %u réglages ont bougé\n", ok, (unsigned)(sizeof C / sizeof C[0]));
    return 0;
}
