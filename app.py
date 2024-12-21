"""
 import tkinter as tk
import sounddevice as sd
import numpy as np
import wave
import threading
import whisper
import os
import torch

class VoiceRecorderApp:
    def __init__(self, master): 
        self.master = master
        self.master.title("Ses Kayıt ve Dönüştürme Uygulaması")

        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 44100  # Örnekleme hızı
        self.main_path = os.getcwd()
        self.x_path = os.path.join(self.main_path, "kayit.wav")
        self.audio_file_path = r"D:\\CODE\\sestenyaziya\\kayit.wav"
        

        # Whisper modelini yükle
        self.model = whisper.load_model("large")

        # GPU desteği var mı kontrol et
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cpu":
            print("Uyarı: GPU kullanılamıyor, işlem CPU'da yapılacak.")

        # Butonlar
        self.start_button = tk.Button(master, text="Kayda Başla", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Kaydı Bitir", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=10)

        self.transcribe_button = tk.Button(master, text="Yazıya Çevir", command=self.transcribe_audio, state="disabled")
        self.transcribe_button.pack(pady=10)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.audio_data = []  # Yeni bir kayıt için önceki veriyi temizle
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.transcribe_button.config(state="disabled")

            # Ses kaydetme işlevini ayrı bir thread'de başlatıyoruz.
            self.record_thread = threading.Thread(target=self.record)
            self.record_thread.start()

    def record(self):
        def callback(indata, frames, time, status):
            if self.is_recording:
                self.audio_data.append(indata.copy())

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=callback):
                while self.is_recording:
                    sd.sleep(100)
        except Exception as e:
            print(f"Ses kaydı sırasında bir hata oluştu: {str(e)}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.transcribe_button.config(state="normal")

            # Thread'i güvenli bir şekilde kapat
            if self.record_thread.is_alive():
                self.record_thread.join()

            # Kaydedilen veriyi WAV dosyasına kaydediyoruz
            self.save_audio()

    def save_audio(self):
        if self.audio_data:
            try:
                audio_data = np.concatenate(self.audio_data, axis=0)
                # PCM formatına dönüştürme
                audio_data = (audio_data * 32767).astype(np.int16)

                with wave.open(self.x_path, 'w') as wf:
                    wf.setnchannels(1)  # Tek kanal (mono)
                    wf.setsampwidth(2)  # Örnek başına 2 byte (16 bit)
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(audio_data.tobytes())
                print(f"Ses dosyası kaydedildi: {self.audio_file_path}")
            except Exception as e:
                print(f"Ses dosyasını kaydederken hata oluştu: {str(e)}")

    def transcribe_audio(self):
        try:
            print("Ses dosyası yolu:", self.audio_file_path)
            if os.path.exists(self.x_path):
                result = self.model.transcribe(self.x_path, fp16=True)  # GPU kullanıyorsanız fp16=True
                print("Metne Dönüşüm Tamamlandı:")
                print(result['text'])
            else:
                print(f"Ses dosyası bulunamadı! Lütfen dosya yolunu kontrol edin: {self.audio_file_path}")
        except Exception as e:
            print(f"Metne dönüştürme sırasında bir hata oluştu: {str(e)}")



root = tk.Tk()
app = VoiceRecorderApp(root)
root.mainloop()
"""