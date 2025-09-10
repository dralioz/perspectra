# Perspectra Library Migration Guide

Bu dosya, FastAPI servisinin kütüphane haline dönüştürülmesi sürecini açıklar.

## Tamamlanan Adımlar

### ✅ 1. Yeni Kütüphane Yapısı Oluşturuldu
```
perspectra_lib/
├── __init__.py              # Ana modül giriş noktası
├── core/
│   ├── __init__.py
│   ├── config.py           # Konfigürasyon sınıfları
│   └── processor.py        # Ana işlemci sınıfı
└── adapters/
    ├── __init__.py
    ├── background_removal.py   # Arka plan temizleme
    └── perspective_correction.py # Perspektif düzeltme
```

### ✅ 2. API Bağımlılıkları Kaldırıldı
- FastAPI, uvicorn ve diğer web framework bağımlılıkları kaldırıldı
- Pydantic sadece konfigürasyon için minimal kullanım
- HTTP request/response modelleri kaldırıldı

### ✅ 3. Temiz Kütüphane API'si Tasarlandı
```python
from perspectra_lib import PerspectraProcessor, PerspectraConfig

# Basit kullanım
processor = PerspectraProcessor()
success, error, result, duration = processor.process_image_from_file("input.jpg")

# Gelişmiş konfigürasyon
config = PerspectraConfig(padding_ratio=0.1, save_transformed=True)
processor = PerspectraProcessor(config)
```

### ✅ 4. Dokümantasyon ve Örnekler
- Kapsamlı README_lib.md
- example_usage.py ile kullanım örnekleri
- test_library.py ile test senaryoları

### ✅ 5. Kurulum ve Dağıtım
- setup.py ile pip kurulumu
- requirements_lib.txt ile minimal bağımlılıklar
- setup_library.py ile kolay kurulum scripti

## Kullanım Kılavuzu

### Hızlı Başlangıç

1. **Kütüphaneyi kur:**
```bash
python setup_library.py
# veya manuel:
pip install -r requirements_lib.txt
pip install -e .
```

2. **Temel kullanım:**
```python
from perspectra_lib import PerspectraProcessor

processor = PerspectraProcessor()
success, error, result, duration = processor.process_image_from_file("test.jpg")

if success:
    # result numpy array olarak döner
    print(f"İşlem {duration:.2f} saniyede tamamlandı")
```

3. **Dosya kaydetme:**
```python
success, error, duration = processor.save_processed_image("input.jpg", "output.jpg")
```

4. **Base64 çıktı:**
```python
success, error, base64_result, duration = processor.process_image_to_base64(image_bytes)
```

### Gelişmiş Konfigürasyon

```python
from perspectra_lib import PerspectraConfig, PerspectraProcessor

config = PerspectraConfig(
    padding_ratio=0.15,        # %15 padding
    save_transformed=True,     # Debug resimleri kaydet
    contours_path="debug/",    # Debug klasörü
    log_level="DEBUG"          # Detaylı log
)

processor = PerspectraProcessor(config)
```

## Önemli Değişiklikler

### FastAPI'den Kütüphaneye Geçiş
- **Öncesi:** HTTP endpoint'leri ile servis
- **Sonrası:** Direkt Python fonksiyon çağrıları

### Bağımlılık Azaltma
- **Öncesi:** 10+ paket (FastAPI, uvicorn, vs.)
- **Sonrası:** 6 core paket (OpenCV, PIL, rembg, vs.)

### API Tasarımı
- **Öncesi:** JSON request/response
- **Sonrası:** Python objects (numpy arrays, tuples)

### Hata Yönetimi
- **Öncesi:** HTTP status kodları
- **Sonrası:** Boolean success + error message

## Test ve Doğrulama

```bash
# Kütüphaneyi test et
python test_library.py

# Örnek kullanımları çalıştır
python example_usage.py

# Paket oluştur
python setup_library.py
```

## Migration Tamamlama Adımları

Kütüphane hazır! Şu adımları takip edebilirsiniz:

1. **Test et:** `python test_library.py`
2. **Örnekleri incele:** `python example_usage.py`
3. **Eski FastAPI dosyalarını temizle:** `python setup_library.py` (seçenek 3)
4. **Dağıt:** PyPI'ye yüklemek için paket oluştur

## Eski vs Yeni Karşılaştırma

### Eski FastAPI Kullanımı:
```python
# Client kodu gerekli
import requests

files = {"image": open("test.jpg", "rb")}
response = requests.post("http://localhost:5000/process", files=files)
result = response.json()
```

### Yeni Kütüphane Kullanımı:
```python
# Direkt kullanım
from perspectra_lib import PerspectraProcessor

processor = PerspectraProcessor()
success, error, result, duration = processor.process_image_from_file("test.jpg")
```

## Faydalar

1. **Performans:** HTTP overhead'i yok
2. **Basitlik:** Direkt fonksiyon çağrıları
3. **Esneklik:** Özelleştirilmiş konfigürasyon
4. **Taşınabilirlik:** Web server gereksinimi yok
5. **Entegrasyon:** Mevcut Python projelere kolay dahil etme

Artık `perspectra` tamamen bağımsız bir Python kütüphanesi!
