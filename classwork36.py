import speech_recognition as sr
import pyttsx3
from googletrans import Translator
def speak(text, language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', language)
    engine.say(text)
    engine.runAndWait()
def translate_text(text, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        print(f"Translated text: {translation.text}")
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""
def display_language_options():
    print("???? Available translation languages: ")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")
    choice = input("Enter the number corresponding to your language choice: ")
    language_map = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"
    }
    return language_map.get(choice,"es")
def main():
    display_language_options()
    dest_language = display_language_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, dest_language)
        speak(translated_text, language=dest_language)
        print(f"Original text: {original_text}")
        print(f"Translated text: {translated_text}")
if __name__ == "__main__":    main()