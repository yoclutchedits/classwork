import threading
import sys

from numpy import diff
try:
    import time
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    import wave
    import speech_recognition as sr
    from speech_recognition import AudioData
except ImportError as e:
    print(f"Required library not found: {e.name}. Please install it using pip.")
    sys.exit(1)
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
def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    if samples.size == 0:
        return {
            'duration': 0,
            'avg_volume': 0,
            'max_volume': 0,
            'samples': samples
        }
    else:
        return {
            'duration': len(samples) / rate,
            'avg_volume': np.mean(np.abs(samples)),
            'max_volume': np.max(np.abs(samples)),
            'samples': samples
        }
def record_audio(label):
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
def display_stats(stats, text, label):
    print(f"\n{'-'*40}")
    print(f"{label}")
    print(f"Duration: {stats['duration']:.2f} seconds")
    print(f"Average Volume: {stats['avg_volume']:.2f}")
    print(f"Maximum Volume: {stats['max_volume']:.2f}")
    print(f"Transcription: {text}")
def compare(stats1, stats2):
    print("\n" + "=" * 40)
    print("COMPARISON RESULTS")
    print("=" * 40)
    if stats1['duration'] == 0 or stats2['duration'] == 0:
        print("⏱️ Cannot compare duration (one recording is empty)")
    else:
        if stats1['duration'] > stats2['duration']:
            longer = "Recording 1"
            diff = ((stats1['duration'] - stats2['duration']) / stats2['duration']) * 100
        else:
            longer = "Recording 2"
            diff = ((stats2['duration'] - stats1['duration']) / stats1['duration']) * 100
        print(f"⏱️ {longer} is longer by {diff:.1f}%")
    if stats1['avg_volume'] == 0 or stats2['avg_volume'] == 0:
        print("🔊 Cannot compare volume (one recording is empty)")
    else:
        if stats1['avg_volume'] > stats2['avg_volume']:
            louder = "Recording 1"
            diff = ((stats1['avg_volume'] - stats2['avg_volume']) / stats2['avg_volume']) * 100
        else:
            louder = "Recording 2"
            diff = ((stats2['avg_volume'] - stats1['avg_volume'])/ stats1['avg_volume']) * 100
        print(f"🔊 {louder} is louder by {diff:.1f}%")
def plot_both_waveforms(stats1, stats2,rate):
    flg,(ax1,ax2)=plt.subplots(2,1,figsize=(12,6))
    t1=np.linspace(0,len(stats1['samples'])/rate,len(stats1['samples']))
    ax1.plot(t1,stats1['samples'],color='blue',linewidth=0.5)
    ax1.set_title("First Recording - duration: {stats1['duration']:.2f}s, avg volume: {stats1['avg_volume']:.0f}")
    ax1.set_ylabel("amplitude")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-35000,35000)
    t2=np.linspace(0,len(stats2['samples'])/rate,len(stats2['samples']))
    ax2.plot(t2,stats2['samples'],color='red',linewidth=0.5)
    ax2.set_title("Second Recording - duration: {stats2['duration']:.2f}s, avg volume: {stats2['avg_volume']:.0f}")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("amplitude")
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-35000,35000)
    plt.tight_layout()
    plt.show()
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
def main():
    print("="*40)
    print("voice recording and analysis")
    print("="*40)
    print("record twice and compare the results")
    print("\nFirst recording:")
    data1, rate1, width1 = record_audio("Recording the first audio sample. Press Enter to stop.")
    stats1 = analyze_audio(data1, rate1)
    text1 = transcribe_audio(data1, rate1, width1)
    display_stats(stats1, text1, "First Recording Stats")
    print("\nSecond recording:")
    data2, rate2, width2 = record_audio("Recording the second audio sample. Press Enter to stop.")
    stats2 = analyze_audio(data2, rate2)
    text2 = transcribe_audio(data2, rate2, width2)
    display_stats(stats2, text2, "Second Recording Stats")
    compare(stats1, stats2)
    plot_both_waveforms(stats1, stats2, rate1)
if __name__ == "__main__":
    main()