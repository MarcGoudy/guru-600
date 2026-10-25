/* L'export de chaque son d'usine, octet par octet, contre le fichier d'usine de Sequential.
 *   cc ... tests/p600_export_bytes.c ; build/p600_export_bytes fact.bin */
#include "felucca_web.c"
int main(int argc, char **argv)
{
    static uint8_t f[3500], o[35];
    static p6imp_t a;
    FILE *fp = fopen(argv[1], "rb");
    uint32_t i, k, same = 0, bytes = 0;
    fread(f, 1, sizeof f, fp); fclose(fp);
    web_nor_erase(); web_boot();
    for (i = 0; i < 100u; i++) {
        p6_of_place(i, &a);
        p6_to_sci(&a, i, o);
        for (k = 0; k < 35u; k++) bytes += o[k] == f[i * 35u + k];
        if (!memcmp(o, f + i * 35u, 35)) same++;
        else if (i < 100) { printf("prog %u :", i); for (k = 0; k < 35u; k++) if (o[k] != f[i*35u+k]) printf(" [%u] %02x/%02x", k, o[k], f[i*35u+k]); printf("\n"); }
    }
    printf("%u / 100 programmes identiques à l'octet ; %u / 3500 octets\n", same, bytes);
    return 0;
}
