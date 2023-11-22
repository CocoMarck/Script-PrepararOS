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
        button_auto.connect('clicked', self.evt_automatic)
        vbox_main.pack_start(button_auto, True, False, 0)
        
        button_apps = Gtk.Button( label=Lang('app_menu') )
        button_apps.connect('clicked', self.evt_application)
        vbox_main.pack_start(button_apps, True, False, 0)
        
        button_apt = Gtk.Button( label='Aptitude' )
        button_apt.connect('clicked', self.evt_aptitude)
        vbox_main.pack_start(button_apt, True, False, 0)
        
        button_repo = Gtk.Button( label=Lang('repos_nonfree') )
        button_repo.connect('clicked', self.evt_repository)
        vbox_main.pack_start(button_repo, True, False, 0)
        
        button_3_buffer = Gtk.Button( label=Lang('on_3_buffer') )
        button_3_buffer.connect('clicked', self.evt_triple_buffer)
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
    
    def evt_automatic(self, widget):
        self.hide()
        dialog = Dialog_Automatic(parent=self)
        dialog.run()
        dialog.destroy()
        self.show_all()
    
    def evt_application(self, widget):
        self.hide()
        dialog = Dialog_apps_menu(parent=self)
        dialog.run()
        dialog.destroy()
        self.show_all()
        
    def evt_aptitude(self, widget):
        self.hide()
        dialog = Dialog_Aptitude(parent=self)
        dialog.run()
        dialog.destroy()
        self.show_all()
    
    def evt_triple_buffer(self, widget):
        self.hide()
        dialog = Dialog_TripleBuffer(parent=self)
        dialog.run()
        dialog.destroy()
        self.show_all()
    
    def evt_repository(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.Repository()
        )
    
    def evt_mouse_cfg(self, widget):
        self.hide()
        dialog = Dialog_mouse_cfg(self)
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
        self.hide()
        dialog = Util_Gtk.Dialog_TextView(
            self,
            text=cfg_file,
            edit=False
        )
        dialog.run()
        dialog.destroy()
        self.show_all()


class Dialog_Automatic(Gtk.Dialog):
    def __init__(self, parent=None):
        super().__init__(
            title='Automatic Mode',
            transient_for=parent,
            flags=0
        )
        
        self.set_resizable(True)
        self.set_default_size(512, 128)
        
        # Contenedor Principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Seccion Vertical - Opción escritorio
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, True, False, 0)
        
        self.checkbutton_app_desktop = Gtk.CheckButton(
            label=Lang('app_desk')
        )
        self.checkbutton_app_desktop.set_active(False)
        hbox.pack_start(self.checkbutton_app_desktop, False, True, 0)
        
        liststore_app_desktop = Gtk.ListStore(str)
        for desktop in [
            'Desktop-xfce4',
            'Desktop-kdeplasma',
            'Desktop-gnome3',
            'Desktop-lxde',
            'Desktop-mate'
        ]:
            liststore_app_desktop.append([desktop])
        
        self.combobox_app_desktop = (
            Gtk.ComboBox.new_with_model(liststore_app_desktop)
        )
        rendertext_app_desktop = Gtk.CellRendererText()
        self.combobox_app_desktop.pack_start(rendertext_app_desktop, True)
        self.combobox_app_desktop.add_attribute(
            rendertext_app_desktop, 'text', 0
        )
        self.combobox_app_desktop.set_active(0)
        hbox.pack_end(self.combobox_app_desktop, False, True, 0)
        
        # Seccion Vertical - Apps Opcional
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, True, False, 0)
        
        self.checkbutton_app_optional = Gtk.CheckButton(
            label=Lang('app_optional')
        )
        self.checkbutton_app_optional.set_active(False)
        hbox.pack_start(self.checkbutton_app_optional, False, True, 0)
        
        self.dir_app_optional = f'{cfg_dir}App_Optional/'
        if not (
            Path(
                self.dir_app_optional + 'App_Optional-wine.txt'
            ).exists() or
            Path(
                self.dir_app_optional + 'App_Optional-flatpak.txt'
            ).exists() or
            Path(
                self.dir_app_optional + 'App_Optional-woeusb-ng.txt'
            ).exists()
        ):
            Util_Debian.App('Optional-wine')
            Util_Debian.App('Optional-flatpak')
            Util_Debian.App('Optional-woeusb-ng')
        
        liststore_app_optional = Gtk.ListStore(str)
        
        archives_app_optional = Files_List(
            files='App_Optional-*.txt',
            path=self.dir_app_optional,
            remove_path=True
        )
        for app_optional in archives_app_optional:
            text_app_optional = (app_optional.split('App_Optional-'))[1]
            text_app_optional = (text_app_optional.split(".txt"))[0]
            liststore_app_optional.append([text_app_optional])
        
        self.combobox_app_optional = Gtk.ComboBox.new_with_model(
            liststore_app_optional
        )
        rendertext_app_optional = Gtk.CellRendererText()
        self.combobox_app_optional.pack_start(rendertext_app_optional, True)
        self.combobox_app_optional.add_attribute(
            rendertext_app_optional, 'text', 0
        )
        self.combobox_app_optional.set_active(0)
        hbox.pack_end(self.combobox_app_optional, False, True, 0)
        
        # Seccion Vertical Final - boton para iniciar
        button_start = Gtk.Button( label=Lang('start') )
        button_start.connect('clicked', self.evt_start_automatic)
        vbox_main.pack_end(button_start, False, False, 0)
        
        # Fin, mostrar todo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_start_automatic(self, widget):
        # Desktop
        if self.checkbutton_app_desktop.get_active() == True:
            iter_app_desktop = self.combobox_app_desktop.get_active_iter()
            model_app_desktop = self.combobox_app_desktop.get_model()
            app_desktop = (
                Util_Debian.App(
                    model_app_desktop[iter_app_desktop][0], '&&\n\n'
                )
            )
        else:
            app_desktop = ''
        
        # Optional
        if self.checkbutton_app_optional.get_active() == True:
            iter_app_optional = self.combobox_app_optional.get_active_iter()
            model_app_optional = self.combobox_app_optional.get_model()
            text_app_optional = model_app_optional[iter_app_optional][0]
            app_optional = f'App_Optional-{text_app_optional}.txt'
            app_optional = Util_Debian.App(
                txt='&&\n\n',
                txt_title=(
                    f'{Lang("app")} {Lang("optional")} / {text_app_optional}'
                ),
                txt_add='',
                cfg_dir='./',
                cfg_file=(
                    self.dir_app_optional +
                    app_optional
                ),
                opc='continue'
            )
        else:
            app_optional = ''
        
        # Iniciar
        Config_Save(
            parent=self,
            cfg = (
                Util_Debian.Aptitude('update') + ' &&\n\n' +
                Util_Debian.App('Essential', '&&\n\n') +
                Util_Debian.App('Dependence', '&&\n\n') +
                Util_Debian.App('Uninstall', '&&\n\n') +
                app_desktop + app_optional +
                Util_Debian.Aptitude('clean')
            )
        )


