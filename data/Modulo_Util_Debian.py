from logic.Modulo_System import(
    CleanScreen
)

from logic.Modulo_Text import(
    Text_Read,
    Ignore_Comment,
    only_one_char
)

from interface.Modulo_ShowPrint import(
    Title,
    Continue
)
from logic.Modulo_Files import *

import pathlib, os, sys, subprocess
from glob import glob

# Obtén la ruta al directorio actual del script
current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )

# Extencion y nombres de archivo
preset_start = 'Script'
fnl = 'txt'

# Script | Construye la ruta a resources desde el directorio que contiene el módulo
dir_data = os.path.join(current_dir, 'resources')
dir_script_apps = os.path.join( dir_data, 'Script_Apps' )
dir_app_optional = os.path.join( dir_script_apps, 'App_Optional' )

# Script | Archivos
file_script_cfg = os.path.join( dir_data, f'Script_CFG.{fnl}' )
file_script_mouse_config = os.path.join( dir_data, f'Script_Mouse-Acceleration.{fnl}' )
file_script_sources = os.path.join( dir_data, f'Script_sources.{fnl}' )
file_script_triple_buffer = os.path.join( dir_data, f'Script_TripleBuffer.{fnl}' )


# Sistema | Directorios archivos
dir_x11_config = os.path.join( '/usr/share/X11/xorg.conf.d/' )
dir_apt = os.path.join( '/etc/apt/' )

# Sistema | Archivos
file_x11_mouse_config = os.path.join( dir_x11_config, '50-mouse-acceleration.conf' )
file_apt_sources = os.path.join( dir_apt, 'sources.list' )


# Constantes
cmd_triple_buffer = 'grep drivers /var/log/Xorg.0.log'
cmd_run_triple_buffer = (
    subprocess.check_output(
        cmd_triple_buffer, shell=True, text=True
    )
)

#print(dir_x11_mouse_config)
#input()




# Programa...
err = '# Configuración erronea'




def Aptitude(opc = 'clean', txt=''):
    apt = 'sudo apt'
    if opc == 'update':
        cmd = f'{apt} {opc} && sudo apt upgrade'

    elif opc == 'clean':
        cmd = f'{apt} autoremove && {apt} {opc}'

    elif opc == 'install':
        cmd = f'{apt} {opc}'

    elif opc == 'purge':
        cmd = f'{apt} {opc}'

    else: cmd = ''
    
    cmd = cmd + ' ' + txt


    return cmd


def get_random_repository():
    '''
    Devuelve un backup de sources.list, con preset random
    '''
    return os.path.join( dir_apt, 'BackUp_sources.list' )


def Repository(txt=''):

    # Detectar si existe sources.list crear texto non-free
    if pathlib.Path(file_script_sources).exists(): pass
    else:
        if pathlib.Path(file_apt_sources).exists():
            archive = Text_Read(
                file_and_path=file_apt_sources,
                option='ModeText'
            )
        
            text_ready = ''
            for line in archive.split('\n'):
                if (
                    line.startswith('deb') and
                    line.endswith('main contrib')
                ):
                    text_ready += f'{line} non-free\n'
                else:
                    text_ready += line + '\n'

            # Para eliminar el ultimo salto de linea
            text_ready = text_ready[:-1]
            with open(file_script_sources, 'w') as file_ready:
                file_ready.write(text_ready)
        else:
            pass

    # Fin Agregar Configuracion
    if pathlib.Path( file_apt_sources ).exists():
        cfg = (Title(text='Repositorios', print_mode=False) +
            f'sudo mv {file_apt_sources} {get_random_repository()} &&\n'
            f'sudo cp {file_script_sources} {file_apt_sources} {txt}')

    else: cfg = f'# No se detecto "{file_apt_sources}"'


    return cfg


