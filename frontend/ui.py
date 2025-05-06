import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000"

def generate_image(prompt):
    resp = requests.post(f"{BACKEND_URL}/generate", json={"prompt": prompt})
    data =  resp.json()
    return "Henüz görsel yok, stub çalıştı."

with gr.Blocks(title="AstroVision") as demo:
    prompt = gr.Textbox(label="Prompt girin", placeholder="Örneğin: 'Neon renkli galaksi...'")
    btn     = gr.Button("Generate")
    out     = gr.Textbox(label="Response")
    btn.click(generate_image, inputs=prompt, outputs=out)

if __name__ == "__main__":
    demo.launch()