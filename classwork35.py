import speech_recognition as sr
import pyttsx3
from datetime import datetime
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""
def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "your name" in command:
        speak("I am your virtual assistant.")
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}.")
    elif "exit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I'M NOT SURE HOW TO RESPOND TO THAT.")
    return True
def main():
    speak("Welcome! I am your virtual assistant. How can I help you?")
    while True:
        command = listen()
        if command:
            if not respond_to_command(command):
                break
if __name__ == "__main__":
    main()