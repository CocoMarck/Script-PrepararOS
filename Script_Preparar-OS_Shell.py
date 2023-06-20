from Modulos import Modulo_Util as Util
from Modulos import Modulo_Util_Debian as Util_Debian
import os, pathlib, subprocess


fnl = 'txt'
err = '# Configuración erronea'

def Script_Menu():
    cfg_file = f'Script_CFG.{fnl}'
    
    loop = True
    while loop == True:
        Util.CleanScreen()
        opc = input(
            Util.Title(txt='Preparar Sistema', see=False) +
            '1. Automatico\n'
            '2. Aplicaciones\n'
            '3. Aptitude\n'
            '4. Repositorios no libres\n'
            '5. Activar Triple buffer\n'
            '6. Configuración de Mouse\n'
            '7. Ejecutar Comando\n'
            '9. Ver comandos creados\n'
            '0. Salir\n'
            'Elige una opción: '
        )
        
        if (
            opc == '1' or
            opc == '2' or
            opc == '3' or
            opc == '4' or
            opc == '5' or
            opc == '6' or
            opc == '7' or
            opc == '9' or
            opc == '0'
        ):
            go = Util.Continue()
            if go == 's':
                pass
            elif go == 'n':
                opc = None
                
        cfg = ''
        cfg_save = True
        if opc == '1':
            cfg = (
                Util_Debian.Aptitude('update') + ' &&\n\n' +
                Util_Debian.App('Essential', '&&\n\n') +
                Util_Debian.App('Dependence','&&\n\n') +
                App_Menu('Desktop','&&\n\n') +
                App_Menu('Optional','&&\n\n') +
                Util_Debian.App('Uninstall', '&&\n\n') +
                Util_Debian.Aptitude('clean')
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
            
            go = Util.Continue()
            if go == 's':
                pass
            elif go == 'n':
                opc = None
            
            if opc == '1':
                cfg = Util_Debian.App(opc='Essential')
                
            elif opc == '2':
                cfg = Util_Debian.App(opc='Dependence')

            elif opc == '3':
                cfg = Util_Debian.App(opc='Uninstall')
                
            elif opc == '4':
                cfg = App_Menu('Desktop')
                
            elif opc == '5':
                cfg = App_Menu('Optional')
            
            else:
                Util.Continue(msg=True)
                cfg_save = False
        
        elif opc == '3':
            opc = input(Util.Title(txt='Opciones aptitude', see=False) +
                '1. Actualizar\n'
                '2. Limpiar\n'
                'Elige una opción: ') 
            
            if opc == '1':
                cfg = Util_Debian.Aptitude('update')
            
            elif opc == '2':
                cfg = Util_Debian.Aptitude('clean')
            
            else:
                Util.Continue(msg=True)
                cfg_save = False
            
        elif opc == '4':
            cfg = Util_Debian.Repository()
            
        elif opc == '5':
            cfg = Triple_Buffer()
            
        elif opc == '6':
            cfg = Mouse_Config()
            
        elif opc == '7':
            cfg_save = False
            cmd = input('Comando: ')
            if cmd == '':
                pass
            else:
                Util.Command_Run( cmd=cmd )
            
        elif opc == '9':
            cfg_save = False
            input(
                Util.Text_Read(cfg_file) + '\n\n'
                'Preciona enter para continuar...'
            )
            
        elif opc == '0':
            cfg_save, loop = False, False
            print('Hasta la proxima.')
            
        elif opc == None:
            cfg_save = False
            cfg = ''
            
        else:
            cfg_save = False
            cfg = err + '\n\n'
            Util.Continue(msg=True)
            
        if cfg_save == True:

            Util.CleanScreen()
            if cfg == '': 
                pass

            else:
                opc = Util.Continue(
                    'Esta es tu configuración: \n\n' + cfg + '\n' +
                    Util.Separator(see=False) + '\n'
                    '¿Continuar?'
                )
                
                if opc == 's':
                    Util.Command_Run(cfg)
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(
                            cfg + '\n' + Util.Separator(see=False) + '\n'
                        )
                    input('Precione enter para continuar...')

                elif opc == 'n':
                    pass
                    
        else:
            pass
                    

def App_Menu(opc='Desktop', txt=''):
    Util.CleanScreen()
    if opc == 'Desktop':
        opc = input(
            Util.Title(f'Aplicaciones de Escritorio', see=False) +
            '1. Xfce4\n'
            '2. KDE Plasma\n'
            '3. Gnome 3\n'
            '4. LXDE\n'
            '5. Mate\n'
            'Elige una opción: '
        )
        
        if opc == '1':
            cfg = Util_Debian.App('Desktop-xfce4', txt=txt)
        
        elif opc == '2':
            cfg = Util_Debian.App('Desktop-kdeplasma', txt=txt)
        
        elif opc == '3':
            cfg = Util_Debian.App('Desktop-gnome3', txt=txt)
        
        elif opc == '4':
            cfg = Util_Debian.App('Desktop-lxde', txt=txt)
            
        elif opc == '5':
            cfg = Util_Debian.App('Desktop-mate', txt=txt)
            
        else:
            cfg = ''

    elif opc == 'Optional':
        if (
            pathlib.Path('./Script_Apps/App_Optional/'
                        'App_Optional-wine.txt').exists() or
        
            pathlib.Path('./Script_Apps/App_Optional/'
                        'App_Optional-flatpak.txt').exists() or
        
            pathlib.Path('./Script_Apps/App_Optional/'
                        'App_Optional-woeusb-ng.txt').exists()
        ): 
            pass
            
        else:
            Util_Debian.App('Optional-wine')
            Util_Debian.App('Optional-flatpak')
            Util_Debian.App('Optional-woeusb-ng')
            
        try:
            path_app_optional = 'Script_Apps/App_Optional/'
            archives = Util.Files_List(
                files='App_Optional-*.txt',
                path=path_app_optional,
                remove_path=True
            )
            
            dict_archive = {}
            menu_archive = ''
            number = 0
            
            for archive in archives:
                number += 1
                menu_archive += f'{number}. {archive}\n'
                dict_archive.update({number : archive})
                
            opc = int(input(
                Util.Title(f'Aplicaciones Opcionales', see=False) +
                menu_archive +
                f'{number+1}. Todas las aplicaciones\n'
                'Elige una opción: '
            ))
            
            if opc in dict_archive:
                cfg = Util_Debian.App(
                    txt=txt,
                    txt_title = 'Applications / Optional',
                    txt_add = '',
                    cfg_dir = './',
                    cfg_file = (
                        path_app_optional +
                        str(dict_archive[opc])
                    ),
                    opc = 'continue'
                )
                
            elif opc == number + 1:
                cfg = ''
                while number > 0:
                    cfg += Util_Debian.App(
                        txt='&&\n\n',
                        txt_title='Application / Optional',
                        txt_add='',
                        cfg_dir='./',
                        cfg_file=(
                            path_app_optional +
                            str(dict_archive[number])
                        ),
                        opc='continue'
                    )
                    number -= 1 
                cfg += 'echo Fin de Apps Opcionales ' + txt
                
            else:
                cfg = ''
                
        except:
            Util.Continue(msg=True)
            cfg = ''

    else:
        cfg = ''
    
    return cfg


def Triple_Buffer(txt=''):
    cmd = 'grep drivers /var/log/Xorg.0.log'
    cmd_run = str(
        subprocess.check_output(
            cmd, shell=True
        )
    )
    
    print(
        f'Comando para ver driver de grafica: "{cmd}"\n'
        '\n' +
        cmd_run + '\n'
    )

    opc = input(
        Util.Title('Activar TripleBuffer', see=False) +
        '1. Grafica AMD\n'
        '2. Grafica Intel\n'
        '0. No hacer nada\n'
        'Elige una opcion: '
    )
    
    if opc == '1':
        opc = '20-radeon.conf'

    elif opc == '2':
        opc = '20-intel-gpu.conf'

    else:
        pass
        
    if (
        opc == '20-radeon.conf' or
        opc == '20-amdgpu.conf' or
        opc == '20-intel-gpu.conf'
    ):
        cfg = Util_Debian.TripleBuffer(opc) + f' {txt}'
        
    elif opc == '0':
        cfg = ''
        
    else:
        Util.Continue(msg=True)
        cfg = ''
        
    return cfg
    

def Mouse_Config():
    Util.Title('Configuración de Mouse')

    if pathlib.Path(
        '/usr/share/X11/xorg.conf.d/'
        '50-mouse-acceleration.conf'
    ).exists():
        option = Util.Continue('AccelerationOFF ¿Activar?')
        if option == 's':
            option = Util_Debian.Mouse_Config('AccelerationON')
        elif option == 'n':
            option = ''
    else:
        option = Util.Continue('AccelerationON ¿Desactivar?')
        if option == 's':
            option = Util_Debian.Mouse_Config('AccelerationOFF')
        elif option == 'n':
            option = ''

    return option


if __name__ == '__main__':
    Script_Menu()