def TripleBuffer(opc='', txt=''):
    cfg = Title(text='Triple Buffer', print_mode=False)
    #os.system('grep drivers /var/log/Xorg.0.log ')

    file_copy = f'sudo cp {file_script_triple_buffer}'
    file_remove = ''
    try:
        archives = (
            sorted(
                pathlib.Path(f'{dir_x11_config}')
                .glob('20-*')
            )
        )
        for arch in archives:
            if pathlib.Path(f'{arch}').exists():
                file_remove = f'sudo rm {dir_x11_config}20-* &&\n'
            else:
                pass
    except:
        pass

    Triple_Buffer = {
        '20-radeon.conf': [
            'Section "Device"',
            '   Identifier  "AMD Graphics"',
            '   Driver      "radeon"',
            '   Option      "TearFree"  "true"',
            'EndSection'
        ],

        '20-amdgpu.conf': [
            'Section "Device"',
            '   Identifier  "AMD Graphics"',
            '   Driver      "amdgpu"',
            '   Option      "TearFree"  "true"',
            'EndSection'
        ],

        '20-intel-gpu.conf': [
            'Section "Device"',
            '   Identifier  "Intel Graphics"',
            '   Driver      "intel"',
            '   Option      "TearFree"  "true"',
            'EndSection'
        ],
    }

    if (opc == '20-radeon.conf' or
        opc == '20-amdgpu.conf' or
        opc == '20-intel-gpu.conf'):

        with open(file_script_triple_buffer, "w") as file_txt:
            for line in Triple_Buffer[opc]:
                file_txt.write(line + "\n")

        file_copy = f'{file_copy} {dir_x11_config}{opc}'

    elif opc == '0': cfg, file_copy, file_remove = '', '', ''
    else:
        Continue(message_error=True)
        cfg, file_copy, file_remove = f'{err} (Triple Buffer)\n\n', '', ''
        

    cfg = cfg + file_remove + file_copy + ' ' + txt


    return cfg




def App(
        opc = '',
        txt = '',
        cfg_save = True,
        cfg_file = '',
        cfg_dir = dir_script_apps,
        txt_title = 'Applications / ',
        txt_add = Aptitude('install'),
    ) -> str:
    '''
    Lee un archivo con instrucciónes de terminal.
    txt_title -> str, agrega un titulo a las instrucciónes.
    txt_add -> str, es para agregar texto al inicio.
    cfg_save -> bool, es para guardar o lo devuelto por la función.
    
    Esto se usa para las opciones preestablecidas:
    opc ->, es la opcion de las prestablecidas
    
    Esto se usa para apps opcionales:
    cfg_dir -> str, es la carpeta del archivo
    cfg_file -> str, es la el archivo
    
    Devuelve un str
    '''

    apps = {
       'Essential' : [
            '# Essential',
            'neofetch'
        ],

        'Dependence' : [
            '# Dependences',
            'p7zip-full'
        ],

        'Uninstall' : [
            '# Unisnstall',
            'mozc-data'
        ],


        'Desktop-xfce4': [
            '# task-xfce-desktop # For install Xfce Desktop',
            'xfce4-goodies'
        ],

        'Desktop-kdeplasma': [
            '# task-kde-desktop # For install KDE Desktop',
            'rofi'                
        ],

        'Desktop-gnome3': [
            '# task-gnome-desktop # For install Gnome Desktop',
            'rofi'
        ],

        'Desktop-lxde': [
            '# task-lxde-desktop # For install lxde Desktop',
            'rofi'
        ],

        'Desktop-mate': [
            '# task-mate-desktop # For install Mate Desktop',
            'rofi'
        ],

        'Optional-flatpak': [
            '# Instalacion de Flatpak'
        ],

        'Optional-wine': [
            '# Instalacion de WineHQ'
        ],

        'Optional-woeusb-ng': [
            '# Instalacion de WoeUSB NG'
        ]                
    }

    if pathlib.Path(dir_script_apps).exists(): pass
    else: os.mkdir(dir_script_apps)

    cfg = ''
    txt_fnl = ''

    if opc in apps:
        txt_title += opc
        cfg_file = f'App_{opc}.{fnl}'
        apps = apps[opc]


        if opc == 'Dependence':
            txt_add = (
                f'sudo dpkg --add-architecture i386 &&\n\n' + Aptitude('install')
            )

        elif opc == 'Uninstall':
            txt_add = Aptitude('purge')


        elif (
            opc == 'Desktop-xfce4' or
            opc == 'Desktop-kdeplasma' or
            opc == 'Desktop-gnome3' or
            opc == 'Desktop-lxde' or
            opc == 'Desktop-mate'
        ):
            cfg_dir = os.path.join( dir_script_apps, 'App_Desktop' )


        elif (
            opc == 'Optional-wine' or
            opc == 'Optional-flatpak' or
            opc == 'Optional-woeusb-ng'
        ):
            cfg_dir = os.path.join( dir_script_apps, 'App_Optional' )
            txt_add = ''
            
    elif opc == 'continue': pass

    elif opc == None: cfg_save = None

    else: cfg_save, cfg = False, f'Aplicaciones / {opc}'


    if cfg_file == '': pass
    else:
         if pathlib.Path(cfg_dir).exists(): pass
         else: os.mkdir(cfg_dir)
         cfg_file = os.path.join( cfg_dir, cfg_file )

    if (
        pathlib.Path(cfg_file).exists() or
        cfg_file == ''
    ): pass


    else:
        with open(cfg_file, "w") as file_cfg:
            for app in apps:
                file_cfg.write(app + "\n")


    if cfg_save == True:
        # Leer Archivo.txt y almacenar info en una sola variable.
        txt_fnl = Ignore_Comment(
            text=Text_Read(
                file_and_path = cfg_file,
                option='ModeText'
            ),
            
            comment='#'
        ).replace('\n', ' ')
        txt_fnl = only_one_char( char=' ', text=txt_fnl )

        if txt_add == '': pass
        else: txt_add += ' '
        cfg = (
            Title(text = txt_title, print_mode=False) +
            f'{txt_add}{txt_fnl} {txt}'
        )

    elif cfg_save == False:
        txt_add = ''
        cfg = f'{err} ({cfg})\n\n'
        Continue(message_error=True)

    else: pass

    CleanScreen()

    return cfg




