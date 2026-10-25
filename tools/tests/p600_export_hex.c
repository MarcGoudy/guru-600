#include "felucca_web.c"
int main(void) { uint8_t o[64]; uint32_t n, k; web_nor_erase(); web_boot(); n = p600_export(1, o);
  for (k = 0; k < n; k++) printf("%d%s", o[k], k + 1 < n ? "," : "\n"); return 0; }
