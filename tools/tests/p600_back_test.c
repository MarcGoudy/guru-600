/* Tous les boutons de page : un appui avance (après NAV_MS), deux appuis rapides reculent ; sans verrou de calque.
 *   cc -O2 -w -I../Felucca/build/gen -I../Felucca/firmware/src -I../Felucca/web/emu -o build/p600_back_test tests/p600_back_test.c -lm */
#include "felucca_web.c"
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 + 0.5), k;
    for (k = 0; k < n; k += 128u)
        web_render(n - k < 128u ? n - k : 128u);
}
static void tap(uint32_t b, double after)
{
    web_buttons(1u << b); run(70);
    web_buttons(0); run(after);
}
static uint32_t shown_mid;                          /* a page shown between the two taps of a double */
static void dbl(uint32_t b)
{
    uint32_t p0;
    web_buttons(1u << b); run(70); web_buttons(0); run(40);
    p0 = ui.home ? 999u : ui.page;
    run(60);
    web_buttons(1u << b); run(70); web_buttons(0);
    shown_mid = p0;
    run(600);
}
static void say(const char *what)
{
    printf("%-28s %-12s lock %u  oct %d\n", what, ui.home ? "HOME" : PAGES[ui.page].title, ui.lock, song.octave);
}
int main(void)
{
    static const struct { uint32_t b; const char *n; } F[] = {{B_EDIT, "EDIT"}, {B_ENV, "ENV"}, {B_LFO, "LFO"},
        {B_FX, "FX"}, {B_SAVE, "SAVE"}, {B_ARP, "ARP"}, {B_SEQ, "SEQ"}, {B_SCL, "SCL"}, {B_GLO, "GLO"}, {B_HOME, "HOME"}};
    uint32_t k;
    char t[64];
    web_nor_erase(); web_boot(); run(7000);
    for (k = 0; k < sizeof F / sizeof F[0]; k++) {
        uint32_t before;
        tap(F[k].b, 600); snprintf(t, sizeof t, "%s", F[k].n); say(t);
        tap(F[k].b, 600); snprintf(t, sizeof t, "%s x1", F[k].n); say(t);
        tap(F[k].b, 600); snprintf(t, sizeof t, "%s x1", F[k].n); say(t);
        before = ui.home ? 999u : ui.page;
        dbl(F[k].b); snprintf(t, sizeof t, "%s x2 rapide", F[k].n); say(t);
        if (shown_mid != before)
            printf("   !! page montrée entre les deux appuis\n");
        dbl(F[k].b); snprintf(t, sizeof t, "%s x2 rapide", F[k].n); say(t);
        if (ui.lock) { printf("   !! calque verrouillé\n"); ui.lock = 0; }
    }
    tap(B_OCTDN, 300); say("OCT- seul");
    return 0;
}
