# seyrannakliyat.net

Seyran Evden Eve Nakliyat — İstanbul merkezli, Türkiye geneli nakliyat firması için
statik web sitesi. GitHub Pages üzerinde yayınlanır.

## ⛔ Önce oku

HTML dosyalarını **elle düzenleme.** `index.html`, `404.html` ve
`*-evden-eve-nakliyat/index.html` dosyalarının hepsi üretilmiştir; bir sonraki
derlemede silinip yeniden yazılır.

Değişiklik iki yerden yapılır:

| Ne değişecek | Nerede |
|---|---|
| Metin, ilçe, semt, telefon, adres, SSS | `_src/data.py` |
| Sayfa yapısı, bölümler, yapısal veri | `_src/build.py` |
| Görünüm | `assets/style.css` |
| Davranış (menü, video, harita, sayaç) | `assets/app.js` |

## Derleme

```bash
python3 _src/build.py      # 26 sayfa + sitemap + robots + 404 üretir
python3 _src/denetim.py    # bağlantı, JSON-LD, tekrar eden başlık ve ağırlık denetimi
python3 _src/media.py      # görsel türevlerini (WebP) yeniden üretir — sadece görsel değişince
```

`denetim.py` hata bulursa 0 dışında bir kodla çıkar; commit etmeden önce çalıştır.

## Kurallar

- **Üçüncü parti istek yok.** Font yerel (`assets/fonts`), ikonlar satır içi SVG,
  analitik yok. Google Haritalar ve videolar kullanıcı tıklayana kadar yüklenmez.
- **CSS ve JS ayrı dosya.** 26 sayfa aynı dosyayı paylaşır, tarayıcı bir kez indirir.
- **Görseller `<picture>` + srcset.** Kaynak JPEG'ler `images/` içinde kalır,
  WebP türevleri `images/w<genişlik>/` altına üretilir.
- **Uydurma bilgi yok.** Sitede geçen her iddia (13 yıl, sigortalı taşıma, ücretsiz
  keşif, 7/24) firma tarafından onaylanmıştır. Yeni bir iddia eklenecekse önce sor.

## İlk açılış ağırlığı

| | gzip |
|---|---|
| index.html | ~9 KB |
| style.css | ~6 KB |
| app.js | ~2 KB |
| font (woff2) | 37 KB |
| hero görsel (w900) | 139 KB |
| **toplam** | **~193 KB** |

İlçe sayfaları ~8 KB; CSS/JS/font önbellekten gelir.

## Yayın

`main` dalına push → GitHub Pages. Özel alan adı `CNAME` dosyasında
(`seyrannakliyat.net`), DNS GitHub Pages IP'lerine bakar.
`.nojekyll` dosyası Jekyll işlemesini kapatır.
