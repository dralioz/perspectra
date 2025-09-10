# Perspectra API

Perspectra API, görüntü işleme ve perspektif düzeltme işlemlerini gerçekleştiren bir FastAPI tabanlı web servisidir. Bu API, yüklenen görüntülerin arka planını kaldırır ve perspektif dönüşümü uygulayarak yukarıdan bakış görünümü elde eder.

## 🎯 Proje Amacı

Perspectra API'nin temel amacı:
- Görüntülerden arka planı kaldırmak
- Nesnenin dört köşesini tespit ederek perspektif düzeltmesi yapmak
- Yukarıdan bakış (top-view) perspektifine dönüştürme
- Kimlik belgesi, döküman veya dikdörtgen nesnelerin düzeltilmiş görüntülerini elde etme

## ✨ Özellikler

- **Arka Plan Kaldırma**: AI tabanlı U2Net modeli kullanarak yüksek kaliteli arka plan kaldırma
- **Perspektif Düzeltme**: Otomatik köşe tespiti ve perspektif dönüşümü
- **RESTful API**: FastAPI ile modern ve hızlı API
- **Docker Desteği**: Kolay deployment ve geliştirme ortamı
- **Logging**: Detaylı loglama ve hata takibi
- **Debug Modu**: Geliştirme sırasında debug desteği
- **CORS Desteği**: Cross-origin istekler için tam destek
- **Base64 Çıktı**: İşlenmiş görüntüleri Base64 formatında döndürme

## 🛠️ Teknoloji Stack

- **Framework**: FastAPI
- **Görüntü İşleme**: OpenCV, PIL (Pillow)
- **AI Model**: rembg (U2Net)
- **Yapılandırma**: Pydantic Settings
- **Container**: Docker & Docker Compose
- **Python**: 3.11+

## 📦 Gereksinimler

- Python 3.11+
- Conda (önerilen) veya Python venv
- Docker (opsiyonel)
- Git

### Python Kütüphaneleri

```txt
fastapi==0.116.1
uvicorn==0.35.0
pydantic==2.11.7
pydantic-settings==2.10.1
pillow==11.3.0
opencv-python==4.12.0.88
rembg==2.0.67
onnxruntime==1.22.1
python-multipart==0.0.20
ecs-logging==2.2.0
```

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/dralioz/perspectra-api.git
cd perspectra-api
```

### 2. Python Ortamını Hazırlayın (Conda ile)

```bash
# Conda environment oluşturun
conda env create -f conda.yaml

# Environment'ı aktive edin
conda activate perspectra

# Bağımlılıkları yükleyin (uv ile hızlı kurulum)
uv pip install -r requirements.txt --system
uv pip install -e . --system
```

**Alternatif olarak pip ile:**

```bash
# Virtual environment oluşturun
python -m venv venv

# Virtual environment'ı aktive edin
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
pip install -e .
```

### 3. Konfigürasyon

`.env.dev` dosyası oluşturun ve gerekli ayarları yapın:

```env
APP_NAME=Perspectra API
PADDING_RATIO=0.05
ENABLE_URL_FETCH=false
IS_ONLY_MASK=true

# Perspektif dönüşüm ayarları
SAVE_CONTOURS=true
CONTOURS_PATH=./debug
SAVE_TRANSFORMED=true

# Model ayarları
USE_LOCAL_MODEL=true
MODEL_URL=https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
MODEL_FILENAME=u2net.onnx

# ONNX Runtime ayarları
ORT_NUM_THREADS=4
ORT_ENABLE_CPU_MEM_ARENA=1
ORT_ENABLE_MEM_PATTERN=1
ORT_ENABLE_PARALLEL_EXECUTION=1
ORT_INTRA_OP_NUM_THREADS=4
ORT_INTER_OP_NUM_THREADS=2
ORT_EXECUTION_MODE=PARALLEL
ORT_GRAPH_OPT_LEVEL=ALL
```

### 4. Uygulamayı Çalıştırın

```bash
# Doğrudan Python ile
python src/main.py

