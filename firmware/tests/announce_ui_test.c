/* SPDX-License-Identifier: GPL-3.0-only */
/* Host test of the screen reader (Guru-600 1.1; src/ui_announce.c over fm1-base's announce.c), on the real UI:
 *   build/host/announce_ui_test      (run_tests.sh builds and runs it)
 * No reader: not a byte, pages, knobs and messages as they come. A reader's HELLO: the answer (GURU-600, version 1),
 * then the screen (HOME, the track and its sound, the four cards); a page: its title and its cards; a knob turned:
 * its label and value once it settles (one SAY, not one a detent); a message: heard whole (KEEP); the MENU: its tab,
 * then each row and value; a dialog: the question and its keys; WHERE: the screen again; BYE, or no HELLO for 5 s:
 * silence again. Every SAY 7-bit, within ANN_MAX. */
#include <stdint.h>
static int ann_cap(const uint8_t *p, uint32_t n);
#define ANN_CAPTURE ann_cap
#define UI_TEST_NO_MAIN 1
#include "ui_test.c"

static char said[64][160];
static uint8_t said_fl[64];
static uint32_t nsaid, nbytes, bad7, hello_ok;
static int ann_cap(const uint8_t *p, uint32_t n)
{
    uint32_t i;
    nbytes += n;
    for (i = 1; i + 1u < n; i++)
        bad7 |= p[i] & 0x80u;
    if (n < 7u || p[0] != 0xF0u || p[n - 1u] != 0xF7u || p[1] != 0x7Du || p[2] != 0x53u || p[3] != 0x52u)
        return bad7 = 1, 0;
    if (p[4] == 1u) {                                     /* HELLO: version, name, 0, link */
        hello_ok = p[5] == 1u && n >= 16u && !memcmp(p + 6, "GURU-600", 8) && p[14] == 0;
        return 0;
    }
    if (p[4] == 16u && nsaid < 64u) {
        uint32_t k = n - 7u < sizeof said[0] - 1u ? n - 7u : sizeof said[0] - 1u;
        memcpy(said[nsaid], p + 6, k);
        said[nsaid][k] = 0;
        said_fl[nsaid++] = p[5];
    }
    return 0;
}
static int bad;
static void ck(const char *what, int ok)
{
    printf("announce: %-86s %s\n", what, ok ? "ok" : "FAIL");
    bad += !ok;
}
static void fr(uint32_t ms)                               /* frames, the main loop's tick with them */
{
    uint32_t i;
    for (i = 0; i < (ms + 15u) / 16u; i++) {
        frame();
        ann_tick(fm1_ms);
    }
}
static void hello(void)
{
    static const uint8_t H[5] = {0x7D, 0x53, 0x52, 1, 1};
    (void)ann_frame(H, 5, fm1_ms);
}
static int has(uint32_t k, const char *w)                 /* SAY k holds w */
{
    const char *s = said[k];
    uint32_t n = str_len(w);
    for (; *s; s++)
        if (!memcmp(s, w, n))
            return 1;
    return 0;
}
static int any(uint32_t from, const char *w)
{
    uint32_t k;
    for (k = from; k < nsaid; k++)
        if (has(k, w))
            return 1;
    return 0;
}
static void dump(uint32_t from)
{
    uint32_t k;
    for (k = from; k < nsaid; k++)
        printf("announce:   SAY %u [%s]\n", said_fl[k], said[k]);
}
int main(void)
{
    track_t *t;
    uint32_t n0, k;
    int ok;
    ui_power_on();
    t = TSEL;
    fr(500);
    go_title("INSERT");
    turn(EN_K1, 1);
    ui_message("SAVED");
    fr(500);
    go_home();
    fr(100);
    ck("no reader: not a byte (pages, a knob, a message)", nbytes == 0);
    hello();
    fr(100);
    ck("HELLO: answered GURU-600, protocol 1", hello_ok);
    dump(0);
    ck("..then the screen: HOME, the track and its sound, the cards", nsaid == 1u && has(0, "HOME, TRACK 1, ") &&
       said_fl[0] == ANN_NOW);
    n0 = nsaid;
    t->p[P_ITYPE] = IT_OFF;
    go_title("INSERT");
    fr(100);
    dump(n0);
    ck("a page: its title and its four cards at once", nsaid == n0 + 1u && has(n0, "INSERT") && has(n0, "INSRT OFF"));
    n0 = nsaid;
    t->p[P_ITYPE] = IT_OFF;
    turn(EN_K1, 1);
    turn(EN_K1, 1);
    turn(EN_K1, 1);
    fr(20);
    ok = nsaid == n0;                                     /* (still turning: nothing yet) */
    fr(600);
    dump(n0);
    ck("a knob turned three detents: one SAY once it settles, its label and value (INSRT FOLD)",
       ok && nsaid == n0 + 1u && has(n0, "INSRT FOLD"));
    n0 = nsaid;
    ui_message("SAVED");
    fr(50);
    dump(n0);
    ck("a message: said as it comes, heard whole (KEEP)", nsaid == n0 + 1u && has(n0, "SAVED") && said_fl[n0] == ANN_KEEP);
    n0 = nsaid;
    hello();                                              /* (the reader's HELLO every 2 s keeps it listening) */
    hold(B_HOME);                                         /* HOME held: the MENU */
    fr(100);
    dump(n0);
    ck("MENU: its tab and the row with its value", nsaid > n0 && has(n0, "MENU") && any(n0, "COLOR"));
    n0 = nsaid;
    for (k = 0; k < 2u; k++)
        turn(EN_PRESET, 1);
    fr(600);
    dump(n0);
    ck("..PRESETS: the next row, said once it settles", nsaid == n0 + 1u);
    press(B_HOME);                                        /* (closes it) */
    fr(100);
    hello();
    n0 = nsaid;
    {
        static const uint8_t W[4] = {0x7D, 0x53, 0x52, 3};
        (void)ann_frame(W, 4, fm1_ms);
    }
    fr(100);
    dump(n0);
    ck("WHERE: the whole screen again, the track and its sound too", nsaid == n0 + 1u && has(n0, "HOME, TRACK 1, "));
    n0 = nsaid;
    fr(5200);
    go_title("INSERT");
    fr(100);
    ck("no HELLO for 5 s: silence again", nsaid == n0);
    hello();
    fr(100);
    n0 = nsaid;
    {
        static const uint8_t B[4] = {0x7D, 0x53, 0x52, 2};
        (void)ann_frame(B, 4, fm1_ms);
    }
    go_home();
    fr(200);
    ck("BYE: silence", nsaid == n0);
    ok = !bad7;
    for (k = 0; k < nsaid; k++)
        ok &= str_len(said[k]) <= ANN_MAX;
    ck("every frame F0 7D 53 52 .. F7, 7-bit, each SAY within ANN_MAX", ok);
    if (bad) {
        printf("ANNOUNCE TEST FAILED (%d)\n", bad);
        return 1;
    }
    printf("announce: all ok\n");
    return 0;
}
