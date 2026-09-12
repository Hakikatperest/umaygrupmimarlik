# -*- coding: utf-8 -*-
"""
Umay Grup Mimarlık — site üreticisi.

    python3 _src/build.py

⛔ Üretilen HTML'i ELLE DÜZENLEME — bir sonraki build ezer. Metin/veri: _src/data.py, biçim: burası.
Görsel türevleri ayrı: _src/media.py (yalnız görsel değişince).

Tasarım referansı: kullanıcının verdiği "ShureArchitects." şablonu — akromatik (açık gri zemin,
beyaz kartlar, siyah şerit), noktayla biten kalın başlıklar, görselin üzerine kayan proje kartları.
"""
import hashlib
import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D  # noqa: E402

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(KOK, "assets", "img")

YIL = 2026
PH_SAYAC = []

# ⚠️ Site hem kök alan adından (umaygrupmimarlik.com) hem de GitHub Pages'in proje alt
# yolundan (hakikatperest.github.io/umaygrupmimarlik/) açılabiliyor. Kök-göreli "/assets/..."
# yolları alt yolda 404 veriyor ve sayfa çıplak metne dönüyor. Bu yüzden tüm iç yollar
# sayfanın derinliğine göre GÖRELİ üretilir. 404.html istisna: GitHub onu her derinlikteki
# uydurma URL için servis ettiği için göreli yol tutmaz, kök-mutlak kalır.
ONEK = ""


def ic(gorece=""):
    """İç bağlantı/varlık yolu — geçerli sayfanın ön ekiyle."""
    if not gorece:
        return ONEK if ONEK else "./"
    return ONEK + gorece


# ─────────────────────────────────────────────────────────────
# Yardımcılar
# ─────────────────────────────────────────────────────────────
def e(s):
    return html.escape(str(s), quote=True)


def m(deger):
    """Metin ver. Yer tutucuysa sarı şeritle göster ve sayaca yaz."""
    if isinstance(deger, dict) and deger.get("_ph"):
        PH_SAYAC.append(deger["t"])
        return '<mark class="ph" title="Bu metin bekleniyor">%s</mark>' % e(deger["t"])
    return e(deger)


def duz(deger):
    """Yer tutucuyu düz metne indirger — meta/alt/JSON-LD gibi işaretleme kaldırmayan yerler için."""
    if isinstance(deger, dict) and deger.get("_ph"):
        PH_SAYAC.append(deger["t"])
        return deger["t"]
    return str(deger)


def bos(deger):
    """Yer tutucu mu? (bağlantı üretip üretmeyeceğimize karar verirken)"""
    return isinstance(deger, dict) and deger.get("_ph")


def damga(gorece):
    """Varlık sürümleme: içerik SHA1'inin ilk 8 hanesi.
    ⚠️ GitHub Pages CSS/JS'i max-age=600 ile servis eder; damga olmadan düzeltme ziyaretçiye
    10 dakika ULAŞMAZ. İçerik değişmezse URL de değişmez."""
    yol = os.path.join(KOK, gorece)
    if not os.path.exists(yol):
        return ic(gorece)
    with open(yol, "rb") as f:
        return "%s?v=%s" % (ic(gorece), hashlib.sha1(f.read()).hexdigest()[:8])


def _turevler(kaynak):
    """images/ kaynak adından assets/img altındaki türev genişliklerini bulur."""
    if not kaynak:
        return None, []
    s = os.path.basename(kaynak).split(".")[0]
    if not os.path.isdir(IMG):
        return s, []
    gen = []
    for f in os.listdir(IMG):
        mm = re.match(r"^%s-w(\d+)\.webp$" % re.escape(s), f)
        if mm:
            gen.append(int(mm.group(1)))
    return s, sorted(gen)


