import openai
import os
import traceback
import logging
import torch
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from diffusers import StableDiffusionPipeline
from transformers import pipeline as hf_pipeline

openai.api_key = os.getenv("OPENAI_API_KEY")

# ——— Logging ——————————————————————————————————————————————
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("astrovision")

# ——— FastAPI & CORS ——————————————————————————————————————
app = FastAPI(title="AstroVision API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["*"],
)

# ——— Global Pipeline Nesneleri —————————————————————————————
pipe: StableDiffusionPipeline = None
captioner = None
device = "cuda" if torch.cuda.is_available() else "cpu"

# ——— Pydantic Modelleri —————————————————————————————————————
class SceneRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Sahneyi tanımlayan metin")
    width: int = Field(512, ge=128, le=1024, description="Genişlik (px)")
    height: int = Field(512, ge=128, le=1024, description="Yükseklik (px)")

class DescribeRequest(BaseModel):
    image_data_b64: str = Field(..., description="PNG biçiminde resim bytes")

# ——— Startup Event: Pipeline’ları Yükle ————————————————————————

@app.on_event("startup")
async def startup_event():
    global pipe, captioner

    logger.info("Stable Diffusion pipeline yükleniyor...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        safety_checker=None,
        torch_dtype=torch.float32
    ).to(device)

    logger.info("Image-to-text pipeline yükleniyor...")
    captioner = hf_pipeline(
        "image-to-text",
        model="Salesforce/blip2-opt-2.7b",
        device=0 if device=="cuda" else -1
    )

    logger.info("Tüm pipeline’lar yüklendi.")

# ——— Healthcheck ——————————————————————————————————————————
@app.get("/health")
async def health():
    return {"status": "ok", "device": device}

# ——— Sahne Üretme Endpoint ————————————————————————————————————
@app.post("/generate-scene", response_class=StreamingResponse)
async def generate_scene(req: SceneRequest):
    try:
        full_prompt = f"Astronomical scene, {req.prompt}"
        logger.info(f"Sahne üretiliyor: '{full_prompt}' ({req.width}x{req.height})")
        image = pipe(
            prompt=full_prompt,
            width=req.width,
            height=req.height,
            num_inference_steps=30
        ).images[0]
        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        logger.info("Sahne başarıyla üretildi.")
        return StreamingResponse(buf, media_type="image/png")
    except ValidationError as e:
        logger.error("ValidationError: %s", e)
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        logger.exception("generate_scene sırasında hata")
        raise HTTPException(status_code=500, detail=str(e))

# ——— Sahne Açıklama Endpoint ——————————————————————————————————
@app.post("/describe-scene")
async def describe_scene(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(BytesIO(content)).convert("RGB")
        results = captioner(img)
        caption = results[0]["generated_text"]
        return JSONResponse({"description": caption})
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))