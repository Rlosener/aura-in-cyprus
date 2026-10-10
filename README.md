# Aura In Cyprus | Kuzey Kıbrıs gayrimenkul sitesi

Aura In Cyprus, Kuzey Kıbrıs gayrimenkul içeriklerini ve iletişim akışını Türkçe sunan çok sayfalı bir web sitesidir. Proje, mevcut Piller HTML temasının sayfa yapısını ve bileşenlerini koruyup Aura markasının görünüm katmanını ekler.

## Tasarım ve marka sistemi

- Derin mavi-yeşil başlık rengi, turkuaz vurgu ve açık soğuk yüzeyler marka paletini oluşturur.
- Mevcut tema header, kart, ilan ve sayfa bileşenleri temel alınır; Aura’ya özgü renkler ve davranışlar `assets/css/aura-theme.css` ve `assets/js/aura-*.js` dosyalarında yer alır.
- Duyarlı sayfa düzeni ilan keşfi, bölge rehberleri ve iletişim içeriğini farklı ekranlarda kullanılabilir tutar.
- Marka varlıkları `assets/` altında saklanır. Mevcut HTML sınıflarını değiştirmeden önce tema ve Aura katmanındaki seçicileri birlikte kontrol edin.

## Teknik yapı

- HTML tabanlı çok sayfalı ön yüz
- PHP ile çalışan iletişim formu uç noktası (`mail.php`)
- Yerel CSS ve JavaScript marka katmanı
- İlan, hizmet, blog, ekip, bölge rehberi ve iletişim sayfaları

Ana giriş dosyaları arasında `index.html`, `property.html`, `property-details.html`, `neighborhood-guide.html` ve `contact.html` bulunur.

## Yerel önizleme

PHP kurulu bir ortamda depo kökünde çalıştırın:

```bash
php -S 127.0.0.1:8000
```

Siteyi [http://127.0.0.1:8000](http://127.0.0.1:8000) adresinde açın. Statik sayfalar önizlenebilir; e-posta teslimi yerel sunucu önizlemesiyle doğrulanmış sayılmaz.

## İletişim formu yapılandırması

`mail.php`, yalnızca POST isteklerini kabul eder, gelen alanları doğrular ve alıcı adresini `AURA_CONTACT_EMAIL` sunucu ortam değişkeninden okur. Geçerli alıcı ve çalışan PHP `mail()` yapılandırması yoksa uç nokta açık bir yapılandırma hatası döndürür. E-posta adresi veya sunucu sırrını kaynak koda eklemeyin.

## Değişiklik yaparken

- Önce ortak tema bileşenlerini ve `assets/css/aura-theme.css` marka katmanını inceleyin.
- Sayfa ve varlık yollarını koruyun; yeniden adlandırma öncesi referansları arayın.
- Form değişikliklerinde başarılı gönderim, doğrulama hatası ve yapılandırılmamış sunucu durumlarını birlikte ele alın.
- Yerel önizleme, gerçek hosting, DNS, TLS ve e-posta teslimini kanıtlamaz; bunlar canlı ortamda ayrıca kontrol edilmelidir.
