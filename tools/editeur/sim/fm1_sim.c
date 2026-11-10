/* Guru-600 : un FM-1 simulé pour essayer l'éditeur P600 sans la machine. Le vrai code de l'éditeur du firmware
 * (editor.c, eng_p600.c, comme tests/editor_test.c), derrière un port MIDI virtuel « Felucca (Guru-600 sim) » que
 * Chrome, Edge, Brave ou Comet voient comme le FM-1. Pas de son.
 * Sur l'entrée standard, une ligne « id valeur » change un paramètre de la piste choisie comme le ferait un bouton
 * du FM-1 (l'éditeur reçoit la poussée CHANGED), « track k » choisit la piste k (0..3). PLAY / STOP / REC de
 * l'éditeur font tourner le battement au tempo (BPM).
 *   sed -n '1,/^static int check/p' ../Felucca/tests/editor_test.c | sed '$d' > build/ed_prelude.c
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/tests -Ibuild -o build/fm1_sim \
 *      editeur/sim/fm1_sim.c -lm -framework CoreMIDI -framework CoreFoundation
 *   build/fm1_sim */
#include "ed_prelude.c"
#include <CoreMIDI/CoreMIDI.h>
#include <pthread.h>
#include <fcntl.h>
#include <unistd.h>
#include <time.h>

static MIDIEndpointRef sim_src;
static pthread_mutex_t sim_mx = PTHREAD_MUTEX_INITIALIZER;
static uint8_t sim_in[1 << 16];
static uint32_t sim_in_r, sim_in_w;

static void sim_read(const MIDIPacketList *pl, void *a, void *b)
{
    const MIDIPacket *p = &pl->packet[0];
    uint32_t i, k;
    (void)a; (void)b;
    pthread_mutex_lock(&sim_mx);
    for (i = 0; i < pl->numPackets; i++, p = MIDIPacketNext(p))
        for (k = 0; k < p->length; k++)
            sim_in[sim_in_w++ & 0xFFFFu] = p->data[k];
    pthread_mutex_unlock(&sim_mx);
}
static void sim_send(const uint8_t *d, uint32_t n)
{
    static uint8_t buf[8192];
    MIDIPacketList *pl = (MIDIPacketList *)buf;
    MIDIPacket *p = MIDIPacketListInit(pl);
    uint32_t i = 0;
    while (i < n) {                                     /* (256 bytes a packet) */
        uint32_t k = n - i > 256u ? 256u : n - i;
        p = MIDIPacketListAdd(pl, sizeof buf, p, 0, k, d + i);
        if (!p) {
            MIDIReceived(sim_src, pl);
            p = MIDIPacketListInit(pl);
            continue;
        }
        i += k;
    }
    MIDIReceived(sim_src, pl);
}

static void sim_reset(void)
{
    uint32_t t, i;
    memset(&song, 0, sizeof song); memset(trk, 0, sizeof trk);
    memset(&ed_w, 0, sizeof ed_w); memset(&ui, 0, sizeof ui);
    memset(&settings, 0, sizeof settings); settings_init();
    host_progress = 1; usb.config = 1;
    for (i = 0; i < G_COUNT; i++) song.g[i] = GP[i].def;
    for (t = 0; t < NTRK; t++) {
        track_defaults(&trk[t]); set_engine_of(&trk[t], ENGI_P600); apply_preset_to(&trk[t], t);
        trk[t].engine = trk[t].eng_req; track_defaults_steps(&trk[t]);
    }
    for (i = 0; i < P6_NIMP; i++) p6_imp[i].used = 0;
    p6_booted = 1; p600_apply();
}

int main(void)
{
    MIDIClientRef cl;
    MIDIEndpointRef dst;
    char line[128];
    uint32_t ln = 0;
    sim_reset();
    if (MIDIClientCreate(CFSTR("Guru-600 sim"), 0, 0, &cl) ||
        MIDISourceCreate(cl, CFSTR("Felucca (Guru-600 sim)"), &sim_src) ||
        MIDIDestinationCreate(cl, CFSTR("Felucca (Guru-600 sim)"), sim_read, 0, &dst)) {
        fprintf(stderr, "fm1_sim: no CoreMIDI port\n");
        return 1;
    }
    fcntl(0, F_SETFL, fcntl(0, F_GETFL) | O_NONBLOCK);
    printf("fm1_sim: port « Felucca (Guru-600 sim) » ready\n");
    fflush(stdout);
    for (;;) {
        struct timespec ms = {0, 1000000};
        uint32_t got = 0;
        int c;
        pthread_mutex_lock(&sim_mx);
        while (sim_in_r != sim_in_w) {
            uint8_t b = sim_in[sim_in_r++ & 0xFFFFu];
            pthread_mutex_unlock(&sim_mx);
            if (b >= 0xF0u || b < 0x80u) { sysex_byte(b); got = 1; }   /* SysEx only (no sound here) */
            if (b == 0xF7u) { ed_service(); host_drain(); }
            pthread_mutex_lock(&sim_mx);
        }
        pthread_mutex_unlock(&sim_mx);
        while ((c = getchar()) != EOF) {                /* « id valeur », « track k » */
            if (c != '\n') { if (ln < sizeof line - 1u) line[ln++] = (char)c; continue; }
            line[ln] = 0; ln = 0;
            {
                int id, v;
                if (sscanf(line, "track %d", &v) == 1 && v >= 0 && v < (int)NTRK) song.sel = (uint8_t)v;
                else if (sscanf(line, "%d %d", &id, &v) == 2 && id >= 0 && id < P_COUNT) TSEL->p[id] = (int16_t)v;
            }
        }
        clearerr(stdin);
        {   /* the transport, as the audio ISR would run it (seq.c): no sound here, the beat only */
            static uint32_t beat_ms;
            if (transport_req == 1u || transport_req == 3u) { song.playing = 1; beat_n = 0; beat_ms = fm1_ms; transport_req = 0; }
            else if (transport_req == 2u) { song.playing = 0; transport_req = 0; }
            if (song.playing && fm1_ms - beat_ms >= 60000u / (uint32_t)(song.g[G_BPM] > 0 ? song.g[G_BPM] : 120)) {
                beat_ms = fm1_ms; beat_n = (beat_n + 1u) & 3u;
            }
        }
        ed_service();                                   /* the pushes (ed_sync) */
        host_drain();
        if (host_wire_n) { sim_send(host_wire, host_wire_n); host_wire_n = 0; }
        if (!got) nanosleep(&ms, 0);
        fm1_ms++;
    }
}
