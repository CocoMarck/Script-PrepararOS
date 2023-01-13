import os, pathlib
import Modulo_Util as Util





fnl = 'txt'
err = '# Configuración erronea'

def Script_Menu():
    cfg_file = f'Script_Preparar-OS_CFG.{fnl}'

    loop = True
    while loop == True:
        Util.CleanScreen()
        opc = input(Util.Title(txt='Preparar sistema', see=False) +
            '1. Automatico\n'
            '2. Aplicaciones\n'
            '3. Aptitude\n'
            '4. Repositorios no libres\n'
            '5. Activar Triple buffer\n'
            '9. Ver comandos creados\n'
            '0. Salir\n'
            'Elige una opción: ')

        if (
            opc == '1' or
            opc == '2' or
            opc == '3' or
            opc == '4' or
            opc == '5' or
            opc == '9' or
            opc == '0'
        ): Continue()
        else: pass

        cfg_save = True
        if opc == '1':
            cfg = (
                apt('update') + ' &&\n\n' +
                App('Essential', '&&\n\n') + App('Dependence','&&\n\n') +
                App('Desktop','&&\n\n') + App('Optional','&&\n\n') +
                App('Uninstall', '&&\n\n') + apt('clean') + ' &&\n\n' +
                TripleBuffer()
            )

        elif opc == '2':
             opc = input(
                       Util.Title('Aplicaciones', see=False) +
                       '1. Necesarias\n'
                       '2. Dependencias\n'
                       '3. Desinstalar\n'
                       '4. Escritorio\n'
                       '5. Opcionales\n'
                       'Elige una opción: '
                   )
             
             if (
                 opc == '1' or
                 opc == '2' or
                 opc == '3' or
                 opc == '4' or
                 opc == '5'
             ):
                 if opc == '1': opc = 'Essential'
                 if opc == '2': opc = 'Dependence'
                 if opc == '3': opc = 'Uninstall'
                 if opc == '4': opc = 'Desktop'
                 if opc == '5': opc = 'Optional'

                 Continue()
                 cfg = App(opc = opc)

             else:
                 Util.Continue(msg=True)
                 cfg_save = False

        elif opc == '3': cfg = System_apt()

        elif opc == '4': cfg = Repository()

        elif opc == '5': cfg = TripleBuffer()

        elif opc == '9':
            cfg_save = False
            if pathlib.Path(cfg_file).exists():
                with open(cfg_file, 'r') as file_cfg:
                    reader = file_cfg.read()
                    input(f'{reader}\n\nPreciona enter para continuar...')

        elif opc == '0':
            cfg_save, loop = False, False
            print('Hasta la proxima...')

        else:
            cfg_save = False
            cfg = err + '\n\n'
            Util.Continue(msg=True)


        if cfg_save == True:
            Util.CleanScreen()
            if cfg == '': pass
            else:
                opc = Util.Continue(cfg + '\n' + Util.Separator() +
                                    '\n¿Continuar?')
                if opc == 's':
                    os.system(cfg)
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(cfg + f'\n#{Util.Separator(see=False)}\n')
                    input('Precione enter para continuar....')
                else: pass




def Continue(txt='¿Continuar?'):
    opc = Util.Continue(txt=txt)
    if opc == 's': pass
    elif opc == 'n': Script_Menu()
    else: pass




def apt(txt = ''):
    cmd = 'sudo apt '
    if txt == 'update':
        cmd = Util.Aptitude('update')

    elif txt == 'clean':
        cmd = Util.Aptitude('clean')

    elif txt == 'install':
        cmd = Util.Aptitude('install')

    elif txt == 'purge':
        cmd = Util.Aptitude('purge')


    return cmd




def System_apt():
    opc = input(Util.Title(txt='Opciones aptitude', see=False) +
        '1. Actualizar\n'
        '2. Limpiar\n'
        'Elige una opción: ') 
    if opc == '1':
        cfg = apt('update')
    elif opc == '2':
        cfg = apt('clean')
    else:
        Util.Continue(msg=True)
        cfg = err + '\n\n'
    Util.CleanScreen()
    return cfg




