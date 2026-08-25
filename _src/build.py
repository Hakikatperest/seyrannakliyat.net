#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seyran Nakliyat — site üreticisi.

  python3 _src/build.py

Ana sayfa + 25 ilçe sayfası + sitemap/robots/404 üretir.

⛔ Üretilen HTML dosyalarını ELLE DÜZENLEME — bir sonraki derlemede silinir.
   Değişiklik data.py ya da bu dosyada yapılır.

Tasarım/performans kuralları:
  · Üçüncü parti istek YOK (font, ikon, harita, analitik hepsi yerel/erteli).
  · CSS ve JS ayrı dosya: 26 sayfa aynı dosyayı paylaşır, bir kez önbelleğe girer.
  · Video ve Google Haritalar tıklanana kadar tek bayt indirmez.
  · Görseller <picture> + srcset ile boyuta göre servis edilir.
"""
import os, sys, re, html, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import FIRMA, OZELLIKLER, HIZMETLER, ILCELER, SSS, ADIMLAR, IPUCU

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = FIRMA['site']

# ── Komşuluk grafiğini simetrikleştir ────────────────────────────────────────
# Veride birkaç bağ tek yönlü yazılmış; sayfa içi linkleme çift yönlü olmalı ki
# her ilçe kendi komşusundan da link alsın.
KOMSU = {s: set(v[2]) for s, v in ILCELER.items()}
for s, ks in list(KOMSU.items()):
    for k in ks:
        KOMSU[k].add(s)

# ── İkonlar (satır içi SVG — ikon fontu yok) ─────────────────────────────────
IK = {
'telefon': '<path d="M6.6 2.5 3.9 3.4a2 2 0 0 0-1.3 2.2c.6 4.1 2.4 7.6 5.3 10.5s6.4 4.7 10.5 5.3a2 2 0 0 0 2.2-1.3l.9-2.7a1.4 1.4 0 0 0-.7-1.7l-3.3-1.6a1.4 1.4 0 0 0-1.6.3l-1.2 1.2a13.7 13.7 0 0 1-5.2-5.2l1.2-1.2a1.4 1.4 0 0 0 .3-1.6L8.3 3.2a1.4 1.4 0 0 0-1.7-.7Z"/>',
'wa': '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2Zm5.1 14c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1a12.6 12.6 0 0 1-6.4-5.7c-.5-.9-.7-1.7-.5-2.5.1-.5.5-1 .8-1.3.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.4l.8 1.9c.1.2 0 .4-.1.6l-.4.5c-.1.2-.3.3-.1.6a9.2 9.2 0 0 0 3.6 3.1c.3.1.5.1.6-.1l.7-.8c.2-.2.4-.2.6-.1l1.8.9c.3.1.4.3.4.5s0 .6-.3 1.2Z"/>',
'kalkan': '<path d="M12 2 4 5.2v6c0 4.7 3.3 9.1 8 10.8 4.7-1.7 8-6.1 8-10.8v-6L12 2Zm3.6 7.3-4.4 4.5a1 1 0 0 1-1.4 0L8 12a1 1 0 0 1 1.4-1.4l1.1 1.1 3.7-3.8a1 1 0 1 1 1.4 1.4Z"/>',
'kutu': '<path d="M12 2 3 6.4v11.2L12 22l9-4.4V6.4L12 2Zm0 2.2 6.2 3-2.3 1.1L9.7 5.3 12 4.2ZM7.5 6.3l6.2 3-1.7.8-6.2-3 1.7-.8ZM5 8.6l6 2.9v7.8l-6-2.9V8.6Zm8 10.7v-7.8l6-2.9v7.8l-6 2.9Z"/>',
'ekip': '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm7.5.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM9 13c-3.9 0-7 2-7 4.5V21h14v-3.5C16 15 12.9 13 9 13Zm7.5.5c-.7 0-1.4.1-2 .3 1.3 1.1 2 2.5 2 4v3.2H23v-3c0-2.3-2.9-4.5-6.5-4.5Z"/>',
'saat': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 10.6 3.4 2a1 1 0 1 1-1 1.7l-3.9-2.3a1 1 0 0 1-.5-.9V6.5a1 1 0 0 1 2 0v6.1Z"/>',
'kamyon': '<path d="M3 5.5A1.5 1.5 0 0 1 4.5 4h9A1.5 1.5 0 0 1 15 5.5V7h2.7c.5 0 1 .2 1.2.6l2 3c.1.2.1.4.1.6V16a1.5 1.5 0 0 1-1.5 1.5h-1.1a3 3 0 0 1-5.8 0H9.5a3 3 0 0 1-5.8 0H3a1.5 1.5 0 0 1-1.5-1.5V5.5H3Zm12 3.5v3.5h4.2L17.2 9H15ZM6.6 16.5a1.2 1.2 0 1 0 2.4 0 1.2 1.2 0 0 0-2.4 0Zm8.4 0a1.2 1.2 0 1 0 2.4 0 1.2 1.2 0 0 0-2.4 0Z"/>',
'pusula': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm3.8 5.4-2.3 5.3a1 1 0 0 1-.5.5l-5.3 2.3a.6.6 0 0 1-.8-.8l2.3-5.3a1 1 0 0 1 .5-.5l5.3-2.3a.6.6 0 0 1 .8.8ZM12 10.7a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6Z"/>',
'pin': '<path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/>',
'ok': '<path d="M9 5.5 15.5 12 9 18.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
'oynat': '<path d="M8 5.1v13.8c0 .8.9 1.3 1.6.9l11-6.9a1.1 1.1 0 0 0 0-1.8l-11-6.9A1.1 1.1 0 0 0 8 5.1Z"/>',
'harita': '<path d="M15 4 9 6 4.4 4.4A1 1 0 0 0 3 5.3v12.4a1 1 0 0 0 .7 1L9 20.5l6-2 4.6 1.6a1 1 0 0 0 1.4-1V6.7a1 1 0 0 0-.7-1L15 4Zm-6 2.3 6 2v9.4l-6-2V6.3Z"/>',
'saat2': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm4.3 6.3-5.6 5.6a1 1 0 0 1-1.4 0l-2.6-2.6a1 1 0 1 1 1.4-1.4l1.9 1.9 4.9-4.9a1 1 0 1 1 1.4 1.4Z"/>',
'ev': '<path d="M12 2.6 2.5 10.3a1 1 0 0 0 .6 1.8H5v8a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-8h1.9a1 1 0 0 0 .6-1.8L12 2.6Z"/>',
'ofis': '<path d="M4 3h9a1 1 0 0 1 1 1v6h6a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm2 3v2h2V6H6Zm4 0v2h2V6h-2ZM6 10v2h2v-2H6Zm4 0v2h2v-2h-2Zm-4 4v2h2v-2H6Zm4 0v2h2v-2h-2Zm6-2v2h2v-2h-2Zm0 4v2h2v-2h-2Z"/>',
'asansor': '<path d="M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Zm3.5 4.2L7.2 9.4h4.6L9.5 6.2Zm5 11.6 2.3-3.2h-4.6l2.3 3.2ZM8 12h8v1.6H8V12Z"/>',
'depo': '<path d="M12 2 2 7v14h6v-7h8v7h6V7L12 2Zm-2 14v5h4v-5h-4Z"/>',
'yol': '<path d="M9.5 3h5l1.6 18H7.9L9.5 3Zm2 3v3h1V6h-1Zm0 5.5v3h1v-3h-1Zm0 5.5v3h1v-3h-1Z"/>',
'yildiz': '<path d="m12 2.8 2.8 5.7 6.3.9-4.6 4.4 1.1 6.2L12 17.1l-5.6 3 1.1-6.2L2.9 9.4l6.3-.9L12 2.8Z"/>',
}
HIZMET_IK = {'evden-eve':'ev','ofis':'ofis','parca':'kutu','asansorlu':'asansor',
             'ambalaj':'kalkan','depolama':'depo','sehirlerarasi':'yol'}

def ikon(ad, sinif=''):
    icerik = IK.get(ad, IK['pin'])
    dolgu = 'none' if 'stroke=' in icerik else 'currentColor'
    return ('<svg viewBox="0 0 24 24" fill="%s" aria-hidden="true"%s>%s</svg>'
            % (dolgu, (' class="%s"' % sinif) if sinif else '', icerik))

def e(t):
    return html.escape(str(t), quote=True)

def slugla(t):
    d = {'ı':'i','İ':'i','ş':'s','Ş':'s','ğ':'g','Ğ':'g','ü':'u','Ü':'u',
         'ö':'o','Ö':'o','ç':'c','Ç':'c','â':'a','Â':'a'}
    t = ''.join(d.get(k, k) for k in t).lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


# ── Varlık sürümleme ─────────────────────────────────────────────────────────
# CSS/JS `max-age=600` ile servis ediliyor; sürüm damgası olmadan düzeltmeler
# ziyaretçiye 10 dakika boyunca ULAŞMIYOR. Dosya içeriğinin özeti damga olur:
# içerik değişmezse URL de değişmez, önbellek boşuna bozulmaz.
def _damga(gorece):
    import hashlib
    yol = os.path.join(KOK, gorece)
    if not os.path.exists(yol):
        return ''
    with open(yol, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]

CSS_SURUM = None
JS_SURUM = None

# ── Ortak parçalar ───────────────────────────────────────────────────────────
TEL = FIRMA['telefon_link']
WA  = 'https://wa.me/' + FIRMA['whatsapp']
WA_METIN = 'https://wa.me/%s?text=%s' % (
    FIRMA['whatsapp'], 'Merhaba%2C%20evden%20eve%20nakliyat%20i%C3%A7in%20fiyat%20almak%20istiyorum.')

def mevcut_genislikler(ad):
    """Bir görselin gerçekten üretilmiş türev genişlikleri.

    Kaynak görsellerin boyutları farklı; küçük olan için büyük türev
    üretilmiyor. srcset'e olmayan bir dosyayı yazmak 404 demek."""
    g = []
    for d in os.listdir(os.path.join(KOK, 'images')):
        m = re.fullmatch(r'w(\d+)', d)
        if m and os.path.exists(os.path.join(KOK, 'images', d, ad + '.webp')):
            g.append(int(m.group(1)))
    return sorted(g)

