import asyncio
import random
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  Run: pip install pyttsx3")
def speak(text, language='en'):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""
async def translate_text(text, target_language="hi"):
    async with Translator() as translator:
        translation = await translator.translate(text, dest=target_language)
        return translation.text
def display_language_options():
    print("Select a language to translate to:")
    print("1. hindi")
    print("2. Tamil")
    print("3. Telugu")
    print("4. Bengali")
    print("5. Marathi")
    print("6. Gujarati")
    print("7. Malayalam")
    print("8. Punjabi")
    print("9. English (default)")
    choice=input("Enter the number corresponding to your choice: ").strip()
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"
    }
    return language_dict.get(choice, "en")
def main():
    target_language = display_language_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = asyncio.run(translate_text(original_text, target_language))
        print(f"Translated Text: {translated_text}")
        speak(translated_text, language="en")
if __name__ == "__main__":
    main()
