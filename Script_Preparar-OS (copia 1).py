import os, pathlib
import Modulo_Util as Util

def Script_Menu():
    cfg_file = 'Script_Preparar-OS_CFG.txt'

    loop = True
    while loop == True:
        Util.CleanScreen()    
        opc = input(Util.Title(txt='Preparar sistema', see=False) +
            '1. Automatico\n'
            '2. Aptitude\n'
            '3. Repositorios no libres\n'
            '4. Activar Triple buffer\n'
            '9. Ver comandos creados\n'
            '0. Salir\n'
            'Elige una opción: ')
        Continue()
        cfg_save = False
        if opc == '1':
            cfg = (apt('update') + ' &&\n\n' +
                App('Essential', '&&\n\n') + App('Dependence','&&\n\n') +
                App('Desktop','&&\n\n') + App('Optional','&&\n\n') +
                App('Uninstall', '&&\n\n') + TripleBuffer('&&\n\n') +
                apt('clean') )
            cfg_save = True
        elif opc == '2':
            cfg = System_apt()
            cfg_save = True
        elif opc == '3':
            cfg = Repository()
            cfg_save = True
        elif opc == '4':
            cfg = TripleBuffer()
            cfg_save = True

        elif opc == '9':
            if pathlib.Path(cfg_file).exists():
                with open(cfg_file, 'r') as file_cfg:
                    reader = file_cfg.read()
                    input(f'{reader}\n\nPreciona enter para continuar...')
        elif opc == '0':
            print('Hasta la proxima...')
            exit()
        else:
            cfg = '#Configuración erronea'
            Util.Continue(txt=opc, msg=True)


        if cfg_save == True:
            opc = Util.Continue(cfg + '\n' + Util.Separator() +
                                '\n¿Continuar?')
            if opc == 's':
                os.system(cfg)
                with open(cfg_file, 'a') as file_cfg:
                    file_cfg.write(cfg + f'\n#{Util.Separator(see=False)}\n')
            elif opc == 'n': pass
            else:
                Util.Continue(txt=opc, msg=True)




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
        cfg = '#Configuración erronea'
    Util.CleanScreen()
    return cfg




