import torch
import numpy as np
import whisper
import torch
import os
import gc
from legal_dictionary import LEGAL_TERMS
import re

class Transcriber:
    def __init__(self):
        try:
            # Belleği temizle
            torch.cuda.empty_cache()
            gc.collect()
            
            # GPU kontrolü
            if torch.cuda.is_available():
                self.device = "cuda"
                torch.cuda.set_per_process_memory_fraction(0.7)
            else:
                self.device = "cpu"
                
            print(f"Kullanılan cihaz: {self.device}")
            
            # Small model yükle
            self.model = whisper.load_model("small").to(self.device)
            print("Small Whisper modeli başarıyla yüklendi.")
            
            self.legal_terms = LEGAL_TERMS

        except Exception as e:
            print(f"Model yükleme hatası: {str(e)}")
            self.device = "cpu"
            self.model = whisper.load_model("small")
            print("Model CPU üzerinde yüklendi.")

    def post_process_legal_text(self, text):
        """Metni hukuki terimler açısından düzeltir"""
        processed_text = text
        
        # Hukuki terimleri kontrol et ve düzelt
        for term in self.legal_terms:
            # Büyük/küçük harf duyarsız arama yap
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            processed_text = pattern.sub(self.legal_terms[term], processed_text)
        
        return processed_text

    def format_legal_document(self, text):
        """Metni hukuki belge formatına dönüştürür"""
        # Tarih formatını düzelt (örn: 01/01/2024)
        date_pattern = r'\d{1,2}/\d{1,2}/\d{4}'
        
        # Paragrafları düzenle
        paragraphs = text.split('\n')
        formatted_text = ""
        
        for paragraph in paragraphs:
            # Boş paragrafları atla
            if not paragraph.strip():
                continue
                
            # Paragrafa numara ekle
            formatted_text += f"- {paragraph.strip()}\n\n"
        
        return formatted_text

    def transcribe_audio_using_cuda(self, audio_path):
        """Ses kaydını metne dönüştürür ve hukuki formata çevirir"""
        try:
            if self.device == "cuda":
                torch.cuda.empty_cache()
                gc.collect()
            
            # Transkripsiyon yap
            result = self.model.transcribe(
                audio_path,
                language="tr",
                fp16=False
            )
            
            # Ham metni al
            raw_text = result["text"]
            
            # Hukuki terimleri düzelt
            processed_text = self.post_process_legal_text(raw_text)
            
            # Hukuki formata dönüştür
            formatted_text = self.format_legal_document(processed_text)
            
            if self.device == "cuda":
                torch.cuda.empty_cache()
                gc.collect()
            
            return formatted_text

        except Exception as e:
            print(f"Transcription Error: {str(e)}")
            return None

    def __del__(self):
        try:
            del self.model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
        except:
            pass
