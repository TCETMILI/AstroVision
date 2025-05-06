import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_generate_default():
    payload = {"prompt":"test","width":64,"height":64}
    r = client.post("/generate-scene", json=payload)
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"

@pytest.mark.parametrize("w,h", [(32,32), (1024,1024)])
def test_generate_invalid_size(w,h):
    r = client.post("/generate-scene", json={"prompt":"x","width":w,"height":h})
    assert r.status_code == 422  # validation error