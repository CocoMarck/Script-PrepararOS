import Modulo_Util as Util
import Modulo_Util_Debian as Util_Debian
import Modulo_Util_Gtk as Util_Gtk
import pathlib, subprocess
from glob import glob

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


cfg_file = f'Script_CFG.txt'
cfg_dir = 'Script_Apps/'

def Config_Save(cfg=''):
    if cfg == '':
        pass
    else:
        dialog = Util_Gtk.Dialog_Command_Run(
            None, cfg=cfg, cfg_file=cfg_file
        )
        dialog.run()
        dialog.destroy()

class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Preparing OS')
        self.set_resizable(True)
        self.set_default_size(160, 256)
        
        # Contenedor Principal
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Seccion Vertical - Botones Principales
        auto_btn = Gtk.Button(label='Automatico')
        auto_btn.connect('clicked', self.evt_automatic)
        box_v.pack_start(auto_btn, True, True, 0)
        
        app_btn = Gtk.Button(label='Aplicaciones')
        app_btn.connect('clicked', self.evt_application)
        box_v.pack_start(app_btn, True, True, 0)
        
        apt_btn = Gtk.Button(label='Aptitude')
        apt_btn.connect('clicked', self.evt_aptitude)
        box_v.pack_start(apt_btn, True, True, 0)
        
        repo_btn = Gtk.Button(label='Repositorios NO LIBRES')
        repo_btn.connect('clicked', self.evt_repository)
        box_v.pack_start(repo_btn, True, True, 0)
        
        triple_buffer_btn = Gtk.Button(label='Activar Triple Buffer')
        triple_buffer_btn.connect('clicked', self.evt_triple_buffer)
        box_v.pack_start(triple_buffer_btn, True, True, 0)
        
        mouse_cfg_btn = Gtk.Button(label='Configuración del mouse')
        mouse_cfg_btn.connect('clicked', self.evt_mouse_cfg)
        box_v.pack_start(mouse_cfg_btn, True, True, 0)
        
        # Seccion Vertical - Boton comando Perzonalizado
        cmdrun_box = Gtk.Box(spacing=4)
        box_v.pack_start(cmdrun_box, True, True, 0)
        
        cmdrun_btn = Gtk.Button(label='Ejecutar Comando')
        cmdrun_btn.connect('clicked', self.evt_command_run)
        cmdrun_box.pack_start(cmdrun_btn, True, True, 0)
        
        self.cmdrun_entry = Gtk.Entry()
        self.cmdrun_entry.set_placeholder_text('Comando')
        cmdrun_box.pack_end(self.cmdrun_entry, True, True, 0)
        
        # Sección Vertical - Boton ver comandos
        view_cmd_btn = Gtk.Button(label='Ver comandos creados')
        view_cmd_btn.connect('clicked', self.evt_view_command)
        box_v.pack_start(view_cmd_btn, True, True, 0)
        
        # Sección Vertical - Boton exit
        exit_btn = Gtk.Button(label='Salir')
        exit_btn.connect('clicked', self.evt_exit)
        box_v.pack_end(exit_btn, True, True, 16)
        
        # Fin, agregar el contenedor prinicpal a la ventana
        self.add(box_v)
        
    def evt_automatic(self, widget):
        dialog = Dialog_Automatic(self)
        dialog.run()
        dialog.destroy()
        
    def evt_application(self, widget):
        dialog = Dialog_Application_Menu(self)
        dialog.run()
        dialog.destroy()
        
    def evt_aptitude(self, widget):
        dialog = Dialog_Aptitude(self)
        response = dialog.run()
        dialog.destroy()
        
    def evt_repository(self, widget):
        Config_Save(cfg=Util_Debian.Repository())
        
    def evt_triple_buffer(self, widget):
        dialog = Dialog_TripleBuffer(self)
        dialog.run()
        dialog.destroy()
        
    def evt_mouse_cfg(self, widget):
        dialog = Dialog_mouse_cfg(self)
        dialog.run()
        dialog.destroy()
        
    def evt_command_run(self, widget):
        if self.cmdrun_entry.get_text() == '':
            pass
        else:
            Util.Command_Run( self.cmdrun_entry.get_text() )
        
    def evt_view_command(self, widget):
        dialog = Util_Gtk.Dialog_TextView(self,
                     text=Util.Text_Read(cfg_file, 'ModeText')
                 )
        dialog.run()
        dialog.destroy()
        
    def evt_exit(self, widget):
        self.destroy()
        

