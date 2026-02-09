import requests
def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    res=requests.get(url)
    if res.status_code==200:
        print(f'the full json is:{res.json()}')
        jd=res.json()
        return f"{jd['setup']}-{jd['punchline']}"
    else:
        return 'failed to retrive joke'
def main():
    print('welcome to random joke generator')
    while True:
        ui=input('press enter to get a joke or press q to quit: ')
        if ui=='q':
            break
        joke=get_random_joke()
        print(joke)
if __name__ == "__main__":
    main()