import os, pathlib
import Modulo_Util as Util

def Script_Menu():
    cfg_file = 'Probar_Modulo_CFG.txt'

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
            cfg = (apt(txt='update') + ' &&\n\n' +
                App_essential(txt='&&\n\n') + App_dependence(txt='&&\n\n') +
                App_desktop(txt='&&\n\n') + App_optional(txt='&&\n\n') +
                App_purge(txt='&&\n\n') + Repository(txt='&&\n\n') +
                TripleBuffer(txt='&&\n\n') +
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
    elif opc == 'n': Main()
    else: pass

def apt(txt = ''):
    cmd = 'sudo apt '
    if txt == 'update':
        cmd = cmd + txt + ' && ' + cmd + 'upgrade'

    elif txt == 'clean':
        cmd = cmd + 'autoremove && ' + cmd + txt

    elif txt == 'install':
        cmd = cmd + txt

    elif txt == 'purge':
        cmd = cmd + txt
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
        cfg = '#Configuración erronea'
    Util.CleanScreen()
    return cfg

def App_essential(txt=''):
    app_est = (Util.Title(txt = 'Programas Necesarios', see=False) +
        f"{apt(txt='install')} "
        'bleachbit transmission p7zip-full eog ffmpeg scrcpy adb htop '
        'neofetch mpv gdebi mangohud thunderbird wget openjfx git curl '
        'youtube-dl gnome-sound-recorder libsdl2-mixer-2.0-0 cpu-x ntp '
        'gnome-disk-utility fonts-noto-color-emoji telegram-desktop &&\n\n' +

        Util.Title(txt='Servico ntp (para que se sincronize la hora)') + '\n'
        f'sudo systemctl enable ntp {txt}')
    return app_est

def App_dependence(txt = ''):
    app_dpc = (Util.Title(txt='Algunas Dependencias', see=False) +
        'sudo dpkg --add-architecture i386 &&\n'
        f"{apt(txt='update')} && {apt(txt='install')} "
        'gir1.2-libxfce4ui-2.0 gir1.2-libxfce4util-1.0 libc6:i386 '
        'libasound2:i386 libasound2-data:i386 libasound2-plugins:i386 '
        'libgtk2.0-0:i386 libxml2:i386 libsm6:i386 libqt5widgets5 ' + txt)
    return app_dpc

def App_desktop(txt=''):
    app_xfce4 = (Util.Title(txt = 'Programas Xfce4', see=False) +
        apt(txt='install') + ' '
        'gnome-calculator eog bijiben gvfs-backends gparted menulibre '
        'lightdm-gtk-greeter-settings gnome-software blueman atril '
        'file-roller xfce4-goodies telegram-desktop redshift-gtk ' + txt)

    app_KDEplasma = (Util.Title(txt = 'Programas', see=False) +
        apt(txt='install') + ' '
        f'rofi {txt}')
    opc = input(Util.Title(txt='Programas para Escritorios', see=False) +
        '1. Xfce4\n'
        '2. Kdenlive\n'
        'Elige una opción: ')
    if opc == '1':
        cfg = app_xfce4
    elif opc == '2':
        cfg = app_KDEplasma
    else:
        cfg = '#Configuracion erronea\n\n'
    Util.CleanScreen()
    return cfg

def App_optional(txt=''):
    flatpak = (Util.Title(txt = 'Flatpak', see=False) +
        f'{apt(txt="install")} flatpak &&\n'
        
        'sudo flatpak remote-add --if-not-exists flathub '
        'https://flathub.org/repo/flathub.flatpakrepo &&\n'

        f"{apt(txt='install')} gnome-software-plugin-flatpak ")

    wine = (Util.Title(txt = 'Wine', see=False) +
        'sudo dpkg --add-architecture i386 && clear &&\n'
        'sudo wget -nc -O /usr/share/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key &&\n'
        'clear &&\n'
        'sudo wget -nc -P /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bullseye/winehq-bullseye.sources &&\n'
        f"{apt(txt='update')} && clear &&\n"
        f"{apt(txt='install')} --install-recommends winehq-stable && clear &&\n"
        'wine --version ')

    woeusb_ng = (Util.Title(txt = 'WoeUSB-ng', see=False) +
        f"{apt(txt='install')} "
        'git p7zip-full python3-pip python3-wxgtk4.0 grub2-common grub-pc-bin '
        '&& sudo pip3 install WoeUSB-ng ')

    opc= input(Util.Title(txt='Aplicaciones opcionales', see=False) +
        '0. Sin apps opcionales\n'
        '1. FlatPak\n'
        '2. Wine\n'
        '3. WoeUSB-NG\n'
        '4. FlatPak y Wine\n'
        '5. Todos\n'
        'Elige una opción: ')
    if opc == '1':
        cfg = flatpak + txt
    elif opc == '2':
        cfg = wine + txt
    elif opc == '3':
        cfg = woeusb_ng + txt
    elif opc == '4':
        cfg = flatpak + '&&\n\n' +  wine + txt
    elif opc == '5':
        cfg = flatpak + '&&\n\n' +  wine + '&&\n\n' + woeusb_ng + txt
    elif opc == '0':
        cfg = ''
    else:
        cfg = '#Configuracion erronea\n\n'
    Util.CleanScreen()
    return cfg

def App_purge(txt=''):
    app_prg = (Util.Title(txt='Desinstalar Programas', see=False) +
        apt(txt='purge') + ' '
        'mozc-data mozc-server mlterm-common xiterm+thai '
        'fcitx-data fcitx5-data goldendict uim anthy kasumi '
        f'audacious {txt}')
    return app_prg

def Repository(txt=''):
    cfg = (Util.Title(txt='Repositorios', see=False) +
        'sudo mv /etc/apt/sources.list /etc/apt/BackUp_sources.list &&\n'
        f'sudo cp sources.txt /etc/apt/sources.list {txt}')
    return cfg

def TripleBuffer(txt=''):
    cfg = Util.Title(txt='Triple Buffer', see=False) + '\n'
    os.system('grep drivers /var/log/Xorg.0.log ')
    print('\n')
    opc = input(Util.Title(txt='Activar Triple buffer', see=False) + '\n'
                '1. Grafica AMD\n'
                '2. Grafica Intel\n'
                '0. No hacer nada\n'
                'Elige una opcion: ')
    Util.CleanScreen()
    file_txt = 'TripleBuffer.txt'
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
        cfg, file_copy = f'#Configuración erronea {txt}', ''
    cfg = cfg + file_copy
    return cfg


if __name__ =='__main__':
   Script_Menu()