def resim(kaynak, alt, sinif="", sizes="100vw", oncelik=False):
    """<picture> üretir. srcset dosya sisteminden okunur — sabit liste yazmak 404 doğuruyor."""
    s, gen = _turevler(kaynak)
    if not gen:
        return ('<div class="gorsel-yok %s" role="img" aria-label="%s"><span>GÖRSEL<br>BEKLENİYOR</span></div>'
                % (e(sinif), e(alt)))
    srcset = ", ".join("%s %dw" % (ic("assets/img/%s-w%d.webp" % (s, g)), g) for g in gen)
    yukleme = ('fetchpriority="high" decoding="async"' if oncelik
               else 'loading="lazy" decoding="async"')
    return (
        '<picture class="%s"><img src="%s" srcset="%s" sizes="%s" '
        'alt="%s" width="%d" %s></picture>'
        % (e(sinif), ic("assets/img/%s-w%d.webp" % (s, gen[-1])), srcset, e(sizes),
           e(alt), gen[-1], yukleme)
    )


def tel_link():
    return "tel:%s" % D.ISLETME["telefon_tel"]


def wa_link():
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (D.ISLETME["whatsapp"], quote(D.WA_MESAJ))


# ─────────────────────────────────────────────────────────────
# Ortak parçalar
# ─────────────────────────────────────────────────────────────
def ust(aktif):
    ogeler = []
    for anahtar in D.MENU_SIRA:
        s = D.SAYFALAR[anahtar]
        yol = ic(s["yol"] + "/" if s["yol"] else "")
        ogeler.append(
            '<li><a href="%s"%s>%s</a></li>'
            % (yol, ' class="etkin" aria-current="page"' if anahtar == aktif else "", e(s["menu"]))
        )
    return """<a class="atla" href="#ana">İçeriğe atla</a>
<header class="ust">
  <div class="ust-ic">
    <a class="logo" href="%s">%s</a>
    <button class="hamburger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Menüyü aç">
      <span></span><span></span><span></span>
    </button>
    <nav id="menu" class="menu" aria-label="Ana menü">
      <ul>%s</ul>
      <div class="menu-ilt">
        <a class="dg dg-ara" href="%s">Hemen Ara</a>
        <small>%s · %s</small>
      </div>
    </nav>
  </div>
</header>""" % (ic(), logo_kilidi(sizes="(max-width:520px) 132px, 176px"),
                "".join(ogeler), tel_link(),
                e(duz(D.ISLETME["telefon_yazi"])), e(duz(D.ISLETME["adres_kisa"])))


# ─────────────────────────────────────────────────────────────
# Logo — kullanıcının verdiği gerçek marka varlığı.
# Kaynak images/umay-mimarlik.webp (aslında JPEG, beyaz zeminli); media.py beyazı saydama
# çevirip kırpıyor ve assets/img/logo-w*.webp kayıpsız türevlerini üretiyor.
# ⛔ Logoyu elle düzenleme; kaynak değişirse `python3 _src/media.py` yeter.
# ─────────────────────────────────────────────────────────────
LOGO_GEN = [160, 240, 320, 480, 640]


def logo_kilidi(sinif="", sizes="160px"):
    srcset = ", ".join("%s %dw" % (ic("assets/img/logo-w%d.webp" % g), g) for g in LOGO_GEN)
    return ('<img class="logo-im %s" src="%s" srcset="%s" sizes="%s" alt="%s" '
            'width="1560" height="500" decoding="async">') % (
        sinif, ic("assets/img/logo-w320.webp"), srcset, e(sizes), e(D.MARKA))


def w4_imza():
    """Web4Medya tasarım imzası.
    ⚠️ Bağlantı SADECE marka adını sarar — 'Web Tasarım:' etiketi <a> DIŞINDA kalır.
    Rozetin tamamı bağlantı olsaydı site geneli anahtar kelimeli tasarımcı linki doğardı."""
    return """<div class="w4"><div class="w4-bag">
  <span class="w4-etiket">Web Tasarım:</span><a class="w4-ad" href="https://www.web4medya.com/" target="_blank" rel="noopener">Web<span class="w4-d">4</span>Medya</a>
</div></div>"""


