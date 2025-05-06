FROM python:3.10-slim

WORKDIR  /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Backend ve frontend portları
EXPOSE 8000 7860


# Başlat: önce backend, sonra frontend
CMD ["sh", "-c", "\
    uvicorn backend.app:app --host 0.0.0.0 --port 8000 & \
    python frontend/ui.py --server.host 0.0.0.0 --server.port 7860"]