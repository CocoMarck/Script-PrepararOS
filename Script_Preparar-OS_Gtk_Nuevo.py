from Modulos.Modulo_System import(
    Command_Run
)

from Modulos.Modulo_Files import(
    Files_List
)

from Modulos import Modulo_Util_Debian as Util_Debian
from Modulos.Modulo_Language import get_text as Lang

from Interface import Modulo_Util_Gtk as Util_Gtk

from pathlib import Path
import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


cfg_file = 'Script_CFG.txt'
cfg_dir = 'Script_Apps/'


def Config_Save(parent=None, cfg=None):
    if not cfg == None:
        dialog = Util_Gtk.Dialog_Command_Run(
            parent=parent,
            cfg=cfg,
            cfg_file=cfg_file
        )
        dialog.run()
        dialog.destroy()

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
        button_repo.connect('clicked', self.evt_repository)
        vbox_main.pack_start(button_repo, True, False, 0)
        
        button_3_buffer = Gtk.Button( label=Lang('on_3_buffer') )
        #button_3_buffer.connect('clicked', self.evt_triple_buffer)
        vbox_main.pack_start(button_3_buffer, True, False, 0)
        
        button_mouse_cfg = Gtk.Button( label=f'{Lang("cfg")} - Mouse' )
        button_mouse_cfg.connect('clicked', self.evt_mouse_cfg)
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
    
    def evt_repository(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.Repository()
        )
    
    def evt_mouse_cfg(self, widget):
        dialog = Dialog_mouse_cfg(self)
        self.hide()
        dialog.run()
        dialog.destroy()
        self.show_all()

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


class Dialog_mouse_cfg(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Mouse Config',
            transient_for=parent,
            flags=0
        )

        self.set_resizable(True)
        self.set_default_size(256, 128)
        
        # Contenedor principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Seccion Vertical - Switch para activar o desactivar aceleracion
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vbox_main.pack_start(hbox, True, False, 0)
        
        mouse_acceleration = self.get_mouse_acceleration()

        self.label_acceleration = Gtk.Label()
        if mouse_acceleration == True:
            self.label_acceleration.set_text( Lang('acclr_on') )
        else:
            self.label_acceleration.set_text( Lang('acclr_off') )
        hbox.pack_start(self.label_acceleration, False, True, 0)
        
        switch_acceleration = Gtk.Switch(
            state=mouse_acceleration
        )
        switch_acceleration.connect(
            'notify::active', self.evt_switch_acceleration
        )
        hbox.pack_end(switch_acceleration, False, True, 0)
        
        # Fin, agregar contenedor principal y mostrar todo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def get_mouse_acceleration(self):
        text_mouse_acceleration =(
            '/usr/share/X11/xorg.conf.d/'
            '50-mouse-acceleration.conf'
        )
        if Path(text_mouse_acceleration).exists():
            return False
        else:
            return True
        
    def evt_switch_acceleration(self, switch, gparam):
        state = switch.get_active()
        if switch.get_active():
            self.label_acceleration.set_text( Lang('acclr_on') )
        else:
            self.label_acceleration.set_text( Lang('acclr_off') )
        self.evt_acceleration(state=state)
    
    def evt_acceleration(self, state=True):
        if state == True:
            option = 'AccelerationON'
        elif state == False:
            option = 'AccelerationOFF'
            
        command=Util_Debian.Mouse_Config( option )
        
        # Funciona pero ten en cuenta que:
        # ¡Se bloquea!, El problema es abrir un dialogo desde otro dialogo, entonces se bloquea la aplicación
        # Aqui estoy abriendo un dialogo encima de otro dialogo, pero no se bloquea la app, porque estoy destruyendo el primer dialogo y solo queda el segundo dialogo, el cual fue abrido desde el primer dialogo.
        self.destroy()
        Config_Save( 
            parent=self,
            cfg=command
        )
        
        # Puedo unicamente ejecutar el comando desde una terminal, aca no se bloquea.
        #Command_Run(
        #    cmd=command
        #)


win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()