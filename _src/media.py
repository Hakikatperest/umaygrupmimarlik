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


def slug(dosya):
    """'2.webp.jpeg' -> '2', 'akustik-analiz.webp' -> 'akustik-analiz'"""
    return os.path.basename(dosya).split(".")[0]


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
        if not os.path.isfile(yol) or ad.startswith("."):
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

    print("\n%d kaynak · %.1f MB -> %.1f MB türev" % (
        sayi, toplam_kaynak / 1048576, toplam_hedef / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(uret())
