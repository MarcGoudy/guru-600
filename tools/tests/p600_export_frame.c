/* L'export (trame complète) des sons d'usine non modifiés contre le fichier de Sequential : les 35 octets du programme */
#include "felucca_web.c"
int main(int argc, char **argv)
{
    static uint8_t f[3500], o[64];
    FILE *fp = fopen(argv[1], "rb");
    uint32_t i, same = 0, n = 0;
    fread(f, 1, sizeof f, fp); fclose(fp);
    web_nor_erase(); web_boot();
    for (i = 0; i < 100u; i++) {
        n = p600_export(i, o);
        if (!memcmp(o + 23, f + i * 35u, 35)) same++;
    }
    printf("trame %u octets ; %u / 100 programmes d'usine identiques à l'octet\n", n, same);
    return 0;
}