def alt_bilgi():
    i = D.ISLETME
    sosyal = ""
    if not bos(i["instagram"]):
        # ⚠️ href ve kullanıcı adı BİRLİKTE doldurulmalı. Eskiden href'teki %s hiç
        # doldurulmuyordu; Instagram yer tutucu olduğu için blok boş üretiliyor ve hata gizleniyordu.
        ig = duz(i["instagram"])
        sosyal = ('<a class="sos" href="%s" target="_blank" rel="noopener">%s<span>@%s</span></a>'
                  % (e(ig), IKON_IG, e(ig.rstrip("/").split("/")[-1])))

    return """<footer class="alt">
  %s
  <div class="alt-kart">
    <div class="alt-logo">%s</div>
    <p class="alt-kisi">%s<br>%s</p>
    <p class="alt-sat">%s</p>
    <p class="alt-sat"><a href="mailto:%s">%s</a></p>
    <p class="alt-sat"><a href="%s">%s</a></p>
    <p class="alt-sos">%s</p>
  </div>
  <div class="alt-serit">
    <p>© %d %s · Tüm hakları saklıdır.</p>
    %s
  </div>
</footer>
<a class="yukari" href="#ana" aria-label="Sayfa başına dön">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>
</a>""" % (
        resim(D.ILETISIM_GORSEL, D.ILETISIM_ALT, "alt-gorsel", "100vw"),
        logo_kilidi("logo-buyuk", sizes="(max-width:520px) 200px, 260px"),
        e(i["kisi"]), e(i["unvan"]),
        m(i["adres"]),
        duz(i["eposta"]), m(i["eposta"]),
        tel_link(), m(i["telefon_yazi"]),
        sosyal,
        YIL, e(D.MARKA),
        w4_imza(),
    )


IKON_IG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2.1.3-.5.2-.9.4-1.2.8-.4.3-.6.7-.8 1.2-.1.4-.3 1-.3 2.1-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c.1 1.1.2 1.7.3 2.1.2.5.4.9.8 1.2.3.4.7.6 1.2.8.4.1 1 .3 2.1.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2.1-.3.5-.2.9-.4 1.2-.8.4-.3.6-.7.8-1.2.1-.4.3-1 .3-2.1.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c-.1-1.1-.2-1.7-.3-2.1-.2-.5-.4-.9-.8-1.2-.3-.4-.7-.6-1.2-.8-.4-.1-1-.3-2.1-.3-1.2-.1-1.6-.1-4.7-.1zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zm6.2-8.3a1.15 1.15 0 1 1-2.3 0 1.15 1.15 0 0 1 2.3 0z"/></svg>')

IKON_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm0 18.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23 4.54 0 8.23 3.69 8.23 8.23s-3.69 8.24-8.23 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.79.97-.14.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.22.25-.85.84-.85 2.04s.87 2.37 1 2.53c.12.16 1.71 2.61 4.14 3.66.58.25 1.03.4 1.38.51.58.19 1.11.16 1.53.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.11-.22-.17-.47-.29z"/></svg>')
IKON_TEL = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2c.28-.28.68-.36 1.04-.25 1.18.39 2.45.6 3.75.6.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.3 21 3 13.7 3 4.5c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.3.21 2.57.6 3.75.11.36.03.76-.25 1.04l-2.23 2.5z"/></svg>')


def dock():
    """Sağ altta alt alta WhatsApp + Hemen Ara."""
    return """<div class="dock">
  <a class="dock-dg dock-wa" href="%s" target="_blank" rel="noopener">
    <span class="dock-ikon">%s</span>WhatsApp'tan Yaz</a>
  <a class="dock-dg dock-ara" href="%s">
    <span class="dock-ikon">%s</span>Hemen Ara</a>
</div>""" % (wa_link(), IKON_WA, tel_link(), IKON_TEL)


