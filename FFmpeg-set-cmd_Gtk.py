import Modulo_Util as Util
import Modulo_Util_Gtk as Util_Gtk
import Modulo_FFmpeg as FFmpeg
import os, pathlib, subprocess

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


sys = Util.System()
cfg_file = 'FFmpeg_cfg.txt'

class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Ventana Main')
        self.set_resizable(False)
        self.set_default_size(224, 128)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Opciones - FFmpeg</b>\n')

        box_v.pack_start(label_title, True, True, 8)

        btn_ffmpeg_compress = Gtk.Button(label='Comprimir videos')
        btn_ffmpeg_compress.connect("clicked", self.evt_ffmpeg_compress)
        box_v.pack_start(btn_ffmpeg_compress, True, True, 0)
        
        btn_ffmpeg_record = Gtk.Button(label='Grabar')
        btn_ffmpeg_record.connect("clicked", self.evt_ffmpeg_record)
        box_v.pack_start(btn_ffmpeg_record, True, True, 0)
        
        btn_ffmpeg_reproduce = Gtk.Button(label='Reproducir')
        btn_ffmpeg_reproduce.connect('clicked', self.evt_ffmpeg_reproduce)
        box_v.pack_start(btn_ffmpeg_reproduce, True, True, 0)
        
        btn_txt_view = Gtk.Button(label='Ver comandos creados')
        btn_txt_view.connect("clicked", self.evt_text_view)
        box_v.pack_start(btn_txt_view, True, True, 0)

        btn_exit = Gtk.Button(label='Salir')
        btn_exit.connect("clicked", self.evt_exit)
        box_v.pack_end(btn_exit, True, True, 16)
        
        self.add(box_v)
        
    def evt_ffmpeg_compress(self, widget):
        dialog = Dialog_FFmpeg_VideoAudio(self, opc='VideoCompress')
        response = dialog.run()
        dialog.destroy()
        print('Comprimir videos')
        
    def evt_ffmpeg_record(self, widget):
        dialog = Dialog_FFmpeg_VideoAudio(self, opc='VideoRecord')
        response = dialog.run()
        dialog.destroy()
        print('Grabar Audio o video')
        
    def evt_ffmpeg_reproduce(self, widget):
        print('Reproducir Audio o Video')
        dialog = Dialog_FFmpeg_Reproduce(self)
        dialog.run()
        dialog.destroy()
        
    def evt_text_view(self, widget):
        if pathlib.Path(cfg_file).exists():
            text = Util.Text_Read(cfg_file, 'ModeText')
        else: 
            text = f'No existe el archivo de texto "{cfg_file}"'
        dialog = Util_Gtk.Dialog_TextView(self, text=text)
        response = dialog.run()
        dialog.destroy()
        print('Abrir archivo de texto')
        
    def evt_exit(self, widget):
        self.destroy() # o tambien 'exit()'


