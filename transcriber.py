import torch
import numpy as np
import librosa
import whisper
import os

class Transcriber:
    def __init__(self):
        # Cihazı seç (GPU varsa kullan, yoksa CPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = whisper.load_model("small").to(self.device)  # Whisper modelini CUDA'ya yükleyelim
        

    def transcribe_audio_using_cuda(self, audio_path):
        """Ses kaydını CUDA ile hızlandırarak metne dönüştürür ve txt dosyasına kaydeder."""
        try:
            # Ses verisini yükle
            audio_data = self.load_audio_data(audio_path)
            if audio_data is None:
                return None

            # Whisper ile ses verisini metne dönüştürme
            result = self.transcribe_with_whisper(audio_data)

            # Çıkan metni terminalde göster ve dosyaya kaydet
            if result:
                print(f"Transcription: {result}")
                self.save_to_file(result)
            return result

        except Exception as e:
            print(f"CUDA Error: {str(e)}")
            return None

    def load_audio_data(self, audio_path):
        """Ses verisini yükleme (Örneğin bir wav dosyası)"""
        try:
            # Librosa ile ses verisini yükleyelim
            audio_data, sr = librosa.load(audio_path, sr=16000)  # 16kHz örnekleme hızı ile yükleme
            return audio_data
        except Exception as e:
            print(f"Error loading audio file: {str(e)}")
            return None

    def transcribe_with_whisper(self, audio_data):
        """CUDA üzerinde Whisper modelini kullanarak ses verisini metne dönüştürür"""
        try:
            # Ses verisini Whisper modeline verip metni alalım (Türkçe dilinde transkripte et)
            result = self.model.transcribe(audio_data, language="tr")
            return result["text"]
        except Exception as e:
            print(f"Error transcribing audio with Whisper: {str(e)}")
            return None
        
    def save_to_file(self, text):
        """Metni txt dosyasına kaydeder."""
        try:
            # Klasörün varlığını kontrol et, yoksa oluştur
            output_dir = "converted_text"
            os.makedirs(output_dir, exist_ok=True)

            # Dosya yolunu oluştur
            output_file = os.path.join(output_dir, "transcription.txt")

            # Metni dosyaya yaz
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(text)

            print(f"Transcription saved to {output_file}")
        except Exception as e:
            print(f"Error saving transcription to file: {str(e)}")
