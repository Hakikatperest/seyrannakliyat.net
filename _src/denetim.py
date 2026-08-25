# -*- coding: utf-8 -*-
"""Üretilen siteyi denetler: bağlantılar, varlıklar, JSON-LD, başlık tekrarı."""
import os, re, json, glob, sys, gzip
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
hata = []

sayfalar = ['index.html', '404.html'] + sorted(glob.glob('*-evden-eve-nakliyat/index.html', root_dir=KOK))
print('Sayfa sayısı:', len(sayfalar))

basliklar, aciklamalar, kanonikler = {}, {}, {}
tum_baglar = set()

for sp in sayfalar:
    h = open(os.path.join(KOK, sp), encoding='utf-8').read()

    t = re.search(r'<title>(.*?)</title>', h, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', h, re.S)
    c = re.search(r'<link rel="canonical" href="(.*?)">', h)
    if not t: hata.append(sp + ': title yok')
    if not d: hata.append(sp + ': description yok')
    if not c: hata.append(sp + ': canonical yok')
    if t: basliklar.setdefault(t.group(1), []).append(sp)
    if d: aciklamalar.setdefault(d.group(1), []).append(sp)
    if c: kanonikler.setdefault(c.group(1), []).append(sp)

    if h.count('<h1') != 1: hata.append('%s: %d adet h1' % (sp, h.count('<h1')))

    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(m.group(1))
        except Exception as ex: hata.append('%s: JSON-LD bozuk — %s' % (sp, ex))

    for m in re.finditer(r'(?:href|src|data-video|data-poster)="(/[^"#]*)"', h):
        tum_baglar.add(m.group(1).split('?')[0])   # ?v= sürüm damgasını at

    for m in re.finditer(r'srcset="([^"]+)"', h):
        for p in m.group(1).split(','):
            u = p.strip().split(' ')[0]
            if u.startswith('/'): tum_baglar.add(u)

    if 'alt=""' in h: hata.append(sp + ': boş alt var')
    for m in re.finditer(r'https?://(?!seyrannakliyat\.net|wa\.me|www\.google\.com/maps)([a-z0-9.\-]+)', h):
        if m.group(1) not in ('schema.org', 'www.w3.org'):
            hata.append('%s: dış kaynak %s' % (sp, m.group(1)))

print('\nYinelenen başlık:', [v for v in basliklar.values() if len(v) > 1] or 'yok')
print('Yinelenen açıklama:', [v for v in aciklamalar.values() if len(v) > 1] or 'yok')
print('Yinelenen canonical:', [v for v in kanonikler.values() if len(v) > 1] or 'yok')

print('\nBağlantı hedefleri:', len(tum_baglar))
kirik = []
for b in sorted(tum_baglar):
    yol = os.path.join(KOK, b.lstrip('/'))
    if b.endswith('/'): yol = os.path.join(yol, 'index.html')
    if not os.path.exists(yol): kirik.append(b)
print('Kırık bağlantı:', kirik or 'yok')
if kirik: hata.extend('kırık: ' + k for k in kirik)

# ağırlık
def gz(p):
    return len(gzip.compress(open(p, 'rb').read(), 6))
ana = os.path.join(KOK, 'index.html')
css = os.path.join(KOK, 'assets/style.css')
js  = os.path.join(KOK, 'assets/app.js')
font= os.path.join(KOK, 'assets/fonts/pjs-var-tr.woff2')
hero= os.path.join(KOK, 'images/w900/seyran-nakliyat.webp')
print('\n── İlk açılış ağırlığı (gzip) ──')
for ad, p in [('index.html', ana), ('style.css', css), ('app.js', js)]:
    print('  %-14s %6.1f KB' % (ad, gz(p) / 1024))
print('  %-14s %6.1f KB (zaten sıkıştırılmış)' % ('font woff2', os.path.getsize(font) / 1024))
print('  %-14s %6.1f KB (hero, w900)' % ('görsel', os.path.getsize(hero) / 1024))
toplam = (gz(ana) + gz(css) + gz(js) + os.path.getsize(font) + os.path.getsize(hero)) / 1024
print('  ────────────────────────')
print('  TOPLAM         %6.1f KB' % toplam)

ilce = os.path.join(KOK, 'fatih-evden-eve-nakliyat/index.html')
print('  ilçe sayfası   %6.1f KB (gzip HTML; CSS/JS/font önbellekten)' % (gz(ilce) / 1024))

print('\n%s' % ('TÜMÜ GEÇTİ' if not hata else 'SORUN (%d):' % len(hata)))
for x in hata[:20]: print('  ✗', x)
sys.exit(1 if hata else 0)
