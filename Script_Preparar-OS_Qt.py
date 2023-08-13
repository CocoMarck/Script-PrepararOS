from Modulos.Modulo_System import(
    Command_Run
)

#from Modulos.Modulo_Text import(
#    Text_Read
#)

from Modulos.Modulo_Files import(
    Files_List
)
from Modulos import Modulo_Util_Debian as Util_Debian
from Modulos.Modulo_Language import get_text as Lang
from Interface import Modulo_Util_Qt as Util_Qt
from pathlib import Path
import subprocess


import sys
from functools import partial
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QScrollArea,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt


cfg_file = f'Script_CFG.txt'
cfg_dir = 'Script_Apps/'


def Config_Save(parent=None, cfg=None):
    if cfg == None:
        pass
    else:
        Util_Qt.Dialog_Command_Run(
            parent=parent,
            cmd=cfg,
            cfg_file=cfg_file
        ).exec()


class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Preparing OS')
        self.resize(308, 308)
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones verticales - Opciones
        vbox_main.addStretch()
        
        button_auto = QPushButton( Lang('auto') )
        #button_auto.clicked.connect(self.evt_automatic)
        vbox_main.addWidget(button_auto)
        
        button_apps = QPushButton( Lang('app_menu') )
        button_apps.clicked.connect(self.evt_application)
        vbox_main.addWidget(button_apps)
        
        button_apt = QPushButton( 'Aptitude' )
        button_apt.clicked.connect(self.evt_aptitude)
        vbox_main.addWidget(button_apt)
        
        button_repo = QPushButton( Lang('repos_nonfree') )
        button_repo.clicked.connect(self.evt_repository)
        vbox_main.addWidget(button_repo)
        
        button_3_buffer = QPushButton( Lang('on_3_buffer') )
        button_3_buffer.clicked.connect(self.evt_triple_buffer)
        vbox_main.addWidget(button_3_buffer)
        
        button_mouse_cfg = QPushButton(
            f'{Lang("cfg")} - Mouse'
        )
        button_mouse_cfg.clicked.connect(self.evt_mouse_cfg)
        vbox_main.addWidget(button_mouse_cfg)
        
        # Seccion Vertical - Ejecutar comando
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        button_exec_cmd = QPushButton(
            f'{Lang("exec")} {Lang("cmd")}'
        )
        button_exec_cmd.clicked.connect(self.evt_exec_command)
        hbox.addWidget( button_exec_cmd )
        
        hbox.addStretch()

        self.entry_exec_cmd = QLineEdit(
            placeholderText=Lang('cmd')
        )
        self.entry_exec_cmd.returnPressed.connect(self.evt_exec_command)
        hbox.addWidget( self.entry_exec_cmd )
        
        # Seccion Vertical - Ver comandos
        vbox_main.addStretch()
        
        button_view_cfg = QPushButton(
            Lang('view_cfg')
        )
        button_view_cfg.clicked.connect(self.evt_view_cfg)
        vbox_main.addWidget(button_view_cfg)
        
        # Seccion Vertical final, salir
        #vbox_main.addStretch()
        
        #button_exit = QPushButton( Lang('exit') )
        #button_exit.clicked.connect(self.evt_exit)
        #vbox_main.addWidget(button_exit)
        
        # Fin, mostrar ventana
        self.show()
    
    def evt_mouse_cfg(self):
        self.hide()
        Dialog_mouse_config(
            parent=self
        ).exec()
        self.show()
    
    def evt_triple_buffer(self):
        self.hide()
        Dialog_TripleBuffer(
            parent=self
        ).exec()
        self.show()
    
    def evt_application(self):
        self.hide()
        Dialog_apps_menu(
            parent=self,
        ).exec()
        self.show()
    
    def evt_aptitude(self):
        self.hide()
        Dialog_Aptitude(
            parent=self
        ).exec()
        self.show()
    
    def evt_repository(self):
        Config_Save(
            parent=self,
            cfg=Util_Debian.Repository()
        )
    
    def evt_exec_command(self):
        command = self.entry_exec_cmd.text()
        if command == '':
            pass
        else:
            Command_Run(
                cmd=command,
                open_new_terminal=True,
                text_input=Lang('continue_enter')
            )
    
    def evt_view_cfg(self):
        self.hide()
        Util_Qt.Dialog_TextEdit(
            self,
            text=cfg_file,
            edit=False
        ).exec()
        self.show()
    
    #def evt_exit(self):
    #    self.close()


