import requests
from keys import hf_key
from colorama import init, Fore, Style
init(autoreset=True)
DEFAULT_MODEL = "google/pegasus-xsum"
headers = {"Authorization": f"Bearer {hf_key}"}
def build_api_url(model_name):
	return f"https://router.huggingface.co/hf-inference/models/{model_name}"
def query(payload, model_name=DEFAULT_MODEL):
	api_url = build_api_url(model_name)
	response = requests.post(api_url, headers=headers, json=payload)
	try:
		return response.json()
	except:
		print("API Response:", response.text)
		return None
def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
	payload = {
		"inputs": text,
		"parameters": {"min_length": min_length, "max_length": max_length}
	}
	print(Fore.BLUE + Style.BRIGHT + f"\nPerforming AI summarization using model: {model_name}")
	result = query(payload, model_name)
	if isinstance(result, list) and result and "summary_text" in result[0]:
		return result[0]["summary_text"]
	else:
		print(Fore.RED + "Error in summarization response:", result)
		return None
def main():
    print(Fore.MAGENTA + Style.BRIGHT + "\nAI Text Summarization Tool\n")
    text = input(Fore.CYAN + "Enter text to summarize: ").strip()
    if not text:
        print(Fore.RED + "Please enter some text.\n")
        return
    try:
        min_length = int(input("Minimum summary length: "))
        max_length = int(input("Maximum summary length: "))
    except ValueError:
        print("Please enter valid numbers")
        return
    model_name = input(f"Model name (default: {DEFAULT_MODEL}): ").strip() or DEFAULT_MODEL
    summary = summarize_text(text, min_length, max_length, model_name)
    if summary:
        print(Fore.GREEN + Style.BRIGHT + "\nSummary:\n" + Fore.WHITE + summary)
if __name__ == "__main__":
	main()
