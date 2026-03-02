import requests
url = "https://uselessfacts.jsph.pl/random.json?language=en"
def get_random_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Random Fact: {fact_data['text']}")
    else:
        print("Failed to retrieve a random fact.")
while True:
    user_input = input("Press Enter to get a random fact or type 'q' to quit: ")
    if user_input.lower() == 'q':
        break
    get_random_fact()