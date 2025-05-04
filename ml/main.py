import speech_recognition as sr
from predict import predict_intent
from agent import execute_action
import time

def listen_and_recognize():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Dinleniyor (konuşmayı başlatın)...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=None)

    try:
        print("Ses tanınıyor...")
        text = recognizer.recognize_google(audio, language="tr-TR")
        print(f"Algılanan metin: {text}")
        return text
    except sr.UnknownValueError:
        return "(Ses anlaşılamadı)"
    except sr.RequestError as e:
        return f"API hatası: {e}"

def main():
    while True:
        print("Konuşmak için Enter'a basın, çıkmak için 'q' yazın.")
        komut = input(">> ").strip()
        if komut.lower() == "q":
            break
        
        text = listen_and_recognize()
        if text.startswith("("):
            print(text)
            continue

        action = predict_intent(text)
        result = execute_action(action)
        print(f"🔧 {result}")
        print("--------------------------")
        time.sleep(1)

if __name__ == "__main__":
    main()
