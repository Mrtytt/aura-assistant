import os
import subprocess
import tkinter as tk
import shutil
from tkinter import scrolledtext

# Başlangıç dizini
current_dir = os.getcwd()

def aura_open(app_path):
    try:
        os.startfile(app_path)
        return f"{app_path} açılıyor..."
    except Exception as e:
        return f"Hata: {e}"

def aura_create_file(filename, directory):
    try:
        full_path = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write("")
        return f"{full_path} oluşturuldu."
    except Exception as e:
        return f"Hata: {e}"

def aura_rename_file(old, new):
    try:
        os.rename(old, new)
        return f"{old} → {new} olarak değiştirildi."
    except Exception as e:
        return f"Hata: {e}"

def aura_list_dir():
    try:
        items = os.listdir(current_dir)
        return "\n".join(items) if items else "Klasör boş."
    except Exception as e:
        return f"Hata: {e}"

def aura_search_file(filename, root_dir="C:/Users"):
    matches = []
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            matches.append(os.path.join(root, filename))
    return "\n".join(matches) if matches else f"'{filename}' bulunamadı."

def aura_delete_file(filename):
    try:
        target = os.path.join(current_dir, filename)
        if os.path.isfile(target):
            os.remove(target)
            return f"{target} silindi."
        else:
            return f"Dosya bulunamadı: {target}"
    except Exception as e:
        return f"Hata: {e}"

def aura_delete_dir(dirname):
    try:
        target = os.path.join(current_dir, dirname)
        if os.path.isdir(target):
            shutil.rmtree(target)
            return f"{target} ve içeriği silindi."
        else:
            return f"Klasör bulunamadı: {target}"
    except Exception as e:
        return f"Hata: {e}"

def aura_copy_file(source, destination):
    try:
        src = os.path.join(current_dir, source)
        dst = os.path.join(current_dir, destination)
        if os.path.isfile(src):
            shutil.copy(src, dst)
            return f"{src} kopyalandı → {dst}"
        else:
            return f"Kaynak dosya bulunamadı: {src}"
    except Exception as e:
        return f"Hata: {e}"

def aura_move_file(source, destination):
    try:
        src = os.path.join(current_dir, source)
        dst = os.path.join(current_dir, destination)
        if os.path.exists(src):
            shutil.move(src, dst)
            return f"{src} taşındı → {dst}"
        else:
            return f"Kaynak bulunamadı: {src}"
    except Exception as e:
        return f"Hata: {e}"

def aura_cat(filename):
    try:
        target = os.path.join(current_dir, filename)
        if os.path.isfile(target):
            with open(target, 'r', encoding='utf-8') as f:
                content = f.read()
            return content if content else "(Dosya boş)"
        else:
            return f"Dosya bulunamadı: {target}"
    except Exception as e:
        return f"Hata: {e}"

def aura_mkdir(dirname):
    try:
        target = os.path.join(current_dir, dirname)
        os.makedirs(target, exist_ok=True)
        return f"Klasör oluşturuldu: {target}"
    except Exception as e:
        return f"Hata: {e}"

def aura_info():
    return f"""
Aura Asistan Komutları:
• open [uygulama_adı]
• create file [dosyaadı] [konum]
• rename [eski] [yeni]
• list dir
• search file [dosyaadı]
• cd [yol] / cd ..     → Klasör değiştir
• pwd                  → Mevcut dizini gösterir
• delete file [dosyaadı]
• delete dir [klasör]
• copy file [kaynak] [hedef]
• move file [kaynak] [hedef]
• cat [dosyaadı]       → Dosya içeriğini gösterir
• mkdir [klasör_yolu]
• clear                → Çıktıyı temizler
• exit / quit
Bilinmeyen komutlar shell komutu olarak denenir.
"""

