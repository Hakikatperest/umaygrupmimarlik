# -*- coding: utf-8 -*-
"""
Umay Grup Mimarlık — site verisi.

Gövde metinleri KULLANICININ kendi metnidir (Sevda Şahinöz). Değiştirme, yalnızca yerleştir.
Hâlâ eksik olanlar PH(...) ile işaretli — build raporunda sayılır, sayfada sarı şeritle görünür.
Metin/veri değişikliği SADECE bu dosyada yapılır, sonra: python3 _src/build.py
"""

SITE = "https://umaygrupmimarlik.com"
MARKA = "Umay Grup Mimarlık"
MARKA_RESMI = "Umay Grup Mimarlık İnşaat Ticaret Limited Şirketi"
MARKA_LOGO = "UmayGrupMimarlık."   # şablondaki gibi bitişik + nokta
MONOGRAM = "UG"


def PH(metin):
    """Yer tutucu — kullanıcıdan bekleniyor."""
    return {"_ph": True, "t": metin}


# ─────────────────────────────────────────────────────────────
# İŞLETME / KİŞİ
# ─────────────────────────────────────────────────────────────
ISLETME = {
    "ad": MARKA,
    "kisi": "Sevda Şahinöz",
    "unvan": "Mimar & EKB Uzmanı",
    "slogan": "Tasarımdan ruhsata, sahadan enerji belgesine.",
    "telefon_yazi": "0507 875 02 03",
    "telefon_tel": "+905078750203",
    "whatsapp": "905078750203",
    "eposta": "sevdashnz@gmail.com",
    "adres": "Bağlarbaşı Mah. Bağdat Cad. No: 370 İç Kapı No: 10, Maltepe / İstanbul",
    "adres_sokak": "Bağlarbaşı Mah. Bağdat Cad. No: 370 İç Kapı No: 10",
    "adres_ilce": "Maltepe",
    "adres_il": "İstanbul",
    "adres_kisa": "Maltepe / İstanbul",
    "calisma": PH("Pazartesi–Cumartesi 09:00–18:00"),
    "harita_url": PH("Google Haritalar yol tarifi bağlantısı"),
    "instagram": PH("https://instagram.com/..."),
    "linkedin": "",
}

WA_MESAJ = ("Merhaba, Projemle ilgili mimari hizmetleriniz hakkında detaylı bilgi almak ve "
            "görüşme talep etmek istiyorum. Uygun olduğunuzda benimle iletişime geçmenizi "
            "rica ederim. İyi çalışmalar.")

# ─────────────────────────────────────────────────────────────
# GİRİŞ — Vizyon & Yaklaşım  (kullanıcının metni, birebir)
# ─────────────────────────────────────────────────────────────
GIRIS_BASLIK = "Vizyon & Yaklaşım."
GIRIS = [
    "Merhaba, ben Mimar ve EKB Uzmanı Sevda Şahinöz.",
    "Mimarlık pratiğimi; estetik değerleri, kullanıcı ihtiyaçlarını, yasal mevzuatları ve teknik "
    "disiplini bir arada sunan bütüncül bir anlayış üzerine kuruyorum. Uzmanlık alanım olan Enerji "
    "Kimlik Belgesi (EKB) ve enerji verimliliği süreçlerinin yanı sıra; projelendirmeden şantiye "
    "yönetimine, ruhsat işlemlerinden teknik akustik raporlamaya kadar inşaat sektörünün tüm "
    "aşamalarında profesyonel ve çözüm odaklı hizmetler sunuyorum.",
    "Yapıların sadece görsel ve fonksiyonel açıdan değil; statik, mekanik, mimari ve çevresel/enerji "
    "standartlarına tam uyumlu bir şekilde hayata geçirilmesini hedefliyorum.",
]