def en_buyuk_turev(ad, tercih):
    """Tercih edilen genişliğe en yakın MEVCUT türev."""
    g = mevcut_genislikler(ad)
    uygun = [x for x in g if x <= tercih]
    return (uygun[-1] if uygun else (g[0] if g else tercih))

def resim(ad, alt, genislikler, boyutlar, sinif='', oncelik=False, en=None, boy=None):
    """<picture>: WebP türevleri + özgün JPEG yedeği."""
    var = set(mevcut_genislikler(ad))
    genislikler = [g for g in genislikler if g in var] or sorted(var)
    kaynak = ', '.join('/images/w%d/%s.webp %dw' % (g, ad, g) for g in genislikler)
    ek = ' fetchpriority="high" decoding="async"' if oncelik else ' loading="lazy" decoding="async"'
    olcu = (' width="%d" height="%d"' % (en, boy)) if en else ''
    return ('<picture>'
            '<source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="/images/%s.jpeg" alt="%s"%s%s%s>'
            '</picture>') % (kaynak, boyutlar, ad, e(alt), olcu, ek,
                             (' class="%s"' % sinif) if sinif else '')

def ust_bar(koyu=False):
    return """<header class="ust%s">
  <div class="kap ust-ic">
    <a class="logo" href="/" aria-label="%s ana sayfa">
      <span class="logo-im" aria-hidden="true">S</span>
      <span><span class="logo-ad">SEYRAN</span><span class="logo-alt">Nakliyat</span></span>
    </a>
    <nav class="menu" id="menu">
      <a href="/#hizmetler">Hizmetler</a>
      <a href="/#nasil">Nasıl Çalışırız</a>
      <a href="/#bolgeler">Hizmet Bölgeleri</a>
      <a href="/#sss">Sık Sorulanlar</a>
      <a href="/#iletisim">İletişim</a>
    </nav>
    <div class="ust-ara">
      <button class="menu-dug" type="button" aria-label="Menü" aria-expanded="false"
              aria-controls="menu"><span></span></button>
      <a class="dg dg-birincil dg-kucuk" href="tel:%s">%s<span class="dg-metin">%s</span></a>
    </div>
  </div>
</header>""" % (' ust-koyu' if koyu else '', e(FIRMA['ad']), TEL,
                ikon('telefon'), e(FIRMA['telefon']))

