import tkinter as tk
from tkinter import filedialog
import os
import vlc

class MP4PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 Player")
        self.root.geometry('800x600')
        
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        
        self.create_ui()
        
        self.log_file = "playback_times.txt"
        # Carpetas para las imágenes
        self.images_folders = {
            "images": "images",
            "senales": "senales",
            "eventos": "eventos"
        }
        # Crear las carpetas si no existen
        for folder in self.images_folders.values():
            os.makedirs(folder, exist_ok=True)
        
    def create_ui(self):
        self.load_button = tk.Button(self.root, text="Load Video", command=self.load_video)
        self.load_button.pack()
        
        self.video_frame = tk.Frame(self.root, bg='black')
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        self.root.update()
        
        # Botones de control de reproducción
        self.play_button = tk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack()
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_video)
        self.pause_button.pack()
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_video)
        self.stop_button.pack()
        
        # Botón original para registrar tiempo y captura en "images"
        self.log_time_button = tk.Button(self.root, text="Log Playback Time", command=lambda: self.log_playback_time("images"))
        self.log_time_button.pack()
        
        # Botón para registrar tiempo y captura en "senales"
        self.log_senales_button = tk.Button(self.root, text="Log Señales", command=lambda: self.log_playback_time("senales"))
        self.log_senales_button.pack()
        
        # Botón para registrar tiempo y captura en "eventos"
        self.log_eventos_button = tk.Button(self.root, text="Log Eventos", command=lambda: self.log_playback_time("eventos"))
        self.log_eventos_button.pack()

    def load_video(self):
        self.video_path = filedialog.askopenfilename(title="Select MP4 Video File", filetypes=[("MP4 files", "*.mp4")])
        if not self.video_path:
            return
        
        media = self.vlc_instance.media_new(self.video_path)
        self.player.set_media(media)
        
        win_id = self.video_frame.winfo_id()
        self.player.set_xwindow(win_id)

    def play_video(self):
        if self.player.get_media():
            self.player.play()
        
    def pause_video(self):
        self.player.pause()
        
    def stop_video(self):
        self.player.stop()
        
    def log_playback_time(self, folder):
        current_time = self.player.get_time()
        with open(self.log_file, "a") as file:
            file.write(f"{current_time}\n")
        print(f"Playback time logged: {current_time}ms in {folder}")
        
        # Tomar y guardar el screenshot en la carpeta especificada
        screenshot_path = os.path.join(self.images_folders[folder], f"screenshot_{current_time}.png")
        self.player.video_take_snapshot(0, screenshot_path, 0, 0)

# Crear la ventana principal y la aplicación
root = tk.Tk()
app = MP4PlayerApp(root)
root.mainloop()