def bildirim():
    """%50 kaydırmada açılan çevrimiçi bildirimi. Kapatılınca sessionStorage'a yazılır."""
    return """<aside class="bildirim" aria-live="polite">
  <button class="bildirim-kapat" type="button" aria-label="Bildirimi kapat">&times;</button>
  <p class="bildirim-bas"><span class="nokta" aria-hidden="true"></span>Şu an çevrimiçiyiz.</p>
  <p>Arayın, projeniz hakkında konuşalım.</p>
  <a class="dg dg-ara" href="%s">Hemen Ara</a>
</aside>""" % tel_link()


def cta_serit():
    return """<section class="cta">
  <div class="sinir">
    <h2 class="bolum-bas">%s</h2>
    <p class="cta-metin">%s</p>
    <p class="dugmeler">
      <a class="dg dg-koyu" href="%s" target="_blank" rel="noopener">WhatsApp ile İletişime Geç</a>
      <a class="dg dg-ara" href="%s">Hemen Ara</a>
    </p>
  </div>
</section>""" % (e(D.CTA_BASLIK), e(D.CTA_METIN), wa_link(), tel_link())


def jsonld(anahtar):
    i = D.ISLETME
    veri = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": D.MARKA,
        "url": D.SITE + "/",
        "description": duz(D.SAYFALAR["anasayfa"]["aciklama"]),
        "telephone": i["telefon_tel"],
        "email": duz(i["eposta"]),
        "address": {"@type": "PostalAddress", "streetAddress": duz(i["adres"]),
                    "addressCountry": "TR"},
        "founder": {"@type": "Person", "name": i["kisi"], "jobTitle": i["unvan"]},
        "areaServed": {"@type": "Country", "name": "Türkiye"},
        "knowsAbout": [h["ad"] for h in D.HIZMETLER],
    }
    if not bos(i["instagram"]):
        veri["sameAs"] = [duz(i["instagram"])]
    if anahtar == "hizmetler":
        veri["hasOfferCatalog"] = {
            "@type": "OfferCatalog", "name": "Hizmetler",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": h["ad"],
                                                   "description": h["ozet"]}}
                for h in D.HIZMETLER
            ],
        }
    import json
    return '<script type="application/ld+json">%s</script>' % json.dumps(
        veri, ensure_ascii=False, separators=(",", ":"))


def iskelet(anahtar, govde, ekstra_bas=""):
    s = D.SAYFALAR[anahtar]
    yol = "/" + s["yol"] + ("/" if s["yol"] else "")
    kanonik = D.SITE + yol
    return """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:locale" content="tr_TR">
<meta name="theme-color" content="#DAD5CC">
<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%s">
<link rel="icon" href="%s" sizes="48x48">
<link rel="icon" type="image/png" href="%s" sizes="192x192">
<link rel="apple-touch-icon" href="%s">
%s%s
<script>document.documentElement.className+=' js';</script>
</head>
<body>
%s
<main id="ana">
%s
</main>
%s
%s
%s
<script src="%s" defer></script>
</body>
</html>
""" % (
        e(duz(s["baslik"])), e(duz(s["aciklama"])), kanonik,
        e(D.MARKA), e(duz(s["baslik"])), e(duz(s["aciklama"])), kanonik,
        damga("assets/fonts/pjs-var-tr.woff2"),
        damga("assets/css/site.css"),
        ic("favicon.ico"), ic("favicon-192.png"), ic("favicon-192.png"),
        jsonld(anahtar), ekstra_bas,
        ust(anahtar),
        govde,
        alt_bilgi(),
        dock(),
        bildirim(),
        damga("assets/js/site.js"),
    )


