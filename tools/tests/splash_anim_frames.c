#include "felucca_web.c"
static void shot(const char *dir, uint32_t n){ char p[600]; uint32_t i; FILE *f; snprintf(p,600,"%s/f%04u.ppm",dir,n); f=fopen(p,"wb");
 fprintf(f,"P6\n240 240\n255\n"); for(i=0;i<240u*240u;i++){ uint16_t v=web_fb[i]; v=(uint16_t)((v>>8)|(v<<8));
 fputc(((v>>11)&31)*255/31,f); fputc(((v>>5)&63)*255/63,f); fputc((v&31)*255/31,f);} fclose(f);}
int main(int argc, char **argv){ uint32_t k, n=0; (void)argc;
 web_nor_erase(); web_boot(); lcd_fill(0,0,240,240,SPL_BG);
 for (k=0; k<=6500u; k+=30u){ splash_anim(k); lcd_sync(); shot(argv[1], n++); }
 return 0;}
