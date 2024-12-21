import torch
import wave
import os
from pydub import AudioSegment
import pyaudio

class VoiceRecorder:
    def __init__(self, output_dir="audio_files/recordings"):
        self.output_dir = output_dir
        self.create_output_dir()
        self.frames = []
        self.is_recording = False
        self.filename = "recording.wav"
        self.p = pyaudio.PyAudio()

    def create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def start_recording(self):
        self.frames = []
        self.is_recording = True
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,  # 44.1kHz örnekleme hızı
                                  input=True,
                                  frames_per_buffer=1024)
        print("Recording started...")
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        print("Recording stopped.")
        self.save_audio()

    def save_audio(self):
        file_path = os.path.join(self.output_dir, self.filename)
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
        print(f"Audio saved to {file_path}")
        
        # Kaydedilen ses dosyasını 16kHz'ye dönüştürme
        converted_file_path = os.path.join(self.output_dir, "converted_16kHz.wav")
        self.convert_to_16kHz(file_path, converted_file_path)

        # Transkripte etme
        self.transcribe_audio(converted_file_path)

    def convert_to_16kHz(self, input_path, output_path):
        # Ses dosyasını 16kHz'e dönüştür
        audio = AudioSegment.from_wav(input_path)
        audio = audio.set_frame_rate(16000)
        audio.export(output_path, format="wav")
        print(f"Audio converted to 16kHz and saved to {output_path}")

