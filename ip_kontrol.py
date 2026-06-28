import os
import re
import socket
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


# ── Sabitler ────────────────────────────────────────────────

KARA_LISTE_DOSYASI = "ip_blacklist.txt"
GECMIS_DOSYASI      = os.path.join(os.path.expanduser("~"), "ip_gecmis.json")
DNSBL_SUNUCUSU      = "zen.spamhaus.org"


# ── Kontrol fonksiyonları ────────────────────────────────────

def ip_formati_dogru_mu(ip):
    desen = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    eslesme = re.match(desen, ip)
    if eslesme == None:
        return False
    for parca in eslesme.groups():
        sayi = int(parca)
        if sayi < 0 or sayi > 255:
            return False
    return True

def yerel_kontrol(ip):
    if not os.path.exists(KARA_LISTE_DOSYASI):
        return False
    with open(KARA_LISTE_DOSYASI, "r", encoding="utf-8") as dosya:
        satirlar = dosya.readlines()
    for satir in satirlar:
        satir = satir.strip()
        if satir == ip:
            return True
    return False

def ip_ters_cevir(ip):
    parcalar = ip.split(".")
    ters_parcalar = list(reversed(parcalar))
    ters_ip = ".".join(ters_parcalar)
    return ters_ip

def online_kontrol(ip):
    ters_ip = ip_ters_cevir(ip)
    sorgu_adresi = ters_ip + "." + DNSBL_SUNUCUSU
    try:
        socket.gethostbyname(sorgu_adresi)
        return True
    except socket.gaierror:
        return False


# ── Geçmiş yönetim fonksiyonları ─────────────────────────────

def gecmisi_yukle():
    if not os.path.exists(GECMIS_DOSYASI):
        return []
    with open(GECMIS_DOSYASI, "r", encoding="utf-8") as dosya:
        return json.load(dosya)

def kayit_ekle(ip, sonuc):
    kayitlar = gecmisi_yukle()
    yeni_kayit = {
        "ip"   : ip,
        "sonuc": sonuc,
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    }
    kayitlar.append(yeni_kayit)
    with open(GECMIS_DOSYASI, "w", encoding="utf-8") as dosya:
        json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)
    return kayitlar

def listeyi_guncelle(kayitlar):
    gecmis_listesi.delete(0, tk.END)
    for kayit in reversed(kayitlar):
        satir = kayit["tarih"] + "   " + kayit["ip"] + "   →   " + kayit["sonuc"]
        gecmis_listesi.insert(tk.END, satir)


# ── Arayüz fonksiyonu ─────────────────────────────────────────

def kontrol_et():
    ip = ip_girisi.get().strip()

    if ip == "":
        messagebox.showwarning("Uyarı", "Lütfen bir IP adresi girin.")
        return

    if not ip_formati_dogru_mu(ip):
        messagebox.showerror("Hata", "Geçersiz IP adresi formatı.")
        return

    yerel_sonuc  = yerel_kontrol(ip)
    online_sonuc = online_kontrol(ip)

    if yerel_sonuc or online_sonuc:
        sonuc_metni = "KARA LİSTEDE"
        sonuc_label.config(text=sonuc_metni, fg="#ef4444")
    else:
        sonuc_metni = "TEMİZ"
        sonuc_label.config(text=sonuc_metni, fg="#10b981")

    kaynak_metni = ""
    if yerel_sonuc:
        kaynak_metni = kaynak_metni + "Yerel liste  "
    if online_sonuc:
        kaynak_metni = kaynak_metni + "Online (Spamhaus)"
    if kaynak_metni == "":
        kaynak_metni = "-"
    kaynak_label.config(text=kaynak_metni)

    kayitlar = kayit_ekle(ip, sonuc_metni)
    listeyi_guncelle(kayitlar)


# ── Arayüz ──────────────────────────────────────────────────

pencere = tk.Tk()
pencere.title("IP Blacklist Kontrol Aracı")
pencere.geometry("600x520")
pencere.resizable(False, False)
pencere.configure(bg="#1e3a5f")

tk.Label(
    pencere,
    text="IP Blacklist Kontrol Aracı",
    font=("Segoe UI", 16, "bold"),
    bg="#1e3a5f",
    fg="white"
).pack(pady=20)

giris_cerceve = tk.Frame(pencere, bg="#1e3a5f")
giris_cerceve.pack(pady=5)

ip_girisi = tk.Entry(
    giris_cerceve,
    font=("Consolas", 13),
    width=20,
    justify="center"
)
ip_girisi.pack(side="left", padx=5)

tk.Button(
    giris_cerceve,
    text="Kontrol Et",
    font=("Segoe UI", 11, "bold"),
    bg="#3b82f6",
    fg="white",
    padx=10,
    pady=5,
    command=kontrol_et
).pack(side="left", padx=5)

tk.Label(
    pencere,
    text="Sonuç:",
    font=("Segoe UI", 10),
    bg="#1e3a5f",
    fg="white"
).pack(pady=(15, 0))

sonuc_label = tk.Label(
    pencere,
    text="—",
    font=("Segoe UI", 20, "bold"),
    bg="#1e3a5f",
    fg="#94a3b8"
)
sonuc_label.pack(pady=5)

kaynak_label = tk.Label(
    pencere,
    text="",
    font=("Segoe UI", 9),
    bg="#1e3a5f",
    fg="#94a3b8"
)
kaynak_label.pack()

tk.Label(
    pencere,
    text="Geçmiş Kontroller",
    font=("Segoe UI", 10, "bold"),
    bg="#1e3a5f",
    fg="#94a3b8"
).pack(anchor="w", padx=20, pady=(15, 0))

gecmis_cerceve = tk.Frame(pencere, bg="#1e3a5f")
gecmis_cerceve.pack(padx=20, pady=4, fill="both", expand=True)

kaydirma = tk.Scrollbar(gecmis_cerceve)
kaydirma.pack(side="right", fill="y")

gecmis_listesi = tk.Listbox(
    gecmis_cerceve,
    font=("Consolas", 9),
    bg="#0f2040",
    fg="#e2e8f0",
    selectbackground="#3b82f6",
    yscrollcommand=kaydirma.set,
    relief="flat",
    bd=0,
    height=10
)
gecmis_listesi.pack(side="left", fill="both", expand=True)
kaydirma.config(command=gecmis_listesi.yview)

listeyi_guncelle(gecmisi_yukle())
pencere.mainloop()