class Dialog_apps_menu(Gtk.Dialog):
    def __init__(self, parent=None):
        super().__init__(
            title=Lang('app_menu'),
            transient_for=parent,
            flags=0
        )
        
        self.set_resizable(True)
        self.set_default_size(256, 0)
        
        # Contenedor Principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Secciones verticales - Opciones
        button_app_essential = Gtk.Button( label=Lang('essential') )
        button_app_essential.connect('clicked', self.evt_app_essential)
        vbox_main.pack_start(button_app_essential, True, False, 0)
        
        button_app_dependence = Gtk.Button( label=Lang('depens') )
        button_app_dependence.connect('clicked', self.evt_app_dependence)
        vbox_main.pack_start(button_app_dependence, True, False, 0)
        
        button_app_uninstall = Gtk.Button( label=Lang('utll') )
        button_app_uninstall.connect('clicked', self.evt_app_uninstall)
        vbox_main.pack_start(button_app_uninstall, True, False, 0)
        
        button_app_desktop = Gtk.Button( label=Lang('desk') )
        button_app_desktop.connect('clicked', self.evt_app_desktop)
        vbox_main.pack_start(button_app_desktop, True, False, 0)
        
        button_app_optional = Gtk.Button( label=Lang('optional') )
        button_app_optional.connect('clicked', self.evt_app_optional)
        vbox_main.pack_start(button_app_optional, True, False, 0)
        
        # Fin, mostrar todo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_app_essential(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(opc='Essential')
        )
        
    def evt_app_dependence(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(opc='Dependence')
        )
        
    def evt_app_uninstall(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App(opc='Uninstall')
        )
    
    def evt_app_desktop(self, widget):
        dialog = Dialog_app_desktop(parent=self)
        dialog.run()
        dialog.destroy()
    
    def evt_app_optional(self, widget):
        dialog = Dialog_app_optional(parent=self)
        dialog.run()
        dialog.destroy()


