/* Guru-600 : les trames de l'éditeur P600 (F0 7D 47 36 ..., editor.c ed_p6) contre le vrai gestionnaire de l'éditeur :
 * NAMES, LOAD, SAVE, STATE, et les réponses à l'import (1) et à l'oubli (3).
 *   sed -n '1,/^static int check/p' ../Felucca/tests/editor_test.c | sed '$d' > build/ed_prelude.c
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/tests -Ibuild -o build/p600_editor_test tests/p600_editor_test.c -lm
 *   build/p600_editor_test */
#include "ed_prelude.c"

static int fails;
static void ok(const char *what, int c) { printf("p600 editor: %-62s %s\n", what, c ? "ok" : "FAIL"); fails += !c; }

static void reset_all(void)
{
    uint32_t t, i;
    memset(&song, 0, sizeof song); memset(trk, 0, sizeof trk);
    memset(&ed_w, 0, sizeof ed_w); memset(&ui, 0, sizeof ui);
    memset(&settings, 0, sizeof settings); settings_init();
    host_progress = 1; host_wire_n = 0;
    sx_ready = sx_collect = sx_busy = 0; so_r = so_w = mi_r = mi_w = 0; usb.config = 1;
    for (i = 0; i < G_COUNT; i++) song.g[i] = GP[i].def;
    for (t = 0; t < NTRK; t++) {
        track_defaults(&trk[t]); set_engine_of(&trk[t], 0); apply_preset_to(&trk[t], 0);
        trk[t].engine = trk[t].eng_req; track_defaults_steps(&trk[t]);
    }
    for (i = 0; i < P6_NIMP; i++) p6_imp[i].used = 0;
    p6_booted = 1; p600_apply();
}
/* a Guru-600 frame: F0 7D 47 36 a.. F7; the answer in host_wire */
static uint32_t g6(const uint8_t *a, uint32_t n)
{
    uint32_t i;
    host_wire_n = 0; ota_frame_done();
    sysex_byte(0xF0); sysex_byte(0x7D); sysex_byte(0x47); sysex_byte(0x36);
    for (i = 0; i < n; i++) sysex_byte(a[i]);
    sysex_byte(0xF7); ed_service(); host_drain();
    return host_wire_n;
}
static int head(uint32_t cmd) { return host_wire_n > 5u && host_wire[0] == 0xF0 && host_wire[1] == 0x7D && host_wire[2] == 0x47 &&
                                       host_wire[3] == 0x36 && host_wire[4] == cmd && host_wire[host_wire_n - 1u] == 0xF7; }

