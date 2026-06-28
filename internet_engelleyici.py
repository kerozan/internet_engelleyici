import os
import sys
import ctypes
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Temel arayüz ayarları (Karanlık tema ve modern görünüm)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
FIREWALL_RULE_PREFIX = "NetBlocker_"

def is_admin():
    """Programın yönetici haklarıyla çalışıp çalışmadığını kontrol eder."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("İnternet ve Program Engelleyici (NetBlocker)")
        self.geometry("700x550")
        self.resizable(False, False)
        
        # Sekmeler oluşturuluyor
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        self.tab_sites = self.tabview.add("Web Siteleri")
        self.tab_programs = self.tabview.add("Programlar")
        
        self.setup_sites_tab()
        self.setup_programs_tab()

    # ==================== SİTE ENGELLEME BÖLÜMÜ ====================
    def setup_sites_tab(self):
        self.tab_sites.grid_columnconfigure(0, weight=1)
        
        # Site Ekleme Paneli
        add_frame = ctk.CTkFrame(self.tab_sites)
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        add_frame.grid_columnconfigure(0, weight=1)
        
        self.site_entry = ctk.CTkEntry(add_frame, placeholder_text="Örn: www.ornek.com")
        self.site_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        
        add_btn = ctk.CTkButton(add_frame, text="Siteyi Engelle", width=120, command=self.add_site)
        add_btn.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        # Engellenen Siteler Listesi Paneli
        list_label = ctk.CTkLabel(self.tab_sites, text="Engellenen Siteler", font=ctk.CTkFont(weight="bold"))
        list_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.sites_scroll = ctk.CTkScrollableFrame(self.tab_sites)
        self.sites_scroll.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.tab_sites.grid_rowconfigure(2, weight=1)
        
        self.load_blocked_sites()

    def add_site(self):
        site = self.site_entry.get().strip().lower()
        if not site:
            messagebox.showwarning("Uyarı", "Lütfen bir site adresi girin.")
            return
            
        try:
            with open(HOSTS_PATH, "r") as f:
                lines = f.readlines()
            
            # Daha önce eklenmiş mi kontrolü
            for line in lines:
                if not line.strip().startswith("#") and site in line:
                    messagebox.showinfo("Bilgi", "Bu site zaten engellenmiş durumda.")
                    return
            
            # Dosyanın sonuna yönlendirme kuralını ekle
            with open(HOSTS_PATH, "a") as f:
                # Son satır boşlukla bitmiyorsa yeni satıra geçmek garanti olsun
                if lines and not lines[-1].endswith("\n"):
                    f.write("\n")
                f.write(f"{REDIRECT_IP} {site}\n")
                
            self.site_entry.delete(0, 'end')
            self.load_blocked_sites()
            messagebox.showinfo("Başarılı", f"'{site}' başarıyla engellendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Hosts dosyasına erişilemedi (Yönetici izni gerekiyor olabilir):\n{str(e)}")

    def remove_site(self, site_to_remove):
        try:
            with open(HOSTS_PATH, "r") as f:
                lines = f.readlines()
                
            with open(HOSTS_PATH, "w") as f:
                for line in lines:
                    if not line.strip().startswith("#") and site_to_remove in line:
                        continue # Engellenecek siteyi içeren satırı atla
                    f.write(line)
                    
            self.load_blocked_sites()
        except Exception as e:
            messagebox.showerror("Hata", f"Hosts dosyası güncellenemedi:\n{str(e)}")

    def load_blocked_sites(self):
        # Mevcut listeyi temizle
        for widget in self.sites_scroll.winfo_children():
            widget.destroy()
            
        try:
            with open(HOSTS_PATH, "r") as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                # Yorum satırı değilse ve 127.0.0.1 içeriyorsa
                if not line.startswith("#") and REDIRECT_IP in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        site = parts[1]
                        # localhost'u atla (sistemin kendi yönlendirmesi)
                        if site == "localhost":
                            continue 
                        
                        item_frame = ctk.CTkFrame(self.sites_scroll)
                        item_frame.pack(fill="x", pady=2, padx=2)
                        
                        lbl = ctk.CTkLabel(item_frame, text=site)
                        lbl.pack(side="left", padx=10, pady=5)
                        
                        btn = ctk.CTkButton(item_frame, text="Engeli Kaldır", width=100, fg_color="#c0392b", hover_color="#922b21",
                                            command=lambda s=site: self.remove_site(s))
                        btn.pack(side="right", padx=10, pady=5)
        except Exception as e:
            lbl = ctk.CTkLabel(self.sites_scroll, text=f"Dosya okuma hatası: {str(e)}")
            lbl.pack(padx=10, pady=10)

    # ==================== PROGRAM ENGELLEME BÖLÜMÜ ====================
    def setup_programs_tab(self):
        self.tab_programs.grid_columnconfigure(0, weight=1)
        
        # Program Ekleme Paneli
        add_frame = ctk.CTkFrame(self.tab_programs)
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        add_frame.grid_columnconfigure(0, weight=1)
        
        self.prog_entry = ctk.CTkEntry(add_frame, placeholder_text="Program Seçin (.exe)", state="disabled")
        self.prog_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        
        self.selected_exe_path = ""
        
        browse_btn = ctk.CTkButton(add_frame, text="Gözat", width=80, command=self.browse_program)
        browse_btn.grid(row=0, column=1, padx=(5, 5), pady=10)
        
        add_btn = ctk.CTkButton(add_frame, text="Programı Engelle", width=120, command=self.add_program)
        add_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        # Engellenen Programlar Listesi Paneli
        list_label = ctk.CTkLabel(self.tab_programs, text="Engellenen Programlar", font=ctk.CTkFont(weight="bold"))
        list_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.programs_scroll = ctk.CTkScrollableFrame(self.tab_programs)
        self.programs_scroll.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.tab_programs.grid_rowconfigure(2, weight=1)
        
        self.load_blocked_programs()

    def browse_program(self):
        filepath = filedialog.askopenfilename(
            title="Engellenecek Programı Seçin",
            filetypes=(("Yürütülebilir Dosyalar", "*.exe"), ("Tüm Dosyalar", "*.*"))
        )
        if filepath:
            self.selected_exe_path = os.path.normpath(filepath)
            self.prog_entry.configure(state="normal")
            self.prog_entry.delete(0, 'end')
            self.prog_entry.insert(0, self.selected_exe_path)
            self.prog_entry.configure(state="disabled")

    def run_cmd(self, cmd):
        """CMD komutu çalıştırır ve çıktısını döndürür."""
        try:
            # CREATE_NO_WINDOW konsol ekranının yanıp sönmesini engeller
            CREATE_NO_WINDOW = 0x08000000 
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)

    def add_program(self):
        if not self.selected_exe_path:
            messagebox.showwarning("Uyarı", "Lütfen engellenecek bir program (.exe) seçin.")
            return
            
        exe_name = os.path.basename(self.selected_exe_path)
        # Kural ismini program yolu olmadan basitçe tutmak için bir ID oluşturuyoruz
        rule_name = f"{FIREWALL_RULE_PREFIX}{exe_name}"
        
        # Giden (Outbound) Bağlantıyı Engelle
        cmd_out = f'netsh advfirewall firewall add rule name="{rule_name}_Out" dir=out action=block program="{self.selected_exe_path}" enable=yes'
        # Gelen (Inbound) Bağlantıyı Engelle
        cmd_in = f'netsh advfirewall firewall add rule name="{rule_name}_In" dir=in action=block program="{self.selected_exe_path}" enable=yes'
        
        success_out, msg_out = self.run_cmd(cmd_out)
        success_in, msg_in = self.run_cmd(cmd_in)
        
        if success_out and success_in:
            messagebox.showinfo("Başarılı", f"'{exe_name}' internet erişimi başarıyla engellendi.")
            self.selected_exe_path = ""
            self.prog_entry.configure(state="normal")
            self.prog_entry.delete(0, 'end')
            self.prog_entry.configure(state="disabled")
            self.load_blocked_programs()
        else:
            messagebox.showerror("Hata", f"Güvenlik duvarı kuralı oluşturulurken hata oluştu.\nOut: {msg_out}\nIn: {msg_in}")

    def remove_program(self, rule_base_name):
        cmd_out = f'netsh advfirewall firewall delete rule name="{rule_base_name}_Out"'
        cmd_in = f'netsh advfirewall firewall delete rule name="{rule_base_name}_In"'
        
        self.run_cmd(cmd_out)
        self.run_cmd(cmd_in)
        
        self.load_blocked_programs()

    def load_blocked_programs(self):
        # Mevcut listeyi temizle
        for widget in self.programs_scroll.winfo_children():
            widget.destroy()
            
        # Güvenlik duvarı kurallarını al (chcp 65001 ile türkçe karakter sorununu çözebiliriz, ancak findstr basittir)
        success, output = self.run_cmd('netsh advfirewall firewall show rule name=all | findstr "Rule Name:"')
        if not success:
            return
            
        added_rules = set()
        
        for line in output.splitlines():
            # "Rule Name:" kısmı Türkçe Windows'da "Kural Adı:" olarak geçebilir, kontrolü esnetelim.
            # Ancak komutu İngilizce parametrelerle verdik. Güvenlik duvarı çıktıları OS diline bağlıdır.
            # En güvenli yol, satır içinde FIREWALL_RULE_PREFIX aramak.
            if FIREWALL_RULE_PREFIX in line:
                # Satırdan tam kural adını çıkaralım. Örn: "Kural Adı:    NetBlocker_chrome.exe_Out"
                parts = line.split(":", 1)
                if len(parts) > 1:
                    full_rule = parts[1].strip()
                    # Base name'i elde et (Out veya In kısmını at)
                    base_name = full_rule.replace("_Out", "").replace("_In", "")
                    
                    if base_name not in added_rules:
                        added_rules.add(base_name)
                        
                        exe_name = base_name.replace(FIREWALL_RULE_PREFIX, "")
                        
                        item_frame = ctk.CTkFrame(self.programs_scroll)
                        item_frame.pack(fill="x", pady=2, padx=2)
                        
                        lbl = ctk.CTkLabel(item_frame, text=exe_name)
                        lbl.pack(side="left", padx=10, pady=5)
                        
                        btn = ctk.CTkButton(item_frame, text="Engeli Kaldır", width=100, fg_color="#c0392b", hover_color="#922b21",
                                            command=lambda b=base_name: self.remove_program(b))
                        btn.pack(side="right", padx=10, pady=5)

if __name__ == "__main__":
    if is_admin():
        # Yönetici yetkisi var, uygulamayı başlat
        app = App()
        app.mainloop()
    else:
        # Yönetici yetkisi yok, UAC (User Account Control) ekranı çıkararak kendini yönetici olarak yeniden başlat
        # Python script dosya yolu sys.argv[0]'da bulunur. PyInstaller vb. ile build edilirse sys.executable olur.
        if getattr(sys, 'frozen', False):
            # Derlenmiş exe ise
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
        else:
            # Script ise
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
