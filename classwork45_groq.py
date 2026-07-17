from openai import OpenAI
import streamlit as st

GROQ_URL = "https://api.groq.com/openai/v1"
FALLBACK_MODELS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    api_key = st.secrets.get("g_key")
    if not api_key:
        raise ValueError("API key not found. Please set 'g_key' in Streamlit secrets.")

    c = OpenAI(api_key=api_key, base_url=GROQ_URL)

    last_error = None
    for m in FALLBACK_MODELS:
        try:
            r = c.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
            continue

    return ("groq model failed\n"
            f"models tried: {FALLBACK_MODELS}\n"
            "fix\n"
            "1) replace the model list with a single model that works for you\n"
            f"error: {last_error}")
