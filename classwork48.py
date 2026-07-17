import io, re
from io import BytesIO
import streamlit as st
from huggingface_hub import InferenceClient
from classwork45_groq import generate_response
import keys
import requests
MATH_SYSTEM = """You are a Math Mastermind.

Solve with clear step-by-step reasoning, correct notation, and a final answer.

Verify when possible; mention an alternative method briefly if relevant."""

CHAT_CSS = """

<style>

.wrap {max-height: 520px; overflow-y: auto; padding-right: 6px;}

.card{border:1px solid #e6e6e6;background:#fff;border-radius:10px;padding:14px 16px;margin:10px 0;

box-shadow:0 1px 2px rgba(0,0,0,0.04);}

.q{font-weight:700;color:#0a6ebd;margin-bottom:8px;}

.meta{display:inline-block;background:#FF9800;color:#fff;padding:2px 8px;border-radius:12px;font-size:12px;margin-left:8px}

.a{white-space:pre-wrap;color:#333;line-height:1.5;}

</style>"""
def export_txt(history):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(history, 1)])
    return io.BytesIO(text.encode('utf-8'))
def teaching_answer(q: str) -> str:
    return generate_response(q, temperature=0.3, max_tokens=1024)
def math_ans(q: str, level: str) -> str:
    prompt = f"{MATH_SYSTEM}\n\nProblem: ({level}) {q}\n\nAnswer:"
    return generate_response(prompt, temperature=0.3, max_tokens=1024)
def run_ai():
    st.title("teaching assistant")
    st.session_state.setdefault("history_ata", [])
    c1, c2 = st.columns([1, 2])
    if c1.button("Clear History"):
        st.session_state.history_ata = []
    if st.session_state.history_ata:
        c2.download_button("Export History", data=export_txt(st.session_state.history_ata), file_name="history.txt", mime="text/plain")
    q=st.text_input("Enter your question here:", placeholder="e.g., Explain the Pythagorean theorem", key="q_ata")
    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                answer = teaching_answer(q)
                st.session_state.history_ata.append({"question": q, "answer": answer})
                st.success("Answer generated!")
                st.rerun()
    if not st.session_state.history_ata:return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html='<div class="wrap">'
    for i, h in enumerate(st.session_state.history_ata, 1):
        html+=f'<div class="card"><div class="q">Q{i}: {h["question"]}</div><div class="a">{h["answer"]}</div></div>'
        st.markdown(html, unsafe_allow_html=True)
def run_math():
    st.title("math problem solver")
    st.session_state.setdefault("history_math", [])
    c1, c2 = st.columns([1, 2])
    if c1.button("Clear History"):
        st.session_state.history_math = []
    if st.session_state.history_math:
        c2.download_button("Export History", data=export_txt(st.session_state.history_math), file_name="history.txt", mime="text/plain")
    with st.form("math_form", clear_on_submit=True):
        q=st.text_area("Enter your math problem here:", placeholder="e.g., Solve for x in the equation 2x + 3 = 7", key="q_math", height=100)
        a,b=st.columns([3,1])
        solve= a.form_submit_button("Solve",use_container_width=True)
        lvl= b.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"],index=1)
        if solve:
            if not q.strip():
                st.warning("Please enter a math problem.")
            else:
                with st.spinner("Solving..."):
                    answer = math_ans(q, lvl)
                    st.session_state.history_math.append({"question": q, "answer": answer})
                    st.success("Problem solved!")
                    st.rerun()
    if not st.session_state.history_math:return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html='<div class="wrap">'
    for i, h in enumerate(st.session_state.history_math, 1):
        html+=f'<div class="card"><div class="q">Q{i}: {h["question"]}<span class="meta">{lvl}</span></div><div class="a">{h["answer"]}</div></div>'
    st.markdown(html+'</div>', unsafe_allow_html=True)
def safe_img_gen():
    filter = "https://filters-zeta.vercel.app/api/filter"
    img_model = "stabilityai/stable-diffusion-3-medium-diffusers"
    img_client = InferenceClient(provider='hf-inference', api_key=keys.hf_key)
    st.title("Image Generation (Safe Mode)")
    def is_safe_prompt(prompt: str):
        try:
            response = requests.post(filter, json={"prompt": prompt}, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"): 
                    return True, None
            else:
                st.error(f"Error checking prompt safety: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            st.error(f"Error occurred while checking prompt safety: {e}")
            return False
    def generate_image(prompt: str):
        safe,error = is_safe_prompt(prompt)
        if not safe:
            st.error(f"Prompt is not safe: {error}")
            return None
        try:
            img=img_client.text_to_image(model=img_model, prompt=prompt)
            return img, None
        except Exception as e:
            st.error(f"Error occurred while generating image: {e}")
            return None
    with st.form("img_form", clear_on_submit=True):
        prompt=st.text_area("Enter your image prompt here:", placeholder="e.g., A serene landscape with mountains and a river at sunset", key="prompt_img", height=100)
        submit=st.form_submit_button("Generate Image")
        if submit:
            if not prompt.strip():
                st.warning("Please enter an image prompt.")
            else:
                with st.spinner("Generating image..."):
                    img,error = generate_image(prompt)
                    if img:
                        st.image(img, caption="Generated Image", use_column_width=True)
                    else:
                        st.error(f"Failed to generate image: {error}")
        im=st.session_state.get("generated_image")
        if im:
            buffer = BytesIO()
            im.save(buffer, format="PNG")
            st.download_button("Download Image", data=buffer.getvalue(), file_name="generated_image.png", mime="image/png")
def main():
    st.set_page_config(page_title="AI Teaching Assistant", page_icon=":robot:", layout="centered")
    st.sidebar.title("AI Teaching Assistant")
    st.sidebar.write("Choose a mode:")
    mode = st.sidebar.radio("", ["Teaching Assistant", "Math Problem Solver", "Image Generation"])
    if mode == "Teaching Assistant":
        run_ai()
    elif mode == "Math Problem Solver":
        run_math()
    elif mode == "Image Generation":
        safe_img_gen()
if __name__ == "__main__":
    main()