class Dialog_Aptitude(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Aptitude')
        self.resize(308, 256)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones Verticales - Botones - Actualizar y limpiar
        button_update = QPushButton(Lang('upd'))
        button_update.clicked.connect(self.evt_apt_update)
        vbox_main.addWidget(button_update)
        
        button_clean = QPushButton(Lang('cln'))
        button_clean.clicked.connect(self.evt_apt_clean)
        vbox_main.addWidget(button_clean)
        
        # Seccion Vertical - Espaciador
        vbox_main.addStretch()
        
        # Seccion Vertical - Boton Instalar
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        button_install = QPushButton(Lang('install'))
        button_install.clicked.connect(self.evt_apt_app_install)
        hbox.addWidget(button_install)
        
        self.entry_install = QLineEdit(
            placeholderText=Lang('app'),
        )
        #self.entry_install.returnPressed.connect(self.evt_apt_app_install)
        hbox.addWidget(self.entry_install)
        
        # Seccion Vertical - Boton Purgar
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        button_purge = QPushButton(Lang('prg'))
        button_purge.clicked.connect(self.evt_apt_app_purge)
        hbox.addWidget(button_purge)
        
        self.entry_purge = QLineEdit(
            placeholderText=Lang('app'),
        )
        #self.entry_purge.returnPressed.connect(self.evt_apt_app_purge)
        hbox.addWidget(self.entry_purge)

    def evt_apt_update(self):
        Config_Save(
            self,
            cfg=Util_Debian.Aptitude('update')
        )
    
    def evt_apt_clean(self):
        Config_Save(
            self,
            cfg=Util_Debian.Aptitude('clean')
        )
    
    def evt_apt_app_install(self):
        if self.entry_install.text() == '':
            pass
        else:
            Config_Save(
                parent=self,
                cfg = (
                    'sudo apt update &&\n\n' +
                    Util_Debian.Aptitude('install') +
                    self.entry_install.text()
                )
            )
    
    def evt_apt_app_purge(self):
        if self.entry_purge.text() == '':
            pass
        else:
            Config_Save(
                parent=self,
                cfg = (
                    Util_Debian.Aptitude('purge') +
                    self.entry_purge.text() + ' &&\n\n'
                    'sudo apt autoremove ' +
                    self.entry_purge.text() + ' &&\n\n' +
                    Util_Debian.Aptitude('clean')
                )
            )
        

class Dialog_apps_menu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(Lang('app_menu'))
        self.resize(308, 256)
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones verticales - Opciones
        button_app_essential = QPushButton(Lang('essential'))
        button_app_essential.clicked.connect(self.evt_app_essential)
        vbox_main.addWidget(button_app_essential)
        
        button_app_dependence = QPushButton(Lang('depens'))
        button_app_dependence.clicked.connect(self.evt_app_dependence)
        vbox_main.addWidget(button_app_dependence)
        
        button_app_uninstall = QPushButton(Lang('utll'))
        button_app_uninstall.clicked.connect(self.evt_app_uninstall)
        vbox_main.addWidget(button_app_uninstall)
        
        button_app_desktop = QPushButton(Lang('desk'))
        button_app_desktop.clicked.connect(self.evt_app_desktop)
        vbox_main.addWidget(button_app_desktop)
        
        button_app_optional = QPushButton(Lang('optional'))
        button_app_optional.clicked.connect(self.evt_app_optional)
        vbox_main.addWidget(button_app_optional)
    
    def evt_app_essential(self):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(opc='Essential')
        )

    def evt_app_dependence(self):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(opc='Dependence')
        )

    def evt_app_uninstall(self):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(opc='Uninstall')
        )
        
    def evt_app_desktop(self):
        Dialog_app_desktop(parent=self).exec()

    def evt_app_optional(self):
        Dialog_app_optional(parent=self).exec()


class Dialog_app_desktop(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(Lang('app_desk'))
        self.resize(308, 128)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones verticales - Opciones
        list_app_desktop = [
            'Desktop-xfce4',
            'Desktop-kdeplasma',
            'Desktop-gnome3',
            'Desktop-lxde',
            'Desktop-mate'
        ]
        
        for app_desktop in list_app_desktop:
            button_app_desktop = QPushButton(app_desktop)
            button_app_desktop.clicked.connect(
                partial(self.evt_app_desktop, button=button_app_desktop)
            )
            vbox_main.addWidget(button_app_desktop)
        
    def evt_app_desktop(self, button):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(button.text())
        )