class Dialog_app_desktop(Gtk.Dialog):
    def __init__(self, parent=None):
        super().__init__(
            title=Lang('app_desk'),
            transient_for=parent,
            flags=0
        )
        
        self.set_resizable(True)
        self.set_default_size(308, 128)
        
        # Contenedor Principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Secciones Verticales - Opciones
        for desktop in [
            'Desktop-xfce4',
            'Desktop-kdeplasma',
            'Desktop-gnome3',
            'Desktop-lxde',
            'Desktop-mate'
        ]:
            button_app_desktop = Gtk.Button(label=desktop)
            button_app_desktop.connect('clicked', self.evt_app_desktop)
            vbox_main.pack_start(button_app_desktop, True, False, 0)
        
        # Fin, mostrar todo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_app_desktop(self, button):
        Config_Save(
            parent=self,
            cfg=Util_Debian.App( button.get_label() )
        )


class Dialog_app_optional(Gtk.Dialog):
    def __init__(self, parent=None):
        super().__init__(
            title=Lang('app_optional'),
            transient_for=parent,
            flags=0
        )
        
        self.set_resizable(True)
        self.set_default_size(512, 512)
        
        # Contenedor principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox_main.set_property('expand', True)
        
        # Secciones verticales - Todos los widgets
        scroll_app_optional = Gtk.ScrolledWindow()
        scroll_app_optional.set_hexpand(True)
        scroll_app_optional.set_vexpand(True)
        vbox_main.pack_start(scroll_app_optional, True, True, 0)
        
        self.dir_app_optional = f'{cfg_dir}App_Optional/'
        if not (
            Path(
                f'{self.dir_app_optional}App_Optional-wine.txt'
            ).exists() or
            Path(
                f'{self.dir_app_optional}App_Optional-flatpak.txt'
            ).exists() or
            Path(
                f'{self.dif_app_optional}App_Optional-woeusb-ng.txt'
            ).exists()
        ):
            Util_Debian.App('Optional-wine')
            Util_Debian.App('Optional-flatpak')
            Util_Debian.App('Optional-woeusb-ng')
        
        try:
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            scroll_app_optional.add(vbox)
            
            archives = Files_List(
                files='App_Optional-*.txt',
                path=self.dir_app_optional,
                remove_path=True
            )
            
            self.list_app_optional = []
            for app_optional in archives:
                text_app_optional = (app_optional.split('App_Optional-'))[1]
                text_app_optional = (text_app_optional.split(".txt"))[0]
                
                button_app_optional = Gtk.Button( label=text_app_optional )
                button_app_optional.connect('clicked', self.evt_app_optional)
                vbox.pack_start(button_app_optional, True, False, 0)
                
                self.list_app_optional.append(text_app_optional)
        except:
            pass
        
        # Seccion Vertical para agregar todas las apps
        button_app_all_optional = Gtk.Button( label=Lang('all_apps') )
        button_app_all_optional.connect('clicked', self.evt_app_all_optional)
        vbox_main.pack_end(button_app_all_optional, False, False, 32)
        
        # Fin, mostrar todo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_app_optional(self, button):
        text_app_optional = button.get_label()
        app_optional = f'App_Optional-{text_app_optional}.txt'
        if text_app_optional in self.list_app_optional:
            Config_Save(
                parent=self,
                cfg = Util_Debian.App(
                    txt_title=f'{Lang("app")} / {text_app_optional}',
                    txt_add='',
                    cfg_dir='./',
                    cfg_file=(
                        self.dir_app_optional +
                        app_optional
                    ),
                    opc='continue'
                )
            )
        else:
            pass
    
    def evt_app_all_optional(self, widget):
        app = ''
        app_all = ''
        line_jump='&&\n\n'
        
        for text_app_optional in self.list_app_optional:
            app_optional = f'App_Optional-{text_app_optional}.txt'
            
            app = Util_Debian.App(
                txt=line_jump,
                txt_title=f'{Lang("app")} / {text_app_optional}',
                txt_add='',
                cfg_dir='./',
                cfg_file=(
                    self.dir_app_optional +
                        app_optional
                ),
                opc='continue'
            )
            app_all += app
        
        # Esto es el caracter 4 de la line_jump...
        if '&' == app_all[-4]:
            app_all = app_all[:-4]
        else:
            pass
        
        # Ejecutar comando para instalar todas las apps opcionales
        Config_Save(
            parent=self,
            cfg=app_all
        )


