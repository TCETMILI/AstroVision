# AstroVision

**AstroVision** FastAPI tabanlı, HuggingFace “text-to-image” pipeline’ı kullanan bir görüntü oluşturma servisi.

---

## 📝 İçindekiler

- [Özellikler](#özellikler)  
- [Önkoşullar](#önkoşullar)  
- [Kurulum](#kurulum)  
- [Kullanım](#kullanım)  
- [Testler](#testler)  
- [CI/CD & Git İşlemleri](#cicd--git-işlemleri)  
- [Katkıda Bulunma](#katkıda-bulunma)  
- [Lisans](#lisans)

---

## Özellikler

- `/health` — Servis durumu ve çalışan cihaz (`cpu`/`cuda`) bilgisini döner.  
- `/generate-scene/` — JSON girişiyle (“prompt”, “width”, “height”) base64-encoded PNG üretir.  
- Otomatik testler (pytest) ve containerizasyon (Docker).

---

## Önkoşullar

- Python ≥ 3.10  
- Git  
- Docker & Docker Compose (opsiyonel)

---

## Kurulum

1. Repo’yu klonlayın:  
   ```bash
   git clone https://github.com/<kullanıcı_adın>/astrovision.git
   cd astrovision

python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

## Kullanım 

uvicorn backend.app:app --reload

python/python3 ui.py

curl -X POST http://localhost:8000/generate-scene \
  -H "Content-Type: application/json" \
  -d '{"prompt":"uzay manzarası","width":512,"height":512}'

curl -X POST http://localhost:8000/describe-scene \
  -H "Content-Type: application/json"

## Testler

pytest tests/test_api.py


MIT © Taha Çetmili