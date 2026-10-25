/* Double appui EDIT : la page suivante ne doit jamais s'afficher entre les deux appuis. */
#include "felucca_web.c"
static uint32_t seen[64];
static void run(double ms)
{
    uint32_t n = (uint32_t)(ms * 44.1 / 128 + 0.5), k;
    for (k = 0; k < n; k++) { web_render(128); seen[ui.page & 63] = 1; }
}
static void tap(uint32_t b, double after) { web_buttons(1u << b); run(70); web_buttons(0); run(after); }
int main(void)
{
    int i, p;
    web_nor_erase(); web_boot(); run(7000);
    for (i = 0; i < 3; i++) tap(B_EDIT, 500);
    printf("départ page %u %s\n", ui.page, PAGES[ui.page].title);
    for (i = 0; i < 3; i++) {
        memset(seen, 0, sizeof seen);
        p = ui.page;
        tap(B_EDIT, 120); tap(B_EDIT, 600);
        printf("double : %u -> %u %-10s pages vues :", p, ui.page, PAGES[ui.page].title);
        for (int k = 0; k < 64; k++) if (seen[k]) printf(" %d", k);
        printf("\n");
    }
    p = ui.page; tap(B_EDIT, 500); printf("simple : %u -> %u\n", p, ui.page);
    tap(B_ENV, 500); p = ui.page; tap(B_EDIT, 120); tap(B_EDIT, 600); printf("ENV puis double EDIT : %u -> %u %s\n", p, ui.page, PAGES[ui.page].title);
    printf("verrou %u\n", ui.lock);
    return 0;
}