def mobil_cubuk():
    return ('<div class="mobil-cubuk">'
            '<a class="dg dg-birincil" href="tel:%s">%sHemen Ara</a>'
            '<a class="dg dg-wa" href="%s" target="_blank" rel="noopener">%sWhatsApp</a>'
            '</div>') % (TEL, ikon('telefon'), WA_METIN, ikon('wa'))

def alt_bilgi():
    ilce_bag = ''.join(
        '<a href="/%s-evden-eve-nakliyat/">%s</a>' % (s, e(v[0]))
        for s, v in sorted(ILCELER.items(), key=lambda x: x[1][0]))
    hizmet_bag = ''.join('<li><a href="/#hizmetler">%s</a></li>' % e(a) for _, a, _ in HIZMETLER[:6])
    return """<footer class="alt">
  <div class="kap">
    <div class="alt-ic">
      <div>
        <a class="logo" href="/" style="margin-bottom:16px">
          <span class="logo-im" aria-hidden="true">S</span>
          <span><span class="logo-ad" style="color:#fff">SEYRAN</span>
          <span class="logo-alt">Nakliyat</span></span>
        </a>
        <p style="font-size:14.5px;max-width:42ch">%s — %s. %s yıldır İstanbul merkezli
        çalışıyor, Türkiye’nin her iline sigortalı taşıma yapıyoruz.</p>
        <p style="font-size:14.5px"><strong style="color:#fff">%s</strong><br>%s</p>
        <p><a class="dg dg-birincil dg-kucuk" href="tel:%s">%s%s</a></p>
      </div>
      <div>
        <h4>Hizmetler</h4>
        <ul>%s</ul>
      </div>
      <div>
        <h4>Hizmet Verdiğimiz İlçeler</h4>
        <div class="alt-ilceler">%s</div>
      </div>
    </div>
    <div class="alt-son">
      <span>&copy; <span id="yil">2026</span> %s. Tüm hakları saklıdır.</span>
      <span>%s</span>
    </div>
  </div>
</footer>""" % (e(FIRMA['tam_ad']), e(FIRMA['slogan']), FIRMA['tecrube_yili'],
                e(FIRMA['adres_kisa']), e(FIRMA['telefon_uluslararasi']),
                TEL, ikon('telefon'), e(FIRMA['telefon']),
                hizmet_bag, ilce_bag, e(FIRMA['ad']), e(FIRMA['alan_adi']))

def iskelet(baslik, aciklama, kanonik, govde, jsonld, koyu_ust=True):
    return """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="theme-color" content="#0e1e3d">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s/images/seyran-nakliyat.jpeg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/pjs-var-tr.woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v=%s">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">%s</script>
</head>
<body>
<a class="atla" href="#icerik">İçeriğe geç</a>
%s
<main id="icerik">
%s
</main>
%s
%s
<script src="/assets/app.js?v=%s" defer></script>
</body>
</html>""" % (e(baslik), e(aciklama), e(kanonik), e(FIRMA['ad']), e(baslik), e(aciklama),
              e(kanonik), SITE, CSS_SURUM, jsonld, ust_bar(koyu_ust), govde,
              alt_bilgi(), mobil_cubuk(), JS_SURUM)

# ── Yapısal veri ─────────────────────────────────────────────────────────────
def isletme_ld(sayfa_url):
    ilce_adlari = ', '.join('"%s"' % v[0] for _, v in sorted(ILCELER.items(), key=lambda x: x[1][0]))
    return """{
"@context":"https://schema.org","@type":"MovingCompany","@id":"%s/#isletme",
"name":"%s","alternateName":"%s","url":"%s","telephone":"%s","slogan":"%s",
"image":"%s/images/seyran-nakliyat.jpeg","priceRange":"₺₺",
"address":{"@type":"PostalAddress","streetAddress":"%s","addressLocality":"%s",
"addressRegion":"İstanbul","postalCode":"%s","addressCountry":"TR"},
"geo":{"@type":"GeoCoordinates","latitude":%s,"longitude":%s},
"openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
"opens":"00:00","closes":"23:59"}],
"areaServed":[{"@type":"Country","name":"Türkiye"},{"@type":"City","name":"İstanbul"}],
"knowsAbout":[%s],
"foundingDate":"%d",
"hasOfferCatalog":{"@type":"OfferCatalog","name":"Nakliyat Hizmetleri","itemListElement":[%s]}}""" % (
        SITE, e(FIRMA['tam_ad']), e(FIRMA['ad']), SITE, FIRMA['telefon_uluslararasi'],
        e(FIRMA['slogan']), SITE, e(FIRMA['sokak']), e(FIRMA['ilce']), FIRMA['posta_kodu'],
        FIRMA['enlem'], FIRMA['boylam'], ilce_adlari, 2026 - FIRMA['tecrube_yili'],
        ','.join('{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s"}}' % e(a)
                 for _, a, _ in HIZMETLER))

def sss_ld(sorular):
    return """{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}""" % ','.join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (e(s), e(c)) for s, c in sorular)

def kirinti_ld(parcalar):
    return """{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}""" % ','.join(
        '{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}' % (i + 1, e(ad), e(url))
        for i, (ad, url) in enumerate(parcalar))

# ── Ortak bölümler ───────────────────────────────────────────────────────────
def guven_serit(ilce_sayisi=25):
    veriler = [(FIRMA['tecrube_yili'], 'yıl', 'Yıllık tecrübe'),
               (ilce_sayisi, '', 'Avrupa yakası ilçesi'),
               (81, ' il', 'Türkiye geneli taşıma'),
               (7, '/24', 'Her gün ulaşılabilir')]
    h = ''.join('<div class="serit-h"><b data-sayac="%d" data-sonek="%s">0%s</b><span>%s</span></div>'
                % (s, e(sonek), e(sonek), e(ad)) for s, sonek, ad in veriler)
    return '<section class="serit"><div class="kap"><div class="serit-ic">%s</div></div></section>' % h

