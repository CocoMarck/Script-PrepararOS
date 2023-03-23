import Modulo_Util as Util
import pathlib, os

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
    file_source = f'Script_Preparar-OS_sources.{fnl}'
    path = '/etc/apt/'

    if pathlib.Path(file_source).exists(): pass
    else:
        with open(file_source, 'w') as source_file:
            source_file.write(
                    '#Debian 11\n'
                    '\n'
                    '# Main Repo - main contrib non-free\n'
                    'deb http://deb.debian.org/debian/ bullseye main contrib non-free\n'
                    '#deb-src http://deb.debian.org/debian/ bullseye main contrib non-free\n'
                    '\n'
                    '# Security Repo - main contrib non-free\n'
                    'deb http://security.debian.org/ bullseye-security main contrib non-free\n'
                    '#deb-src http://security.debian.org/ bullseye-security main contrib non-free\n'
                    '\n'
                    '# Updates Repo - main contrib non-free\n'
                    'deb http://deb.debian.org/debian bullseye-updates main contrib non-free\n'
                    '#deb-src http://deb.debian.org/debian bullseye-updates main\n'
                    '\n'
                    '# Proposed Updates Repo - main contrib non-free\n'
                    '#deb http://deb.debian.org/debian/ bullseye-proposed-updates main contrib non-free\n'
                    '#deb-src http://deb.debian.org/debian/ bullseye-proposed-updates main contrib non-free\n'
                    '\n'
                    '# bullseye-backports, previously on backports.debian.org\n'
                    'deb http://deb.debian.org/debian/ bullseye-backports main contrib non-free\n'
                    '#deb-src http://deb.debian.org/debian/ bullseye-backports main contrib non-free\n'
                    '\n'
                    '# Testing repo used to get software not in the normal repos\n'
                    '#deb http://deb.debian.org/debian/ testing main contrib non-free\n'
                    '\n'
                    '# Unstable repo used to get software not in the normal repos\n'
                    '#deb http://deb.debian.org/debian/ unstable main contrib non-free'
            )



    if pathlib.Path(path + 'sources.list').exists():
        cfg = (Util.Title(txt='Repositorios', see=False) +
            f'sudo mv {path}sources.list {path}BackUp_sources.list &&\n'
            f'sudo cp {file_source} {path}sources.list {txt}')

    else: cfg = f'sudo cp {file_source} {path}sources.list {txt}'


    return cfg


def TripleBuffer(opc='', txt=''):
    cfg = Util.Title(txt='Triple Buffer', see=False)
    #os.system('grep drivers /var/log/Xorg.0.log ')

    path = '/etc/X11/xorg.conf.d/'
    file_txt = f'Script_Preparar-OS_TripleBuffer.{fnl}'
    file_copy = f'sudo cp {file_txt}'
    file_remove = f'sudo rm {path}20-* &&\n'

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
        cfg_dir = './Script_Preparar-OS_Apps/',
        txt_title = 'Applications / ',
        txt_add = Aptitude('install'),
    ):


    apps = {
       'Essential' : [
            'bleachbit',
            'transmission',
            'p7zip-full',
            'eog',
            'ffmpeg',
            'scrcpy',
            'adb',
            'htop',
            'neofetch',
            'mpv',
            'gdebi',
            'mangohud',
            'thunderbird',
            'wget',
            'openjfx',
            'git',
            'curl',
            'youtube-dl',
            'gnome-sound-recorder',
            'libsdl2-mixer-2.0-0',
            'cpu-x',
            'ntp',
            'gnome-disk-utility',
            'fonts-noto-color-emoji',
            'telegram-desktop',
            '&& sudo systemctl enable ntp'
        ],

        'Dependence' : [
            'gir1.2-libxfce4ui-2.0',
            'gir1.2-libxfce4util-1.0',
            'libc6:i386',
            'libasound2:i386',
            'libasound2-data:i386',
            'libasound2-plugins:i386',
            'libgtk2.0-0:i386',
            'libxml2:i386',
            'libsm6:i386',
            'libqt5widgets5'
        ],

        'Uninstall' : [
            'mozc-data',
            'mozc-server',
            'mlterm-common',
            'xiterm+thai',
            'fcitx-data',
            'fcitx5-data',
            'goldendict',
            'uim',
            'anthy',
            'kasumi',
            'audacious'
        ],


        'Desktop-xfce4': [
            'gnome-calculator', 
            'eog',
            'bijiben',
            'gvfs-backends',
            'gparted',
            'menulibre',
            'lightdm-gtk-greeter-settings',
            'gnome-software',
            'blueman',
            'atril',
            'file-roller',
            'xfce4-goodies',
            'telegram-desktop',
            'redshift-gtk'
        ],

        'Desktop-kdeplasma': [
            'rofi'                
        ],

        'Desktop-gnome3': [
            'rofi'
        ],

        'Desktop-lxde': [
            'rofi'
        ],

        'Desktop-mate': [
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

    if pathlib.Path('Script_Preparar-OS_Apps').exists(): pass
    else: os.mkdir('Script_Preparar-OS_Apps')

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
        with open(cfg_file, "r") as file_txt:
            txt_file = file_txt.readlines()
            txt_fnl = ''
            for txt_ln in txt_file:
                txt_fnl += txt_ln.replace('\n', ' ')


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
