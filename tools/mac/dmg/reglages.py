# Réglages dmgbuild de l'image disque Guru-600 (lancés par make_dmg.sh, qui passe les chemins en defines).
import os
installer = defines['installer']          # le document script « Installer Guru-600.scptd »
files = [installer]
hide_extensions = [os.path.basename(installer)]
icon = defines['icns']                    # l'icône du disque
background = defines['fond']              # le fond 660 x 420 (TIFF 1x + 2x)
window_rect = ((200, 140), (660, 420))
default_view = 'icon-view'
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
icon_size = 128
text_size = 13
icon_locations = {os.path.basename(installer): (152, 238)}
format = 'UDZO'
compression_level = 9
filesystem = 'HFS+'
