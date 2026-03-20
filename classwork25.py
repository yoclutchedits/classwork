import requests
from keys import hf_key
from PIL import Image
from io import BytesIO
from datetime import datetime
from huggingface_hub import InferenceClient
models=[
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",
]
client = InferenceClient(api_key=hf_key)
print(f"primary model: {models[0]}")
print(f"type 'quit' to exit")
while True:
    p=input("enter a prompt: ").strip()
    if p.lower() == "quit":
        print("goodbye!")
        break
    if not p:
        print("please enter a prompt")
        continue
    print(f"generating image for prompt: {p}")
    image=None
    for model in models:
        try:
            image = client.text_to_image(model=model, prompt=p)
            break
        except Exception as e:
            print(f"error with model {model}: {e}")
            continue
    if image:
        t=datetime.now().strftime("%Y%m%d_%H%M%S")
        filename=f"generated_image_{t}.png"
        image.save(filename)
        print(f"image saved as {filename}")
        image.show()
        print()
    else:
        print("failed to generate image with all models, please try again later")
print("thank you for using the image generation tool!")