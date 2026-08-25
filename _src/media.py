#!/usr/bin/env python3
"""
Görsel türevlerini üretir (WebP, birden çok genişlik).

Kaynak JPEG'ler images/ altında durur ve DEĞİŞTİRİLMEZ; türevler
images/w<genişlik>/ altına yazılır. HTML <picture> ile önce WebP'yi,
desteklenmiyorsa özgün JPEG'i kullanır.

Not: cwebp'nin varsayılan `-m 6 -pass 10` ayarı görsel başına saniyeler
harcayıp dosyayı bazen BÜYÜTÜYOR; bu yüzden kodlama Pillow ile yapılıyor
(method=4, quality=80). EXIF yönü de burada sabitlenir.
"""
import os, glob
from PIL import Image, ImageOps

KOK = os.path.join(os.path.dirname(__file__), '..')
KAYNAK = os.path.join(KOK, 'images')
GENISLIKLER = [1600, 1200, 900, 768, 600, 400]
KALITE = 80

def main():
    toplam_kaynak = toplam_uretilen = 0
    for yol in sorted(glob.glob(os.path.join(KAYNAK, '*.jpeg'))):
        ad = os.path.splitext(os.path.basename(yol))[0]
        im = ImageOps.exif_transpose(Image.open(yol)).convert('RGB')
        toplam_kaynak += os.path.getsize(yol)
        print('  %-24s %dx%d' % (ad, im.width, im.height))

        for g in GENISLIKLER:
            if g > im.width:
                continue
            hedef_dizin = os.path.join(KAYNAK, 'w%d' % g)
            os.makedirs(hedef_dizin, exist_ok=True)
            hedef = os.path.join(hedef_dizin, ad + '.webp')
            oran = g / im.width
            yeni = im.resize((g, max(1, round(im.height * oran))), Image.LANCZOS)
            yeni.save(hedef, 'WEBP', quality=KALITE, method=4)
            boyut = os.path.getsize(hedef)
            toplam_uretilen += boyut
            print('      w%-5d %7.0f KB' % (g, boyut / 1024))

        # Özgün genişlik listede yoksa tam boy WebP de üret (hero için).
        if im.width not in GENISLIKLER and im.width < min(GENISLIKLER):
            hedef_dizin = os.path.join(KAYNAK, 'w%d' % im.width)
            os.makedirs(hedef_dizin, exist_ok=True)
            hedef = os.path.join(hedef_dizin, ad + '.webp')
            im.save(hedef, 'WEBP', quality=KALITE, method=4)
            print('      w%-5d %7.0f KB (özgün)' % (im.width, os.path.getsize(hedef) / 1024))

    print('\n  kaynak toplam    : %.1f MB' % (toplam_kaynak / 1048576))
    print('  türev toplam     : %.1f MB' % (toplam_uretilen / 1048576))

if __name__ == '__main__':
    main()
