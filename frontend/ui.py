# frontend/ui.py
import time
from io import BytesIO
import gradio as gr
import requests
from PIL import Image

API_BASE = "http://127.0.0.1:8000"

# ——— Sahne üretme fonksiyonu ———————————————————————————————
def generate_scene(prompt: str, width: int, height: int):
    """
    Sahne üretme isteği atar, 
    dönen resmi ve status mesajını verir,
    ayrıca Açıkla butonunu aktif etmek için True/False flag'i döner.
    """
    start = time.time()
    try:
        resp = requests.post(
            f"{API_BASE}/generate-scene",
            json={"prompt": prompt, "width": width, "height": height},
            timeout=600
        )
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        elapsed = time.time() - start
        # Üçüncü değer: Açıkla butonunu aktif etsin diye True
        return img, f"✅ Oluşturuldu ({elapsed:.1f}s)", True
    except Exception as e:
        # Hata olursa resim yok, mesaj ve buton pasif
        return None, f"❌ Hata: {e}", False

# ——— Sahne açıklama fonksiyonu ——————————————————————————————
def describe_scene(img):
    try:
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        files = {"file": ("scene.png", buf, "image/png")}
        resp = requests.post(
            f"{API_BASE}/describe-scene",
            files=files,
            timeout=600
        )
        resp.raise_for_status()
        return resp.json().get("description", "—")
    except Exception as e:
        return f"❌ Hata: {e}"

# ——— Preset’leri prompt alanına kopyalayan fonksiyon ————————
def apply_preset(p):
    # Seçilen preset’i doğrudan prompt textbox’a yazar
    return p if p is not None else gr.update()

# ——— Gradio Blokları —————————————————————————————————————
with gr.Blocks(title="🌌 AstroVision", theme="citrus") as demo:
    gr.Markdown("## 📡 AstroVision")

    # ----- Preset + Prompt Bölümü -----
    with gr.Column():
        preset = gr.Dropdown(
            choices=[
                "Black Hole in a distant galaxy",
                "Colorful nebula swirling clouds",
                "Martian landscape at sunrise",
                "Ringed planet with asteroid belt",
                "Space station orbiting Earth"
            ],
            label="🛠️ Ön Ayarlar (Presets)",
            value=None,
            interactive=True
        )
        inp_prompt = gr.Textbox(
            label="✍️ Prompt",
            placeholder="Black Hole, Nebula, Mars landscape…",
            lines=2
        )
        # Preset seçildiğinde prompt'u güncelle
        preset.change(fn=apply_preset, inputs=[preset], outputs=[inp_prompt])

    # ----- Boyut Seçimi -----
    with gr.Row():
        inp_width  = gr.Slider(128, 1024, value=512, step=64, label="Genişlik (px)")
        inp_height = gr.Slider(128, 1024, value=512, step=64, label="Yükseklik (px)")

    # ----- Butonlar ve Durum -----
    btn_create = gr.Button("🌠 Sahneyi Oluştur")
    out_status = gr.Markdown("", visible=False, label="Durum")
    btn_describe = gr.Button("💬 Sahneyi Açıkla")

    # ----- Görüntü ve Açıklama Çıktıları -----
    with gr.Row():
        out_image = gr.Image(label="🖼️ Oluşturulan Sahne", type="pil", interactive=False)
    out_desc = gr.Textbox(label="📝 Açıklama", interactive=False, visible=True)

    # ——— Event Zinciri —————————————————————————————
    # Sahneyi Oluştur → img, durum, buton-enable flag
    create_call = btn_create.click(
        fn=generate_scene,
        inputs=[inp_prompt, inp_width, inp_height],
        outputs=[out_image, out_status],
        show_progress=True
    )
    create_call.then(
        fn=lambda enabled: gr.update(interactive=enabled),
        inputs=[btn_describe],     # aslında create_call.then fonksiyonuna giden flag
        outputs=[btn_describe]
    )

    # Açıklama isteği
    btn_describe.click(
        fn=describe_scene,
        inputs=[out_image],
        outputs=[out_desc]
    ).then(
        fn=lambda desc: gr.update(visible=True),
        inputs=[out_desc],
        outputs=[out_desc]
    )

    gr.Markdown("***\n© 2025 AstroVision")

# Kuyruğa al, sonra başlat
if __name__ == "__main__":
    demo.queue(max_size=4)
    demo.launch()
