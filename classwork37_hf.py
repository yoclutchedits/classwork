import keys
from huggingface_hub import InferenceClient
models=getattr(keys, "HF_MODEL", ["meta-llama/Llama-3.1-8B-Instruct"] )
def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512)-> str:
    key=getattr(keys, "hf_key", None)
    if key is None:
        raise ValueError("API key not found. Please set the 'hf_key' variable in the keys module.")
    last_error = None
    for m in models:
        try:
            c=InferenceClient(token=key)
            r=c.chat_completions(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
    return ("hf model failed\n"
            f"models tried: {models}\n"
            "fix\n"
            "1) switch to groq by importing classwork37_groq.py in classwork37_run.py\n "
            "2) replace the model list with a single model that works for you\n"
            f"error: {last_error}")
    