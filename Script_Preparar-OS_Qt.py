from Modulos.Modulo_System import(
    Command_Run
)

from Modulos.Modulo_Text import(
    Text_Read
)

from Modulos.Modulo_Files import(
    Files_List
)
from Modulos import Modulo_Util_Debian as Util_Debian
from Modulos.Modulo_Language import get_text as Lang
from Interface import Modulo_Util_Qt as Util_Qt
import pathlib, subprocess


import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
)


cfg_file = f'Script_CFG.txt'
cfg_dir = 'Script_Apps/'


class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Preparing OS')
        self.resize(308, 308)
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones verticales - Opciones
        button_auto = QPushButton( Lang('auto') )
        #button_auto.clicked.connect(self.evt_automatic)
        vbox_main.addWidget(button_auto)
        
        button_apps = QPushButton( Lang('app_menu') )
        #button_apps.clicked.connect(self.evt_application)
        vbox_main.addWidget(button_apps)
        
        button_apt = QPushButton( 'Aptitude' )
        #button_apt.clicked.connect(self.evt_aptitude)
        vbox_main.addWidget(button_apt)
        
        button_repo = QPushButton( Lang('repos_nonfree') )
        #button_repo.clicked.connec(self.evt_repository)
        vbox_main.addWidget(button_repo)
        
        button_3_buffer = QPushButton( Lang('on_3_buffer') )
        #button_3_buffer.clicked.connect(self.evt_triple_buffer)
        vbox_main.addWidget(button_3_buffer)
        
        button_mouse_cfg = QPushButton(
            f'{Lang("cfg")} - {Lang("cmd")}'
        )
        #button_mouse_cfg.clicked.connect(self.evt_mouse_cfg)
        vbox_main.addWidget(button_mouse_cfg)
        
        # Seccion Vertical - Ejecutar comando
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        button_exec_cmd = QPushButton(
            f'{Lang("exec")} {Lang("cmd")}'
        )
        #button_exec_cmd.clicked.connect(self.evt_exec_command)
        hbox.addWidget( button_exec_cmd )
        
        hbox.addStretch()

        entry_exec_cmd = QLineEdit(
            placeholderText=Lang('cmd')
        )
        hbox.addWidget( entry_exec_cmd )
        
        # Seccion Vertical - Ver comandos
        button_view_cfg = QPushButton(
            Lang('view_cfg')
        )
        #button_view_cfg.clicked.connect(self.evt_view_cfg)
        vbox_main.addWidget(button_view_cfg)
        
        # Seccion Vertical final, salir
        vbox_main.addStretch()
        
        button_exit = QPushButton( Lang('exit') )
        #button_exit.clicked.connect(self.evt_exit)
        vbox_main.addWidget(button_exit)
        
        # Fin, mostrar ventana
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Main()
    sys.exit(app.exec())