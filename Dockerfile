# 1. Build image
FROM python:3.10-slim AS builder

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları (eğer gerekirse ekleyin)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını yükle
COPY deployment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Final image
FROM python:3.10-slim

WORKDIR /app

# Çalıştırma zamanı bağımlılıkları
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Uygulama kodunu kopyala
COPY backend/ .

# Uvicorn’u global olarak ekleyelim
RUN pip install --no-cache-dir uvicorn

# Container çalıştırıldığında expose edeceğimiz port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
