import speech_recognition as sr

def listen_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Konuşun...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio, language="tr-TR")
        print(f"Tanındı: {text}")
        return text
    except:
        return ""
