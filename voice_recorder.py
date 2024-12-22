import pyaudio
import wave
import os
import whisper
import torch
import numpy as np
import threading
from datetime import datetime

class VoiceRecorder:
    def __init__(self):
        # Ses kayıt parametreleri
        self.chunk = 2048
        self.format = pyaudio.paFloat32
        self.channels = 1
        self.rate = 44100
        
        # Dizinleri oluştur
        self.audio_dir = "audio_files/recordings"
        self.output_dir = "converted_text"
        
        for directory in [self.audio_dir, self.output_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Dosya yolları
        self.recording_path = os.path.join(self.audio_dir, "recording.wav")
        self.transcript_path = os.path.join(self.output_dir, "transcription.txt")
        
        # PyAudio nesnesi
        self.p = pyaudio.PyAudio()
        
        # Whisper modelini yükle
        print("Whisper modeli yükleniyor...")
        self.model = whisper.load_model("medium")
        print("Model hazır!")
        
        # Kayıt durumu
        self.is_recording = False
        self.frames = []

        # Başlangıçta temizlik yap
        self.cleanup_temp_files()

    def cleanup_temp_files(self):
        """Geçici dosyaları temizle"""
        try:
            if os.path.exists(self.recording_path):
                os.remove(self.recording_path)
            if os.path.exists(self.transcript_path):
                os.remove(self.transcript_path)
        except Exception as e:
            print(f"Temizlik hatası: {str(e)}")

    def start_recording(self):
        """Kayıt başlatma"""
        try:
            self.cleanup_temp_files()
            self.frames = []
            self.is_recording = True
            
            # Ses akışını başlat
            self.stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index=None
            )
            
            print("Kayıt başladı - konuşabilirsiniz...")
            
            # Kayıt işlemini ayrı thread'de başlat
            self._record()
                
        except Exception as e:
            print(f"Kayıt sırasında bir sorun oluştu: {str(e)}")
            self.is_recording = False

    def _record(self):
        """Sürekli kayıt yapan iç fonksiyon"""
        try:
            if self.is_recording and hasattr(self, 'stream'):
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
                # 10ms sonra tekrar çağır
                threading.Timer(0.01, self._record).start()
        except Exception as e:
            print(f"Kayıt döngüsü hatası: {str(e)}")
            self.is_recording = False

    def stop_recording(self):
        """Kaydı durdur ve yazıya çevir"""
        try:
            print("Kayıt durduruluyor...")
            self.is_recording = False
            
            if hasattr(self, 'stream'):
                self.stream.stop_stream()
                self.stream.close()
            
            if self.frames:
                # Ses verilerini WAV formatına çevir
                audio_data = np.frombuffer(b''.join(self.frames), dtype=np.float32)
                audio_data = (audio_data * 32767).astype(np.int16)
                
                with wave.open(self.recording_path, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(2)
                    wf.setframerate(self.rate)
                    wf.writeframes(audio_data.tobytes())
                
                print("Yazıya çevirme başladı...")
                result = self.model.transcribe(
                    self.recording_path,
                    language="tr",
                    task="transcribe",
                    temperature=0.2,
                    best_of=3,
                    beam_size=5,
                    fp16=torch.cuda.is_available(),
                    initial_prompt="Bu bir hukuki metindir.",
                    condition_on_previous_text=True,
                    compression_ratio_threshold=2.4,
                    no_speech_threshold=0.6
                )
                
                transcribed_text = result["text"].strip()
                with open(self.transcript_path, 'w', encoding='utf-8') as f:
                    f.write(transcribed_text)
                
                print(f"Yazıya çevirme tamamlandı!")
                return transcribed_text
            
        except Exception as e:
            print(f"İşlem hatası: {str(e)}")
            return None
        
        finally:
            self.frames = []

    def __del__(self):
        """Temizlik işlemleri"""
        try:
            if hasattr(self, 'stream'):
                self.stream.stop_stream()
                self.stream.close()
            self.p.terminate()
            self.cleanup_temp_files()
        except:
            pass