def sss_bolum(sorular, baslik='Sık Sorulan Sorular',
              spot='Taşınmadan önce en çok merak edilenler.'):
    kutular = ''.join(
        '<details class="sor gel"><summary>%s</summary><div class="cevap"><p>%s</p></div></details>'
        % (e(s), e(c)) for s, c in sorular)
    return """<section class="bolum" id="sss">
  <div class="kap">
    <div class="merkez" style="margin-bottom:38px">
      <span class="ust-etiket">Merak edilenler</span>
      <h2>%s</h2>
      <p class="spot">%s</p>
    </div>
    <div class="sss">%s</div>
  </div>
</section>""" % (e(baslik), e(spot), kutular)

def iletisim_bolum():
    satir = lambda ik, et, dg: (
        '<div class="ilet-sat"><i>%s</i><div><b>%s</b>%s</div></div>' % (ikon(ik), e(et), dg))
    return """<section class="bolum" id="iletisim" style="background:var(--zemin-2)">
  <div class="kap">
    <div class="merkez" style="margin-bottom:38px">
      <span class="ust-etiket">İletişim</span>
      <h2>Taşınma tarihinizi konuşalım</h2>
      <p class="spot">Ücretsiz keşif için arayın; eve gelip eşyayı görelim, net fiyatı size yazılı verelim.</p>
    </div>
    <div class="iletisim">
      <div class="ilet-kutu gel">
        %s%s%s%s
        <div style="display:flex;gap:11px;flex-wrap:wrap;margin-top:20px">
          <a class="dg dg-birincil" href="tel:%s">%sHemen Ara</a>
          <a class="dg dg-wa" href="%s" target="_blank" rel="noopener">%sWhatsApp</a>
        </div>
      </div>
      <div class="harita gel">
        <button class="harita-perde" type="button" data-harita="%s"
                aria-label="Google Haritalar’da ofis konumunu aç">
          <i>%s</i>
          <b>Ofisimiz — %s</b>
          <span>Haritayı görmek için tıklayın. Sayfa hızını korumak için gömülü harita
          ancak siz isteyince yükleniyor.</span>
        </button>
      </div>
    </div>
  </div>
</section>""" % (
        satir('telefon', 'Telefon / WhatsApp',
              '<a href="tel:%s">%s</a>' % (TEL, e(FIRMA['telefon_uluslararasi']))),
        satir('pin', 'Adres', '<span>%s</span>' % e(FIRMA['adres_kisa'])),
        satir('saat', 'Çalışma saatleri', '<span>Haftanın 7 günü, 24 saat</span>'),
        satir('yol', 'Hizmet alanı', '<span>%s</span>' % e(FIRMA['kapsam'])),
        TEL, ikon('telefon'), WA_METIN, ikon('wa'),
        e(FIRMA['harita_embed']), ikon('harita'), e(FIRMA['ilce']))

def son_cagri(baslik, metin):
    return """<section class="bolum">
  <div class="kap">
    <div class="cta gel">
      <h2>%s</h2>
      <p>%s</p>
      <div class="cta-dug">
        <a class="dg dg-birincil" href="tel:%s">%s%s</a>
        <a class="dg dg-wa" href="%s" target="_blank" rel="noopener">%sWhatsApp’tan yazın</a>
      </div>
    </div>
  </div>
</section>""" % (e(baslik), e(metin), TEL, ikon('telefon'), e(FIRMA['telefon']),
                 WA_METIN, ikon('wa'))