class Dialog_Aptitude(Gtk.Dialog):
    def __init__(self, parent=None):
        super().__init__(
            title='Aptitude',
            transient_for=parent,
            flags=0
        )
        
        self.set_resizable(True)
        self.set_default_size(308, 0)
        
        # Contenedor principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Secciones Verticales - Botones actualizar y limpiar
        button_update = Gtk.Button( label=Lang('upd') )
        button_update.connect('clicked', self.evt_apt_update)
        vbox_main.pack_start(button_update, False, False, 0)
        
        button_clean = Gtk.Button( label=Lang('cln') )
        button_clean.connect('clicked', self.evt_apt_clean)
        vbox_main.pack_start(button_clean, False, False, 0)
        
        # Seccion Vertical - Boton Instalar paquete
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, True, False, 0)

        button_install = Gtk.Button( label=Lang('install') )
        button_install.connect('clicked', self.evt_apt_app_install)
        hbox.pack_start(button_install, False, False, 0)
        
        self.entry_install = Gtk.Entry()
        self.entry_install.set_placeholder_text( Lang('app') )
        self.entry_install.connect('activate', self.evt_apt_app_install)
        hbox.pack_end(self.entry_install, False, False, 0)
        
        # Seccion Vertical - Boton eliminar paquete
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, True, False, 0)

        button_purge = Gtk.Button( label=Lang('prg') )
        button_purge.connect('clicked', self.evt_apt_app_purge)
        hbox.pack_start(button_purge, False, False, 0)
        
        self.entry_purge = Gtk.Entry()
        self.entry_purge.set_placeholder_text( Lang('app') )
        self.entry_purge.connect('activate', self.evt_apt_app_purge)
        hbox.pack_end(self.entry_purge, False, False, 0)
        
        # Fin, mostrar dialogo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_apt_update(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.Aptitude('update')
        )
        
    def evt_apt_clean(self, widget):
        Config_Save(
            parent=self,
            cfg=Util_Debian.Aptitude('clean')
        )
    
    def evt_apt_app_install(self, widget):
        app_to_install = self.entry_install.get_text()
        if not app_to_install == '':
            Config_Save(
                parent=self,
                cfg = (
                    'sudo apt update &&\n\n' +
                    Util_Debian.Aptitude('install') +
                    app_to_install
                )
            )
    
    def evt_apt_app_purge(self, widget):
        app_to_purge = self.entry_purge.get_text()
        if not app_to_purge == '':
            Config_Save(
                parent=self,
                cfg = (
                    Util_Debian.Aptitude('purge') +
                    app_to_purge + ' &&\n\n'
                    'sudo apt autoremove ' +
                    app_to_purge + ' &&\n\n' +
                    Util_Debian.Aptitude('clean')
                )
            )


class Dialog_TripleBuffer(Gtk.Dialog):
    def __init__(self, parent=None):
        super().__init__(
            title='Triple Buffer Config',
            transient_for=parent,
            flags=0
        )
        self.set_resizable(True)
        self.set_default_size(308, 256)
        
        # Contenedor principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Seccion vertical - Comando para ver Triple Buffer
        command = 'grep drivers /var/log/Xorg.0.log'
        command_run = subprocess.check_output(
            command, shell=True, text=True
        )
        label = Gtk.Label()
        label.set_markup(
            f'<i>{Lang("cmd")}: "{command}</i>\n'
            '\n'
            f'<b>{command_run}</b>'
        )
        label.set_line_wrap(True)
        #label.set_max_width_chars(0) # Para verse bien (Posible Bug)
        label.set_selectable(True)
        vbox_main.pack_start(label, False, True, 0)
        
        # Secciones Verticales - Botones
        list_graphic = [
            Lang('gpc_amd'),
            Lang('gpc_intel'),
        ]
        for graphic in list_graphic:
            button_graphic = Gtk.Button(label=graphic)
            button_graphic.connect('clicked', self.evt_TripleBuffer_graphic)
            vbox_main.pack_start(button_graphic, True, False, 0)
        
        # Fin, mostrar dialogo
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def get_dict_graphic(self):
        dict_graphic = {
            Lang('gpc_amd'): '20-radeon.conf',
            Lang('gpc_intel'): '20-intel-gpu.conf'
        }
        return dict_graphic
    
    def evt_TripleBuffer_graphic(self, button):
        button_graphic = button.get_label()
        dict_graphic = self.get_dict_graphic()
        
        if button_graphic in dict_graphic:
            graphic = dict_graphic[button_graphic]
            
            Config_Save(
                parent=self,
                cfg=Util_Debian.TripleBuffer(graphic)
            )
        else:
            pass


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
        #self.destroy()
        #Config_Save( 
        #    parent=self,
        #    cfg=command
        #)
        
        # Puedo unicamente ejecutar el comando desde una terminal, aca no se bloquea.
        Command_Run(
            cmd=command
        )


win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()