# ─────────────────────────────────────────────────────────────
# HİZMETLER  (kullanıcının metni, birebir)
# ─────────────────────────────────────────────────────────────
HIZMETLER = [
    {
        "no": "01",
        "slug": "mimari-proje-ve-ruhsat",
        "gorsel": "ruhsat-projesi-dosyasi.webp",
        "gorsel_alt": "Ruhsat projesi dosyasının bileşenleri: mimari, statik, mekanik tesisat ve elektrik projeleri",
        "ad": "Mimari Proje ve Ruhsat Süreçleri",
        "ozet": "Yasal mevzuata, estetik kaygılara ve kullanıcı ihtiyaçlarına uygun teknik ve sanatsal rehber.",
        "metin": [
            "Bir yapının yasal mevzuatlara, estetik kaygılara ve kullanıcı ihtiyaçlarına uygun "
            "teknik/sanatsal rehberini hazırlıyorum. İnşaat ruhsatı alım sürecinde mimari, statik, "
            "mekanik ve elektrik disiplinlerinin birbiriyle tam uyum içinde çalışmasını sağlıyor; "
            "vaziyet planından kat planlarına, kesit ve cephe detaylarına kadar tüm çizimleri "
            "titizlikle hazırlıyorum.",
        ],
    },
    {
        "no": "02",
        "slug": "santiye-sefligi",
        "gorsel": "santiye-sefligi.webp",
        "gorsel_alt": "Şantiye şefliğinde yapı inşaat alanına göre aynı anda üstlenilebilecek maksimum iş sayısı tablosu",
        "ad": "Şantiye Şefliği ve Saha Yönetimi",
        "ozet": "Yapım sürecinin fen, sanat, sağlık ve imar mevzuatına uygun yürütülmesi.",
        "metin": [
            "Yapım ve uygulama süreçlerinin fen, sanat, sağlık ve imar mevzuatına uygun şekilde "
            "yürütülmesini sağlıyorum. Yasal metrekare sınırları ve yönetmelikler çerçevesinde, "
            "projelerin sahada doğru ve güvenli bir şekilde yükselmesi için şantiye şefliği görevini "
            "üstleniyorum.",
        ],
    },
    {
        "no": "03",
        "slug": "fenni-mesul-tus",
        "ad": "Fenni Mesul Sözleşmesi (TUS)",
        "ozet": "Yapı Denetim Kanunu dışında kalan projelerde yasal Teknik Uygulama Sorumluluğu.",
        "metin": [
            "Yapı Denetim Kanunu dışında kalan alanlardaki projelerde, binaların mevzuata ve "
            "projesine uygunluğunu denetlemek üzere yasal Teknik Uygulama Sorumluluğu (TUS) hizmeti "
            "veriyorum.",
        ],
    },
    {
        "no": "04",
        "slug": "enerji-kimlik-belgesi",
        "gorsel": "on-hesap-simulasyon.webp",
        "gorsel_alt": "EKB süreci: proje aşamasında ön hesap ve simülasyon, ardından nihai sertifikasyon",
        "ad": "Enerji Kimlik Belgesi (EKB) ve Ön Hesap Raporlaması",
        "ozet": "Ruhsat öncesi enerji verimliliği simülasyonu ve yasal EKB süreci.",
        "metin": [
            "Yapı ruhsatı öncesinde binanızın enerji verimliliğini simüle eden ön hesap raporlarını "
            "hazırlıyor; binanızın asgari enerji sınıfı koşullarını (C sınıfı ve üzeri) sağlaması "
            "için yasal EKB ve ön tasarım raporlama süreçlerini yürütüyorum.",
        ],
    },
    {
        "no": "05",
        "slug": "akustik-rapor",
        "gorsel": "akustik-analiz.webp",
        "gorsel_alt": "Akustik süreç: proje aşamasında gürültü analizi ve simülasyon, ardından nihai akustik rapor",
        "ad": "Akustik Rapor ve Gürültü Kontrolü",
        "ozet": "Ruhsat aşamasında zorunlu teknik akustik raporlama.",
        "metin": [
            "Binaların Gürültüye Karşı Korunması Hakkında Yönetmelik uyarınca; konut, ticari alan, "
            "eğitim, sağlık ve konaklama tesisleri için yapı ruhsatı aşamasında zorunlu olan teknik "
            "akustik raporlama hizmetlerini sağlıyorum.",
        ],
    },
]

# ─────────────────────────────────────────────────────────────
# NEDEN BİRLİKTE ÇALIŞMALIYIZ  (kullanıcının metni, birebir)
# ─────────────────────────────────────────────────────────────
NEDEN_BASLIK = "Neden Birlikte Çalışmalıyız?"
NEDEN = [
    {
        "ad": "Bütüncül Yaklaşım",
        "metin": "Mimari tasarımdan teknik detaylara, ruhsat onaylarından saha denetimine kadar "
                 "sürecin her adımında tek noktadan profesyonel destek.",
    },
    {
        "ad": "Mevzuat Uyumluluğu",
        "metin": "Güncel imar kanunları, enerji verimliliği ve akustik yönetmeliklerine %100 uyumlu "
                 "teknik dosya hazırlığı.",
    },
    {
        "ad": "Disiplinlerarası Koordinasyon",
        "metin": "Statik, mekanik ve elektrik mühendislik gruplarıyla kusursuz proje entegrasyonu.",
    },
]

# ─────────────────────────────────────────────────────────────
# KAPANIŞ ÇAĞRISI  (kullanıcının metni, birebir)
# ─────────────────────────────────────────────────────────────
CTA_BASLIK = "Projeniz İçin Danışmanlık ve Fiyat Bilgisi Alın."
CTA_METIN = ("Projenizin ruhsat, tasarım, şantiye şefliği, EKB, EKB Ön Hesap Sonuç raporu, Akustik "
             "rapor veya teknik raporlama ihtiyaçları için doğrudan iletişime geçebilirsiniz.")