# ── Ana sayfa ────────────────────────────────────────────────────────────────
def ana_sayfa():
    rozet = lambda ik, t: '<span class="rozet">%s%s</span>' % (ikon(ik), e(t))

    kahraman = """<section class="kahraman">
  <div class="kap kahraman-ic">
    <div>
      <span class="ust-etiket">%s · %s yıldır</span>
      <h1>İstanbul’da evden eve nakliyat<em>Hassasiyet Taşır</em></h1>
      <p class="kahraman-spot">Eşyanızı biz toplarız, biz paketleriz, biz kurarız.
      İstanbul’un Avrupa yakasındaki 25 ilçenin tamamına ve İstanbul merkezli olarak
      Türkiye’nin her iline sigortalı taşıma yapıyoruz. Keşif ücretsiz, fiyat baştan net.</p>
      <div class="kahraman-dug">
        <a class="dg dg-birincil" href="tel:%s">%s%s</a>
        <a class="dg dg-cam" href="%s" target="_blank" rel="noopener">%sWhatsApp’tan fiyat alın</a>
      </div>
      <div class="rozetler">%s%s%s%s</div>
    </div>
    <div class="sahne">
      <div class="egik">
        %s
        <div class="egik-kart"><i>%s</i><div><b>%s yıl</b><span>Aynı ekip, aynı özen</span></div></div>
      </div>
    </div>
  </div>
</section>""" % (
        e(FIRMA['alt_slogan']), FIRMA['tecrube_yili'], TEL, ikon('telefon'), e(FIRMA['telefon']),
        WA_METIN, ikon('wa'),
        rozet('kalkan', 'Sigortalı taşıma'), rozet('pusula', 'Ücretsiz keşif'),
        rozet('saat', '7/24 ulaşım'), rozet('yol', 'Türkiye geneli'),
        resim('seyran-nakliyat', 'Seyran Nakliyat’ın İstanbul’daki kapalı kasa nakliye aracı',
              [400, 600, 768, 900, 1200], '(max-width:1000px) 92vw, 46vw', oncelik=True, en=1448, boy=1086),
        ikon('kalkan'), FIRMA['tecrube_yili'])

    hizmet_kart = ''.join(
        """<article class="kart kart-hizmet gel">
      <div class="kart-im">%s</div><h3>%s</h3><p>%s</p></article>"""
        % (ikon(HIZMET_IK.get(k, 'kutu')), e(ad), e(ac)) for k, ad, ac in HIZMETLER)

    hizmetler = """<section class="bolum" id="hizmetler">
  <div class="kap">
    <div class="merkez" style="margin-bottom:44px">
      <span class="ust-etiket">Hizmetlerimiz</span>
      <h2>Taşınmanın her adımı bizde</h2>
      <p class="spot">Eşyayı sökmekten yeni evinizde yerine kurmaya kadar tek ekip, tek sorumluluk.
      Aradaki hiçbir işi başkasına devretmiyoruz.</p>
    </div>
    <div class="izgara iz-3">%s</div>
  </div>
</section>""" % hizmet_kart

    ozellik_kart = ''.join(
        """<article class="kart gel"><div class="kart-im">%s</div><h3>%s</h3><p>%s</p></article>"""
        % (ikon(ik), e(ad), e(ac)) for ik, ad, ac in OZELLIKLER)

    neden = """<section class="bolum" style="background:var(--zemin-2)" id="neden">
  <div class="kap">
    <div class="merkez" style="margin-bottom:44px">
      <span class="ust-etiket">Neden Seyran Nakliyat</span>
      <h2>Taşınma günü sürpriz yaşamazsınız</h2>
      <p class="spot">Nakliyatta işler genelde iki yerde bozulur: fiyat sonradan değişir ya da
      eşya zarar görür. İkisini de baştan kapatıyoruz.</p>
    </div>
    <div class="izgara iz-3">%s</div>
  </div>
</section>""" % ozellik_kart

    adim_kart = ''.join('<article class="adim gel"><h3>%s</h3><p>%s</p></article>' % (e(a), e(b))
                        for a, b in ADIMLAR)
    nasil = """<section class="bolum" id="nasil">
  <div class="kap">
    <div class="merkez" style="margin-bottom:52px">
      <span class="ust-etiket">Nasıl çalışırız</span>
      <h2>Dört adımda yeni evinizdesiniz</h2>
      <p class="spot">Aramanızla teslim arasında ne olacağını baştan bilirsiniz.</p>
    </div>
    <div class="adimlar">%s</div>
  </div>
</section>""" % adim_kart

    gal = [('paketleme2', 'Kapalı kasa araca numaralanarak yerleştirilmiş kolilerin görünümü',
            'Numaralı koli düzeni'),
           ('seyran-nakliyat1', 'Battaniye ve balonlu naylonla paketlenmiş yatak odası takımı',
            'Yatak odası paketleme'),
           ('seyran-nakliyat2', 'Streç filmle sarılmış salon takımı ve koltuklar',
            'Salon takımı paketleme'),
           ('paketleme', 'Araç içinde balonlu naylonla sarılmış yatak ve baza',
            'Yatak ve baza koruması')]
    galeri_ic = ''.join(
        '<figure class="gal gel">%s<figcaption>%s</figcaption></figure>'
        % (resim(ad, alt, [400, 600, 768, 900], '(max-width:620px) 46vw, (max-width:1000px) 46vw, 23vw'), e(bas))
        for ad, alt, bas in gal)

    galeri = """<section class="bolum bolum-koyu" id="paketleme">
  <div class="kap">
    <div class="merkez" style="margin-bottom:40px">
      <span class="ust-etiket">Sahadan</span>
      <h2 style="color:#fff">Ambalajlama işin yarısıdır</h2>
      <p class="spot">Eşyanın zarar gördüğü yer araç değil, çoğu zaman merdiven ve kapı önüdür.
      Bu yüzden her parçayı ayrı yöntemle paketliyor, kolileri numaralandırıyoruz —
      yeni evde hangi kutunun nereye gideceği bellidir.</p>
    </div>
    <div class="galeri">%s</div>
  </div>
</section>""" % galeri_ic

    vids = [('nakliye-video', 'seyran-nakliyat', 'Araç ve ekip'),
            ('nakliye-video2', 'paketleme2', 'Yükleme düzeni'),
            ('nakliye-video3', 'seyran-nakliyat3', 'Ofisimiz'),
            ('nakliye-video4', 'paketleme', 'Paketleme')]
    video_ic = ''.join(
        """<div class="vid gel">
      <img src="/images/w%d/%s.webp" alt="%s" loading="lazy" decoding="async"
           style="object-fit:cover">
      <button class="vid-dug" type="button" data-video="/video/%s.mp4" data-poster="/images/w%d/%s.webp"
              aria-label="%s videosunu oynat"><i>%s</i><b>%s</b></button>
    </div>""" % (en_buyuk_turev(poster, 900), poster, e(bas + ' — Seyran Nakliyat'),
                 v, en_buyuk_turev(poster, 900), poster, e(bas), ikon('oynat'), e(bas))
        for v, poster, bas in vids)

    videolar = """<section class="bolum" id="videolar">
  <div class="kap">
    <div class="merkez" style="margin-bottom:40px">
      <span class="ust-etiket">Videolar</span>
      <h2>İşimizi kendiniz görün</h2>
      <p class="spot">Videolar siz oynat demeden yüklenmez; sayfa bu yüzden hızlı açılır.</p>
    </div>
    <div class="videolar">%s</div>
  </div>
</section>""" % video_ic

    ilce_bag = ''.join(
        '<a class="ilce" href="/%s-evden-eve-nakliyat/">%s<span>%s<small>Evden eve nakliyat</small></span></a>'
        % (s, ikon('pin'), e(v[0])) for s, v in sorted(ILCELER.items(), key=lambda x: x[1][0]))

    bolgeler = """<section class="bolum bolum-koyu" id="bolgeler">
  <div class="kap">
    <div class="merkez" style="margin-bottom:40px">
      <span class="ust-etiket">Hizmet bölgeleri</span>
      <h2 style="color:#fff">Avrupa yakasının 25 ilçesi</h2>
      <p class="spot">İlçenizin sayfasında o bölgeye özel taşıma koşullarını,
      hizmet verdiğimiz semtleri ve fiyatı etkileyen şeyleri yazdık.
      Ayrıca İstanbul merkezli olarak Türkiye’nin her iline taşıma yapıyoruz.</p>
    </div>
    <div class="ilceler">%s</div>
  </div>
</section>""" % ilce_bag

    govde = (kahraman + guven_serit() + hizmetler + neden + nasil + galeri + videolar
             + bolgeler + sss_bolum(SSS) + iletisim_bolum()
             + son_cagri('Taşınma tarihiniz belli mi?',
                         'Bir telefon yeterli. Eve gelir, eşyayı görür, net fiyatı yazılı veririz. '
                         'Keşif için sizden ücret almıyoruz.'))

    ld = '[%s,%s,%s]' % (
        isletme_ld(SITE), sss_ld(SSS),
        '{"@context":"https://schema.org","@type":"WebSite","name":"%s","url":"%s"}'
        % (e(FIRMA['ad']), SITE))

    return iskelet(
        'Evden Eve Nakliyat İstanbul | %s — Sigortalı Taşıma' % FIRMA['ad'],
        'İstanbul evden eve nakliyat: Avrupa yakasının 25 ilçesine ve Türkiye’nin her iline '
        'sigortalı taşıma. %s yıllık tecrübe, ücretsiz keşif, profesyonel ambalajlama. '
        'Hemen arayın: %s' % (FIRMA['tecrube_yili'], FIRMA['telefon']),
        SITE + '/', govde, ld)