# ─────────────────────────────────────────────────────────────
# Bölümler
# ─────────────────────────────────────────────────────────────
def hero():
    """Kahraman: üst çubuktaki logonun NET BEYAZ sürümü, maskeden yükselerek açılır.
    Not: 2026-09-12'de kısa süre "UG" harflerine döndürüldü, kullanıcı logolu hâlin kalmasını istedi.
    UG'ye dönmek gerekirse: mono-satir + mono-harf + mono-cizgi kalıbı (git geçmişinde)."""
    gen = [160, 240, 320, 480, 640, 900]
    srcset = ", ".join("%s %dw" % (ic("assets/img/logo-beyaz-w%d.webp" % g), g) for g in gen)
    return """<section class="hero">
  %s
  <span class="hero-mono">
    <span class="mono-maske"><img class="hero-logo" src="%s" srcset="%s"
      sizes="(max-width:620px) 74vw, min(46vw, 620px)" alt="%s"
      width="1560" height="500" fetchpriority="high" decoding="async"></span>
  </span>
</section>""" % (resim(D.HERO_GORSEL, D.HERO_ALT, "hero-gorsel", "100vw", oncelik=True),
                 ic("assets/img/logo-beyaz-w640.webp"), srcset, e(D.MARKA))


def proje_bloklari(projeler, baslik=None):
    """Görselin üzerine kayan kartlar — şablondaki 'Our Featured Projects.' düzeni.
    Kartlar sırayla dolu beyaz / çerçeveli olarak değişir (şablonda ikisi de var)."""
    parcalar = []
    if baslik:
        parcalar.append('<h2 class="bolum-bas">%s</h2>' % e(baslik))
    for idx, p in enumerate(projeler):
        yon = "sag" if idx % 2 else "sol"
        cerce = " kart-cerceve" if idx % 3 == 2 else ""
        detay = " · ".join(x for x in [duz(p["kategori"]), duz(p["konum"]), duz(p["yil"])] if x)
        parcalar.append("""<article class="proje %s">
  <div class="proje-gorsel">%s</div>
  <div class="proje-kart%s">
    <h3>%s</h3>
    <span class="kural"></span>
    <p>%s</p>
    <p class="proje-detay">%s</p>
    <span class="ok" aria-hidden="true"><svg viewBox="0 0 64 12"><path d="M0 6h58M52 1l6 5-6 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></span>
  </div>
</article>""" % (yon,
                 resim(p["gorsel"], duz(p["alt"]), "", "(min-width:900px) 60vw, 100vw"),
                 cerce, m(p["ad"]), m(p["ozet"]), e(detay)))
    return '<section class="projeler-bolum"><div class="sinir">%s</div></section>' % "".join(parcalar)


def hizmet_bloklari(tam=False):
    parcalar = []
    for h in D.HIZMETLER:
        gorsel = ""
        if tam and h.get("gorsel"):
            gorsel = '<figure class="hizmet-gorsel">%s<figcaption>%s</figcaption></figure>' % (
                resim(h["gorsel"], h.get("gorsel_alt", h["ad"]), "", "(min-width:900px) 55vw, 100vw"),
                e(h.get("gorsel_alt", h["ad"])))
        govde = "".join("<p>%s</p>" % m(x) for x in h["metin"]) if tam else "<p>%s</p>" % m(h["ozet"])
        parcalar.append("""<article class="hizmet%s" id="%s">
  <div class="hizmet-metin">
    <span class="hizmet-no">%s</span>
    <h3>%s</h3>
    <span class="kural"></span>
    %s
  </div>
  %s
</article>""" % ("" if gorsel else " hizmet-tek", e(h["slug"]), e(h["no"]),
                 e(h["ad"]), govde, gorsel))
    return "".join(parcalar)


def neden_bloklari():
    kartlar = "".join(
        '<div class="neden-kart"><h3>%s</h3><span class="kural"></span><p>%s</p></div>' % (
            e(n["ad"]), e(n["metin"]))
        for n in D.NEDEN)
    return """<section class="neden">
  <div class="sinir">
    <h2 class="bolum-bas">%s</h2>
    <div class="neden-izgara">%s</div>
  </div>
</section>""" % (e(D.NEDEN_BASLIK), kartlar)


def giris_bloklari(kisa=False):
    paragraflar = D.GIRIS[:2] if kisa else D.GIRIS
    return "".join("<p>%s</p>" % m(x) for x in paragraflar)


