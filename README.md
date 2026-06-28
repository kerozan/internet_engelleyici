# İnternet ve Program Engelleyici (NetBlocker)

NetBlocker, Windows işletim sistemlerinde belirli web sitelerine ve programlara (.exe) internet erişimini kolayca engellemenizi sağlayan, modern ve kullanıcı dostu bir araçtır.

## Özellikler

- **Web Sitesi Engelleme:** İstenmeyen web sitelerine erişimi Windows `hosts` dosyasını düzenleyerek engeller.
- **Program Engelleme:** Seçilen programların (.exe) internete çıkışını Windows Güvenlik Duvarı (Firewall) kuralları oluşturarak engeller.
- **Aktif Engellemeleri Yönetme:** Engellenen site ve programları listeleyebilir ve istediğiniz zaman engeli tek tıkla kaldırabilirsiniz.
- **Modern Arayüz:** `customtkinter` ile geliştirilmiş, karanlık tema destekli şık ve modern arayüz.
- **Tamamen Türkçe:** Kullanımı kolay, anlaşılır Türkçe arayüz.

## Kurulum ve Çalıştırma

1. Python 3.8 veya üzeri bir sürümün yüklü olduğundan emin olun.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı çalıştırın:
   ```bash
   python internet_engelleyici.py
   ```

> **Önemli Not:** Uygulama, Windows sistem dosyalarını ve Güvenlik Duvarı kurallarını değiştirdiği için **Yönetici (Administrator)** haklarıyla çalıştırılmalıdır. Normal çalıştırıldığında sizden otomatik olarak yönetici izni isteyecektir.

## Sürüm Notları
Detaylı sürüm bilgileri için [CHANGELOG.md](CHANGELOG.md) dosyasını inceleyebilirsiniz.

## Lisans
Bu proje açık kaynaklıdır ve kişisel kullanım için ücretsizdir.