# veya uvicorn ile
uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload
```

## 🐳 Docker ile Kurulum

### Production Modu

```bash
# Docker image'ını build edin
make docker-build

# Uygulamayı çalıştırın
docker run -p 5000:5000 perspectra-api:1.0.0
```

### Development/Debug Modu

```bash
# Debug modunda başlatın
make start-debug

# Logları takip edin
make tail-logs

# Durdurın
make down-debug
```

## 📖 API Kullanımı

### Base URL
```
http://localhost:5000
```

### Swagger UI
API dokümantasyonuna şu adresten erişebilirsiniz:
```
http://localhost:5000/swagger
```

### Ana Endpoint

#### POST `/perspectra/removing-background`

Görüntü yükleyerek arka plan kaldırma ve perspektif düzeltme işlemi yapar.

**Request:**
```bash
curl -X POST "http://localhost:5000/perspectra/removing-background" \
  -H "Content-Type: multipart/form-data" \
  -F "session_id=test-session-123" \
  -F "guid=unique-guid-456" \
  -F "channel_id=web-channel" \
  -F "image=@/path/to/your/image.jpg"
```

**Form Data:**
- `session_id` (string): Oturum kimliği
- `guid` (string): Benzersiz işlem kimliği
- `channel_id` (string): Kanal kimliği
- `image` (file): İşlenecek görüntü dosyası

**Response:**
```json
{
  "is_background_removed": true,
  "is_image_wrapped": true,
  "error_message": "",
  "result": true,
  "duration": 2.5,
  "processed_image": "iVBORw0KGgoAAAANSUhEUgAA..." // Base64 encoded image
}
```

### Health Check

#### GET `/health`

Servisin sağlık durumunu kontrol eder.

```bash
curl -X GET "http://localhost:5000/health"
```

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2024-09-03T12:00:00",
  "service": "Perspectra API"
}
```

## 🔧 Geliştirme

### Ortam Hazırlığı

Geliştirme yapmadan önce conda environment'ını aktive ettiğinizden emin olun:

```bash
conda activate perspectra
```

### Kod Kalitesi

```bash
# Kod formatlama
make format

# Format kontrolü
make check-format

# Linting
make lint
```

### Test Çalıştırma

```bash
# Unit testler
make run-unit-tests

# Integration testler
make run-integration-tests

# Tüm testler
make run-all-tests
```

### Debug Modu

Debug modunda çalıştırmak için:

```bash
# Debug container'ını başlat
make start-debug

# Debug port: 5678 (VS Code remote debugging için)
# API port: 5001
```

## 📁 Proje Yapısı

```
perspectra-api/
├── src/
│   ├── api/
│   │   ├── adapters/          # İş mantığı adapterleri
│   │   │   ├── perspective_adapter.py    # Perspektif dönüşümü
│   │   │   └── remove_background_adapter.py  # Arka plan kaldırma
│   │   ├── routers/           # API route'ları
│   │   │   ├── health_router.py
│   │   │   └── perspectra_router.py
│   │   └── services/          # Servis katmanı
│   │       └── perspectra_service.py
│   ├── core/                  # Çekirdek bileşenler
│   │   ├── config.py          # Konfigürasyon
│   │   ├── logger.py          # Logging
│   │   └── normalizer.py      # Veri normalizasyonu
│   ├── models/                # Veri modelleri
│   │   ├── requests.py        # Request modelleri
│   │   └── responses.py       # Response modelleri
│   └── main.py               # Ana uygulama
├── models/                   # AI modelleri
│   └── u2net.onnx
├── tests/                    # Test dosyaları
├── images/                   # Örnek görüntüler
├── conda.yaml               # Conda environment tanımı
├── docker-compose.debug.yml  # Debug docker compose
├── Dockerfile               # Production dockerfile
├── Dockerfile.debug         # Debug dockerfile
├── Makefile                 # Otomatik komutlar
├── requirements.txt         # Python bağımlılıkları
└── pyproject.toml          # Proje konfigürasyonu
```

## 🧠 Algoritma Detayları

### 1. Arka Plan Kaldırma
- **Model**: U2Net (U-squared Network)
- **Framework**: rembg kütüphanesi
- **Çıktı**: RGB formatında arka planı kaldırılmış görüntü

