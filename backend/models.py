from pydantic import BaseModel, Field
from diffusers import StableDiffusionPipeline
import torch

class SceneRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=200)
    width: int = Field(128, ge=64, le=512)
    height: int = Field(128, ge=64, le=512)
    num_inference_steps: int = Field(50, ge=1, le=200)
    guidance_scale: float = Field(7.5, ge=1.0, le=20.0)
    seed: int | None = None

# Cihaz Tanımı:
device = "cuda" if torch.cuda.is_available() else "cpu"

# Pipeline Tanımı:
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)
