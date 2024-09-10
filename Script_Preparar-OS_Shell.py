from interface.Modulo_ShowPrint import(
    Title,
    Separator,
    Continue
)

from logic.Modulo_System import(
    CleanScreen,
    Command_Run
)

from logic.Modulo_Text import(
    Text_Read
)

from logic.Modulo_Files import(
    Files_List
)
from data import Modulo_Util_Debian as Util_Debian
from data.Modulo_Language import get_text as Lang
import os, pathlib, subprocess


fnl = 'txt'
err = '# Configuración erronea'

def Script_Menu():
    cfg_file = Util_Debian.file_script_cfg
    
    loop = True
    while loop == True:
        CleanScreen()
        opc = input(
            Title(text=Lang('prepar_sys'), print_mode=False) +
            f'1. {Lang("auto")}\n'
            f'2. {Lang("app_menu")}\n'
            '3. Aptitude\n'
            f'4. {Lang("repos_nonfree")}\n'
            f'5. {Lang("on_3_buffer")}\n'
            f'6. {Lang("cfg_mouse")}\n'
            f'7. {Lang("exec_cmd")}\n'
            f'9. {Lang("view_cfg")}\n'
            f'0. {Lang("exit")}\n'
            f'{Lang("set_option")}: '
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
            go = Continue()
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
                Title(Lang("app_menu"), print_mode=False) +
                f'1. {Lang("essential")}\n'
                f'2. {Lang("depens")}\n'
                f'3. {Lang("utll")}\n'
                f'4. {Lang("desk")}\n'
                f'5. {Lang("optional")}\n'
                f'{Lang("set_option")}: '
            )
            
            go = Continue()
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
                Continue(message_error=True)
                cfg_save = False
        
        elif opc == '3':
            opc = input(Title(
                    text='Aptitude',
                    print_mode=False
                ) +
                f'1. {Lang("upd")}\n'
                f'2. {Lang("cln")}\n'
                f'{Lang("set_option")}: ') 
            
            if opc == '1':
                cfg = Util_Debian.Aptitude('update')
            
            elif opc == '2':
                cfg = Util_Debian.Aptitude('clean')
            
            else:
                Continue(message_error=True)
                cfg_save = False
            
        elif opc == '4':
            cfg = Util_Debian.Repository()
            
        elif opc == '5':
            cfg = Triple_Buffer()
            
        elif opc == '6':
            cfg = Mouse_Config()
            
        elif opc == '7':
            cfg_save = False
            cmd = input(f'{Lang("cmd")}: ')
            if cmd == '':
                pass
            else:
                Command_Run( 
                    cmd=cmd,
                    open_new_terminal=False,
                    text_input=Lang('continue_enter')
                )
            
        elif opc == '9':
            cfg_save = False
            text_read = Text_Read(cfg_file)
            if text_read == None:
                text_read = 'ERROR'
            else:
                pass
            input(
                text_read + '\n\n'
                f'{Lang("continue_enter")}...'
            )
            
        elif opc == '0':
            cfg_save, loop = False, False
            print(f'{Lang("bye")}...')
            
        elif opc == None:
            cfg_save = False
            cfg = ''
            
        else:
            cfg_save = False
            cfg = err + '\n\n'
            Continue(message_error=True)
            
        if cfg_save == True:

            CleanScreen()
            if cfg == '': 
                pass

            else:
                opc = Continue(
                    f'{Lang("cfg")}: \n\n' + cfg + '\n' +
                    Separator(print_mode=False) + '\n'
                    f'¿{Lang("continue")}?'
                )
                
                if opc == 's':
                    Command_Run(
                        cfg, open_new_terminal=False,
                        text_input=Lang('continue_enter')
                    )
                    with open(cfg_file, 'a') as file_cfg:
                        file_cfg.write(
                            cfg + '\n' + Separator(print_mode=False) + '\n'
                        )
                    #input(f'{Lang("continue_enter")}...')

                elif opc == 'n':
                    pass
                    
        else:
            pass
                    

def App_Menu(opc='Desktop', txt=''):
    CleanScreen()
    if opc == 'Desktop':
        opc = input(
            Title(Lang('app_desk'), print_mode=False) +
            '1. Xfce4\n'
            '2. KDE Plasma\n'
            '3. Gnome 3\n'
            '4. LXDE\n'
            '5. Mate\n'
            f'{Lang("set_option")}: '
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
        try:
            path_app_optional = Util_Debian.dir_app_optional
            
            # Poner archivos en un diccionario
            archives = Util_Debian.get_app_optional(remove_path=True)
            
            dict_archive = {}
            menu_archive = ''
            number = 0
            
            for archive in archives:
                number += 1
                menu_archive += f'{number}. {archive}\n'
                dict_archive.update({number : archive})
            
            # Menu de selección de App-Optional    
            opc = int(input(
                Title(Lang('app_optional'), print_mode=False) +
                menu_archive +
                f'{number+1}. {Lang("all_apps")}\n'
                f'{Lang("set_option")}: '
            ))
            
            if opc in dict_archive:
                # Selección indivudual
                cfg = Util_Debian.App(
                    txt=txt,
                    txt_title = 'Applications / Optional',
                    txt_add = '',
                    cfg_dir = path_app_optional,
                    cfg_file = str(dict_archive[opc]),
                    opc = 'continue'
                )
                
            elif opc == number + 1:
                # Seleccionar todo
                cfg = ''
                while number > 0:
                    cfg += Util_Debian.App(
                        txt='&&\n\n',
                        txt_title='Application / Optional',
                        txt_add='',
                        cfg_dir=path_app_optional,
                        cfg_file= str(dict_archive[number]),
                        opc='continue'
                    )
                    number -= 1 
                cfg += 'echo Fin de Apps Opcionales ' + txt
                
            else:
                cfg = ''
                
        except:
            Continue(message_error=True)
            cfg = ''

    else:
        cfg = ''
    
    return cfg


def Triple_Buffer(txt=''):
    cmd = Util_Debian.cmd_triple_buffer
    cmd_run = Util_Debian.cmd_run_triple_buffer
    
    print(
        f'{Lang("cmd")}: "{cmd}"\n'
        '\n' +
        cmd_run + '\n'
    )

    opc = input(
        Title(Lang('on_3_buffer'), print_mode=False) +
        f'1. {Lang("gpc_amd")}\n'
        f'2. {Lang("gpc_intel")}\n'
        f'0. {Lang("do_none")}\n'
        f'{Lang("set_option")}: '
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
        Continue(message_error=True)
        cfg = ''
        
    return cfg
    

def Mouse_Config():
    Title( Lang('cfg_mouse') )

    if Util_Debian.exists_mouse_config():
        option = Continue(f'{Lang("acclr_off")} ¿{Lang("on")}?')
        if option == 's':
            option = Util_Debian.Mouse_Config('AccelerationON')
        elif option == 'n':
            option = ''
    else:
        option = Continue(f'{Lang("acclr_on")} ¿{Lang("off")}?')
        if option == 's':
            option = Util_Debian.Mouse_Config('AccelerationOFF')
        elif option == 'n':
            option = ''

    return option


if __name__ == '__main__':
    Script_Menu()