# ─────────────────────────────────────────────────────────────
# PROJELER
# gorsel: images/ altındaki kaynak dosya. Ad/konum/yıl ⏳ kullanıcıdan bekleniyor.
# ─────────────────────────────────────────────────────────────
PROJELER = [
    {
        "slug": "proje-1",
        "ad": PH("Proje 1 adı"),
        "ozet": PH("Proje 1 — 1-2 cümlelik tanım"),
        "kategori": PH("Konut"),
        "yil": PH("20XX"),
        "konum": PH("İlçe/İl"),
        "gorsel": "2.webp.jpeg",
        "alt": "Doğal ışık alan beton kolonlu iç mekân",
    },
    {
        "slug": "proje-2",
        "ad": PH("Proje 2 adı"),
        "ozet": PH("Proje 2 — 1-2 cümlelik tanım"),
        "kategori": PH("Ticari"),
        "yil": PH("20XX"),
        "konum": PH("İlçe/İl"),
        "gorsel": "3.webp.jpeg",
        "alt": "Gökyüzüne karşı eğrisel beyaz cephe",
    },
    {
        "slug": "proje-3",
        "ad": PH("Proje 3 adı"),
        "ozet": PH("Proje 3 — 1-2 cümlelik tanım"),
        "kategori": PH("Kamu"),
        "yil": PH("20XX"),
        "konum": PH("İlçe/İl"),
        "gorsel": "4.webp.jpeg",
        "alt": "Karo kaplı üçgen kabuk çatı detayı",
    },
    {
        "slug": "proje-4",
        "ad": PH("Proje 4 adı"),
        "ozet": PH("Proje 4 — 1-2 cümlelik tanım"),
        "kategori": PH("Ofis"),
        "yil": PH("20XX"),
        "konum": PH("İlçe/İl"),
        "gorsel": "5.webp.jpeg",
        "alt": "Konsol çıkmalı brüt beton kütle",
    },
    {
        "slug": "proje-5",
        "ad": PH("Proje 5 adı"),
        "ozet": PH("Proje 5 — 1-2 cümlelik tanım"),
        "kategori": PH("Konut"),
        "yil": PH("20XX"),
        "konum": PH("İlçe/İl"),
        "gorsel": "6.webp.jpeg",
        "alt": "Ahşap panelli, çatı ışıklıklı aydınlık hacim",
    },
]

HERO_GORSEL = "banner.webp"
HERO_ALT = "Gökyüzüne karşı brüt beton cephe"
ILETISIM_GORSEL = "7.webp.jpeg"
ILETISIM_ALT = "Gün ışığı alan açık plan ofis"

# ─────────────────────────────────────────────────────────────
# SAYFALAR
# ⚠️ Ayrı sayfa açmadan önce: varyasyon değil, ayrı NİYET olmalı.
# ─────────────────────────────────────────────────────────────
SAYFALAR = {
    "anasayfa": {
        "yol": "",
        "menu": "Ana Sayfa",
        "baslik": "Umay Grup Mimarlık | Mimari Proje, Ruhsat, EKB ve Akustik Rapor",
        "aciklama": "Mimar ve EKB Uzmanı Sevda Şahinöz: mimari proje ve ruhsat süreçleri, şantiye "
                    "şefliği, fenni mesuliyet (TUS), Enerji Kimlik Belgesi ve akustik raporlama.",
        "h1": "Umay Grup Mimarlık.",
    },
    "hakkimda": {
        "yol": "hakkimda",
        "menu": "Hakkımda",
        "baslik": "Hakkımda | Mimar & EKB Uzmanı Sevda Şahinöz",
        "aciklama": "Estetik değerleri, kullanıcı ihtiyaçlarını, yasal mevzuatı ve teknik disiplini "
                    "bir arada ele alan bütüncül bir mimarlık pratiği.",
        "h1": "Hakkımda.",
    },
    "hizmetler": {
        "yol": "hizmetler",
        "menu": "Hizmetler",
        "baslik": "Hizmetler | Mimari Proje, Ruhsat, Şantiye Şefliği, EKB, Akustik Rapor",
        "aciklama": "Mimari proje ve ruhsat süreçleri, şantiye şefliği ve saha yönetimi, fenni mesul "
                    "sözleşmesi (TUS), Enerji Kimlik Belgesi ve akustik raporlama hizmetleri.",
        "h1": "Uzmanlık Alanlarım ve Hizmetler.",
    },
    "projeler": {
        "yol": "projeler",
        "menu": "Projeler",
        "baslik": "Projeler | Umay Grup Mimarlık",
        "aciklama": "Tamamlanan ve yürüyen mimari projelerden bir seçki.",
        "h1": "Projeler.",
    },
    "iletisim": {
        "yol": "iletisim",
        "menu": "İletişim",
        "baslik": "İletişim | Umay Grup Mimarlık",
        "aciklama": "Projenizin ruhsat, tasarım, şantiye şefliği, EKB veya akustik rapor ihtiyaçları "
                    "için doğrudan iletişime geçin.",
        "h1": "İletişim.",
    },
}

MENU_SIRA = ["anasayfa", "hakkimda", "hizmetler", "projeler", "iletisim"]

# ─────────────────────────────────────────────────────────────
# SSS  (⏳ gerçek sorular/cevaplar kullanıcıdan bekleniyor)
# ─────────────────────────────────────────────────────────────
SSS = [
    {"s": PH("Sık sorulan soru 1"), "c": PH("Cevap 1 — 2-4 cümle")},
    {"s": PH("Sık sorulan soru 2"), "c": PH("Cevap 2 — 2-4 cümle")},
    {"s": PH("Sık sorulan soru 3"), "c": PH("Cevap 3 — 2-4 cümle")},
]
