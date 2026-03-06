import requests
from keys import hf_key
MODEL_ID = "facebook/bart-large-mnli"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {hf_key}"}
TOPICS = ["sports", "technology", "politics", "health", "business"]
def ask_hf(headline: str):
    payload = {"inputs": headline, "parameters": {"candidate_labels": TOPICS}}
    r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
    if not r.ok:
        raise RuntimeError(f"HF error {r.status_code}: {r.text}")
    return r.json()
def best_topic(prediction: list):
    if not prediction:
        raise ValueError("Empty prediction list")
    best = max(prediction, key=lambda x: x.get("score", 0))
    return best.get("label"), best.get("score")
def bar(score: float) -> str:
    blocks = int(score * 10)
    return "█" * blocks + "░" * (10 - blocks)
def show(headline: str, prediction: list):
    top_label, top_score = best_topic(prediction)
    print("\n" + "=" * 60)
    print(" News Topic Classifier")
    print("=" * 60)
    print(f"Headline: {headline}")
    print(f"Best topic: {top_label}")
    print(f"Confidence: {round(top_score*100,1)}% [{bar(top_score)}]")
    print("\nTop 3 guesses:")
    top3 = sorted(prediction, key=lambda x: x.get("score", 0), reverse=True)[:3]
    for i, p in enumerate(top3, start=1):
        lbl = p.get("label", "N/A")
        sc = p.get("score", 0)
        print(f"{i}. {lbl:<12}{round(sc*100,1)}% {bar(sc)}")
    print("=" * 60)
def main():
    print("Welcome to the news topic classifier!")
    print("Enter a news headline to see its predicted topic.")
    print("Type 'exit' to quit.")
    print(f"Available topics: {', '.join(TOPICS)}")
    while True:
        headline = input("\nEnter headline: ").strip()
        if headline.lower() == "exit":
            print("Goodbye!")
            break
        if not headline:
            print("Please enter a valid headline.")
            continue
        try:
            prediction = ask_hf(headline)
            if isinstance(prediction, list) and prediction and "label" in prediction[0]:
                show(headline, prediction)
            else:
                print("Unexpected response format from Hugging Face API.")
        except Exception as e:
            print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()