# ─────────────────────────────────────────────────────────────
# Sayfalar
# ─────────────────────────────────────────────────────────────
def sayfa_anasayfa():
    govde = (
        hero()
        + """<section class="giris">
  <div class="sinir dar">
    <h1 class="bolum-bas">%s</h1>
    <p class="ust-baslik">%s · %s</p>
    <div class="metin">%s</div>
    <p class="dugmeler"><a class="dg" href="%shakkimda/">Hakkımda</a><a class="dg dg-koyu" href="%shizmetler/">Hizmetler</a></p>
  </div>
</section>""" % (e(D.SAYFALAR["anasayfa"]["h1"]), e(D.ISLETME["unvan"]), e(D.ISLETME["kisi"]),
                 giris_bloklari(kisa=True), ic(), ic())
        + proje_bloklari(D.PROJELER[:3], "Öne Çıkan Projeler.")
        + '<p class="orta-baglanti"><a class="dg" href="%sprojeler/">Tüm Projeler</a></p>' % ic()
        + """<section class="hizmetler-bolum">
  <div class="sinir">
    <h2 class="bolum-bas">Uzmanlık Alanlarım.</h2>
    <div class="hizmet-akis">%s</div>
    <p class="orta-baglanti"><a class="dg" href="%shizmetler/">Hizmet Detayları</a></p>
  </div>
</section>""" % (hizmet_bloklari(tam=False), ic())
        + neden_bloklari()
        + cta_serit()
    )
    return iskelet("anasayfa", govde)


def sayfa_hakkimda():
    govde = """<section class="sayfa-bas">
  <div class="sinir dar">
    <h1 class="bolum-bas">%s</h1>
    <p class="ust-baslik">%s · %s</p>
  </div>
</section>
<section class="giris">
  <div class="sinir dar">
    <h2 class="bolum-bas sol-bas">%s</h2>
    <div class="metin">%s</div>
  </div>
</section>
%s
%s""" % (e(D.SAYFALAR["hakkimda"]["h1"]), e(D.ISLETME["unvan"]), e(D.ISLETME["kisi"]),
         e(D.GIRIS_BASLIK), giris_bloklari(), neden_bloklari(), cta_serit())
    return iskelet("hakkimda", govde)


def sayfa_hizmetler():
    govde = """<section class="sayfa-bas">
  <div class="sinir dar">
    <h1 class="bolum-bas">%s</h1>
  </div>
</section>
<section class="hizmetler-bolum tam">
  <div class="sinir">%s</div>
</section>
%s
%s""" % (e(D.SAYFALAR["hizmetler"]["h1"]), hizmet_bloklari(tam=True), neden_bloklari(), cta_serit())
    return iskelet("hizmetler", govde)


def sayfa_projeler():
    govde = """<section class="sayfa-bas">
  <div class="sinir dar">
    <h1 class="bolum-bas">%s</h1>
  </div>
</section>
%s
%s""" % (e(D.SAYFALAR["projeler"]["h1"]), proje_bloklari(D.PROJELER), cta_serit())
    return iskelet("projeler", govde)


def sayfa_iletisim():
    i = D.ISLETME
    satirlar = [
        ("Telefon", '<a href="%s">%s</a>' % (tel_link(), m(i["telefon_yazi"]))),
        ("WhatsApp", '<a href="%s" target="_blank" rel="noopener">Mesaj gönder</a>' % wa_link()),
        ("E-posta", '<a href="mailto:%s">%s</a>' % (duz(i["eposta"]), m(i["eposta"]))),
        ("Adres", m(i["adres"])),
        ("Çalışma Saatleri", m(i["calisma"])),
    ]
    if not bos(i["harita_url"]):
        satirlar.append(("Yol Tarifi",
                         '<a href="%s" target="_blank" rel="noopener">Haritada aç</a>' % duz(i["harita_url"])))
    liste = "".join('<div class="ilt-satir"><dt>%s</dt><dd>%s</dd></div>' % (e(a), b)
                    for a, b in satirlar)
    govde = """<section class="sayfa-bas">
  <div class="sinir dar">
    <h1 class="bolum-bas">%s</h1>
    <p class="cta-metin">%s</p>
  </div>
</section>
<section class="iletisim">
  <div class="sinir dar">
    <dl class="ilt">%s</dl>
    <p class="dugmeler">
      <a class="dg dg-koyu" href="%s" target="_blank" rel="noopener">WhatsApp ile İletişime Geç</a>
      <a class="dg dg-ara" href="%s">Hemen Ara</a>
    </p>
  </div>
</section>""" % (e(D.SAYFALAR["iletisim"]["h1"]), e(D.CTA_METIN), liste, wa_link(), tel_link())
    return iskelet("iletisim", govde)


