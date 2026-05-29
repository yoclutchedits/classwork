from classwork38_groq import generate_response
import time
def temprature_prompt():
    print("="*100)
    print("advanced prompting: temperature + instructions")
    print("="*100)
    print("part 1: temperature")
    base=input("enter a prompt: ").strip()
    for t,label in [(0.1, "low"), (0.5, "medium"), (1.0, "high")]:
        print(f"\ntemperature: {t} ({label})")
        print(generate_response(base, temperature=t, max_tokens=512))
        time.sleep(1)
    print("\npart 2: instructions")
    topic=input("enter a topic: ").strip()
    prompts = [
    f"Summarize key facts about {topic} in 3-4 sentences.",
    f"Explain {topic} as if I'm a 10-year-old child.",
    f"Write a pro/con list about {topic}.",
    f"Create a fictional news headline from 2050 about {topic}.",
]
    for i, p in enumerate(prompts, 1):
        print(f"\nprompt {i}: {p}")
        print(generate_response(p, temperature=0.7, max_tokens=512))
        time.sleep(1)
    print("\npart 3: your turn")
    custom_prompt=input("enter a custom prompt: ").strip()
    try:
        temp=float(input("enter a temperature (0.0-1.0): ").strip())
        if not (0.0 <= temp <= 1.0):
            raise ValueError("Temperature must be between 0.0 and 1.0")
    except ValueError:
        print("Invalid temperature. Using default of 0.7.")
        temp = 0.7
    print(f"\nresponse for custom prompt with temperature {temp}:")
    print(generate_response(custom_prompt, temperature=temp, max_tokens=512))
    print("\n reflection")
    print("1) how did changing the temperature affect the responses?")
    print("2) which of the instructions generated the most interesting response and why?")
    print("3) how would you modify the custom prompt to get a different type of response?")
    print("genertate content -> rewrite -> create a sequence .")
def pseudo_stream(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def bonus_pseudo_streaming():
    choice = input("\nbonus: streaming-like output? (y/n): ").strip().lower()
    if choice == 'y':
        prompt = input("enter a prompt for streaming response: ").strip()
        response = generate_response(prompt, temperature=0.7, max_tokens=512)
        print("\nstreaming response:")
        pseudo_stream(response)
if __name__ == "__main__":
    temprature_prompt()
    bonus_pseudo_streaming()