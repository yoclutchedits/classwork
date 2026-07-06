import re
from io import BytesIO
import streamlit as st
import requests
from huggingface_hub import InferenceClient
from classwork46_hf import generate_response
FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
ENHANCE_SYS=("improve prompts for text-to-image generation, return only the improved prompt, do not add any other text"
            "add subjects, adjectives, and details to the prompt to make it more descriptive and visually appealing")
NEAGATIVE="low quality, blurry, bad anatomy, disfigured, poorly drawn, deformed, extra limbs, close up, b&w, weird colors, blurry, duplicate, watermark, signature, text"
img_cli=InferenceClient(model=MODEL_ID, token=st.secrets["hf_key"])
def check_prompt(prompt: str) :
    try:
        r=requests.post(FILTER_API_URL, json={"prompt": prompt}, timeout=10)
        r.raise_for_status()
        data=r.json()
        if not isinstance(data, dict):
            return({"ok": False, "error": "Invalid response format from filter API"})
        return data
    except requests.RequestException as e:
        return({"ok": False, "error": str(e)})
def enhance_prompt(prompt: str) -> str:
    out=generate_response(f"{ENHANCE_SYS}\n\nUser prompt: {prompt}", temperature=0.7, max_new_tokens=512)
    return (out or prompt).strip()
def generate_image(prompt: str):
    filter_result=check_prompt(prompt)
    if not filter_result.get("ok", False):
        return {"ok": False, "error": filter_result.get("error", "Unknown error")}
    if filter_result.get("flagged", False):
        return {"ok": False, "error": "Prompt flagged by content filter"}
    enhanced_prompt=enhance_prompt(prompt)
    try:
        return img_cli.text_to_image(
            prompt=prompt,
            negative_prompt=NEAGATIVE,
            model=MODEL_ID,
        ),None
    except Exception as e:
        return None, str(e)
        if "negative prompt" in msg.lower() or "unexpected keyword" in msg.lower():
            return None, "The generated image was flagged by the content filter due to inappropriate content."
            try:
                return img_cli.text_to_image(
                    prompt=prompt,
                    negative_prompt=NEAGATIVE,
                    model=MODEL_ID,
                ),None
            except Exception as e:
                return None, str(e)
        if any(x in msg.lower() for x in ["420","payment required","pre-paid credit"]):
            return None, "The generated image was flagged by the content filter due to inappropriate content."
        if "404" in msg.lower() or "not found" in msg.lower():
            return None, "The generated image was flagged by the content filter due to inappropriate content."
        return None, f"Error generating image: {msg}"
def main():
    st.set_page_config(page_title="Text-to-Image Generation",layout="centered", page_icon="🖼️")
    st.title("Text-to-Image Generation")
    st.info("This app generates images from text prompts using the Stable Diffusion XL model. Please enter a prompt below and click 'Generate Image'.")
    with st.form("prompt_form"):
        raw_prompt=st.text_area("Enter your prompt:", height=150)
        submitted=st.form_submit_button("Generate Image")
        if submitted:
            raw_prompt=raw_prompt.strip()
            if not raw_prompt:
                st.error("Please enter a prompt.")
                return
            raw_check=check_prompt(raw_prompt)
            if not raw_check.get("ok", False):
                st.error(f"Error checking prompt: {raw_check.get('error', 'Unknown error')}")
                return
            with st.spinner("enhancing prompt and generating image..."):
                final_prompt=enhance_prompt(raw_prompt)
            enhanced_check=check_prompt(final_prompt)
            if not enhanced_check.get("ok"):
                st.error(f"Error checking enhanced prompt: {enhanced_check.get('error', 'Unknown error')}")
                return
            st.markdown(f"**Enhanced Prompt:**")
            st.code(final_prompt)
            with st.spinner("Generating image..."):
                image, error=generate_image(final_prompt)
                if error:
                    st.error(f"Error generating image: {error}")
                st.image(image, caption="Generated Image", use_column_width=True)
                st.session_state.generated_image=image
            image = st.session_state.get("generated_image")
        if image:
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            st.download_button(
                "Download Image",
                buffer.getvalue(),
                "generated_image.png",
                "image/png"
                    )
if __name__=="__main__":
    main()