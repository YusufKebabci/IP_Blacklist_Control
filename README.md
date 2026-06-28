# IP Blacklist Kontrol Aracı

Girilen bir IP adresinin kara listede olup olmadığını **yerel dosya** ve **online DNSBL sorgusu** ile kontrol eden Python/Tkinter masaüstü uygulaması.

## Özellikler

- IPv4 format doğrulama (regex ile)
- Yerel kara liste dosyasından kontrol (`ip_blacklist.txt`)
- Online kontrol — Spamhaus DNSBL sorgusu (`socket` modülü ile, API key gerektirmez)
- Geçmiş kayıt sistemi (JSON dosyasına otomatik kayıt)
- Sade ve okunabilir Tkinter arayüzü

## Kullanılan Kütüphaneler

- `os`
- `re`
- `socket`
- `json`
- `datetime`
- `tkinter`

## Kurulum ve Çalıştırma

```bash
git clone https://github.com/YusufKebabci/ip-blacklist-kontrol.git
cd ip-blacklist-kontrol
python ip_kontrol.py
```


## Nasıl Çalışır?

1. Kullanıcı bir IP adresi girer.
2. Program IP formatını doğrular.
3. `ip_blacklist.txt` dosyasında yerel kontrol yapılır.
4. IP, ters çevrilip `zen.spamhaus.org` adresine DNS sorgusu olarak gönderilir.
5. Sonuç ekranda gösterilir ve `ip_gecmis.json` dosyasına kaydedilir.

## Proje Yapısı

```
ip-blacklist-kontrol/
├── ip_kontrol.py        # Ana uygulama
├── ip_blacklist.txt     # Örnek yerel kara liste
├── README.md
└── .gitignore
```