class Dialog_FFmpeg_VideoAudio(Gtk.Dialog):
    def __init__(self, parent, opc='VideoCompress'):
        self.cfg = ''
        self.opc = opc
    
        if self.opc == 'VideoCompress':
            self.txt_title = 'Comprimir Video'
            btn_path_str = 'Elegir Video'
            
        elif self.opc == 'VideoRecord':
            self.txt_title = 'Grabar Video'
            btn_path_str = 'Guardar Video como...'
            
        elif self.opc == 'AudioRecord':
            self.txt_title = 'Grabar Audio'
            btn_path_str = 'Guardar Audio como...'
            
        else: 
            self.txt_title = 'Title for else'
            btn_path_str = 'Button for else'
    
        super().__init__(title=f'{opc}', transient_for=parent, flags=0)
        self.set_default_size(352, 0)
        
        box_data = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        # Para acomodar la box/caja
        box_data.set_homogeneous(False)
        box_data.set_property("expand", True)
        box_data.set_property("halign", Gtk.Align.CENTER)
        
        label_title = Gtk.Label()
        label_title.set_markup(f'<big><b>{self.txt_title}</b></big>\n')
        box_data.pack_start(label_title, True, True, 8)

        btn_path = Gtk.Button(label=btn_path_str)
        btn_path.connect("clicked", self.evt_path)
        box_data.pack_start(btn_path, True, True, 0)
        self.pth = ''

        if (
            self.opc == 'VideoRecord' or
            self.opc == 'VideoCompress'
        ):
            crf_box = Gtk.Box(spacing=4)
            box_data.pack_start(crf_box, True, True, 0)

            self.crf_CheckButton = Gtk.CheckButton(label='Calidad (CRF de 0-50)')
            self.crf_CheckButton.set_active(True)
            crf_box.pack_start(self.crf_CheckButton, False, False, 0)

            crf_SpinButton_adj = Gtk.Adjustment(
                                    upper=50, step_increment=1, 
                                    page_increment=10, 
                                    value=30
                                 )
            self.crf_SpinButton = Gtk.SpinButton()
            self.crf_SpinButton.set_adjustment(crf_SpinButton_adj)
            self.crf_SpinButton.set_numeric(True)
            crf_box.pack_start(self.crf_SpinButton, False, False, 8)
        

            fps_box = Gtk.Box(spacing=4)
            box_data.pack_start(fps_box, True, True, 0)
        
            self.fps_CheckButton = Gtk.CheckButton(label='Fotogramas (FPS)')
            self.fps_CheckButton.set_active(True)
            fps_box.pack_start(self.fps_CheckButton, False, False, 0)
        
            self.fps_SpinButton = Gtk.SpinButton()
            fps_SpinButton_adj = Gtk.Adjustment(
            step_increment=1, page_increment=10
            )
            self.fps_SpinButton.set_adjustment(fps_SpinButton_adj)
            self.fps_SpinButton.set_range(1, 100)
            self.fps_SpinButton.set_value(25)
            self.fps_SpinButton.set_numeric(True)
            fps_box.pack_start(self.fps_SpinButton, False, False, 34)
        
        
            rez_box = Gtk.Box(spacing=4)
            box_data.pack_start(rez_box, True, True, 0)
        
            self.rez_CheckButton = Gtk.CheckButton(label='Resolucion (H x V)')
            self.rez_CheckButton.set_active(True)
            rez_box.pack_start(self.rez_CheckButton, False, False, 0)
        
            self.rez_entryH = Gtk.Entry()
            self.rez_entryH.set_text('1280')
            self.rez_entryH.set_width_chars(8)
            rez_box.pack_start(self.rez_entryH, False, False, 0)
        
            rez_label_HxV = Gtk.Label(label='x')
            rez_box.pack_start(rez_label_HxV, False, False, 0)
        
            self.rez_entryV = Gtk.Entry()
            self.rez_entryV.set_text('720')
            self.rez_entryV.set_width_chars(8)
            rez_box.pack_start(self.rez_entryV, False, False, 0)
        else: pass
        
        # Zona de preset
        if self.opc == 'VideoRecord':
            preset_box = Gtk.Box(spacing=4)
            box_data.pack_start(preset_box, True, True, 0)
            
            self.preset_CheckButton = Gtk.CheckButton(label='Uso de CPU')
            self.preset_CheckButton.set_active(True)
            preset_box.pack_start(self.preset_CheckButton, False, False, 0)
            
            preset_ListStore = Gtk.ListStore(str)
            presets = [
                '-preset ultrafast',
                '-preset superfast',
                '-preset veryfast',
                '-preset faster',
                '-preset fast',
                '-preset medium',
                '-preset slow',
                '-preset slower',
                '-preset veryslow',
            ]
            for preset in presets:
                preset_ListStore.append([preset])
                
            self.preset_ComboBox = Gtk.ComboBox.new_with_model(preset_ListStore)
            preset_CellRendererText = Gtk.CellRendererText()
            self.preset_ComboBox.pack_start(preset_CellRendererText, True)
            self.preset_ComboBox.add_attribute(preset_CellRendererText, "text", 0)
            self.preset_ComboBox.set_active(5)
            preset_box.pack_start(self.preset_ComboBox, False, False, 44)
        else: pass
            
        # Zona de Audio
        if (
            self.opc == 'VideoRecord' or
            self.opc == 'AudioRecord'
        ):
            audio_box = Gtk.Box(spacing=0)
            box_data.pack_start(audio_box, True, True, 0)
            
            self.audio_CheckButton = Gtk.CheckButton(label='Audio')
            self.audio_CheckButton.connect('toggled', self.evt_audio)

            if self.opc == 'VideoRecord':
                self.audio_CheckButton.set_active(False)
            else:
                self.audio_CheckButton.set_active(True)

            audio_box.pack_start(self.audio_CheckButton, False, False, 0)
            
            self.audio_Entry = Gtk.Entry()
            self.audio_Entry.set_width_chars(8)
            #self.audio_Entry.set_placeholder('Audio')
            audio_box.pack_start(self.audio_Entry, False, False, 86)
        else: pass
        
        
        self.label_path = Gtk.Label()
        self.label_path.set_markup('<b>(Aqui se mostrara el Video/Audio)</b>')
        self.label_path.set_line_wrap(True)
        box_data.pack_start(self.label_path, True, True, 0)
        
        self.label_cfg = Gtk.Label()
        self.label_cfg.set_line_wrap(True)
        self.label_cfg.set_selectable(True)
        box_data.pack_start(self.label_cfg, True, True, 0)
        
        if (
            self.opc == 'VideoRecord' or
            self.opc == 'AudioRecord'
        ):
            if self.opc == 'VideoRecord':
                recordmode_txt = 'MODO Grabar solo Audio'
            elif self.opc == 'AudioRecord':
                recordmode_txt = 'MODO Grabar solo Video'
            recordmode_btn = Gtk.Button(label=recordmode_txt)
            recordmode_btn.connect('clicked', self.evt_recordmode)
            box_data.pack_start(recordmode_btn, True, True, 0)
        else: pass
        
        add_cfg_btn = Gtk.Button(label=self.txt_title)
        add_cfg_btn.connect('clicked', self.evt_add_cfg)
        box_data.pack_end(add_cfg_btn, True, True, 0)
        
        box_main = self.get_content_area()
        box_main.add(box_data)
        self.show_all()
        
    def evt_recordmode(self, widget):
        self.destroy()
        if self.opc == 'VideoRecord':
            dialog = Dialog_FFmpeg_VideoAudio(self, opc='AudioRecord')
            response = dialog.run()
            dialog.destroy()
        elif self.opc == 'AudioRecord':
            dialog = Dialog_FFmpeg_VideoAudio(self, opc='VideoRecord')
            response = dialog.run()
            dialog.destroy()
        else: pass
        
    def evt_audio(self, widget):
        if self.audio_CheckButton.get_active() == True:
            if (
                sys == 'linux' or
                sys == 'win'
            ):
                if sys == 'linux':
                    cmd = 'pactl list short sources'
                elif sys == 'win':
                    cmd = 'ffmpeg -list_devices true -f dshow -i dummy'
                dialog = Util_Gtk.Dialog_TextView(
                             self,
                             text=(
                                 'Para ver los dispositivos de audio.\n'
                                 'Ejecuta este comando en terminal/consola.\n\n'
                                 f'Comando: {cmd}'
                             )
                         )
                response = dialog.run()
                dialog.destroy()
        
    def evt_add_cfg(self, widget):
        Util.CleanScreen()
        
        crf, fps, rez_HxV = '', '', ''
        if (
            self.opc == 'VideoCompress' or
            self.opc == 'VideoRecord'
        ):
            if self.crf_CheckButton.get_active() == True:
                crf = FFmpeg.CRF(self.crf_SpinButton.get_value_as_int())
            else: pass
            
            if self.fps_CheckButton.get_active() == True:
                fps = FFmpeg.FPS(self.fps_SpinButton.get_value_as_int())
            else: pass
            
            if self.rez_CheckButton.get_active() == True:
                rez_HxV = FFmpeg.Resolution(
                    rez_H=self.rez_entryH.get_text(), 
                    rez_V=self.rez_entryV.get_text()
                )
            else: pass
        else: pass
        
        preset = ''
        if self.opc == 'VideoRecord':
            if self.preset_CheckButton.get_active() == True:
                preset_iter = self.preset_ComboBox.get_active_iter()
                preset_model = self.preset_ComboBox.get_model()
                preset = preset_model[preset_iter][0]
            else: pass
        else: pass

        audio = ''
        if (
            self.opc == 'VideoRecord' or
            self.opc == 'AudioRecord'
        ):
            if self.audio_CheckButton.get_active() == True:
                audio = FFmpeg.Audio(self.audio_Entry.get_text())
            else: 
                if self.opc == 'AudioRecord':
                    audio = FFmpeg.Audio()
                else:
                    audio = ''
        else: pass
        
        # Zona de Ruta de Archivo
        if self.pth == '':
            print('No se a establecido el Video/Audio')
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text='No se a establecido el Video/Audio'
            )
            dialog.format_secondary_text(
                'Selecciona aceptar para continuar'
            )
            dialog.run()
            dialog.destroy()
            
        else:
            print(
                f'Audio/Video : "{self.pth}"\n'
                f'CRF: "{crf}"\n'
                f'FPS: "{fps}"\n'
                f'Resolución: "{rez_HxV}"\n'
                f'Preset: "{preset}"\n'
                f'Audio: "{audio}"'
            )
            
            if self.opc == 'VideoCompress':
                self.cfg = (
                    f'ffmpeg -i "{self.pth}" {crf} {fps} {rez_HxV} '
                    f'"{self.pth}_Comprimido.mkv"'
                )
            elif self.opc == 'VideoRecord':
                if self.fps_CheckButton.get_active() == False:
                    fps = FFmpeg.FPS(10)
                self.cfg = (
                    f'ffmpeg {FFmpeg.Desktop_Render()} '
                    f'{audio} {crf} {preset} {fps} '
                    f'{rez_HxV} "{self.pth}.mkv"'
                )
                txt=''
            elif self.opc == 'AudioRecord':
                self.cfg = f'ffmpeg {audio} "{self.pth}.ogg"'
            
            self.label_cfg.set_markup(
                f'<small><i>{self.cfg}</i></small>'
            )
            
            # Ejecutar comando
            dialog = Util_Gtk.Dialog_Command_Run(
                self, cfg=self.cfg, txt=self.txt_title, cfg_file=cfg_file
            )
            dialog.run()
            dialog.destroy()
            #dialog = Gtk.MessageDialog(
            #    transient_for=self,
            #    flags=0,
            #    message_type=Gtk.MessageType.QUESTION,
            #    buttons=Gtk.ButtonsType.YES_NO,
            #    text=self.txt_title
            #)
            #dialog.format_secondary_text(self.cfg)
            #rsp = dialog.run()
            #if rsp == Gtk.ResponseType.YES:
            #    os.system(f"xfce4-terminal --startup-id= -e '{self.cfg}'")
            #elif rsp == Gtk.ResponseType.NO:
            #    print('NO Precionado')
            #dialog.destroy()
        
            
    def evt_path(self, widget):
        if (
            self.opc == 'VideoRecord' or
            self. opc == 'AudioRecord'
        ):
            dialog = Gtk.FileChooserDialog(
                parent=self,
                action=Gtk.FileChooserAction.SAVE
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
            )
        elif self.opc == 'VideoCompress':    
            dialog = Gtk.FileChooserDialog(
                title='Selecciona un Video', parent=self,
                action=Gtk.FileChooserAction.OPEN
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            )
        
        self.add_flt(dialog)
            
        rsp = dialog.run()
        if rsp == Gtk.ResponseType.OK:
            self.pth = dialog.get_filename()
            self.label_path.set_text(f'Archivo: {self.pth}')
            print('Audio/Video Agregado')
            
        elif rsp == Gtk.ResponseType.CANCEL:
            self.cfg = ''
            print('Cancelar clickeado')
            
        dialog.destroy()
        
    def add_flt(self, dialog):
        flt_video = Gtk.FileFilter()
        flt_video.set_name("Archivos de Video")
        flt_video.add_mime_type("video/*")
        dialog.add_filter(flt_video)
        