int main(void)
{
    uint8_t a[64];
    uint32_t n, i, k, places;
    char nm[20];
    reset_all();

    /* STATE: track 1, ANALOG */
    a[0] = 10; g6(a, 1);
    ok("STATE: answer", head(10) && host_wire_n == 11u);
    ok("STATE: track 1, ANALOG", host_wire[5] == 0 && host_wire[6] == 0);

    /* LOAD place 200 (two 7-bit bytes): P600 set first */
    a[0] = 9; a[1] = 200 & 127; a[2] = 200 >> 7; g6(a, 3);
    ok("LOAD 200: answer 9 dest rc 0", head(9) && host_wire[5] == (200 & 127) && host_wire[6] == 1 && host_wire[7] == 0);
    ok("LOAD 200: track is P600, preset 200", TSEL->eng_req == ENGI_P600 && TSEL->preset == 200);
    ok("LOAD 200: its cutoff", TSEL->p[P_E0 + 4] == P600_PRESETS[200].e[4]);
    a[0] = 10; g6(a, 1);
    ok("STATE after LOAD: P600, 200, not kept", host_wire[6] == ENGI_P600 && host_wire[7] == (200 & 127) && host_wire[8] == 1 && host_wire[9] == 0);

    /* NAMES: 16 places from 0, then the last 15 (254 is the last place) */
    a[0] = 8; a[1] = 0; a[2] = 0; a[3] = 16; g6(a, 4);
    ok("NAMES 0..15: answer", head(8) && host_wire[7] == 16);
    for (i = 0, k = 8, places = 0; i < 16u && k < host_wire_n - 1u; i++) {
        uint32_t j = 0;
        k++;                                            /* kept */
        while (host_wire[k] && j < 19u) nm[j++] = (char)host_wire[k++];
        nm[j] = 0; k++;
        places += !strcmp(nm, p6_ram[i].name);
    }
    ok("NAMES 0..15: the 16 names as p6_ram", places == 16u && k == host_wire_n - 1u);
    a[1] = 240 & 127; a[2] = 240 >> 7; a[3] = 16; g6(a, 4);
    ok("NAMES from 240: 15 places (to 254)", head(8) && host_wire[7] == 15);
    a[3] = 17; n = g6(a, 4);
    ok("NAMES k = 17: no answer", n == 0);

    /* SAVE: change the cutoff, keep it in place 200 */
    TSEL->p[P_E0 + 4] = 11;
    a[0] = 6; a[1] = 200 & 127; a[2] = 200 >> 7; g6(a, 3);
    ok("SAVE 200: answer rc 0", head(6) && host_wire[7] == 0);
    ok("SAVE 200: kept, its cutoff", p6_find(200) >= 0 && p6_imp[p6_find(200)].e[4] == 11);
    a[0] = 8; a[1] = 200 & 127; a[2] = 200 >> 7; a[3] = 1; g6(a, 4);
    ok("NAMES 200: kept flag", head(8) && host_wire[8] == 1);
    apply_preset(0); a[0] = 9; a[1] = 200 & 127; a[2] = 200 >> 7; g6(a, 3);
    ok("LOAD 200 again: the kept cutoff", TSEL->p[P_E0 + 4] == 11);

    /* RENAME (7, 10/11): a kept place's name, the place number first; a factory place refused (3); 11 letters at most */
    a[0] = 7; a[1] = 200 & 127; a[2] = 200 >> 7; memcpy(a + 3, "MY BRASS", 8); g6(a, 11);
    ok("RENAME 200: answer 7 dest rc 0", head(7) && host_wire[5] == (200 & 127) && host_wire[7] == 0);
    ok("RENAME 200: named 201 MY BRASS", p6_ram[200].name && !strcmp(p6_ram[200].name, "201 MY BRASS"));
    ok("RENAME 200: still kept, its cutoff", p6_find(200) >= 0 && p6_imp[p6_find(200)].e[4] == 11);
    a[0] = 7; a[1] = 200 & 127; a[2] = 200 >> 7; memcpy(a + 3, "ABCDEFGHIJKLMNOP", 16); g6(a, 19);
    ok("RENAME 200: 11 letters kept", p6_ram[200].name && !strcmp(p6_ram[200].name, "201 ABCDEFGHIJK"));
    a[0] = 7; a[1] = 5; a[2] = 0; memcpy(a + 3, "NOPE", 4); g6(a, 7);
    ok("RENAME 5 (a factory sound): rc 3, unchanged", head(7) && host_wire[7] == 3 && p6_find(5) < 0);

    /* FORGET (3): answered, the original back */
    a[0] = 3; a[1] = 200 & 127; a[2] = 200 >> 7; g6(a, 3);
    ok("FORGET 200: answer 3 dest rc 0", head(3) && host_wire[5] == (200 & 127) && host_wire[7] == 0);
    ok("FORGET 200: not kept", p6_find(200) < 0);

    /* IMPORT (1): Sequential's dump of factory program 0 into place 210 */
    {
        static p6imp_t m;
        uint8_t sci[35];
        p6_of_place(0, &m); p6_to_sci(&m, 0, sci);
        a[0] = 1; a[1] = 210 & 127; a[2] = 210 >> 7;
        for (i = 0; i < 35u; i++) a[3 + i] = sci[i];
        g6(a, 38);
        ok("IMPORT 210: answer 1 dest rc 0", head(1) && host_wire[5] == (210 & 127) && host_wire[6] == 1 && host_wire[7] == 0);
        ok("IMPORT 210: kept", p6_find(210) >= 0);
    }

    /* RESET SOUNDS (2): answered, every place its own sound */
    a[0] = 2; g6(a, 1);
    ok("RESET: answer 2 rc 0, nothing kept", head(2) && host_wire[7] == 0 && p6_find(210) < 0);

    /* MORPH: place 0's sound (A) half way to place 1's (B) */
    a[0] = 9; a[1] = 0; a[2] = 0; g6(a, 3);
    {
        int32_t ca = TSEL->p[P_E0 + 4], cb = P600_PRESETS[1].e[4], cm;
        a[0] = 11; a[1] = 1; a[2] = 0; a[3] = 50; g6(a, 4);
        cm = TSEL->p[P_E0 + 4];
        ok("MORPH 50 %: answer 11 b pos rc 0", head(11) && host_wire[5] == 1 && host_wire[7] == 50 && host_wire[8] == 0);
        ok("MORPH 50 %: the cutoff half way", cm == ca + (cb - ca) * 50 / 100);
        a[0] = 13; g6(a, 1);
        ok("MORPH state: B 1, 50 %", head(13) && host_wire[5] == 1 && host_wire[7] == 50);
        a[0] = 11; a[1] = 1; a[2] = 0; a[3] = 0; g6(a, 4);
        ok("MORPH 0 %: A again", TSEL->p[P_E0 + 4] == ca);
        a[3] = 101; n = g6(a, 4);
        ok("MORPH 101 %: no answer", n == 0);
    }
    /* MUTATE: a variant (the amount kept) */
    {
        int16_t before[P_COUNT];
        uint32_t diff = 0;
        memcpy(before, TSEL->p, sizeof before);
        a[0] = 12; a[1] = 127; g6(a, 2);
        for (i = 0; i < P_COUNT; i++) diff += before[i] != TSEL->p[i];
        ok("MUTATE 127: answer 12 amt rc 0", head(12) && host_wire[5] == 127 && host_wire[6] == 0);
        ok("MUTATE 127: the sound changed", diff > 0);
        a[0] = 13; g6(a, 1);
        ok("MUTATE: amount kept", host_wire[8] == 127);
        a[0] = 12; a[1] = 0; n = g6(a, 2);
        ok("MUTATE 0: no answer", n == 0);
    }

    /* SAVE on a track that is not P600: rc 2, nothing kept */
    set_engine(0);
    a[0] = 6; a[1] = 5; a[2] = 0; g6(a, 3);
    ok("SAVE on ANALOG: rc 2", head(6) && host_wire[7] == 2 && p6_find(5) < 0);
    a[0] = 11; a[1] = 1; a[2] = 0; a[3] = 50; g6(a, 4);
    ok("MORPH on ANALOG: rc 2", head(11) && host_wire[8] == 2);

    /* out of range: no answer */
    a[0] = 9; a[1] = 127; a[2] = 1; n = g6(a, 3);
    ok("LOAD 255: no answer", n == 0);

    /* the Felucca frames still answer */
    host_wire_n = 0; ota_frame_done();
    sysex_byte(0xF0); sysex_byte(ED_HDR0); sysex_byte(ED_HDR1); sysex_byte(ED_HDR2); sysex_byte(ED_PING); sysex_byte(0xF7);
    ed_service(); host_drain(); n = host_wire_n;
    ok("PING still answered", n > 0);

    /* the beat (14): pushed while watched, on start / stop and on each beat */
    host_wire_n = 0; ota_frame_done();
    sysex_byte(0xF0); sysex_byte(ED_HDR0); sysex_byte(ED_HDR1); sysex_byte(ED_HDR2); sysex_byte(ED_WATCH); sysex_byte(1); sysex_byte(0xF7);
    ed_service(); host_drain();
    song.playing = 1; beat_n = 2; host_wire_n = 0; ed_service(); host_drain();
    {
        uint32_t j, f = 0;
        for (j = 0; j + 7 < host_wire_n; j++)
            if (host_wire[j] == 0xF0 && host_wire[j + 1] == 0x7D && host_wire[j + 2] == 0x47 && host_wire[j + 4] == 14 && host_wire[j + 5] == 1 && host_wire[j + 6] == 2) f = 1;   /* (14 playing beat armed step) */
        ok("BEAT: pushed (playing, beat 3)", f);
        host_wire_n = 0; ed_service(); host_drain();
        for (j = 0, f = 0; j + 7 < host_wire_n; j++) if (host_wire[j] == 0xF0 && host_wire[j + 4] == 14) f = 1;
        ok("BEAT: not again on the same beat", !f);
        song.playing = 0; host_wire_n = 0; ed_service(); host_drain();
        for (j = 0, f = 0; j + 7 < host_wire_n; j++) if (host_wire[j] == 0xF0 && host_wire[j + 4] == 14 && host_wire[j + 5] == 0) f = 1;
        ok("BEAT: the stop pushed", f);
    }

    /* TRANSPORT (15): PLAY asks for the start, REC arms the selected track (the beat push says so) */
    host_wire_n = 0; ota_frame_done();   /* (WATCH off: no beat push before the answers) */
    sysex_byte(0xF0); sysex_byte(ED_HDR0); sysex_byte(ED_HDR1); sysex_byte(ED_HDR2); sysex_byte(ED_WATCH); sysex_byte(0); sysex_byte(0xF7);
    ed_service(); host_drain();
    transport_req = 0; song.playing = 0; song.rec = 0;
    a[0] = 15; a[1] = 1; g6(a, 2);
    ok("PLAY: answer, a start asked", head(15) && transport_req == 1);
    song.playing = 1; transport_req = 0;
    a[1] = 1; g6(a, 2);
    ok("PLAY while playing: a stop asked", head(15) && host_wire[5] == 1 && (transport_req == 2 || !song.playing));   /* (the host's
                                                    * watchdog stops it while the answer goes out) */
    a[1] = 3; g6(a, 2);
    ok("REC: track 1 armed", head(15) && (song.rec & 1u) && host_wire[6] == (song.rec & 0x7F));
    a[1] = 4; g6(a, 2);
    {
        uint32_t j, f = 0;   /* (the beat push may go out: no answer to 15 only) */
        for (j = 0; j + 5 < host_wire_n; j++) if (host_wire[j] == 0xF0 && host_wire[j + 1] == 0x7D && host_wire[j + 2] == 0x47 && host_wire[j + 4] == 15) f = 1;
        ok("TRANSPORT op 4: no answer", !f);
    }

    printf(fails ? "p600 editor: %d FAIL\n" : "p600 editor: all ok\n", fails);
    return fails != 0;
}