# ─────────────────────────────────────────────────────────────
# Yardımcı dosyalar
# ─────────────────────────────────────────────────────────────
def sitemap():
    satir = []
    for anahtar in D.MENU_SIRA:
        s = D.SAYFALAR[anahtar]
        yol = "/" + s["yol"] + ("/" if s["yol"] else "")
        satir.append("  <url><loc>%s%s</loc></url>" % (D.SITE, yol))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
            % "\n".join(satir))


def robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % D.SITE


def sayfa_404():
    govde = """<section class="sayfa-bas dort">
  <div class="sinir dar">
    <h1 class="bolum-bas">Sayfa bulunamadı.</h1>
    <p class="cta-metin">Aradığınız sayfa taşınmış veya kaldırılmış olabilir.</p>
    <p class="dugmeler"><a class="dg dg-koyu" href="%s">Ana Sayfa</a><a class="dg" href="%siletisim/">İletişim</a></p>
  </div>
</section>""" % (ic(), ic())
    # 404 menüde yok; iskeleti anasayfa anahtarıyla kurup başlığı değiştiriyoruz.
    cikti = iskelet("anasayfa", govde)
    cikti = cikti.replace("<title>%s</title>" % e(duz(D.SAYFALAR["anasayfa"]["baslik"])),
                          "<title>Sayfa bulunamadı | %s</title>" % e(D.MARKA))
    cikti = cikti.replace('<link rel="canonical" href="%s/">\n' % D.SITE, "")
    return cikti.replace("</head>", '<meta name="robots" content="noindex">\n</head>')


# ─────────────────────────────────────────────────────────────
def yaz(gorece, icerik):
    yol = os.path.join(KOK, gorece)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)
    return len(icerik.encode("utf-8"))


def main():
    # CSS/JS önce yazılır: damga() bunların SHA1'ini okuyor.
    from varliklar import CSS, JS
    yaz("assets/css/site.css", CSS)
    yaz("assets/js/site.js", JS)

    ciktilar = {
        "index.html": sayfa_anasayfa,
        "hakkimda/index.html": sayfa_hakkimda,
        "hizmetler/index.html": sayfa_hizmetler,
        "projeler/index.html": sayfa_projeler,
        "iletisim/index.html": sayfa_iletisim,
        "404.html": sayfa_404,
    }
    global ONEK
    toplam = 0
    for yol, fn in ciktilar.items():
        derinlik = yol.count("/")
        # 404 her derinlikteki URL için servis edilir → göreli yol tutmaz, kök-mutlak kalır.
        ONEK = "/" if yol == "404.html" else "../" * derinlik
        n = yaz(yol, fn())
        toplam += n
        print("  %-26s onek=%-6s %6.1f KB" % (yol, repr(ONEK), n / 1024))
    ONEK = ""

    yaz("sitemap.xml", sitemap())
    yaz("robots.txt", robots())
    if not os.path.exists(os.path.join(KOK, ".nojekyll")):
        open(os.path.join(KOK, ".nojekyll"), "w").close()

    print("\n%d sayfa · %.1f KB HTML" % (len(ciktilar), toplam / 1024))
    if PH_SAYAC:
        benzersiz = sorted(set(PH_SAYAC))
        print("\n⏳ %d yer tutucu (%d benzersiz) — kullanıcıdan bekleniyor:" % (
            len(PH_SAYAC), len(benzersiz)))
        for x in benzersiz:
            print("   · %s" % x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