# ── Ofise uzaklık (komşuluk grafiğinde adım sayısı) ──────────────────────────
# Gerçek kilometre bilgimiz yok; uydurmak yerine komşuluk grafiğinden çıkarılan
# "kaç ilçe ötede" bilgisini kullanıyoruz. Bu doğrulanabilir bir ifade.
def _uzakliklar():
    from collections import deque
    d = {FIRMA['ilce'].lower().replace('ü', 'u').replace('ö', 'o'): 0}
    d = {'gungoren': 0}
    q = deque(['gungoren'])
    while q:
        s = q.popleft()
        for k in KOMSU[s]:
            if k not in d:
                d[k] = d[s] + 1
                q.append(k)
    return d
UZAKLIK = _uzakliklar()

def _yakinlik_cumlesi(slug, ad):
    n = UZAKLIK.get(slug, 3)
    if n == 0:
        return ('Ofisimiz zaten %s’de, Haznedar’da. Bu ilçedeki taşımalara genellikle '
                'yarım saat içinde ulaşıyoruz.' % ad)
    if n == 1:
        return ('%s, ofisimizin bulunduğu Güngören’in komşu ilçesi. Aracımız kısa sürede '
                'adreste oluyor, bu da özellikle aynı gün çıkan işlerde fark yaratıyor.' % ad)
    if n == 2:
        return ('%s ile Güngören’deki ofisimiz arasında kısa bir mesafe var; ekibimiz bu '
                'bölgeye düzenli olarak çıkıyor.' % ad)
    return ('%s Avrupa yakasının uzak ilçelerinden; bu bölgeye çıkarken aracı ve ekibi '
            'işin tamamını tek seferde bitirecek şekilde planlıyoruz.' % ad)


def _kapsam_cumlesi(slug, ad, semtler, komsular):
    """Girişin ikinci paragrafı. Yakınlık cümlesi kahramanda zaten geçtiği için
    burada TEKRARLANMAZ; kapsam ve tipik iş türü anlatılır."""
    ilk = ', '.join(semtler[:3])
    kom = [ILCELER[k][0] for k in komsular[:2]]
    kom_metin = ' ve '.join(kom) if kom else 'komşu ilçeler'
    return ('%s başta olmak üzere %s’nin bütün mahallelerinde çalışıyoruz. '
            'Bu ilçede en sık yaptığımız üç iş şu: ilçe içinde ev değiştirme, '
            '%s yönüne taşınma ve İstanbul dışına çıkan şehirler arası nakliye. '
            'Üçünde de eşyayı aynı ekip topluyor, taşıyor ve yeni adreste kuruyor.'
            % (ilk, ad, kom_metin))

