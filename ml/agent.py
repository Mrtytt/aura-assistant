import os
import shutil
import subprocess
import re
from parser import parse_nl_command

# Aksiyon fonksiyonları, parametre alırlar
def create_file(yer: str, dosya_adi: str, tur: str, content: str = ""):
    try:
        # "yer" parametresindeki " klasörüne" ibaresini kaldır ve path oluştur
        loc = yer.replace(' klasörüne', '').replace(' klasöre', '')
        base = os.path.expanduser('~')
        dir_path = os.path.join(base, loc)
        # Klasör yoksa oluştur
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # Tam dosya yolu
        file_path = os.path.join(dir_path, f"{dosya_adi}.{tur}")
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Yeni dosya oluşturuldu: {file_path}"
    except Exception as e:
        return f"Dosya oluşturulurken hata oluştu: {e}"

def delete_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"Dosya silindi: {file_path}"
        return f"Dosya bulunamadı: {file_path}"
    except Exception as e:
        return f"Dosya silinirken hata oluştu: {e}"

def mkdir(dir_path: str):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            return f"Klasör oluşturuldu: {dir_path}"
        return f"Klasör zaten var: {dir_path}"
    except Exception as e:
        return f"Klasör oluşturulurken hata oluştu: {e}"

def delete_dir(dir_path: str):
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            return f"Klasör silindi: {dir_path}"
        return f"Klasör bulunamadı: {dir_path}"
    except Exception as e:
        return f"Klasör silinirken hata oluştu: {e}"

def rename(old_name: str, new_name: str):
    try:
        if os.path.exists(old_name):
            target_dir = os.path.dirname(new_name)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir)
            os.rename(old_name, new_name)
            return f"{old_name} → {new_name} olarak yeniden adlandırıldı"
        return f"Dosya bulunamadı: {old_name}"
    except Exception as e:
        return f"Yeniden adlandırma hatası: {e}"

def cat(file_path: str):
    try:
        if os.path.exists(file_path):
            return open(file_path).read()
        return f"Dosya bulunamadı: {file_path}"
    except Exception as e:
        return f"Dosya okunurken hata: {e}"

def cd(dir_path: str):
    try:
        if os.path.exists(dir_path):
            os.chdir(dir_path)
            return f"Dizin değişti: {dir_path}"
        return f"Klasör bulunamadı: {dir_path}"
    except Exception as e:
        return f"Dizin değiştirilirken hata: {e}"

def pwd():
    return os.getcwd()

def list_dir(dir_path: str = None):
    try:
        path = dir_path or os.getcwd()
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Listeleme hatası: {e}"

def copy_file(src: str, dest: str):
    try:
        shutil.copy(src, dest)
        return f"Kopyalandı: {src} → {dest}"
    except Exception as e:
        return f"Kopyalama hatası: {e}"

def move_file(src: str, dest: str):
    try:
        shutil.move(src, dest)
        return f"Taşındı: {src} → {dest}"
    except Exception as e:
        return f"Taşıma hatası: {e}"

def search_file(file_path: str):
    return f"Bulundu: {file_path}" if os.path.exists(file_path) else f"Bulunamadı: {file_path}"

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    return "Ekran temizlendi"

def info():
    return {"OS": os.name, "PWD": os.getcwd(), "Python": os.sys.version.split()[0]}

# Eylem haritası
actions = {
    "create_file": create_file,
    "delete_file": delete_file,
    "mkdir": mkdir,
    "delete_dir": delete_dir,
    "rename": rename,
    "cat": cat,
    "cd": cd,
    "pwd": pwd,
    "list_dir": list_dir,
    "copy_file": copy_file,
    "move_file": move_file,
    "search_file": search_file,
    "clear": clear,
    "info": info
}

def execute_action(action: str, *args):
    func = actions.get(action)
    if not func:
        return f"Tanımsız eylem: {action}"
    try:
        return func(*args)
    except TypeError:
        return f"Parametre uyumsuzluğu: {action} beklenen parametre sayısı farklı"
    except Exception as e:
        return f"Eylem çalıştırılırken hata: {e}"

if __name__ == "__main__":
    print("Agent hazır. Doğal dil veya komut satırı formatı kullanabilirsiniz.")
    while True:
        raw = input("Komut> ")
        if raw.strip().lower() in ['exit', 'çıkış']:
            print("Çıkılıyor...")
            break

        action, param_dict = parse_nl_command(raw)

        # Parametreleri uygun biçime dönüştür
        if isinstance(param_dict, dict) and 'yer' in param_dict:
            # create_file için özel işleme
            yer = param_dict['yer']
            dosya_adi = param_dict['dosya_adi']
            tur = param_dict['tur']
            # yer: "model klasörüne" gibi, sonundaki 'klasörüne' ibaresini kaldırıp path yap
            yer_path = yer.replace(' klasörüne', '').replace(' klasöre', '')
            base = os.path.expanduser('~')
            full_dir = os.path.join(base, yer_path)
            full_path = os.path.join(full_dir, f"{dosya_adi}.{tur}")
            args = [full_path, ""]
        elif isinstance(param_dict, dict) and 'params' in param_dict:
            args = param_dict['params']
        else:
            # fallback
            args = []

        # Aksiyonu çalıştır
        output = execute_action(action, *args)
        print(output)
