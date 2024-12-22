# Sesli Konuşma - Metin Dönüştürücü
Bu Python uygulaması, sesli konuşmaları gerçek zamanlı olarak yazıya dönüştüren bir araçtır. OpenAI'nin Whisper modelini kullanarak yüksek doğrulukta transkripsiyon sağlar.
## Özellikler
- 🎤 Gerçek zamanlı ses kaydı
 📝 Türkçe dil desteği
 💻 Kullanıcı dostu arayüz
 📄 Word belgesi olarak dışa aktarma
 🔍 Yüksek doğruluk oranı
 🚀 Orta boy Whisper modeli ile optimum performans
## Gereksinimler
- Python 3.8 veya üzeri
 FFmpeg
 Mikrofon
 PyAudio ve bağımlılıkları
## Kurulum
1. Repoyu klonlayın:
bash
git clone [repo-url]
cd ses-metin-donusturucu
2. Virtual environment oluşturun:
bash
Windows
python -m venv venv
.\venv\Scripts\activate
Linux/macOS
python3 -m venv venv
source venv/bin/activate
3. Gerekli kütüphaneleri yükleyin:
bash
pip install -r requirements.txt
4. FFmpeg kurulumu:
bash
Windows
winget install ffmpeg
Linux
sudo apt install ffmpeg
macOS
brew install ffmpeg

## Kullanım

1. Uygulamayı başlatın:
 bash
python main.py

2. Ana pencerede:
   - "Kayda Başla" butonuna tıklayın
   - Konuşmanızı yapın
   - "Kaydı Durdur" ile kaydı bitirin
   - Dönüştürülen metni kontrol edin
   - İsterseniz "Word'e Aktar" ile kaydedin

## Sorun Giderme

### PyAudio Kurulum Sorunları

Windows için:
bash
pip install pipwin
pipwin install pyaudio

Linux için:
bash
sudo apt-get install python3-pyaudio
veya
sudo apt-get install portaudio19-dev python3-pyaudio

macOS için:
bash
brew install portaudio
pip install pyaudio

## Notlar

- İlk çalıştırmada Whisper modeli (yaklaşık 1.5GB) otomatik indirilecektir
- Yüksek kaliteli mikrofon kullanımı, daha iyi sonuçlar sağlar
- Sessiz bir ortamda kullanım önerilir
- Model orta boy (medium) olarak ayarlanmıştır - hız ve doğruluk dengesi için

## Teknik Detaylar

- Whisper AI modeli kullanılmaktadır
- Threading ile performans optimizasyonu yapılmıştır
- 44.1kHz ses örnekleme hızı
- 32-bit float ses formatı
- Mono kanal kayıt

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
