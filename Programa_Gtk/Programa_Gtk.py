import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Dialog_Start(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Dialogo Empezar', transient_for=parent, flags=0)
        self.set_default_size(256, 64)
                
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Dialogo Empezar</b>')
        label_title.set_justify(Gtk.Justification.CENTER)
        box_v.pack_start(label_title, True, True, 0)
        
        btn_demo = Gtk.Button(label='Boton de prueba')
        btn_demo.connect('clicked', self.evt_demo)
        box_v.pack_start(btn_demo, True, True, 0)
        
        box_main = self.get_content_area()
        box_main.add(box_v)
        self.show_all()
        
    def evt_demo(self, widget):
        print('Boton de prueba, precionado')


class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Ventana Main')
        self.set_default_size(256, 128)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Ventana Main</b>')
        label_title.set_justify(Gtk.Justification.CENTER)
        box_v.pack_start(label_title, True, True, 0)

        btn_start = Gtk.Button(label='Empezar')
        btn_start.connect("clicked", self.evt_start)
        box_v.pack_start(btn_start, True, True, 0)

        btn_exit = Gtk.Button(label='Salir')
        btn_exit.connect("clicked", self.evt_exit)
        box_v.pack_start(btn_exit, True, True, 0)
        
        self.add(box_v)
        
        #self.add(label_title)
        
        #table = Gtk.Grid()
        #table.add(label_title)
        #table.attach(btn_start, 0, 1, 2, 1)
        #table.attach(btn_exit, 0, 2, 1, 1)
        
        #self.add(table)
        
    def evt_start(self, widget):
        dialog = Dialog_Start(self)
        response = dialog.run()
        dialog.destroy()
        print('Abriendo ventana')
        
    def evt_exit(self, widget):
        exit()
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
