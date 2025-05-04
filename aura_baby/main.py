import tkinter as tk
from speech.listener import listen_from_mic
from learner import get_response, teach
from memory import load_memory, save_memory

load_memory()

def on_listen():
    text = listen_from_mic()
    if not text:
        response = "Seni duyamadım."
    else:
        response = get_response(text)
        if response.startswith("Bilmiyorum"):
            teach(text, input("Bunu nasıl yanıtlamalıyım? "))
    update_output(f"Kullanıcı: {text}\nAura: {response}")

def update_output(text):
    output_box.config(state="normal")
    output_box.insert(tk.END, text + "\n\n")
    output_box.config(state="disabled")
    output_box.see(tk.END)

def on_close():
    save_memory()
    root.destroy()

root = tk.Tk()
root.title("Baby AI")
root.geometry("600x400")

listen_button = tk.Button(root, text="🎤 Konuş", font=("Arial", 16), command=on_listen)
listen_button.pack(pady=10)

output_box = tk.Text(root, height=20, font=("Consolas", 12), state="disabled", wrap="word")
output_box.pack(fill="both", expand=True, padx=10)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
