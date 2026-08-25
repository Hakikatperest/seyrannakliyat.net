#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logo türevlerini üretir.

Kaynak `images/seyran-nakliyat-logo.png` (1536x1024, şeffaf zemin, 1,1 MB)
sitede DOĞRUDAN kullanılmaz — çok ağır. Buradan iki varyant çıkar:

  logo/seyran-logo.webp       açık zemin için (özgün renkler: lacivert + turuncu)
  logo/seyran-logo-acik.webp  koyu zemin için (lacivert yazı beyaza çevrilir)

Koyu zemin varyantı şart: alt bilgi lacivert ve özgün logodaki lacivert
"SEYRAN" yazısı orada tamamen kayboluyor.
"""
import os
from PIL import Image

KOK = os.path.join(os.path.dirname(__file__), '..')
KAYNAK = os.path.join(KOK, 'images', 'seyran-nakliyat-logo.png')
HEDEF = os.path.join(KOK, 'images', 'logo')
GENISLIKLER = [180, 280, 420]

def turuncu_mu(r, g, b):
    """Turuncu marka rengi mi — koyu zemin varyantında korunacak."""
    return r > 110 and r > b + 40

def acik_varyant(im):
    """Lacivert olan her şeyi beyaza çevir, turuncuyu koru."""
    im = im.copy()
    px = im.load()
    W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if not turuncu_mu(r, g, b):
                px[x, y] = (255, 255, 255, a)
    return im

def main():
    os.makedirs(HEDEF, exist_ok=True)
    im = Image.open(KAYNAK).convert('RGBA')
    im = im.crop(im.getbbox())                   # şeffaf kenar boşluklarını at
    print('  kırpıldı: %dx%d' % im.size)

    acik = acik_varyant(im)

    for ad, kaynak in (('seyran-logo', im), ('seyran-logo-acik', acik)):
        for g in GENISLIKLER:
            oran = g / kaynak.width
            k = kaynak.resize((g, max(1, round(kaynak.height * oran))), Image.LANCZOS)
            for uzanti, kayit in (('webp', dict(format='WEBP', quality=88, method=4)),
                                  ('png', dict(format='PNG', optimize=True))):
                yol = os.path.join(HEDEF, '%s-%d.%s' % (ad, g, uzanti))
                k.save(yol, **kayit)
            print('    %-22s w%-4d %5.0f KB (webp)' % (
                ad, g, os.path.getsize(os.path.join(HEDEF, '%s-%d.webp' % (ad, g))) / 1024))

    # Favicon: yalnızca "S" işareti (logonun üst bölümü)
    ust = im.crop((0, 0, im.width, int(im.height * 0.47)))
    ust = ust.crop(ust.getbbox())
    kare = max(ust.size)
    tuval = Image.new('RGBA', (kare, kare), (0, 0, 0, 0))
    tuval.alpha_composite(ust, ((kare - ust.width) // 2, (kare - ust.height) // 2))
    for boy in (180, 512):
        tuval.resize((boy, boy), Image.LANCZOS).save(
            os.path.join(HEDEF, 'isaret-%d.png' % boy), format='PNG', optimize=True)
    print('    isaret-180/512.png üretildi (%dx%d kaynak)' % ust.size)

if __name__ == '__main__':
    main()