def Mouse_Config(opc='', txt='') -> str:
    '''
    Guarda o elimina un archivo que desactiva la aceleración del mouse
    '''
    title = Title(text='Mouse Config', print_mode=False)

    file_copy = f'sudo cp {file_script_mouse_config}'
    file_remove = f'sudo rm {dir_x11_config}*mouse-acceleration*.conf &&\n'
    
    if opc == 'AccelerationON':
        file_copy = f'echo "{opc}"'

    elif opc == 'AccelerationOFF':
        with open(file_script_mouse_config, "w") as file_txt:
            file_txt.write(
                'Section "InputClass"\n'
                '    Identifier "my_mouse"\n'
                '    MatchIsPointer "yes"\n'
                '    Option "AccelerationProfile" "-1"\n'
                '    Option "AccelerationScheme" "none"\n'
                '    Option "AccelSpeed" "-1"\n'
                'EndSection'
            )

        file_copy = f'{file_copy} {file_x11_mouse_config}'
        file_remove = ''
        
    else:
        title, file_remove, file_copy, txt = '', '', '', ''

    cfg = title + file_remove + file_copy + ' ' + txt

    return cfg




# Obtener App-Optionar opcional:
def get_app_optional(remove_path=True) -> list:
    return Files_List(
        files='App_Optional-*.txt',
        path=os.path.join( dir_app_optional, '' ),
        remove_path=remove_path
    )
    
    

def exists_mouse_config() -> bool:
    if pathlib.Path(file_x11_mouse_config).exists():
        return True
    else:
        return False




# Agregar archivos necesarios:
# Agregar App-Optional default
if (
    pathlib.Path( 
        os.path.join(dir_app_optional, 'App_Optional-wine.txt' ) 
    ).exists() or

    pathlib.Path( 
        os.path.join(dir_app_optional, 'App_Optional-flatpak.txt') 
    ).exists() or

    pathlib.Path( 
        os.path.join(dir_app_optional, 'App_Optional-woeusb-ng.txt') 
    ).exists()
): 
    pass
    
else:
    App('Optional-wine')
    App('Optional-flatpak')
    App('Optional-woeusb-ng')