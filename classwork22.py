import requests
hf_key="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"
model_id="facebook/bart-large-mnli"
url=f"https://router.huggingface.co/hf-inference/models/{model_id}"
headers={"Authorization":f"Bearer {k}"}
topic=["sports","technology","politics","health","business"]
def ask_hf(headline:str):
    payload={"inputs":headline,"parameters":{"candidate_labels":topic}}
    r=requests.post(url,json=payload,headers=headers)
    if not r.ok:
        raise RuntimeError(f"Error: {r.status_code}")
    return r.json()
def best_topic(prediction:list):
    best=max(prediction,key=lambda x:x["score"])
    return best["label"],best["score"]
def bar(score:float)->str:
    pct=(score*100)
    blocks=int(pct*20)
    return "█"+ blocks + "░" + (10-blocks)
def show(headline:str,prediction:list):
    top_label,top_score=best_topic(prediction)
    print("\n"+"="*60)
    print("??? news topic classification ???")
    print("="*60)
    print(f"Headline: {headline}")
    print(f"best topic: {top_label}")
    print(f"confidence: {round(top_score*100,1)}%")
    print("\n top 3 guesses:")
    top3=sorted(prediction,key=lambda x:x["score"],reverse=True)[:3]
    for i,p in enumerate(top3,start=1):
        print(f"{i}. {p['label']:<12}{round(p['score']*100,1)}% {bar(p['score'])}")
    print("="*60)
def main():
    print("welcome to the news topic classifier!")
    print("enter a news headline to see its predicted topic.")
    print("type 'exit' to quit.")
    print(f"available topics: {', '.join(topic)}")
    while True:
        headline=input("\nEnter headline: ")
        if headline.lower()=="exit":
            print("goodbye!")
            break
        if not headline.strip():
            print("please enter a valid headline.")
            continue
        try:
            prediction=ask_hf(headline)
            if isinstance(prediction,list) and prediction and "label" in prediction[0]:
                show(headline,prediction)
            else:
                print("unexpected response format from Hugging Face API.")
        except Exception as e:
            print(f"an error occurred: {e}")
if __name__=="__main__":
    main()