/* Guru-600 : les outils du séquenceur que l'éditeur lance (ui_tools.c ed_tool, trame 16 d'editor.c) sur la piste choisie.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/p600_tool_test tests/p600_tool_test.c -lm
 *   build/p600_tool_test */
#include "felucca_web.c"
static int fails;
static void ok(const char *what, int c) { printf("p600 tools: %-60s %s\n", what, c ? "ok" : "FAIL"); fails += !c; }
static void notes(track_t *t, const uint8_t *n, uint32_t len)
{
    uint32_t i;
    t->p[P_SLEN] = (int16_t)len;
    for (i = 0; i < NSTEP; i++) step_clear(&t->step[i]);
    for (i = 0; i < len; i++) if (n[i]) { t->step[i].time = ST_NOTE; t->step[i].n = 1; t->step[i].note[0] = n[i]; }
}
int main(void)
{
    static const uint8_t A[8] = {60, 0, 62, 0, 64, 0, 0, 67};
    track_t *t;
    uint32_t i, hits;
    web_nor_erase(); web_boot();
    for (i = 0; i < 2400u; i++) web_render(128);   /* (about 7 s: the boot screen over) */
    t = TSEL;
    notes(t, A, 8);
    ok("REVERSE: answer 0", ed_tool(TL_REV, 0, 0, 0) == 0);
    ok("REVERSE: 67 first, 60 last", t->step[0].note[0] == 67 && t->step[7].note[0] == 60);
    notes(t, A, 8);
    ok("SHIFT >: answer 0", ed_tool(TL_RIGHT, 0, 0, 0) == 0);
    ok("SHIFT >: 60 on step 2, 67 wrapped to step 1", t->step[1].note[0] == 60 && t->step[0].note[0] == 67);
    notes(t, A, 8);
    ed_tool(TL_LEFT, 0, 0, 0);
    ok("SHIFT <: 62 on step 2, 60 wrapped to step 8", t->step[1].note[0] == 62 && t->step[7].note[0] == 60);
    notes(t, A, 8);
    ed_tool(TL_CLEAR, 0, 0, 0);
    for (i = 0, hits = 0; i < 8; i++) hits += t->step[i].time == ST_NOTE && t->step[i].n;
    ok("CLEAR: no note left", hits == 0);
    notes(t, A, 8);
    ok("DOUBLE: answer 0", ed_tool(TL_DOUBLE, 0, 0, 0) == 0);
    ok("DOUBLE: LEN 16, steps 9..16 as 1..8", t->p[P_SLEN] == 16 && t->step[8].note[0] == 60 && t->step[15].note[0] == 67);
    ed_tool(TL_HALF, 0, 0, 0);
    ok("HALF: LEN 8 again", t->p[P_SLEN] == 8);
    notes(t, A, 16);
    t->p[P_SLEN] = 16;
    ok("EUCLID 5/16: answer 0", ed_tool(TL_EUCLID, 5, 16, 0) == 0);
    for (i = 0, hits = 0; i < 16; i++) hits += t->step[i].time == ST_NOTE && t->step[i].n;
    ok("EUCLID 5/16: five notes", hits == 5);
    notes(t, A, 8);
    ok("RANDOM: answer 0", ed_tool(TL_RANDOM, 0, 0, 0) == 0);
    for (i = 0, hits = 0; i < 8; i++) hits += t->step[i].time == ST_NOTE && t->step[i].n;
    ok("RANDOM: notes there", hits > 0);
    ok("COOK: answer 0", ed_tool(TL_COOK, 0, 0, 0) == 0);
    for (i = 0; i < NSTEP; i++) step_clear(&t->step[i]);
    ok("COOK on nothing: answer 1 (nothing done)", ed_tool(TL_COOK, 0, 0, 0) == 1);
    ok("a tool out of range: answer 1", ed_tool(99, 0, 0, 0) == 1);
    printf(fails ? "p600 tools: %d FAIL\n" : "p600 tools: all ok\n", fails);
    return fails != 0;
}