### 2. Perspektif Düzeltme
- **Contour Detection**: En büyük konturu bulma
- **Corner Detection**: 4 köşe noktası tespiti
- **Point Ordering**: Köşeleri saat yönünde sıralama (TL, TR, BR, BL)
- **Perspective Transform**: Dikdörtgen forma dönüştürme
- **Padding**: %5 oranında kenar boşluğu ekleme

### 3. İşlem Akışı
1. Görüntü yükleme ve validasyon
2. Arka plan kaldırma işlemi
3. Mask üzerinde contour detection
4. Köşe noktalarını tespit etme ve sıralama
5. Orijinal görüntüye perspektif dönüşümü uygulama
6. Base64 formatında çıktı üretme

## ⚙️ Konfigürasyon

### Ortam Değişkenleri

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `APP_NAME` | Uygulama adı | Perspectra API |
| `PADDING_RATIO` | Kenar boşluğu oranı | 0.05 |
| `SAVE_CONTOURS` | Contour debug görüntülerini kaydet | true |
| `SAVE_TRANSFORMED` | Dönüştürülmüş görüntüleri kaydet | true |
| `USE_LOCAL_MODEL` | Yerel model kullan | true |
| `MODEL_FILENAME` | Model dosya adı | u2net.onnx |

### ONNX Runtime Optimizasyonu

ONNX Runtime performansını artırmak için çeşitli optimizasyon ayarları:

```env
ORT_NUM_THREADS=4
ORT_ENABLE_CPU_MEM_ARENA=1
ORT_ENABLE_MEM_PATTERN=1
ORT_ENABLE_PARALLEL_EXECUTION=1
ORT_EXECUTION_MODE=PARALLEL
ORT_GRAPH_OPT_LEVEL=ALL
```

## 📊 Performans

### Tipik İşlem Süreleri
- **640x480 görüntü**: ~1-2 saniye
- **1280x720 görüntü**: ~2-4 saniye
- **1920x1080 görüntü**: ~4-8 saniye

### Optimizasyon İpuçları
- Görüntü boyutunu mümkün olduğunca küçük tutun
- ONNX Runtime thread sayısını CPU core sayısına göre ayarlayın
- Docker container'ı için yeterli memory ayırın (minimum 2GB)

## 🔍 Hata Ayıklama

### Debug Görüntüleri

`SAVE_CONTOURS=true` ve `SAVE_TRANSFORMED=true` ayarları ile debug görüntüleri otomatik olarak kaydedilir:

```
debug/
├── 20240903_120000/
│   ├── original_mask.png          # Orijinal mask
│   ├── contours.png               # Tespit edilen contourlar
│   ├── original_with_corners.png  # Köşe noktaları işaretli orijinal
│   └── transformed.png            # Dönüştürülmüş görüntü
```

### Log Levels

```python
# Logger konfigürasyonu
logger.init_log_worker(log_level=logging.DEBUG)
```

### Yaygın Hatalar

1. **"Maskede kontur bulunamadı"**: Arka plan kaldırma başarısız olmuş
2. **"Error finding contour corners"**: Köşe tespiti başarısız
3. **"Model download failed"**: Model indirme sorunu

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Geliştirme Kuralları

- Kod formatlamada Black ve isort kullanın
- Flake8 linting kurallarına uyun
- Test coverage %80'in üzerinde tutun
- Commit mesajlarında conventional commits kullanın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Durmuş Ali Öztürk**
- Email: durmusdali.dali@gmail.com
- GitHub: [@dralioz](https://github.com/dralioz)

## 🙏 Teşekkürler

- [rembg](https://github.com/danielgatis/rembg) - Arka plan kaldırma kütüphanesi
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [OpenCV](https://opencv.org/) - Bilgisayar görü kütüphanesi

## 📞 Destek

Sorunlar veya sorular için:
1. [GitHub Issues](https://github.com/dralioz/perspectra-api/issues) açın
2. Email ile iletişime geçin: durmusdali.dali@gmail.com

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