class Dialog_Automatic(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Automatic Mode', transient_for=parent, flags=0)
        self.set_default_size(512, -1)
        self.set_resizable(False)
        
        # Contenedor Principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_property("expand", True)
        
        # Seccion 1 Apps Desktop
        hbox_app_desktop = Gtk.Box(spacing=0)
        vbox.pack_start(hbox_app_desktop, True, True, 0)
        
        self.CheckButton_app_desktop = Gtk.CheckButton(label='App Desktop')
        #self.CheckButton_app_desktop.set_active(True)
        hbox_app_desktop.pack_start(
            self.CheckButton_app_desktop, False, True, 0
        )
        
        liststore_app_desktop = Gtk.ListStore(str)
        app_desktop = [
            'Desktop-xfce4',
            'Desktop-kdeplasma',
            'Desktop-gnome3',
            'Desktop-lxde',
            'Desktop-mate',
        ]
        for app in app_desktop:
            liststore_app_desktop.append([app])
            
        self.ComboBox_app_desktop = (
            Gtk.ComboBox.new_with_model(liststore_app_desktop)
        )
        CellRendererText_app_desktop = Gtk.CellRendererText()
        self.ComboBox_app_desktop.pack_start(CellRendererText_app_desktop, True)
        self.ComboBox_app_desktop.add_attribute(
            CellRendererText_app_desktop, 'text', 0
        )
        self.ComboBox_app_desktop.set_active(0)
        hbox_app_desktop.pack_end(self.ComboBox_app_desktop, False, True, 0)
        
        
        # Seccion 2 Apps Optional
        hbox_app_optional = Gtk.Box(spacing=64)
        vbox.pack_start(hbox_app_optional, True, True, 0)
        
        self.CheckButton_app_optional = Gtk.CheckButton(label='App Optional')
        #self.CheckButton_app_optional.set_active(True)
        hbox_app_optional.pack_start(self.CheckButton_app_optional, True, True, 0)
        
        if (
            pathlib.Path(f'{cfg_dir}/App_Optional/'
                        'App_Optional-wine.txt').exists() or
        
            pathlib.Path(f'{cfg_dir}/App_Optional/'
                        'App_Optional-flatpak.txt').exists() or
        
            pathlib.Path(f'{cfg_dir}/App_Optional/'
                        'App_Optional-woeusb-ng.txt').exists()
        ): pass
        else:
            Util_Debian.App('Optional-wine')
            Util_Debian.App('Optional-flatpak')
            Util_Debian.App('Optional-woeusb-ng')

        liststore_app_optional = Gtk.ListStore(str)
        self.path_app_optional = f'{cfg_dir}App_Optional/'
        archives = Util.Files_List(
            files='App_Optional-*.txt',
            path=self.path_app_optional,
            remove_path=True
        )
        for arch in archives:
            liststore_app_optional.append([f'{arch}'])
        
        self.ComboBox_app_optional = Gtk.ComboBox.new_with_model(
            liststore_app_optional
        )
        CellRendererText_app_optional = Gtk.CellRendererText()
        self.ComboBox_app_optional.pack_start(CellRendererText_app_optional, True)
        self.ComboBox_app_optional.add_attribute(
            CellRendererText_app_optional, 'text', 0
        )
        self.ComboBox_app_optional.set_active(0)
        hbox_app_optional.pack_end(self.ComboBox_app_optional, False, True, 0)
        
        # Seccion Final Iniciar y Salir
        hbox = Gtk.Box(spacing=64)
        vbox.pack_end(hbox, False, True, 0)
        
        button_automatic = Gtk.Button(label='Iniciar')
        button_automatic.connect('clicked', self.evt_automatic)
        hbox.pack_start(button_automatic, False, True, 0)
        
        button_exit = Gtk.Button(label='Salir')
        button_exit.connect('clicked', self.evt_exit)
        hbox.pack_end(button_exit, False, True, 0)
        
        self.get_content_area().add(vbox)
        self.show_all()
        
    def evt_automatic(self, widget):
        # Seccion 1 Desktop
        if self.CheckButton_app_desktop.get_active() == True:
            iter_app_desktop = self.ComboBox_app_desktop.get_active_iter()
            model_app_desktop = self.ComboBox_app_desktop.get_model()
            app_desktop = (
                Util_Debian.App(model_app_desktop[iter_app_desktop][0], '&&\n\n')
            )
        else:
            app_desktop = ''
            
        if self.CheckButton_app_optional.get_active() == True:
            iter_app_optional = self.ComboBox_app_optional.get_active_iter()
            model_app_optional = self.ComboBox_app_optional.get_model()
            app_optional = (
                Util_Debian.App(
                    txt = '&&\n\n',
                    txt_title = 'Applications / Optional',
                    txt_add = '',
                    cfg_dir = './',
                    cfg_file = (
                        self.path_app_optional + 
                        model_app_optional[iter_app_optional][0]
                    ),
                    opc = 'continue'
                )
            )
        else:
            app_optional = ''
    
        # Seccion Final Start
        Config_Save(
            Util_Debian.Aptitude('update') + ' &&\n\n' +
            Util_Debian.App('Essential', '&&\n\n') +
            Util_Debian.App('Dependence', '&&\n\n') +
            Util_Debian.App('Uninstall', '&&\n\n') +
            app_desktop + app_optional +
            Util_Debian.Aptitude('clean')
        )
        
    def evt_exit(self, widget):
        self.destroy()
        

class Dialog_Aptitude(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Aptitude Options', transient_for=parent, flags=0)
        self.set_resizable(False)
        self.set_default_size(256, -1)
        
        # Contenedor Principal
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_v.set_property("expand", True)
        
        # Boton para Actualizar
        update_button = Gtk.Button(label='Actualizar')
        update_button.connect('clicked', self.evt_update)
        box_v.pack_start(update_button, True, False, 0)
        
        # Boton para Limpiar
        clean_button = Gtk.Button(label='Limpiar Apps')
        clean_button.connect('clicked', self.evt_clean)
        box_v.pack_start(clean_button, True, False, 0)
        
        # Boton para Instalar app
        box_h = Gtk.Box(spacing=4)
        box_v.pack_start(box_h, True, True, 0)
        
        install_button = Gtk.Button(label='Instalar App')
        install_button.connect('clicked', self.evt_install)
        box_h.pack_start(install_button, True, True, 0)
        
        self.install_entry = Gtk.Entry()
        self.install_entry.set_placeholder_text('Aplicación')
        box_h.pack_end(self.install_entry, False, True, 0)
        
        # Boton para Desinstalar app
        box_h = Gtk.Box(spacing=4)
        box_v.pack_start(box_h, True, True, 0)
        
        purge_button = Gtk.Button(label='Purgar App')
        purge_button.connect('clicked', self.evt_purge)
        box_h.pack_start(purge_button, True, True, 0)
        
        self.purge_entry = Gtk.Entry()
        self.purge_entry.set_placeholder_text('Aplicación')
        box_h.pack_end(self.purge_entry, False, True, 0)
        
        # Sección final, salir
        exit_button = Gtk.Button(label='Salir')
        exit_button.connect('clicked', self.evt_exit)
        box_v.pack_end(exit_button, True, False, 16)
        
        self.get_content_area().add(box_v)
        self.show_all()
        
    def evt_update(self, widget):
        Config_Save(
            cfg=Util_Debian.Aptitude('update')
        )
        
    def evt_clean(self, widget):
        Config_Save(
            cfg=Util_Debian.Aptitude('clean')
        )
        
    def evt_install(self, widget):
        if self.install_entry.get_text() == '':
            cfg = ''
        else:
            cfg = (
                'sudo apt update &&\n\n' +
                Util_Debian.Aptitude('install') +
                self.install_entry.get_text()
            )

        Config_Save(
            cfg=cfg
        )
        
    def evt_purge(self, widget):
        if self.purge_entry.get_text() == '':
            cfg = ''
        else:
            cfg = (
                Util_Debian.Aptitude('purge') +
                self.purge_entry.get_text() + ' &&\n\n'
                'sudo apt autoremove ' +
                self.purge_entry.get_text() + ' &&\n\n' +
                Util_Debian.Aptitude('clean')
            )
            
        Config_Save(
            cfg=cfg
        )
        
    def evt_exit(self, widget):
        self.destroy()


class Dialog_TripleBuffer(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Triple Buffer Config', transient_for=parent, flags=0
        )
        self.set_resizable(False)
        self.set_default_size(304, 128)
        
        # Contenedor Principal
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_v.set_property("expand", True)
        
        # Secciones Verticales - Opciones
        cmd = 'grep drivers /var/log/Xorg.0.log'
        cmd_run = str(
                      subprocess.check_output(
                          cmd, shell=True, text=True
                      )
                  )
        label_command = Gtk.Label()
        label_command.set_markup(
            f'<i>Comando: "{cmd}"</i>\n\n'
            f'<b>{cmd_run}</b>'
        )
        label_command.set_line_wrap(True)
        label_command.set_max_width_chars(0) # Para verse bien (Posible bug)
        label_command.set_selectable(True)
        box_v.pack_start(label_command, True, True, 8)
        
        btn_GraphicAMD = Gtk.Button(label='Grafica AMD')
        btn_GraphicAMD.connect('clicked', self.evt_GraphicAMD)
        box_v.pack_start(btn_GraphicAMD, True, True, 0)
        
        btn_GraphicIntel = Gtk.Button(label='Grafica Intel')
        btn_GraphicIntel.connect('clicked', self.evt_GraphicIntel)
        box_v.pack_start(btn_GraphicIntel, True, True, 0)
        
        btn_none = Gtk.Button(label='Salir')
        btn_none.connect('clicked', self.evt_none)
        box_v.pack_end(btn_none, True, False, 16)
        
        # Fin, Mostrar Contenedor principal y todo
        self.get_content_area().add(box_v)
        self.show_all()
        
    def evt_GraphicAMD(self, widget):
        Config_Save(
            cfg=Util_Debian.TripleBuffer('20-radeon.conf')
        )
        
    def evt_GraphicIntel(self, widget):
        Config_Save(
            cfg=Util_Debian.TripleBuffer('20-intel-gpu.conf')
        )
        
    def evt_none(self, widget):
        self.destroy()
        

class Dialog_Application_Menu(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Application Menu', transient_for=parent, flags=0
        )
        self.set_resizable(False)
        self.set_default_size(256, -1)
        
        # Contenedor Principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Secciones Verticales - Opciones
        button_App_Essential = Gtk.Button(label='Esensiales')
        button_App_Essential.connect('clicked', self.evt_App_Essential)
        vbox.pack_start(button_App_Essential, True, True, 0)
        
        button_App_Dependence = Gtk.Button(label='Dependencias')
        button_App_Dependence.connect('clicked', self.evt_App_Dependence)
        vbox.pack_start(button_App_Dependence, True, True, 0)
        
        button_App_Uninstall = Gtk.Button(label='Desinstalar')
        button_App_Uninstall.connect('clicked', self.evt_App_Uninstall)
        vbox.pack_start(button_App_Uninstall, True, True, 0)
        
        button_App_Desktop = Gtk.Button(label='Escritorio')
        button_App_Desktop.connect('clicked', self.evt_App_Desktop)
        vbox.pack_start(button_App_Desktop, True, True, 0)
        
        button_App_Optional = Gtk.Button(label='Opcionales')
        button_App_Optional.connect('clicked', self.evt_App_Optional)
        vbox.pack_start(button_App_Optional, True, True, 0)
        
        button_Exit = Gtk.Button(label='Salir')
        button_Exit.connect('clicked', self.evt_Exit)
        vbox.pack_end(button_Exit, False, False, 16)
        
        # Fin, Mostrar contenedor principal y todo
        self.get_content_area().add(vbox)
        self.show_all()
        
    def evt_App_Essential(self, widget):
        Config_Save(
            Util_Debian.App(opc='Essential')
        )
        
    def evt_App_Dependence(self, widget):
        Config_Save(
            Util_Debian.App(opc='Dependence')
        )
        
    def evt_App_Uninstall(self, widget):
        Config_Save(
            Util_Debian.App(opc='Uninstall')
        )
        
    def evt_App_Desktop(self, widget):
        dialog = Dialog_Application_Desktop(self)
        dialog.run()
        dialog.destroy()
        
    def evt_App_Optional(self, widget):
        dialog = Dialog_Application_Optional(self)
        dialog.run()
        dialog.destroy()
        
    def evt_Exit(self, widget):
        self.destroy()


class Dialog_Application_Desktop(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Application Desktop', transient_for=parent, flags=0
        )
        self.set_default_size(256, -1)
        self.set_resizable(False)
        
        # Establecer Bara titular
        HeaderBar_title = Gtk.HeaderBar()
        HeaderBar_title.set_show_close_button(True)
        HeaderBar_title.props.title = 'Aplicaciones Escritorio'
        self.set_titlebar(HeaderBar_title)
        
        # Contenedor Principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Secciones verticales - Opciones
        button_app_desktop = Gtk.Button(label='Desktop-xfce4')
        button_app_desktop.connect('clicked', self.evt_app_desktop)
        vbox.pack_start(button_app_desktop, True, True, 0)
        
        button_app_desktop = Gtk.Button(label='Desktop-kdeplasma')
        button_app_desktop.connect('clicked', self.evt_app_desktop)
        vbox.pack_start(button_app_desktop, True, True, 0)
        
        button_app_desktop = Gtk.Button(label='Desktop-gnome3')
        button_app_desktop.connect('clicked', self.evt_app_desktop)
        vbox.pack_start(button_app_desktop, True, True, 0)
        
        button_app_desktop = Gtk.Button(label='Desktop-lxde')
        button_app_desktop.connect('clicked', self.evt_app_desktop)
        vbox.pack_start(button_app_desktop, True, True, 0)
        
        button_app_desktop = Gtk.Button(label='Desktop-mate')
        button_app_desktop.connect('clicked', self.evt_app_desktop)
        vbox.pack_start(button_app_desktop, True, True, 0)
        
        button_exit = Gtk.Button(label='Salir')
        button_exit.connect('clicked', self.evt_exit)
        vbox.pack_end(button_exit, True, False, 16)
        
        # Fin Mostrar contenedor principal y todo
        self.get_content_area().add(vbox)
        self.show_all()
        
    def evt_app_desktop(self, button):
        Config_Save(
            Util_Debian.App( button.get_label() )
        )
        
    def evt_exit(self, widget):
        self.destroy()


class Dialog_Application_Optional(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Application Optional', transient_for=parent, flags=0
        )
        #Metodo 1 self.fullscreen()
        #Metodo 2 display = Gdk.Screen.get_default()
        #Metodo 2 self.set_default_size(display.get_width(), display.get_height())
        self.set_default_size(512, 512)
        #self.set_resizable(False)
        
        # Barra titular 
        HeaderBar_title = Gtk.HeaderBar()
        HeaderBar_title.set_show_close_button(True)
        HeaderBar_title.props.title = 'Aplicaciones Opcionales'
        self.set_titlebar(HeaderBar_title)
        
        # Contnedor Principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Secciones verticales - Todos los widgets
        scroll_button = Gtk.ScrolledWindow()
        scroll_button.set_hexpand(True)
        scroll_button.set_vexpand(True)
        vbox.pack_start(scroll_button, True, True, 0)
        
        if (
            pathlib.Path(f'{cfg_dir}/App_Optional/'
                        'App_Optional-wine.txt').exists() or
        
            pathlib.Path(f'{cfg_dir}/App_Optional/'
                        'App_Optional-flatpak.txt').exists() or
        
            pathlib.Path(f'{cfg_dir}/App_Optional/'
                        'App_Optional-woeusb-ng.txt').exists()
        ): pass
        else:
            Util_Debian.App('Optional-wine')
            Util_Debian.App('Optional-flatpak')
            Util_Debian.App('Optional-woeusb-ng')
            
        try:
            vbox_scroll = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            scroll_button.add(vbox_scroll)
        
            self.path_app_optional = f'{cfg_dir}App_Optional/'
            archives = Util.Files_List(
                files='App_Optional-*.txt',
                path=self.path_app_optional,
                remove_path=True
            )
            self.arch_list = []
            #nmr = 0
            for arch in archives:
                #nmr += 1
                #print(f'{nmr}. {arch}')
                button_app = Gtk.Button(label=f'{arch}')
                button_app.connect('clicked', self.evt_button_app)
                vbox_scroll.pack_start(button_app, False, True, 0)
                
                self.arch_list.append(f'{arch}')
            
        except:
            pass
        
        button_app_all = Gtk.Button(label='Todas las apps')
        button_app_all.connect('clicked', self.evt_app_all)
        vbox.pack_start(button_app_all, False, False, 0)
        
        button_exit = Gtk.Button(label='Salir')
        button_exit.connect('clicked', self.evt_exit)
        vbox.pack_end(button_exit, False, False, 16)
        
        # Fin Mostrar contenedor principal y todo
        self.get_content_area().add(vbox)
        self.show_all()
        
    def evt_button_app(self, button_app):
        print(f'{button_app.get_label()}')
        print(self.arch_list)
        if button_app.get_label() in self.arch_list:
            Config_Save(
                Util_Debian.App(
                    txt_title = 'Applications / Optional',
                    txt_add = '',
                    cfg_dir = './',
                    cfg_file = (
                        self.path_app_optional +
                        button_app.get_label()
                    ),
                    opc = 'continue'
                )
            )
        else:
            pass
            
    def evt_app_all(self, button):
        app = ''
        app_all = ''
        line_jump = '&&\n\n'
        
        for arch in self.arch_list:
            app = Util_Debian.App(
                txt = line_jump,
                txt_title = 'Applications / Optional',
                txt_add = '',
                cfg_dir = './',
                cfg_file = (
                    self.path_app_optional +
                    arch
                ),
                opc = 'continue'
            )
            app_all += app
            
        #Este es el caracter 4 de line_jump...
        if '&' == app_all[-4]:
            app_all = app_all[:-4]
        else:
            pass
            
        Config_Save(app_all)
    
    def evt_exit(self, widget):
        self.destroy()
        

class Dialog_mouse_cfg(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Mouse Config')
        self.set_default_size(256, 128)
        
        # Contenedor Principal
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox_main.set_property('expand', True)
        
        # Seccion Vertical 1 - Activar/Desactivar Aceleracion
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        vbox_main.pack_start(hbox, True, False, 0)
        
        self.label_acceleration = Gtk.Label(label='')
        hbox.pack_start(self.label_acceleration, False, True, 0)
        
        switch_acceleration = Gtk.Switch()
        if pathlib.Path(
            '/usr/share/X11/xorg.conf.d/'
            '50-mouse-acceleration.conf'
        ).exists():
            switch_acceleration.set_active(False)
            self.label_acceleration.set_text('AccelerationOFF:')
        else:
            switch_acceleration.set_active(True)
            self.label_acceleration.set_text('AccelerationON')
        switch_acceleration.connect('notify::active', self.evt_acceleration)
        hbox.pack_end(switch_acceleration, False, True, 0)
        
        # Fin, agregar contenedor principal y mostrar todo
        self.get_content_area().add(vbox_main)
        self.show_all()
        
    def evt_acceleration(self, switch, gparam):
        if switch.get_active():
            option = 'AccelerationON'
        else:
            option = 'AccelerationOFF'
        self.label_acceleration.set_text(f'{option}:')
        Config_Save( Util_Debian.Mouse_Config( option ) )
            
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()