def App(
        opc = '',
        txt = '',
        cfg_file = '',
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
            ]
        }
    ):

    cfg = '# Sin configurar\n\n'
    cfg_save = True
    cfg_dir = './Script_Preparar-OS_Apps/'
    txt_title = ''
    txt_add = ''
    txt_fnl = ''
    fnl = 'txt'

    if (
        opc == 'Essential' or
        opc == 'Dependence' or
        opc == 'Uninstall'
    ):
        txt_title = 'Applications / ' + opc
        txt_add = apt(txt='install')
        cfg_file = f'App_{opc}.{fnl}'
        apps = apps[opc]

        if opc == 'Dependence':
            txt_add = (
                f'sudo dpkg --add-architecture i386 {txt}' + apt('install')
            )

        elif opc == 'Uninstall':
            txt_add = apt('purge')


    elif opc == 'Desktop':
        cfg_file_desktop = {
            'xfce4' : f'App_{opc}-Xfce4.{fnl}',
            'kdeplasma' : f'App_{opc}-KDE-Plasma.{fnl}'
        }

        apps = {
            'xfce4': [
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

            'kdeplasma': [
                'rofi',
                ''
            ]
        }

        if (
            pathlib.Path(cfg_file_desktop['xfce4']).exists() and
            pathlib.Path(cfg_file_desktop['kdeplasma']).exists()
        ): pass

        else:
            App(cfg_file = cfg_file_desktop['xfce4'],
                apps = apps['xfce4'])

            App(cfg_file = cfg_file_desktop['kdeplasma'],
                apps = apps['kdeplasma'])



        opc = input(Util.Title(txt='Programas para Escritorios', see=False) +
            '1. Xfce4\n'
            '2. Kdenlive\n'
            'Elige una opción: ')
            
        if opc == '1':
            cfg_file = cfg_file_desktop['xfce4']
            txt_title = 'Programas para Xfce4'
            txt_add = apt(txt='install')


        elif opc == '2':
            cfg_file = cfg_file_desktop['kdeplasma']
            txt_title = 'Programas para KDE Plasma'
            txt_add = apt(txt='install')


        else: cfg_save = False


    elif (
        opc == 'Optional' or
        opc == 'flatpak' or
        opc == 'wine' or
        opc == 'woeusb-ng'
    ):
        cfg = ''
        cfg_save = None

        apps = {
            'flatpak': [
                f'{apt(txt="install")} flatpak &&\n'
        
                'sudo flatpak remote-add --if-not-exists flathub '
                'https://flathub.org/repo/flathub.flatpakrepo &&\n'

                f'{apt(txt="install")} gnome-software-plugin-flatpak'
            ],

            'wine': [
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

            'woeusb-ng': [
                f'{apt(txt="install")} '
                'git p7zip-full python3-pip python3-wxgtk4.0 grub2-common '
                'grub-pc-bin && sudo pip3 install WoeUSB-ng'
            ]
        }

        if opc == 'Optional':
            opc = input(Util.Title(txt='Aplicaciones opcionales', see=False) +
                '0. Sin apps opcionales\n'
                '1. FlatPak\n'
                '2. Wine\n'
                '3. WoeUSB-NG\n'
                '9. Todos\n'
                'Elige una opción: ')
            if opc == '0': opc = None
            elif opc == '1': opc = 'flatpak'
            elif opc == '2': opc = 'wine'
            elif opc == '3': opc = 'woeusb-ng'
            elif opc == '9': opc = 'all'
            else: opc = ''
        else: pass

        if (
            opc == 'flatpak' or
            opc == 'wine' or
            opc == 'woeusb-ng'
        ): 
            cfg_save = True
            cfg_file = f'App_Optional-{opc}.{fnl}'
            txt_title = f'Optional / {opc}'
            apps = apps[opc]

        elif opc == 'all':
            cfg = (
                App(txt='&&\n\n', opc = 'flatpak') +
                App(txt='&&\n\n', opc = 'wine') +
                App(txt='&&\n\n', opc = 'woeusb-ng')
            )

        elif opc == None:
            cfg, txt = '', ''

        else:
            cfg = '# Configuración erronea (Applicaciones opcionales)\n\n'
            Util.Continue(msg=True)


    else: pass


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
            txt_add + txt_fnl + txt
        )

    else:
        txt_add = ''
        #Util.Continue(msg=True)

    Util.CleanScreen()

    return cfg





def Repository(txt=''):
    file_source = 'Script_Preparar-OS_sources.txt'

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



    cfg = (Util.Title(txt='Repositorios', see=False) +
        'sudo mv /etc/apt/sources.list /etc/apt/BackUp_sources.list &&\n'
        f'sudo cp {file_source} /etc/apt/sources.list {txt}')


    return cfg




def TripleBuffer(txt=''):
    cfg = Util.Title(txt='Triple Buffer', see=False)
    os.system('grep drivers /var/log/Xorg.0.log ')
    print('\n')
    opc = input(Util.Title(txt='Activar Triple buffer', see=False) +
                '1. Grafica AMD\n'
                '2. Grafica Intel\n'
                '0. No hacer nada\n'
                'Elige una opcion: ')
    Util.CleanScreen()
    file_txt = 'Script_Preparar-OS_TripleBuffer.txt'
    file_copy = f'sudo cp {file_txt}'
    path = '/etc/X11/xorg.conf.d/'
    if opc == '1':
        with open(file_txt, 'w') as file_txt:
            file_txt.write('Section "Device"\n'
                           '   Identifier  "AMD Graphics"\n'
                           '   Driver      "radeon"\n'
                           '   Option      "TearFree"  "true"\n'
                           'EndSection')
        file_copy = (f'{file_copy} {path}20-radeon.conf &&\n\n'
                     f'sudo rm {path}20-intel-gpu.conf && \n'
                     f'sudo rm {path}20-amdgpu.conf {txt}')
    elif opc == '2':
        with open(file_txt, 'w') as file_txt:
            file_txt.write('Section "Device"\n'
                           '   Identifier  "Intel Graphics"\n'
                           '   Driver      "intel"\n'
                           '   Option      "TearFree"  "true"\n'
                           'EndSection')

        file_copy = (f'{file_copy} {path}20-intel-gpu.conf &&\n\n'
                     f'sudo rm {path}20-radeon.conf && \n'
                     f'sudo rm {path}20-amdgpu.conf {txt}')
    elif opc == '0':
        cfg, file_copy = '', ''
    else:
        Util.Continue(msg=True)
        cfg, file_copy = f'# Configuración erronea {txt}', ''

    cfg = cfg + file_copy


    return cfg




if __name__ =='__main__':
   Script_Menu()