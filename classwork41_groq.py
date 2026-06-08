from openai import OpenAI
import keys
GROQ_URL = "https://api.groq.com/openai/v1"
model = getattr(keys, "GROQ_MODEL", ["llama-3.1-8b-instant","mixtral-8x7b-32768"])
def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512)-> str:
    key=getattr(keys, "g_key", None)
    if not key:
        raise ValueError("API key not found. Please set the 'g_key' variable in the keys module.")
    c=OpenAI(api_key=key, base_url=GROQ_URL)
    last_error = None
    for m in model:
        try:
            r=c.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
            continue
    return ("groq model failed\n"
            f"models tried: {model}\n"
            "fix\n"
            "1) replace the model list with a single model that works for you\n"
            f"error: {last_error}")
    