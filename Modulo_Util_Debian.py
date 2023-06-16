import Modulo_Util as Util
import pathlib, os
from glob import glob

fnl = 'txt'
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


def Repository(txt=''):
    # Ruta y archivo
    file_source = f'Script_sources.{fnl}'
    path = '/etc/apt/'

    # Detectar si existe sources.list crear texto non-free
    if pathlib.Path(file_source).exists(): pass
    else:
        if pathlib.Path(f'{path}sources.list').exists():
            archive = Util.Text_Read(
                file_and_path=f'{path}sources.list',
                opc='ModeText'
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
            with open(file_source, 'w') as file_ready:
                file_ready.write(text_ready)
        else:
            pass

    # Fin Agregar Configuracion
    if pathlib.Path(path + 'sources.list').exists():
        cfg = (Util.Title(txt='Repositorios', see=False) +
            f'sudo mv {path}sources.list {path}BackUp_sources.list &&\n'
            f'sudo cp {file_source} {path}sources.list {txt}')

    else: cfg = f'# No se detecto "{path}sources.list"'


    return cfg


def TripleBuffer(opc='', txt=''):
    cfg = Util.Title(txt='Triple Buffer', see=False)
    #os.system('grep drivers /var/log/Xorg.0.log ')

    path = '/etc/X11/xorg.conf.d/'
    file_txt = f'Script_TripleBuffer.{fnl}'
    file_copy = f'sudo cp {file_txt}'
    file_remove = ''
    try:
        archives = (
            sorted(
                pathlib.Path(f'{path}')
                .glob('20-*')
            )
        )
        for arch in archives:
            if pathlib.Path(f'{arch}').exists():
                file_remove = f'sudo rm {path}20-* &&\n'
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

        with open(file_txt, "w") as file_txt:
            for line in Triple_Buffer[opc]:
                file_txt.write(line + "\n")

        file_copy = f'{file_copy} {path}{opc}'

    elif opc == '0': cfg, file_copy, file_remove = '', '', ''
    else:
        Util.Continue(msg=True)
        cfg, file_copy, file_remove = f'{err} (Triple Buffer)\n\n', '', ''
        

    cfg = cfg + file_remove + file_copy + ' ' + txt


    return cfg
    
def App(
        opc = '',
        txt = '',
        cfg_save = True,
        cfg_file = '',
        cfg_dir = './Script_Apps/',
        txt_title = 'Applications / ',
        txt_add = Aptitude('install'),
    ):


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

    if pathlib.Path('Script_Apps').exists(): pass
    else: os.mkdir('Script_Apps')

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
            cfg_dir += f'App_Desktop/'


        elif (
            opc == 'Optional-wine' or
            opc == 'Optional-flatpak' or
            opc == 'Optional-woeusb-ng'
        ):
            cfg_dir += f'App_Optional/'
            txt_add = ''
            
    elif opc == 'continue': pass

    elif opc == None: cfg_save = None

    else: cfg_save, cfg = False, f'Aplicaciones / {opc}'


    if cfg_file == '': pass
    else:
         if pathlib.Path(cfg_dir).exists(): pass
         else: os.mkdir(cfg_dir)
         cfg_file = cfg_dir + cfg_file

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
        txt_fnl = Util.Ignore_Comment(
            text=Util.Text_Read(
                file_and_path = cfg_file,
                opc='ModeText'
            ),
            
            comment='#'
        ).replace('\n', ' ')

        if txt_add == '': pass
        else: txt_add += ' '
        cfg = (
            Util.Title(txt = txt_title, see=False) +
            f'{txt_add}{txt_fnl} {txt}'
        )

    elif cfg_save == False:
        txt_add = ''
        cfg = f'{err} ({cfg})\n\n'
        Util.Continue(msg=True)

    else: pass

    Util.CleanScreen()

    return cfg


def Mouse_Config(opc='', txt=''):
    title = Util.Title(txt='Mouse Config', see=False)

    path = '/usr/share/X11/xorg.conf.d/'
    file_txt = f'Script_Mouse-Acceleration.{fnl}'
    file_copy = f'sudo cp {file_txt}'
    file_remove = f'sudo rm {path}*mouse-acceleration*.conf &&\n'
    
    if opc == 'AccelerationON':
        file_copy = '# Acceleration ON'

    elif opc == 'AccelerationOFF':
        with open(file_txt, "w") as file_txt:
            file_txt.write(
                'Section "InputClass"\n'
                '    Identifier "my_mouse"\n'
                '    MatchIsPointer "yes"\n'
                '    Option "AccelerationProfile" "-1"\n'
                '    Option "AccelerationScheme" "none"\n'
                '    Option "AccelSpeed" "-1"\n'
                'EndSection'
            )

        file_copy = f'{file_copy} {path}50-mouse-acceleration.conf'
        file_remove = ''
        
    else:
        title, file_remove, file_copy, txt = '', '', '', ''

    cfg = title + file_remove + file_copy + ' ' + txt

    return cfg