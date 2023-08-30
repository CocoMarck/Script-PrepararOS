from Modulos.Modulo_System import(
    Command_Run
)

from Modulos.Modulo_Files import(
    Files_List
)

from Modulos import Modulo_Util_Debian as Util_Debian
from Modulos.Modulo_Language import get_text as Lang

from Interface import Modulo_Util_Gtk as Util_Gtk

import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


cfg_file = 'Script_CFG.txt'
cfg_dir = 'Script_Apps/'


class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Preparing OS')
        self.set_resizable(True)
        self.set_default_size(308, 308)
        
        # Contenedor principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        
        # Seccion verticales - Opciones
        button_auto = Gtk.Button( label=Lang('auto') )
        #button_auto.connect('clicked', self.evt_automatic)
        vbox_main.pack_start(button_auto, True, False, 0)
        
        button_apps = Gtk.Button( label=Lang('app_menu') )
        #button_apps.connect('clicked', self.evt_application)
        vbox_main.pack_start(button_apps, True, False, 0)
        
        button_apt = Gtk.Button( label='Aptitude' )
        #button_apt.connect('clicked', self.evt_aptitude)
        vbox_main.pack_start(button_apt, True, False, 0)
        
        button_repo = Gtk.Button( label=Lang('repos_nonfree') )
        #button_repo.connect('clicked', self.evt_repository)
        vbox_main.pack_start(button_repo, True, False, 0)
        
        button_3_buffer = Gtk.Button( label=Lang('on_3_buffer') )
        #button_3_buffer.connect('clicked', self.evt_triple_buffer)
        vbox_main.pack_start(button_3_buffer, True, False, 0)
        
        button_mouse_cfg = Gtk.Button( label=f'{Lang("cfg")} - Mouse' )
        #button_mouse_cfg.connect('clicked', self.evt_mouse_cfg)
        vbox_main.pack_start(button_mouse_cfg, True, False, 0)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, True, False, 16)
        
        button_exec_cmd = Gtk.Button( 
            label=f"{Lang('exec')} {Lang('cmd')}" 
        )
        button_exec_cmd.connect('clicked', self.evt_exec_command)
        hbox.pack_start(button_exec_cmd, False, True, 0)
        
        self.entry_exec_cmd = Gtk.Entry()
        self.entry_exec_cmd.connect('activate', self.evt_exec_command)
        self.entry_exec_cmd.set_placeholder_text(Lang('cmd'))
        hbox.pack_end(self.entry_exec_cmd, False, True, 0)
        
        # Secciones vertical final - ver comandos
        button_view_cfg = Gtk.Button(label=Lang('view_cfg') )
        button_view_cfg.connect('clicked', self.evt_view_cfg)
        vbox_main.pack_end(button_view_cfg, False, True, 0)
        
        # Fin, mostrar todo
        self.add(vbox_main)
    
    def evt_exec_command(self, widget):
        command = self.entry_exec_cmd.get_text()
        if not command == '':
            # Solo se activa si hay texto, entonces si es un comando.
            Command_Run(
                cmd=command,
                open_new_terminal=True,
                text_input=Lang('continue_enter')
            )
    
    def evt_view_cfg(self, widget):
        dialog = Util_Gtk.Dialog_TextView(
            self,
            text=cfg_file,
            edit=False
        )
        self.hide()
        dialog.run()
        dialog.destroy()

        self.show_all()


win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()