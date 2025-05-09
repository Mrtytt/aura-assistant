import sounddevice as sd
import queue
import json
import subprocess
from vosk import Model, KaldiRecognizer
from transformers import pipeline

q = queue.Queue()

# Ses callback
def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    q.put(bytes(indata))

# Vosk modeli
model = Model("models/vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)

# Eğitilmiş intent sınıflandırıcısı
classifier = pipeline("text-classification", model="my-intent-classifier")

# Komut yorumlayıcı
def execute_command(label, text):
    if label == "open_browser":
        subprocess.Popen(["start", "chrome"], shell=True)
        print("Opening browser...")
    elif label == "open_calculator":
        subprocess.Popen(["calc"], shell=True)
        print("Opening calculator...")
    elif label == "search_web":
        query = text.lower().replace("search", "").strip()
        subprocess.Popen(["start", f"https://www.google.com/search?q={query}"], shell=True)
        print(f"Searching: {query}")
    elif label == "get_time":
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        print("Current time is:", now)
    elif label == "exit":
        print("Goodbye!")
        exit()
    else:
        print("Unknown command.")

print("🎤 Speak something...")

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            if not text:
                continue

            print("You said:", text)

            # Metni sınıflandır
            out = classifier(text)[0]
            label = out["label"]
            score = out["score"]

            print(f"Predicted intent: {label} ({score:.2f})")
            if score > 0.8:
                execute_command(label, text)
            else:
                print("Sorry, I couldn't understand that.")
