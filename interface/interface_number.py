'''
Este modulo es para información numerica relacionada con la interfaz.
Por ejemplo:
Valores xy de dimenciónes de ventana.
Valores xy de para fuente de texto.
Valores xy de para iconos.
'''
from logic.display_number import *


# Establecer dimenciones de windegts y ventana
# Limite de resolucion: Anchura y altura de 480px como minimo.
num_font = get_display_number(divisor=120)
num_space_padding = int(num_font/4)
nums_margin = [ num_font/4, num_font/8 ]

nums_win_main = [
    get_display_number(multipler=0.2, based='width'),
    get_display_number(multipler=0.35, based='height')
]

nums_win_automatic = [
    get_display_number(multipler=0.2, based='width'),
    get_display_number(multipler=0.15, based='height')
]

nums_win_apps = [
    get_display_number(multipler=0.14, based='width'),
    get_display_number(multipler=0.2, based='height')
]

nums_win_app_desktop = [
    get_display_number(multipler=0.17, based='width'),
    get_display_number(multipler=0.2, based='height')
]

nums_win_app_optional = [
    get_display_number(multipler=0.275, based='width'),
    get_display_number(multipler=0.475, based='height')
]

nums_win_apt = [
    get_display_number(multipler=0.17, based='width'),
    get_display_number(multipler=0.17, based='height')
]

nums_win_triple_buffer = [
    get_display_number(multipler=0.17, based='width'),
    get_display_number(multipler=0.25, based='height')
]

nums_win_mouse_cfg = [
    get_display_number(multipler=0.135, based='width'),
    get_display_number(multipler=0.125, based='height')
]

nums_win_command_run = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.25, based='height')
]

nums_win_text_edit = [
    get_display_number(multipler=0.3, based='width'),
    get_display_number(multipler=0.3, based='height')
]