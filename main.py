import tkinter as tk
from tkinter import messagebox
import threading
from voice_recorder import VoiceRecorder
from transcriber import Transcriber


class VoiceRecordingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recording and Transcription")
        self.root.geometry("600x400")

        self.recorder = VoiceRecorder()
        self.transcriber = Transcriber()

        # Ses Kaydını Başlat Butonu
        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        # Ses Kaydını Durdur Butonu
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Yazıya Çevir Butonu
        self.convert_button = tk.Button(self.root, text="Convert to Text", command=self.convert_to_text, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        # Text Alanı (Dönüştürülen metnin görüntüleneceği alan)
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=20)

        # Kayıt Durumu (Thread kontrolü için)
        self.is_recording = False

    def start_recording(self):
        """Ses kaydını başlatır."""
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)  # Kaydı başlatınca butonu devre dışı bırak
        self.stop_button.config(state=tk.NORMAL)    # Durdu butonunu aktif et
        threading.Thread(target=self.record_audio).start()  # Kaydı bir iş parçacığında başlat

    def record_audio(self):
        """Ses kaydını başlatma işlemini ayrı bir iş parçacığında yap."""
        try:
            self.recorder.start_recording()  # Ses kaydını başlat
            while self.is_recording:  # Kullanıcı durdurana kadar kayıt devam eder
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Recording error: {e}")

    def stop_recording(self):
        """Ses kaydını durdurur ve kaydedilen dosyayı kaydeder."""
        self.is_recording = False
        try:
            self.recorder.stop_recording()
            self.stop_button.config(state=tk.DISABLED)  # Kaydettikten sonra durdur butonunu devre dışı bırak
            self.convert_button.config(state=tk.NORMAL)  # Çevir butonunu aktif et
        except Exception as e:
            messagebox.showerror("Error", f"Stop recording error: {e}")

    def convert_to_text(self):
        """Ses kaydını metne dönüştürür ve metni Text alanına yazar."""
        threading.Thread(target=self.run_conversion).start()  # Arka planda dönüşümü başlat

    def run_conversion(self):
        """CUDA ile hızlandırılmış dönüşüm işlemi."""
        try:
            # Ses kaydının yolu
            audio_path = "audio_files/recordings/recording.wav"
            transcription = self.transcriber.transcribe_audio_using_cuda(audio_path)  # CUDA ile dönüşüm

            print(f"Transkripsiyon: {transcription}")  # Debug için terminalde göster

            if transcription:
                self.root.after(0, lambda: self.update_text_area(transcription))  # Arayüzü güncelle
            else:
                self.root.after(0, lambda: messagebox.showwarning("Warning", "No speech detected."))
        except Exception as e:
            print(f"Transcription error: {e}")  # Hata durumunda terminalde göster
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))

    def update_text_area(self, text):
        """Text alanını günceller."""
        self.text_area.delete(1.0, tk.END)  # Mevcut metni temizle
        self.text_area.insert(tk.END, text)  # Yeni metni ekle


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecordingApp(root)
    root.mainloop()
