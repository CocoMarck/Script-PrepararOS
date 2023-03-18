import Modulo_Util as Util
import Modulo_Util_Debian as Util_Debian
import Modulo_Util_Gtk as Util_Gtk
import pathlib, subprocess
from glob import glob

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


cfg_file = f'Script_Preparar-OS_CFG.txt'

def Config_Save(cfg=''):
    if cfg == '':
        pass
    else:
        dialog = Util_Gtk.Dialog_Command_Run(
            None, cfg=cfg
        )
        dialog.run()
        dialog.destroy()
        with open(cfg_file, 'a') as file_cfg:
                file_cfg.write(cfg + f'\n#{Util.Separator(see=False)}\n')


class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Window Main')
        self.set_resizable(False)
        self.set_default_size(160, 256)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        title_label = Gtk.Label()
        title_label.set_markup('<b>Preparar Sistema</b>')
        box_v.pack_start(title_label, False, False, 16)
        
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
        
        view_cmd_btn = Gtk.Button(label='Ver comandos creados')
        view_cmd_btn.connect('clicked', self.evt_view_command)
        box_v.pack_start(view_cmd_btn, True, True, 0)
        
        exit_btn = Gtk.Button(label='Salir')
        exit_btn.connect('clicked', self.evt_exit)
        box_v.pack_end(exit_btn, True, True, 16)
        
        self.add(box_v)
        
    def evt_automatic(self, widget):
        print('Preparación automatica')
        
    def evt_application(self, widget):
        print('Instalar Aplicaciones')
        dialog = Dialog_Application_Menu(self)
        dialog.run()
        dialog.destroy()
        
    def evt_aptitude(self, widget):
        print('Menu Aptitude')
        dialog = Dialog_Aptitude(self)
        response = dialog.run()
        dialog.destroy()
        
    def evt_repository(self, widget):
        print('Cambiar repositorios')
        Config_Save(cfg=Util_Debian.Repository())
        
    def evt_triple_buffer(self, widget):
        print('Activar Triple Buffer')
        dialog = Dialog_TripleBuffer(self)
        dialog.run()
        dialog.destroy()
        
    def evt_view_command(self, widget):
        print('Abrir texto y ver comandos creados')
        dialog = Util_Gtk.Dialog_TextView(self,
                     text=Util.Text_Read(cfg_file, 'ModeText')
                 )
        dialog.run()
        dialog.destroy()
        
    def evt_exit(self, widget):
        print('Hasta la proxima...')
        self.destroy()
        

class Dialog_Aptitude(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Dialog Aptitude', transient_for=parent, flags=0)
        self.set_resizable(False)
        self.set_default_size(256, -1)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_v.set_property("expand", True)
        
        title_label = Gtk.Label()
        title_label.set_markup(f'<b>Aptitude</b>')
        box_v.pack_start(title_label, False, False, 16)
        
        update_button = Gtk.Button(label='Actualizar')
        update_button.connect('clicked', self.evt_update)
        box_v.pack_start(update_button, True, False, 0)
        
        
        clean_button = Gtk.Button(label='Limpiar Apps')
        clean_button.connect('clicked', self.evt_clean)
        box_v.pack_start(clean_button, True, False, 0)
        
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
        
    def evt_exit(self, widget):
        self.destroy()

class Dialog_TripleBuffer(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Dialog TripleBuffer', transient_for=parent, flags=0
        )
        self.set_resizable(False)
        self.set_default_size(304, 128)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box_v.set_property("expand", True)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Triple Buffer</b>')
        box_v.pack_start(label_title, True, True, 0)
        
        cmd = 'grep drivers /var/log/Xorg.0.log'
        cmd_run = str(
                      subprocess.check_output(
                          cmd, shell=True
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
            title='Dialog Application', transient_for=parent, flags=0
        )
        self.set_resizable(False)
        self.set_default_size(256, -1)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Aplicaciónes</b>')
        vbox.pack_start(label_title, True, True, 16)
        
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
        Config_Save(
            Util_Debian.App(opc='Desktop-xfce4', txt='&&\n\n') +
            Util_Debian.App(opc='Desktop-kdeplasma', txt='&&\n\n') +
            Util_Debian.App(opc='Desktop-gnome3', txt='&&\n\n') +
            Util_Debian.App(opc='Desktop-lxde', txt='&&\n\n') +
            Util_Debian.App(opc='Desktop-mate', txt='&&\n\n')
        )
        
    def evt_App_Optional(self, widget):
        dialog = Dialog_ApplicationOptional(self)
        dialog.run()
        dialog.destroy()
        
    def evt_Exit(self, widget):
        self.destroy()


class Dialog_ApplicationOptional(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title='Application Optional', transient_for=parent, flags=0
        )
        #Metodo 1 self.fullscreen()
        #Metodo 2 display = Gdk.Screen.get_default()
        #Metodo 2 self.set_default_size(display.get_width(), display.get_height())
        self.set_default_size(512, 512)
        #self.set_resizable(False)
        cfg_dir = './Script_Preparar-OS_Apps/'
        
        HeaderBar_title = Gtk.HeaderBar()
        HeaderBar_title.set_show_close_button(True)
        HeaderBar_title.props.title = 'Aplicaciones Opcionales'
        self.set_titlebar(HeaderBar_title)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
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
        
            archives = (
                sorted(pathlib.Path(f'{cfg_dir}/App_Optional')
                .glob('App_Optional-*.txt'))
            )
            self.arch_list = []
            #nmr = 0
            for arch in archives:
                #nmr += 1
                #print(f'{nmr}. {arch}')
                button_app = Gtk.Button(label=f'{arch}')
                button_app.connect('clicked', self.evt_button_app)
                vbox_scroll.pack_start(button_app, True, False, 0)
                
                self.arch_list.append(f'{arch}')
            
        except:
            pass
        
        button_app_all = Gtk.Button(label='Todas las apps')
        button_app_all.connect('clicked', self.evt_app_all)
        vbox_scroll.pack_end(button_app_all, True, False, 0)
        
        button_exit = Gtk.Button(label='Salir')
        button_exit.connect('clicked', self.evt_exit)
        vbox.pack_end(button_exit, False, False, 16)
        
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
                    cfg_file = button_app.get_label(),
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
                cfg_file = arch,
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
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()