class Dialog_FFmpeg_Reproduce(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='FFmpeg Reproduce', transient_for=parent, flags=0)
        self.set_default_size(512, 256)
        #self.set_border_width(4) # Poner un margen a la ventana
        
        notebook = Gtk.Notebook() # Contenedor de Pestañas
        
        # Pestaña 1
        page_archive = Gtk.Box() # Pestaña
        page_archive.set_border_width(8) # Poner margen en la pestaña
        notebook.append_page(
            page_archive, Gtk.Label(label='Reproducir Archivo - Audio/Video')
        )
        
        button_archive = Gtk.Button(label='Seleccionar archivo')
        button_archive.connect('clicked', self.evt_set_archive)
        page_archive.pack_start(button_archive, True, True, 0)
        
        # Pestaña 2
        page_audio = Gtk.Box()
        page_audio.set_border_width(8)
        notebook.append_page(
            page_audio, Gtk.Label(label='Reproducir Dispositivo de Audio')
        )
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_property('expand', True)
        page_audio.add(vbox)
        
        audio_cmd = (
            subprocess.check_output(
                FFmpeg.Command("Audio"), shell=True, text=True
            )
        )
        label_audio_cmd = Gtk.Label()
        label_audio_cmd.set_markup(
            '<b>Comando para ver dispositivos de audio:\n</b>'
            f'"{FFmpeg.Command("Audio")}"\n\n'
            '\n'
            f'<b>{FFmpeg.Message("Audio")}\n</b>'
            f'<small><i>{audio_cmd}</i></small>'
        )
        label_audio_cmd.set_line_wrap(True)
        #label_audio_cmd.set_max_chars(0)
        label_audio_cmd.set_selectable(True)
        vbox.pack_start(label_audio_cmd, True, True, 0)
        
        hbox = Gtk.Box(spacing=4)
        vbox.pack_start(hbox, True, True, 0)
        
        label_audio = Gtk.Label(label='Audio')
        hbox.pack_start(label_audio, False, True, 0)
        
        self.entry_audio = Gtk.Entry()
        self.entry_audio.set_placeholder_text('Audio - Dispositivo')
        hbox.pack_start(self.entry_audio, False, True, 8)
        
        button_audio = Gtk.Button(label='Reproducir Audio')
        button_audio.connect('clicked', self.evt_set_audio)
        vbox.pack_end(button_audio, True, True, 16)
        
        # Para mostrar los widgets
        self.get_content_area().add(notebook)
        self.show_all()
        
    def evt_set_archive(self, button):
        dialog = Gtk.FileChooserDialog(
            title='Selecciona un Video/Audio', parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_flt(dialog)
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            dialog_cmd = Util_Gtk.Dialog_Command_Run(
                self,
                cfg = (
                    'ffplay -i '
                    f'"{dialog.get_filename()}" '
                ),
                cfg_file = cfg_file
            )
            dialog_cmd.run()
            dialog_cmd.destroy()
            
        elif response == Gtk.ResponseType.CANCEL:
            pass
            
        dialog.destroy()
        
    def evt_set_audio(self, widget):
        if self.entry_audio.get_text() == '':
            pass
        else:
            dialog = Util_Gtk.Dialog_Command_Run(
                self,
                cfg = (
                    'ffplay ' +
                    FFmpeg.Audio( self.entry_audio.get_text() )
                ),
                cfg_file = cfg_file
            )
            dialog.run()
            dialog.destroy()
        
    def add_flt(self, dialog):
        flt_video = Gtk.FileFilter()
        flt_video.set_name("Archivos de Video")
        flt_video.add_mime_type("video/*")
        flt_video.add_mime_type("audio/*")
        dialog.add_filter(flt_video)
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()