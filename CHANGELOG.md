# Değişim Günlüğü (Changelog)

Bu dosyada `İnternet Engelleyici` projesinde yapılan tüm önemli değişiklikler sürümler halinde tutulmaktadır.

## [1.1.0] - 2026-06-28

### Eklenenler (Added)
- Uygulama ana ekranına ve pencere başlığına sürüm numarası (`v1.1.0`) eklendi.
- "Toplu Ekle" butonu sayesinde, alt alta liste halindeki siteleri kopyalayıp yapıştırarak tek seferde engelleme özelliği eklendi.
- "Hosts Dosyası" sekmesi eklenerek dosyayı canlı görüntüleme ve manuel düzenleme imkanı getirildi.
- "Geri Al" (Undo) özelliği eklendi. Yanlışlıkla silinen site ve program engelleri tek tuşla geri getirilebiliyor.

### Düzeltilenler (Fixed)
- Hosts dosyasında `0.0.0.0` IP adresiyle engellenmiş sitelerin program tarafından görülmemesi sorunu çözüldü.
- Bir siteyi listeden çıkarırken ismen benzeyen diğer sitelerin de (örn. `site.com` ve `www.site.com`) yanlışlıkla silinmesini engelleyen tam eşleşme (exact match) düzeltmesi yapıldı.
- Güvenlik duvarı (`netsh`) çıktılarındaki Türkçe karakter uyuşmazlığından kaynaklı programın çökme hatası giderildi (Unicode Decode Hatası).
- Program arka planda UAC izniyle başlatıldığında ekranda siyah terminal penceresi kalması sorunu `pythonw` kullanılarak düzeltildi.

## [1.0.0] - 2026-06-28

### Eklenenler (Added)
- Modern ve karanlık tema destekli kullanıcı arayüzü (`customtkinter` kullanılarak) oluşturuldu.
- Web sitelerini (domain) engelleyebilme ve engeli kaldırabilme özelliği (Hosts dosyası manipülasyonu) eklendi.
- Programların (.exe) internet erişimini engelleyebilme ve engeli kaldırabilme özelliği (Windows Güvenlik Duvarı entegrasyonu) eklendi.
- Engellenen siteleri ve programları ayrı sekmelerde gösteren dinamik liste görünümü eklendi.
- Uygulama başlangıcında otomatik Yönetici (Admin) izni (UAC) isteme mekanizması eklendi.
- Proje dokümantasyonları (README.md, CHANGELOG.md) hazırlandı.
- İlk Git repository'si oluşturuldu.
