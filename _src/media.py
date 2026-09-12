# -*- coding: utf-8 -*-
"""
Görsel boru hattı — images/ altındaki kaynaklardan assets/img/ altına WebP türevleri üretir.

Yalnızca GÖRSEL değiştiğinde çalıştır:  python3 _src/media.py

⚠️ Pillow ile üretiliyor, cwebp ile DEĞİL. Varsayılan cwebp ayarı (-m 6 -pass 10) görsel başına
   saniyeler yer ve dosyayı büyütebiliyor — bkz. reference_medialibrary_cwebp_optimizer.
⚠️ images/ altındaki bazı dosyaların uzantısı yanıltıcı (.webp ama içerik PNG/JPEG).
   Pillow içeriğe bakarak açtığı için uzantıya güvenmiyoruz.
"""
import os
import sys

from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, "images")
HEDEF = os.path.join(KOK, "assets", "img")

GENISLIKLER = [480, 800, 1200, 1600]
KALITE = 82

# Logo genel akışın dışında işlenir: beyaz zemini saydama çevrilir, kırpılır, kayıpsız kaydedilir.
LOGO_KAYNAK = "umay-mimarlik.webp"
LOGO_GENISLIKLER = [160, 240, 320, 480, 640]
LOGO_RENK = (0x48, 0x58, 0x4D)      # logonun kendi yeşili — marka varlığı, değiştirme
LOGO_ISARET_KUTU = (256, 117, 712, 596)   # yalnız ev işareti (favicon için)
FAVI_ZEMIN = (0x3B, 0x3C, 0x39)
FAVI_CIZGI = (0xF2, 0xF0, 0xEB)


def slug(dosya):
    """'2.webp.jpeg' -> '2', 'akustik-analiz.webp' -> 'akustik-analiz'"""
    return os.path.basename(dosya).split(".")[0]


def _boya(logo, renk):
    """Saydam logoyu tek renge boyar (alfa korunur) — kahraman için beyaz sürüm."""
    yeni = Image.new("RGBA", logo.size, renk + (255,))
    yeni.putalpha(logo.getchannel("A"))
    return yeni


def _saydamlastir(im):
    """Beyaz zeminli, tek tonlu çizgi logosunu saydam alfaya çevirir.

    ⚠️ Kaynak JPEG olduğu için kenarlar beyaza karşı yumuşatılmış. Pikseli olduğu gibi
    maskelemek beyaz hale bırakır. Bunun yerine parlaklıktan alfa türetip RENGİ SABİT
    logo rengine çekiyoruz — kenarlar temiz kalıyor, beyaz saçak oluşmuyor.
    """
    im = im.convert("RGB")
    gri = im.convert("L")
    L0 = int(0.299 * LOGO_RENK[0] + 0.587 * LOGO_RENK[1] + 0.114 * LOGO_RENK[2])
    lut = [max(0, min(255, round(255 * (255 - L) / (255 - L0)))) for L in range(256)]
    alfa = gri.point(lut)
    duz = Image.new("RGB", im.size, LOGO_RENK)
    duz.putalpha(alfa)
    return duz


def _kirp(im, pay=6):
    """Saydam kenar payını atar, çevresine küçük bir nefes payı bırakır."""
    kutu = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if not kutu:
        return im
    x1, y1, x2, y2 = kutu
    return im.crop((max(0, x1 - pay), max(0, y1 - pay),
                    min(im.width, x2 + pay), min(im.height, y2 + pay)))


