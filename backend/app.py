from fastapi import FastAPI, HTTPException
from models import SceneRequest, pipe, device 
from logger import timed
from fastapi.responses import StreamingResponse
from io import BytesIO
import torch, hashlib

app = FastAPI(title="AstroVision API")

cache: dict[str, bytes] = {}

@app.post("/generate-scene")
@timed
async def generate_scene(req: SceneRequest):
    # 1) Cache key
    key_raw = f"{req.prompt}|{req.width}x{req.height}|{req.num_inference_steps}|{req.guidance_scale}|{req.seed}"
    key = hashlib.sha256(key_raw.encode()).hexdigest()

    # 2) Cache hit
    if key in cache:
        buf = BytesIO(cache[key])
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    try:
        # 3) Tohum set et
        if req.seed is not None:
            torch.manual_seed(req.seed)
        # 4) Görsel üret
        result = pipe(
            req.prompt,
            width=req.width,
            height=req.height,
            num_inference_steps=req.num_inference_steps,
            guidance_scale=req.guidance_scale,
        )
        image = result.images[0]
        # PNG Dönüşümü
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek
        # Cache Kaydet
        cache[key] = buf.getvalue()
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")
        