# ── İlçe sayfası ─────────────────────────────────────────────────────────────
def ilce_sayfa(slug):
    ad, semtler, _, notu = ILCELER[slug]
    url = '%s/%s-evden-eve-nakliyat/' % (SITE, slug)
    baslik_h1 = '%s Evden Eve Nakliyat' % ad
    komsular = sorted(KOMSU[slug], key=lambda s: ILCELER[s][0])

    kahraman = """<section class="kahraman">
  <div class="kap" style="padding-bottom:8px">
    <nav class="kirinti" aria-label="Yol">
      <a href="/">Ana sayfa</a><span>›</span>
      <a href="/#bolgeler">Hizmet bölgeleri</a><span>›</span>
      <span style="color:#dae6fb">%s</span>
    </nav>
  </div>
  <div class="kap kahraman-ic" style="padding-top:22px">
    <div>
      <span class="ust-etiket">İstanbul · Avrupa yakası</span>
      <h1>%s</h1>
      <p class="kahraman-spot">%s Sigortalı taşıma, profesyonel ambalajlama ve
      ücretsiz keşif ile %s’de eşyanızı biz toplar, biz kurarız.</p>
      <div class="kahraman-dug">
        <a class="dg dg-birincil" href="tel:%s">%s%s</a>
        <a class="dg dg-cam" href="%s" target="_blank" rel="noopener">%sWhatsApp’tan fiyat alın</a>
      </div>
      <div class="rozetler">%s%s%s</div>
    </div>
    <div class="sahne">
      <div class="egik">
        %s
        <div class="egik-kart"><i>%s</i><div><b>%s</b><span>Evden eve nakliyat</span></div></div>
      </div>
    </div>
  </div>
</section>""" % (
        e(ad), e(baslik_h1), e(_yakinlik_cumlesi(slug, ad)), e(ad),
        TEL, ikon('telefon'), e(FIRMA['telefon']), WA_METIN, ikon('wa'),
        '<span class="rozet">%sSigortalı taşıma</span>' % ikon('kalkan'),
        '<span class="rozet">%sÜcretsiz keşif</span>' % ikon('pusula'),
        '<span class="rozet">%sAsansörlü taşıma</span>' % ikon('asansor'),
        resim('seyran-nakliyat', '%s evden eve nakliyat aracı — Seyran Nakliyat' % ad,
              [400, 600, 768, 900, 1200], '(max-width:1000px) 92vw, 46vw', oncelik=True,
              en=1448, boy=1086),
        ikon('pin'), e(ad))

    semt_et = ''.join('<li>%s</li>' % e(s) for s in semtler)
    hizmet_li = ''.join('<li><strong>%s</strong> — %s</li>' % (e(a), e(c)) for _, a, c in HIZMETLER)

    metin = """<section class="bolum">
  <div class="kap">
    <div class="metin gel">
      <h2>%s’de nakliyat neden farklı?</h2>
      <p>%s</p>
      <p>%s</p>

      <h2>%s’de verdiğimiz hizmetler</h2>
      <ul>%s</ul>

      <h2>%s’de hizmet verdiğimiz semtler</h2>
      <p>Aşağıdaki semtlerin tamamına ve ilçenin diğer mahallelerine taşıma yapıyoruz.
      Semtiniz listede görünmüyorsa da arayın — %s’nin tamamı hizmet alanımızda.</p>
      <ul class="etiketler">%s</ul>

      <h2>%s’de nakliyat fiyatını ne belirler?</h2>
      <p>Telefonda duyduğunuz rakamın taşıma günü değişmemesi için fiyatı şu beş kalem üzerinden
      çıkarıyoruz:</p>
      <ul>
        <li><strong>Eşya hacmi</strong> — kaç odalı bir ev taşınıyor, eşya ne kadar yer kaplıyor.</li>
        <li><strong>Kat ve asansör durumu</strong> — %s’de asansörsüz bina oranı düşük değil;
            asansörlü araç gerekip gerekmediği fiyatı doğrudan etkiler.</li>
        <li><strong>Adrese erişim</strong> — aracın bina önüne yanaşıp yanaşamaması,
            sokağın genişliği ve park imkânı.</li>
        <li><strong>Mesafe</strong> — %s içinde mi taşınıyorsunuz, başka ilçeye mi, başka şehre mi.</li>
        <li><strong>Ambalajlama ihtiyacı</strong> — kırılacak eşya, piyano, büyük ekran televizyon
            gibi özel koruma isteyen parçalar.</li>
      </ul>

      <div class="vurgu-kutu">
        <p><b>Keşif ücretsiz, fiyat yazılı.</b> %s’deki adresinize gelir, eşyayı yerinde görür
        ve size net fiyat veririz. Görmeden telefonda söylenen kesin rakamlar taşıma günü
        değişme eğiliminde olduğu için biz bu yolu tercih etmiyoruz.</p>
      </div>

      <h2>%s’de taşınacaklara bir tavsiye</h2>
      <p>%s</p>

      <h2>%s’de asansörlü taşıma</h2>
      <p>Dar merdiven, dönerli sahanlık ve eşya geçirmeyen küçük asansörler, İstanbul’da
      taşımanın en sık karşılaşılan zorluğu. Böyle durumlarda eşyayı merdivenden indirmeye
      çalışmak hem saatler alıyor hem de çarpma riskini büyütüyor. %s’de bu tip binalarda
      asansörlü taşıma aracı kuruyor, eşyayı pencereden ya da balkondan güvenle indiriyoruz.
      Sokakta araç kurmaya uygun yer olup olmadığını keşif sırasında kontrol ediyoruz.</p>
    </div>
  </div>
</section>""" % (e(ad), e(notu), e(_kapsam_cumlesi(slug, ad, semtler, komsular)), e(ad), hizmet_li,
                e(ad), e(ad), semt_et, e(ad), e(ad), e(ad), e(ad),
                e(ad), e(IPUCU.get(slug, '')), e(ad), e(ad))

    adim_kart = ''.join('<article class="adim gel"><h3>%s</h3><p>%s</p></article>' % (e(a), e(b))
                        for a, b in ADIMLAR)
    nasil = """<section class="bolum" style="background:var(--zemin-2)">
  <div class="kap">
    <div class="merkez" style="margin-bottom:52px">
      <span class="ust-etiket">Nasıl çalışırız</span>
      <h2>%s’de taşınma dört adımda biter</h2>
    </div>
    <div class="adimlar">%s</div>
  </div>
</section>""" % (e(ad), adim_kart)

    komsu_bag = ''.join(
        '<a class="ilce" href="/%s-evden-eve-nakliyat/">%s<span>%s<small>Evden eve nakliyat</small></span></a>'
        % (k, ikon('pin'), e(ILCELER[k][0])) for k in komsular)

    yakin = """<section class="bolum bolum-koyu">
  <div class="kap">
    <div class="merkez" style="margin-bottom:34px">
      <span class="ust-etiket">Yakın ilçeler</span>
      <h2 style="color:#fff">%s’ye komşu ilçelerde de hizmetteyiz</h2>
      <p class="spot">%s’den bu ilçelere (ya da tersine) yapılan taşımalar günlük işimiz;
      iki adres arasındaki yolu ve trafiği biliyoruz.</p>
    </div>
    <div class="ilceler">%s</div>
    <p class="merkez" style="margin-top:30px">
      <a class="dg dg-cam" href="/#bolgeler">Tüm ilçeleri görün%s</a></p>
  </div>
</section>""" % (e(ad), e(ad), komsu_bag, ikon('ok'))

    ilce_sss = [
        ('%s’de aynı gün taşıma yapıyor musunuz?' % ad,
         'Program müsaitse yapıyoruz; %s için elimizde araç varsa aynı gün çıkabiliyoruz. '
         'Yine de eşya hacmi belliyse ve ambalajlama gerekiyorsa bir gün öncesinden haber '
         'vermeniz hem fiyatı hem süreyi netleştirir.' % ad),
        ('%s’de asansörsüz binadan taşıma nasıl oluyor?' % ad,
         'Asansörlü taşıma aracıyla. Eşya pencereden veya balkondan indiriliyor; hem çok daha '
         'hızlı hem de merdivende çarpma riski ortadan kalkıyor. Sokakta aracı kuracak yer olup '
         'olmadığını keşifte kontrol ediyoruz.'),
        ('%s’den başka bir şehre taşınıyorum, taşır mısınız?' % ad,
         'Taşırız. İstanbul merkezliyiz ama Türkiye’nin her iline nakliyat yapıyoruz. '
         'Şehirler arası taşımada da eşyanız sigortalı ve aynı ekibin sorumluluğunda.'),
    ] + SSS[:4]

    kirintilar = [('Ana sayfa', SITE + '/'),
                  ('Hizmet bölgeleri', SITE + '/#bolgeler'),
                  (baslik_h1, url)]
    ld = '[%s,%s,%s,%s]' % (
        isletme_ld(url), sss_ld(ilce_sss), kirinti_ld(kirintilar),
        '{"@context":"https://schema.org","@type":"Service","serviceType":"Evden Eve Nakliyat",'
        '"name":"%s","provider":{"@id":"%s/#isletme"},'
        '"areaServed":{"@type":"AdministrativeArea","name":"%s, İstanbul"},"url":"%s"}'
        % (e(baslik_h1), SITE, e(ad), e(url)))

    govde = (kahraman + guven_serit() + metin + nasil + yakin
             + sss_bolum(ilce_sss, '%s nakliyat hakkında sık sorulanlar' % ad,
                         '%s’de taşınacakların en çok sorduğu şeyler.' % ad)
             + iletisim_bolum()
             + son_cagri('%s’de taşınacaksanız bir telefon yeterli' % ad,
                         'Eve gelir, eşyayı görür, net fiyatı veririz. Keşif ücretsizdir.'))

    return iskelet(
        '%s | Sigortalı Taşıma — %s' % (baslik_h1, FIRMA['ad']),
        '%s evden eve nakliyat: sigortalı taşıma, asansörlü nakliyat, profesyonel ambalajlama. '
        '%s ve çevresinde %s yıllık tecrübe, ücretsiz keşif. Hemen arayın: %s'
        % (ad, ', '.join(semtler[:3]), FIRMA['tecrube_yili'], FIRMA['telefon']),
        url, govde, ld)

