import tkinter as tk
import speech_recognition as sr
import os
import threading
import time
import webbrowser

# --- NLP kısmı ---
def yorumla_ve_uygula(cumle):
    cumle = cumle.lower()

    if "dosya oluştur" in cumle:
        yol = os.path.expanduser("~/Masaüstü/yenidosya.txt")
        try:
            with open(yol, "w", encoding="utf-8") as f:
                f.write("")
            return f"Dosya oluşturuldu: {yol}"
        except Exception as e:
            return f"Dosya oluşturulamadı: {e}"

    elif "chrome'u aç" in cumle or "chrome aç" in cumle:
        try:
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            return "Chrome açılıyor..."
        except:
            return "Chrome açılamadı."

    elif "masaüstünü göster" in cumle:
        try:
            yol = os.path.expanduser("~/Masaüstü")
            dosyalar = os.listdir(yol)
            return "Masaüstündeki dosyalar:\n" + "\n".join(dosyalar)
        except:
            return "Masaüstü erişilemedi."

    elif "selam" in cumle or "merhaba" in cumle:
        return "Merhaba! Size nasıl yardımcı olabilirim?"

    elif "kapat" in cumle or "çık" in cumle:
        return "Uygulama kapatılıyor..."

    else:
        return "Ne demek istediğini anlayamadım."

# --- Arayüz ---
pencere = tk.Tk()
pencere.title("Aura - Sesli Yardımcı")
pencere.geometry("1200x800")

metin_alani = tk.Text(pencere, font=("Consolas", 12))
metin_alani.pack(padx=10, pady=10, fill="both", expand=True)
metin_alani.config(state="disabled")

def yazdir(mesaj):
    metin_alani.config(state="normal")
    metin_alani.insert(tk.END, mesaj + "\n")
    metin_alani.config(state="disabled")
    metin_alani.see(tk.END)

# --- Dinleme fonksiyonu ---
def dinlemeyi_baslat():
    threading.Thread(target=sesle_komut_al, daemon=True).start()

def sesle_komut_al():
    yazdir("🎤 Dinleniyor... (konuşmayı kesince algılanacak)")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1.2  # Sessizlik algı eşiği
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            text = recognizer.recognize_google(audio, language="tr-TR")
            yazdir(f"{text}")
            cevap = yorumla_ve_uygula(text)
            yazdir(cevap)
            if "kapatılıyor" in cevap:
                pencere.after(2000, pencere.destroy)
        except sr.UnknownValueError:
            yazdir("Konuşma anlaşılamadı.")
        except sr.RequestError:
            yazdir("Google API erişim hatası.")
        except Exception as e:
            yazdir(f"Hata: {e}")

# --- Konuş butonu ---
konus_buton = tk.Button(pencere, text="Konuş", font=("Consolas", 14), command=dinlemeyi_baslat)
konus_buton.pack(pady=10)

pencere.mainloop()
