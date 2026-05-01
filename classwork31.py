import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData
stop_event = threading.Event()
def wait_for_enter():
    input("Press Enter to stop recording...")
    stop_event.set()
def spinner():
    char='|/-\\'
    i=0
    while not stop_event.is_set():
        sys.stdout.write('\rRecording... ' + char[i % 4])
        sys.stdout.flush()
        i+=1
        time.sleep(0.1)
    print("\nRecording stopped.")
def record_audio():
    p=pyaudio.PyAudio()
    steam=p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024)
    frames=[]
    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()
    while not stop_event.is_set():
        frames.append(steam.read(1024))
    steam.stop_stream()
    steam.close()
    width=p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b''.join(frames), 16000, width
def save_audio(data, rate, width, filename="output.wav"):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"Audio saved to {filename}")
def transcribe_audio(data, rate, width):
    recognizer = sr.Recognizer()
    audio=AudioData(data, rate, width)
    try:
        text=recognizer.recognize_google(audio)
        print("Transcription:", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
def plot_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color='blue')
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
def main():
    print("="*40)
    print("Hello AI, can you hear me?")
    print("="*40)
    print("speak into your mic")
    audio_data, rate, width = record_audio()
    save_audio(audio_data, rate, width)
    transcribe_audio(audio_data, rate, width)
    plot_waveform(audio_data, rate)
if __name__ == "__main__":
    main()