def logo_uret(kok):
    kaynak = os.path.join(KAYNAK, LOGO_KAYNAK)
    if not os.path.isfile(kaynak):
        print("  ⚠️ logo kaynağı yok:", LOGO_KAYNAK)
        return
    ham = Image.open(kaynak)
    logo = _kirp(_saydamlastir(ham))
    print("  %-28s %dx%d -> saydam, kırpılmış %dx%d (oran %.2f:1)" % (
        LOGO_KAYNAK, ham.width, ham.height, logo.width, logo.height, logo.width / logo.height))

    for g in LOGO_GENISLIKLER:
        if g > logo.width:
            continue
        yeni = logo.resize((g, round(logo.height * g / logo.width)), Image.LANCZOS)
        yeni.save(os.path.join(HEDEF, "logo-w%d.webp" % g), "WEBP", lossless=True, method=4)
    print("     türevler: %s" % ", ".join("w%d" % g for g in LOGO_GENISLIKLER if g <= logo.width))

    # Kahraman fotoğrafının üzerinde kullanılan NET BEYAZ sürüm
    beyaz = _boya(logo, (255, 255, 255))
    for g in LOGO_GENISLIKLER + [900]:
        if g > logo.width:
            continue
        yeni = beyaz.resize((g, round(beyaz.height * g / beyaz.width)), Image.LANCZOS)
        yeni.save(os.path.join(HEDEF, "logo-beyaz-w%d.webp" % g), "WEBP", lossless=True, method=4)
    print("     beyaz sürüm: %s" % ", ".join(
        "w%d" % g for g in LOGO_GENISLIKLER + [900] if g <= logo.width))

    # ── Favicon: yalnız ev işareti, kurum zeminli kare ────────
    # ⚠️ Google WebP favicon'u YOK SAYAR; kare ve 48'in katı ICO/PNG şart.
    isaret = _kirp(_saydamlastir(ham.crop(LOGO_ISARET_KUTU)), pay=0)
    for boy in (48, 96, 192):
        kenar = round(boy * 0.62)                       # işaret kenarlardan nefes alsın
        olcek = min(kenar / isaret.width, kenar / isaret.height)
        i2 = isaret.resize((max(1, round(isaret.width * olcek)),
                            max(1, round(isaret.height * olcek))), Image.LANCZOS)
        # işareti krem renge boya (kurum zemin üzerinde)
        boyali = Image.new("RGBA", i2.size, FAVI_CIZGI + (255,))
        boyali.putalpha(i2.getchannel("A"))
        kare = Image.new("RGBA", (boy, boy), FAVI_ZEMIN + (255,))
        kare.paste(boyali, ((boy - i2.width) // 2, (boy - i2.height) // 2), boyali)
        kare.convert("RGB").save(os.path.join(kok, "favicon-%d.png" % boy), "PNG", optimize=True)
    # ICO: 48 + 96 birlikte
    Image.open(os.path.join(kok, "favicon-96.png")).save(
        os.path.join(kok, "favicon.ico"), sizes=[(48, 48), (96, 96)])
    print("     favicon: favicon.ico (48+96) · favicon-48/96/192.png")


def uret():
    os.makedirs(HEDEF, exist_ok=True)
    if not os.path.isdir(KAYNAK):
        print("images/ klasörü yok", file=sys.stderr)
        return 1

    toplam_kaynak = 0
    toplam_hedef = 0
    sayi = 0

    for ad in sorted(os.listdir(KAYNAK)):
        yol = os.path.join(KAYNAK, ad)
        if not os.path.isfile(yol) or ad.startswith(".") or ad == LOGO_KAYNAK:
            continue
        try:
            im = Image.open(yol)
        except Exception:
            continue  # görsel değil

        im = im.convert("RGB")
        s = slug(ad)
        gen_asil = im.width
        toplam_kaynak += os.path.getsize(yol)

        # ⚠️ BÜYÜTME YOK — kaynaktan geniş türev üretmek dosyayı şişirir, netlik kazandırmaz.
        hedefler = [g for g in GENISLIKLER if g < gen_asil]
        # Kaynağın kendi genişliği de bir türev olsun; yoksa 640 px'lik bir kaynaktan yalnızca
        # w480 üretilip elde olan çözünürlüğün bir kısmı boşa gidiyor. Zaten üretilmiş en büyük
        # türeve çok yakınsa (<%15 fark) eklemiyoruz — neredeyse aynı dosyayı iki kez taşımayalım.
        if not hedefler or gen_asil > hedefler[-1] * 1.15:
            hedefler.append(gen_asil)

        uretilen = []
        for g in hedefler:
            if g == gen_asil:
                yeni = im
            else:
                yeni = im.resize((g, round(im.height * g / gen_asil)), Image.LANCZOS)
            cikti = os.path.join(HEDEF, "%s-w%d.webp" % (s, g))
            yeni.save(cikti, "WEBP", quality=KALITE, method=4)
            toplam_hedef += os.path.getsize(cikti)
            uretilen.append(g)

        sayi += 1
        print("  %-28s %4dx%-4d -> %s" % (ad, im.width, im.height,
                                          ", ".join("w%d" % g for g in uretilen)))

    logo_uret(KOK)

    print("\n%d kaynak · %.1f MB -> %.1f MB türev" % (
        sayi, toplam_kaynak / 1048576, toplam_hedef / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(uret())