# ── Yardımcı sayfalar ────────────────────────────────────────────────────────
def sayfa_404():
    ilce_bag = ''.join(
        '<a class="ilce" href="/%s-evden-eve-nakliyat/">%s<span>%s</span></a>'
        % (s, ikon('pin'), e(v[0])) for s, v in sorted(ILCELER.items(), key=lambda x: x[1][0])[:8])
    govde = """<section class="kahraman">
  <div class="kap kahraman-ic" style="grid-template-columns:1fr;text-align:center;padding:90px 0">
    <div>
      <span class="ust-etiket" style="justify-content:center">404</span>
      <h1>Aradığınız sayfa bulunamadı</h1>
      <p class="kahraman-spot" style="margin-inline:auto">Adres değişmiş olabilir.
      Ana sayfadan devam edebilir ya da ilçenizin sayfasına geçebilirsiniz.</p>
      <div class="kahraman-dug" style="justify-content:center">
        <a class="dg dg-birincil" href="/">Ana sayfaya dön</a>
        <a class="dg dg-cam" href="tel:%s">%s%s</a>
      </div>
    </div>
  </div>
</section>
<section class="bolum"><div class="kap"><div class="ilceler">%s</div></div></section>""" % (
        TEL, ikon('telefon'), e(FIRMA['telefon']), ilce_bag)
    return iskelet('Sayfa bulunamadı | ' + FIRMA['ad'],
                   'Aradığınız sayfa bulunamadı.', SITE + '/404.html', govde,
                   isletme_ld(SITE))

def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#ff8b45"/><stop offset=".55" stop-color="#f26722"/>'
            '<stop offset="1" stop-color="#d8232a"/></linearGradient></defs>'
            '<rect width="64" height="64" rx="15" fill="url(#g)"/>'
            '<text x="32" y="45" font-family="Segoe UI,Roboto,Helvetica,Arial,sans-serif" '
            'font-size="38" font-weight="800" fill="#fff" text-anchor="middle">S</text></svg>')

def sitemap(tarih):
    girdiler = ['<url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq>'
                '<priority>1.0</priority></url>' % (SITE, tarih)]
    for s, v in sorted(ILCELER.items(), key=lambda x: x[1][0]):
        girdiler.append('<url><loc>%s/%s-evden-eve-nakliyat/</loc><lastmod>%s</lastmod>'
                        '<changefreq>monthly</changefreq><priority>0.8</priority></url>'
                        % (SITE, s, tarih))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
            % '\n'.join(girdiler))

def robots():
    return 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE

# ── Derleme ──────────────────────────────────────────────────────────────────
def yaz(gorece_yol, icerik):
    yol = os.path.join(KOK, gorece_yol)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, 'w', encoding='utf-8') as f:
        f.write(icerik)
    return len(icerik.encode('utf-8'))

def main():
    import datetime
    global CSS_SURUM, JS_SURUM
    CSS_SURUM = _damga('assets/style.css')
    JS_SURUM = _damga('assets/app.js')
    print('  varlık sürümü: css=%s js=%s' % (CSS_SURUM, JS_SURUM))
    tarih = os.environ.get('BUILD_DATE') or datetime.date.today().isoformat()

    # Eski ilçe klasörlerini temizle (yeniden adlandırma olursa artık kalmasın).
    for d in os.listdir(KOK):
        if d.endswith('-evden-eve-nakliyat') and os.path.isdir(os.path.join(KOK, d)):
            shutil.rmtree(os.path.join(KOK, d))

    toplam = 0
    toplam += yaz('index.html', ana_sayfa())
    print('  index.html')
    for slug in sorted(ILCELER, key=lambda s: ILCELER[s][0]):
        b = yaz('%s-evden-eve-nakliyat/index.html' % slug, ilce_sayfa(slug))
        toplam += b
        print('  %-34s %6.0f KB' % (slug + '-evden-eve-nakliyat/', b / 1024))

    toplam += yaz('404.html', sayfa_404())
    toplam += yaz('favicon.svg', favicon())
    toplam += yaz('sitemap.xml', sitemap(tarih))
    toplam += yaz('robots.txt', robots())
    yaz('CNAME', FIRMA['alan_adi'] + '\n')
    yaz('.nojekyll', '')

    print('\n  %d sayfa · toplam HTML %.0f KB' % (len(ILCELER) + 2, toplam / 1024))

if __name__ == '__main__':
    main()