def handle_command():
    global current_dir
    komut = command_entry.get().strip()
    lower = komut.lower()
    result = ""

    if lower.startswith("open"):
        result = aura_open(komut.replace("open ","", 1))

    elif lower.startswith("create file"):
        try:
            _, _, filename, directory = komut.split(maxsplit=3)
            result = aura_create_file(filename, directory)
        except:
            result = "Kullanım: create file [dosyaadı] [konum]"

    elif lower.startswith("rename"):
        try:
            _, old, new = komut.split(maxsplit=2)
            result = aura_rename_file(old, new)
        except:
            result = "Kullanım: rename eski.txt yeni.txt"

    elif lower == "list dir":
        result = aura_list_dir()

    elif lower.startswith("search file"):
        try:
            parts = komut.split(maxsplit=2)
            if len(parts) < 3:
                result = "Kullanım: search file dosyaadı"
            else:
                filename = parts[2]
                result = aura_search_file(filename)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower.startswith("cd"):
        try:
            target = komut[3:].strip()
            if target == "":
                result = "Kullanım: cd [yol] veya cd .."
            else:
                new_path = os.path.abspath(os.path.join(current_dir, target))
                if os.path.isdir(new_path):
                    current_dir = new_path
                    result = f"Dizin değiştirildi: {current_dir}"
                else:
                    result = f"Klasör bulunamadı: {new_path}"
        except Exception as e:
            result = f"Hata: {e}"

    elif lower == "pwd":
        result = f"Mevcut dizin: {current_dir}"

    elif lower.startswith("delete file"):
        try:
            parts = komut.split(maxsplit=2)
            if len(parts) < 3:
                result = "Kullanım: delete file [dosyaadı]"
            else:
                filename = parts[2]
                result = aura_delete_file(filename)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower.startswith("delete dir"):
        try:
            parts = komut.split(maxsplit=2)
            if len(parts) < 3:
                result = "Kullanım: delete dir [klasör]"
            else:
                dirname = parts[2]
                result = aura_delete_dir(dirname)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower.startswith("copy file"):
        try:
            parts = komut.split(maxsplit=3)
            if len(parts) < 4:
                result = "Kullanım: copy file [kaynak] [hedef]"
            else:
                _, _, source, destination = parts
                result = aura_copy_file(source, destination)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower.startswith("move file"):
        try:
            parts = komut.split(maxsplit=3)
            if len(parts) < 4:
                result = "Kullanım: move file [kaynak] [hedef]"
            else:
                _, _, source, destination = parts
                result = aura_move_file(source, destination)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower.startswith("cat"):
        try:
            parts = komut.split(maxsplit=1)
            if len(parts) < 2:
                result = "Kullanım: cat [dosyaadı]"
            else:
                filename = parts[1]
                result = aura_cat(filename)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower.startswith("mkdir"):
        try:
            parts = komut.split(maxsplit=1)
            if len(parts) < 2:
                result = "Kullanım: mkdir [klasör_yolu]"
            else:
                dirname = parts[1]
                result = aura_mkdir(dirname)
        except Exception as e:
            result = f"Hata: {e}"

    elif lower == "clear":
        output_box.config(state="normal")
        output_box.delete(1.0, tk.END)
        output_box.config(state="disabled")
        command_entry.delete(0, tk.END)
        return

    elif lower == "info":
        result = aura_info()

    elif lower in ["exit", "quit"]:
        root.destroy()
        return

    else:
        # Bilinmeyen komutları yerel shell'de çalıştırmayı deneyelim
        try:
            completed = subprocess.run(komut, shell=True, capture_output=True, text=True, cwd=current_dir)
            output = completed.stdout.strip() if completed.stdout.strip() else completed.stderr.strip()
            result = output if output else "Komut çalıştırıldı."
        except Exception as e:
            result = f"Hata: {e}"

    # Çıktıyı göster
    output_box.config(state="normal")
    output_box.insert(tk.END, f"[{current_dir}] >> {komut}\n{result}\n\n")
    output_box.config(state="disabled")
    output_box.see(tk.END)
    command_entry.delete(0, tk.END)

# GUI ayarları
root = tk.Tk()
root.title("Aura - Terminal Asistanı")
root.geometry("800x500")

command_entry = tk.Entry(root, font=("Consolas", 14))
command_entry.pack(fill="x", padx=10, pady=10)
command_entry.bind("<Return>", lambda event: handle_command())

output_box = scrolledtext.ScrolledText(root, state="disabled", font=("Consolas", 12), wrap="word")
output_box.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
