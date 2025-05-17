# tests/test_api.py

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Dizin yapısına göre backend modülüne erişim yolu:
current_dir = os.path.dirname(__file__)
backend_dir = os.path.abspath(os.path.join(current_dir, '..', 'backend'))

sys.path.insert(0, backend_dir)

from app import app

client = TestClient(app)

# Sağlık kontrolü (health-check) Endpoint Testi
def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "device": "cpu"}
