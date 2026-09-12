# Umay Grup Mimarlık

`umaygrupmimarlik.com` — statik site, GitHub Pages'te yayında.

## Yapı

    _src/data.py       tüm metin ve veri  ← DEĞİŞİKLİK BURADA YAPILIR
    _src/varliklar.py  CSS + JS kaynağı
    _src/build.py      sayfa üreticisi
    _src/media.py      görsel türevleri (yalnız görsel değişince)
    images/            kaynak görseller (buraya yüklenir)
    assets/img/        üretilen WebP türevleri

## Kullanım

    python3 _src/media.py     # yeni görsel eklediyseniz önce bu
    python3 _src/build.py     # sayfaları üretir

⛔ Üretilen HTML dosyalarını (index.html, hizmetler/index.html …) elle düzenlemeyin —
bir sonraki `build.py` çalışmasında üzerine yazılır.

Eksik metinler `_src/data.py` içinde `PH("…")` ile işaretlidir; sayfada sarı şeritle görünür
ve `build.py` çalışınca listelenir.
