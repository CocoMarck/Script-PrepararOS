import Modulo_Util as Util
import Modulo_Util_Gtk as Util_Gtk
import pathlib

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
        

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
        
    def evt_aptitude(self, widget):
        print('Menu Aptitude')
        dialog = Dialog_Aptitude(self)
        dialog.run()
        dialog.destroy()
        
    def evt_repository(self, widget):
        print('Cambiar repositorios')
        
    def evt_triple_buffer(self, widget):
        print('Activar Triple Buffer')
        
    def evt_view_command(self, widget):
        print('Abrir texto y ver comandos creados')
        dialog = Util_Gtk.Dialog_TextView(self)
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
        dialog = Util_Gtk.Dialog_Command_Run(
                     self, cfg=Util.Aptitude('update'), txt='Actualizar'
                 )
        dialog.run()
        dialog.destroy()
        
    def evt_clean(self, widget):
        dialog = Util_Gtk.Dialog_Command_Run(
                     self, cfg=Util.Aptitude('clean'), txt='Limpiar'
                 )
        dialog.run()
        dialog.destroy()
        
    def evt_exit(self, widget):
        self.destroy()
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()