def App(
        opc = '',
        txt = '',
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
            f'{apt(txt="install")} flatpak &&\n'
        
            'sudo flatpak remote-add --if-not-exists flathub '
            'https://flathub.org/repo/flathub.flatpakrepo &&\n'

            f'{apt(txt="install")} gnome-software-plugin-flatpak'
        ],

        'Optional-wine': [
            'sudo dpkg --add-architecture i386 && clear &&\n'

            'sudo wget -nc -O /usr/share/keyrings/winehq-archive.key '
            'https://dl.winehq.org/wine-builds/winehq.key &&\n'

            'clear &&\n'

            'sudo wget -nc -P /etc/apt/sources.list.d/ '
            'https://dl.winehq.org/wine-builds/debian/dists/bullseye/'
            'winehq-bullseye.sources &&\n'

            f'{apt(txt="update")} && clear &&\n'

            f'{apt(txt="install")} '
            '--install-recommends winehq-stable && clear &&\n'

            'wine --version'
        ],

        'Optional-woeusb-ng': [
            f'{apt(txt="install")} '
            'git p7zip-full python3-pip python3-wxgtk4.0 grub2-common '
            'grub-pc-bin && sudo pip3 install WoeUSB-ng'
        ]                
    }

    if pathlib.Path('Script_Preparar-OS_Apps').exists(): pass
    else: os.mkdir('Script_Preparar-OS_Apps')

    cfg = '# Sin configurar\n\n'
    cfg_save = True
    cfg_file = ''
    cfg_dir = './Script_Preparar-OS_Apps/'
    txt_title = 'Applications / '
    txt_add = apt('install')
    txt_fnl = ''

    if (
        opc == 'Desktop' or
        opc == 'Optional'
    ):
        if opc == 'Desktop':
            opc = input(
                Util.Title(f'{txt_title}{opc}', see = False) +
                '1. Xfce 4\n'
                '2. KDE Plasma\n'
                '3. Gnome 3\n'
                '4. LXDE\n'
                '5. Mate\n'
                'Elige una opcion: '
            )
        

            if opc == '1': opc = 'Desktop-xfce4'
            elif opc == '2': opc = 'Desktop-kdeplasma'
            elif opc == '3': opc = 'Desktop-gnome3'
            elif opc == '4': opc = 'Desktop-lxde'
            elif opc == '5': opc = 'Desktop-mate'
            else: opc = 'Escritorio'

        elif opc == 'Optional':
            opc = input(
                Util.Title(f'{txt_title}{opc}', see = False) +
                '1. Wine HQ\n'
                '2. Flatpak\n'
                '3. WoeUSB NG\n'
                '9. Todas las Aplicaciones\n'
                'Elige una opcion: '
            )
            if opc == '1': opc = 'Optional-wine'
            elif opc == '2': opc = 'Optional-flatpak'
            elif opc == '3': opc = 'Optional-woeusb-ng'
            elif opc == '9':
                opc = None
                cfg = (
                    App('Optional-wine', '&&\n\n') +
                    App('Optional-flatpak','&&\n\n') +
                    App('Optional-woeusb-ng') + txt
                )
            else: opc = 'Opcionales'

        if (
            opc == 'Desktop-xfce4' or
            opc == 'Desktop-kdeplasma' or
            opc == 'Desktop-gnome3' or
            opc == 'Desktop-lxde' or
            opc == 'Desktop-mate' or
            opc == 'Optional-wine' or
            opc == 'Optional-flatpak' or
            opc == 'Optional-woeusb-ng'
        ): pass


    if (
        opc == 'Essential' or
        opc == 'Dependence' or
        opc == 'Uninstall' or

        opc == 'Desktop-xfce4' or
        opc == 'Desktop-kdeplasma' or
        opc == 'Desktop-gnome3' or
        opc == 'Desktop-lxde' or
        opc == 'Desktop-mate' or

        opc == 'Optional-wine' or
        opc == 'Optional-flatpak' or
        opc == 'Optional-woeusb-ng'
    ):
        txt_title += opc
        cfg_file = f'App_{opc}.{fnl}'
        apps = apps[opc]


        if opc == 'Dependence':
            txt_add = (
                f'sudo dpkg --add-architecture i386 {txt}' + apt('install')
            )

        elif opc == 'Uninstall':
            txt_add = apt('purge')


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




def TripleBuffer(txt=''):
    cfg = Util.Title(txt='Triple Buffer', see=False)
    os.system('grep drivers /var/log/Xorg.0.log ')

    path = '/etc/X11/xorg.conf.d/'
    file_txt = f'Script_Preparar-OS_TripleBuffer.{fnl}'
    file_copy = f'sudo cp {file_txt}'
    file_remove = f'sudo rm {path}'

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

    print('\n')
    opc = input(
              Util.Title(txt='Activar Triple buffer', see=False) +
              '1. Grafica AMD\n'
              '2. Grafica Intel\n'
              '0. No hacer nada\n'
              'Elige una opcion: '
          )

    if opc == '1': opc = '20-radeon.conf'
    elif opc == '2': opc = '20-intel-gpu.conf'
    else: pass

    if (opc == '20-radeon.conf' or
        opc == '20-amdgpu.conf' or
        opc == '20-intel-gpu.conf'):

        with open(file_txt, "w") as file_txt:
            for line in Triple_Buffer[opc]:
                file_txt.write(line + "\n")

        file_copy = f'{file_copy} {path}{opc}\n\n'

        if opc == '20-radeon.conf':
            file_remove = (f'{file_remove}20-amdgpu.conf && \n'
                           f'{file_remove}20-intel-gpu.conf')

        elif opc == '20-amdgpu.conf':
            file_remove = (f'{file_remove}20-redeon.conf && \n'
                           f'{file_remove}20-intel-gpu.conf')

        elif opc == '20-intel-gpu.conf':
            file_remove = (f'{file_remove}20-redeon.conf && \n'
                           f'{file_remove}20-amdgpu.conf')


    elif opc == '0': cfg, file_copy, file_remove = '', '', ''
    else:
        Util.Continue(msg=True)
        cfg, file_copy, file_remove = f'{err} (Triple Buffer)\n\n', '', ''
        

    cfg = cfg + file_copy + file_remove + ' ' + txt


    return cfg




if __name__ =='__main__':
   Script_Menu()