import keys
from huggingface_hub import InferenceClient
models = getattr(keys, "models", ["meta-llama/Llama-3.1-8B-Instruct"])
def generate_response(prompt: str, temperature: float = 0.7, max_new_tokens: int = 512) -> str:
    key=getattr(keys, "hf_key", None)
    if not key:
        raise ValueError("Hugging Face API key not found in keys.py")
    last_err=None
    for m in models:
        try:
            c=InferenceClient(model=m, token=key)
            r=c.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_new_tokens
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err=e
    raise last_err