class Dialog_app_optional(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle( Lang('app_optional') )
        self.resize(308, 360)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccioner Verticales - Botones
        # Scroll
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        vbox_main.addWidget(scroll_area)
        
        # Scroll - Contenedor de Widgets
        widget_buttons = QWidget()
        
        # Scroll - Layout
        vbox = QVBoxLayout()
        widget_buttons.setLayout(vbox)
        
        # Scroll - Layout - Botones en orden vertical
        self.path_app_optional = f'{cfg_dir}App_Optional/'
        if (
            Path(
                f'{self.path_app_optional}'
                'App_Optional-wine.txt'
            ).exists() or
            Path(
                f'{self.path_app_optional}'
                'App_Optional-flatpak.txt'
            ).exists() or
            Path(
                f'{self.path_app_optional}'
                'App_Optional-woeusb-ng.txt'
            ).exists()
        ):
            pass
        else:
            Util_Debian.App('Optional-wine')
            Util_Debian.App('Optional-flatpak')
            Util_Debian.App('Optional-woeusb-ng')
        
        try:
            archives_app_optional = Files_List(
                files='App_Optional-*.txt',
                path=self.path_app_optional,
                remove_path=True
            )
            
            self.list_app_optional = []
            for text_app_optional in archives_app_optional:
                button_app_optional = QPushButton(text_app_optional)
                button_app_optional.clicked.connect(
                    partial(self.evt_app_optional, button=button_app_optional)
                )
                vbox.addWidget(button_app_optional)
                
                self.list_app_optional.append(text_app_optional)
        except:
            pass
        
        # Scroll - Agregar widgets
        scroll_area.setWidget(widget_buttons)
        
        # Seccion Vertical - Boton para todas las apps
        vbox_main.addStretch()
        
        button_all_app_optional = QPushButton(Lang('all_apps'))
        button_all_app_optional.clicked.connect(
            self.evt_all_app_optional
        )
        vbox_main.addWidget(button_all_app_optional)
    
    def evt_app_optional(self, button):
        if button.text() in self.list_app_optional:
            Config_Save(
                parent = self,
                cfg = Util_Debian.App(
                    txt_title = f'{Lang("app")} / {button.text()}',
                    txt_add = '',
                    cfg_dir = './',
                    cfg_file = (
                        self.path_app_optional +
                        button.text()
                    ),
                    opc = 'continue'
                )
            )
        else:
            pass
    
    def evt_all_app_optional(self):
        app = ''
        app_all = ''
        line_jump = '&&\n\n'
        
        for text_app_optional in self.list_app_optional:
            app = Util_Debian.App(
                txt = line_jump,
                txt_title = f'{Lang("app")} / {text_app_optional}',
                txt_add = '',
                cfg_dir = './',
                cfg_file = (
                    self.path_app_optional +
                    text_app_optional
                ),
                opc = 'continue'
            )
            app_all += app
        
        # Este es el caracter 4 de line_jump...
        if '&' == app_all[-4]:
            app_all = app_all[:-4]
        else:
            pass
        
        Config_Save(
            parent=self,
            cfg=app_all
        )
    
class Dialog_TripleBuffer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle( 'Triple Buffer Config' )
        self.resize(308, 256)
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones Vertical - Comando para ver Triple Buffer
        command = 'grep drivers /var/log/Xorg.0.log'
        command_run = subprocess.check_output(
            command, shell=True, text=True
        )
        label_command = QLabel(
            f'<i>{Lang("cmd")}: "{command}</i>\n'
            '\n'
            f'<b>{command_run}</b>'
        )
        label_command.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        label_command.setWordWrap(True)
        vbox_main.addWidget(label_command)
        
        # Secciones Verticales - Botones
        list_graphics = [
            Lang('gpc_amd'),
            Lang('gpc_intel')
        ]
        for graphic in list_graphics:
            button_graphic = QPushButton(graphic)
            button_graphic.clicked.connect(
                partial(
                    self.evt_TripleBuffer_graphic, button=button_graphic
                )
            )
            vbox_main.addWidget(button_graphic)
    
    def evt_TripleBuffer_graphic(self, button):
        dict_graphics = {
            Lang('gpc_amd'): '20-radeon.conf',
            Lang('gpc_intel'): '20-intel-gpu.conf'
        }
        
        if button.text() in dict_graphics:
            graphic = dict_graphics[button.text()]

            Config_Save(
                parent=self,
                cfg=Util_Debian.TripleBuffer(graphic)
            )
        else:
            pass
            #graphic = button.text()


class Dialog_mouse_config(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Mouse Config')
        self.resize(256, 128)
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical - Aceleración - Activar/Desactivar
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        button_acceleration = QPushButton()
        button_acceleration.setCheckable(True)
        button_acceleration.clicked.connect(
            partial(
                self.evt_mouse_acceleration_onoff,
                button=button_acceleration
            )
        )
        hbox.addWidget(button_acceleration)
        
        if Path(
            '/usr/share/X11/xorg.conf.d/'
            '50-mouse-acceleration.conf'
        ).exists():
            button_acceleration.setChecked(False)
            button_acceleration.setText(Lang("acclr_off"))
        else:
            button_acceleration.setChecked(True)
            button_acceleration.setText(Lang("acclr_on"))
    
    def evt_mouse_acceleration_onoff(self, button):
        if button.isChecked() == True:
            option = 'AccelerationON'
            button.setText( Lang('acclr_on') )
        else:
            option = 'AccelerationOFF'
            button.setText( Lang('acclr_off') )

        Config_Save( 
            parent=self,
            cfg=Util_Debian.Mouse_Config(option)
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Main()
    sys.exit(app.exec())