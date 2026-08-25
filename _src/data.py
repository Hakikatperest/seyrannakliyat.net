# -*- coding: utf-8 -*-
"""
Seyran Nakliyat — site verisi.

İçerik ilkesi: her ilçe sayfası GERÇEK yerel bilgiyle farklılaşır (semtler,
komşu ilçeler, o ilçede taşımayı zorlaştıran somut şey). Anahtar kelime
doldurma yok; sayfayı okuyan insan işine yarayan bir şey öğrenmeli.

"komsular" sadece Avrupa yakasındaki gerçek sınır komşularıdır — sayfa içi
linkleme buradan üretilir.
"""

FIRMA = {
    'ad': 'Seyran Nakliyat',
    'tam_ad': 'Seyran Evden Eve Nakliyat',
    'slogan': 'Hassasiyet Taşır',
    'alt_slogan': 'Kaliteli Taşımacılığın Adresi',
    'telefon': '0532 237 80 66',
    'telefon_link': '+905322378066',
    'whatsapp': '905322378066',
    'adres': 'Haznedar Mah. Tevfik Fikret Sk. No:65, 34160 Güngören / İstanbul',
    'adres_kisa': 'Haznedar Mah. Tevfik Fikret Sk. No:65 Güngören, İstanbul',
    'sokak': 'Haznedar Mah. Tevfik Fikret Sk. No:65',
    'telefon_uluslararasi': '+90 532 237 80 66',
    'ilce': 'Güngören',
    'il': 'İstanbul',
    'posta_kodu': '34160',
    'tecrube_yili': 13,
    'alan_adi': 'seyrannakliyat.net',
    'site': 'https://seyrannakliyat.net',
    # İstanbul merkezli ama hizmet alanı Türkiye geneli (kullanıcı bildirdi).
    'kapsam': 'İstanbul merkezli, Türkiye’nin her yerine',
    'harita_embed': (
        'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d188.15891497970367'
        '!2d28.871783869592836!3d41.01338269059347!2m3!1f0!2f0!3f0!3m2!1i1024!2i768'
        '!4f13.1!3m3!1m2!1s0x14cabb30443683b5%3A0xfe6ca1cd23855f91'
        '!2sHaznedar%2C%20Tevfik%20Fikret%20Sk.%20No%3A65%2C%2034160%20G%C3%BCng%C3%B6ren'
        '%2F%C4%B0stanbul!5e0!3m2!1str!2str!4v1787665165050!5m2!1str!2str'
    ),
    'enlem': 41.013382,
    'boylam': 28.871783,
}

# Sitede iddia edilebilecek gerçek özellikler (kullanıcı onayladı).
OZELLIKLER = [
    ('kalkan', 'Sigortalı Taşıma',
     'Eşyalarınız yola çıktığı andan yerine yerleştiği ana kadar sigorta kapsamındadır.'),
    ('kutu', 'Profesyonel Ambalajlama',
     'Balonlu naylon, streç film, battaniye ve özel koli ile kırılmaya karşı tam koruma.'),
    ('ekip', 'Uzman Kadro',
     'Sertifikalı ve deneyimli taşıma personeli; eşyayı taşıyan da toplayan da aynı ekip.'),
    ('saat', 'Zamanında Teslim',
     'Söz verdiğimiz gün ve saatte kapınızdayız; taşıma günü sürpriz yaşamazsınız.'),
    ('kamyon', 'Geniş Araç Filosu',
     'Tek odalık eşyadan komple daireye kadar her hacme uygun araç seçeneği.'),
    ('pusula', 'Ücretsiz Ekspertiz',
     'Eve gelip eşyayı yerinde görür, net fiyat veririz — keşif için ücret almayız.'),
]

HIZMETLER = [
    ('evden-eve', 'Evden Eve Nakliyat',
     'Komple ev taşıma: sökme, ambalajlama, yükleme, taşıma, kurulum ve yerleştirme dahil.'),
    ('ofis', 'Ofis ve İş Yeri Taşıma',
     'Dosya, arşiv ve ekipmanı numaralandırarak taşırız; iş kaybınız en aza iner.'),
    ('parca', 'Parça Eşya Taşıma',
     'Tek koltuk, buzdolabı ya da birkaç koli için komple araç ücreti ödemezsiniz.'),
    ('asansorlu', 'Asansörlü Taşıma',
     'Dar merdiven ve asansörsüz binalarda eşya pencereden güvenle indirilir.'),
    ('ambalaj', 'Paketleme ve Ambalajlama',
     'Yatak odası, salon takımı ve mutfak eşyası için ayrı ayrı ambalaj yöntemi.'),
    ('depolama', 'Eşya Depolama',
     'Taşıma ile yerleşme arasında boşluk varsa eşyanız kapalı depoda bekler.'),
    ('sehirlerarasi', 'Şehirler Arası Nakliyat',
     'İstanbul merkezliyiz ama Türkiye’nin her iline taşıyoruz; uzun yolda da eşyanız '
     'sigortalı ve aynı ekibin sorumluluğunda.'),
]

# slug: (ad, semtler, komşu ilçe slugları, o ilçeye özgü taşıma notu)
ILCELER = {
'arnavutkoy': ('Arnavutköy',
    ['Hadımköy', 'Taşoluk', 'Bolluca', 'Haraççı', 'Boğazköy', 'Yeşilbayır', 'Deliklikaya', 'İmrahor'],
    ['basaksehir', 'eyupsultan', 'sultangazi', 'esenyurt', 'catalca'],
    'Arnavutköy İstanbul’un yüz ölçümü en geniş ilçelerinden biri; Hadımköy ile Boğazköy arası '
    'tek başına yarım saatlik yol demek. Bu yüzden burada taşımanın kritik konusu bina değil '
    'mesafe: aracın gün içinde kaç sefer yapacağı baştan doğru hesaplanmazsa taşıma ertesi güne sarkar.'),

'avcilar': ('Avcılar',
    ['Ambarlı', 'Denizköşkler', 'Cihangir', 'Merkez', 'Firuzköy', 'Tahtakale', 'Üniversite', 'Mustafa Kemal Paşa'],
    ['kucukcekmece', 'esenyurt', 'beylikduzu'],
    'Avcılar’ın konut dokusu büyük ölçüde 1990’ların apartmanlarından oluşuyor: dar merdiven boşluğu, '
    'çoğu binada dolap ve buzdolabı geçirmeyen asansör. Ambarlı ve Denizköşkler taraflarında '
    'taşımaların çoğunu asansörlü araçla yapıyoruz. E-5 ve metrobüs hattına yakın sokaklarda '
    'sabah saatlerinde araç park etmek ayrı bir iş, bu yüzden yükleme saatini erkene alıyoruz.'),

'bagcilar': ('Bağcılar',
    ['Güneşli', 'Kirazlı', 'Mahmutbey', 'Yenimahalle', 'Demirkapı', 'Barbaros', 'Yıldıztepe', 'Fevziçakmak'],
    ['bahcelievler', 'gungoren', 'esenler', 'basaksehir', 'kucukcekmece'],
    'Bağcılar’da sokaklar dar, binalar çoğunlukla beş-altı katlı ve önemli bir kısmı asansörsüz. '
    'Kamyonun bina önüne yanaşabilmesi çoğu zaman komşularla önceden konuşmayı gerektiriyor. '
    'Ekibimiz Bağcılar taşımalarına genellikle asansörlü araç ve ek personelle çıkar; '
    'eşyanın merdivenden inmesini beklemek hem süreyi hem riski büyütüyor.'),

'bahcelievler': ('Bahçelievler',
    ['Şirinevler', 'Yenibosna', 'Soğanlı', 'Kocasinan', 'Siyavuşpaşa', 'Zafer', 'Çobançeşme', 'Cumhuriyet'],
    ['bagcilar', 'gungoren', 'bakirkoy', 'kucukcekmece'],
    'Şirinevler ve Yenibosna çevresi metro–metrobüs aktarmasının tam üstünde; gündüz saatlerinde '
    'araç bekletmek neredeyse imkânsız. Bahçelievler taşımalarını bu yüzden ya sabah erken ya da '
    'öğleden sonra planlıyoruz. İç mahallelerde apartmanlar geniş, asansörler görece elverişli — '
    'burada asıl iş ambalajlama ve yerleştirmede.'),

'bakirkoy': ('Bakırköy',
    ['Ataköy', 'Yeşilköy', 'Florya', 'Yeşilyurt', 'Şenlikköy', 'Osmaniye', 'Zeytinlik', 'Cevizlik', 'Kartaltepe'],
    ['bahcelievler', 'zeytinburnu', 'kucukcekmece'],
    'Bakırköy’de iki ayrı taşıma dünyası var: Ataköy’ün site blokları ve Yeşilköy–Florya’nın '
    'müstakil evleri. Sitelerde yönetimden giriş izni almak, asansör saatini ayırtmak ve '
    'zemini korumak zorunlu; müstakil evlerde ise bahçe kapısı genişliği ve iç merdiven '
    'taşımanın seyrini belirliyor. İkisinde de keşif yapmadan fiyat vermiyoruz.'),

'basaksehir': ('Başakşehir',
    ['Kayaşehir', 'Başak', 'Bahçeşehir', 'Güvercintepe', 'Ziya Gökalp', 'Şahintepe', 'Altınşehir'],
    ['arnavutkoy', 'sultangazi', 'esenler', 'bagcilar', 'kucukcekmece', 'esenyurt'],
    'Başakşehir toplu konut ilçesi: Kayaşehir ve Bahçeşehir tarafında yüksek katlı bloklar, '
    'kayıtlı giriş, asansör rezervasyonu ve çoğu sitede belirli taşınma saatleri var. '
    'Burada taşımanın yarısı evrak işi — yönetimle bir gün önceden konuşup asansörü ayırtmak, '
    'taşıma gününde saatlerce beklemenin önüne geçiyor.'),

'bayrampasa': ('Bayrampaşa',
    ['Yıldırım', 'Muratpaşa', 'Vatan', 'Terazidere', 'Kartaltepe', 'Altıntepsi', 'Yenidoğan', 'İsmetpaşa'],
    ['esenler', 'gaziosmanpasa', 'eyupsultan', 'zeytinburnu', 'fatih'],
    'Bayrampaşa’da konut ile sanayi iç içe; gün ortasında sokakların çoğu yükleme yapan '
    'ticari araçlarla dolu oluyor. Otogar ve Vatan Caddesi çevresinde trafik akışı taşıma '
    'saatini doğrudan etkiliyor. Bu ilçede aracı bina önüne yanaştırabilmek için sabahın '
    'erken saatlerini tercih ediyoruz.'),

'besiktas': ('Beşiktaş',
    ['Levent', 'Etiler', 'Ortaköy', 'Bebek', 'Arnavutköy', 'Kuruçeşme', 'Balmumcu', 'Gayrettepe', 'Akatlar', 'Ulus'],
    ['sisli', 'sariyer', 'kagithane'],
    'Beşiktaş yokuş demek. Ortaköy, Bebek ve Arnavutköy sahil mahallelerinde sokaklar dar, '
    'birçok binanın girişi merdivenli ve araç park etmek çoğu zaman izne bağlı. Levent–Etiler '
    'tarafında ise rezidans kuralları devreye giriyor: yük asansörü, saat kısıtı, zemin koruma. '
    'Beşiktaş taşımalarında keşif, fiyattan çok yöntemi belirlemek için önemli.'),

'beylikduzu': ('Beylikdüzü',
    ['Gürpınar', 'Yakuplu', 'Kavaklı', 'Barış', 'Adnan Kahveci', 'Cumhuriyet', 'Marmara', 'Sahil'],
    ['avcilar', 'esenyurt', 'buyukcekmece'],
    'Beylikdüzü planlı kurulmuş bir ilçe: yollar geniş, siteler düzenli, aracı bina önüne '
    'yanaştırmak kolay. Buna karşılık neredeyse her sitenin kendi taşınma kuralı var — '
    'giriş saati, yük asansörü kullanımı, kapıcı bildirimi. Beylikdüzü’nde işi hızlandıran şey '
    'ekip değil, bir gün önceden yapılan tek bir telefon görüşmesi.'),

'beyoglu': ('Beyoğlu',
    ['Cihangir', 'Galata', 'Karaköy', 'Kasımpaşa', 'Tarlabaşı', 'Halıcıoğlu', 'Piyalepaşa', 'Kuloğlu'],
    ['sisli', 'kagithane', 'besiktas', 'fatih', 'eyupsultan'],
    'Beyoğlu, İstanbul’da taşınması en zor ilçelerden biri. Cihangir ve Galata’da sokaklar '
    'kamyon girmeyecek kadar dar, binalar tarihi ve merdivenler dönerli; asansör çoğu binada yok. '
    'Burada eşyanın büyük kısmı pencereden asansörlü araçla iniyor, bir kısmı da elde taşınıyor. '
    'Keşif yapmadan Beyoğlu için fiyat vermek mümkün değil.'),

'buyukcekmece': ('Büyükçekmece',
    ['Mimarsinan', 'Kumburgaz', 'Celaliye', 'Kamiloba', 'Türkoba', 'Atatürk', 'Güzelce', 'Ahmediye'],
    ['beylikduzu', 'esenyurt', 'catalca', 'silivri'],
    'Büyükçekmece göl ve sahil boyunca uzuyor; Kumburgaz ile Mimarsinan arası ciddi bir mesafe. '
    'İlçede yazlıktan kalıcı konuta dönmüş çok sayıda site var, bu sitelerin bir kısmında '
    'yaz aylarında taşınma saati kısıtlanıyor. Şehir merkezine olan uzaklık nedeniyle '
    'taşımaları tek seferde bitirecek araç boyutuyla planlıyoruz.'),

'catalca': ('Çatalca',
    ['Ferhatpaşa', 'Kaleiçi', 'Ovayenice', 'Çanakça', 'Hallaçlı', 'Elbasan', 'Nakkaş', 'Subaşı', 'Kestanelik'],
    ['buyukcekmece', 'silivri', 'arnavutkoy'],
    'Çatalca kırsal karakterini korumuş bir ilçe; taşımaların önemli kısmı köy yerleşimlerine '
    'yapılıyor. Burada dikkat edilmesi gereken şey bina değil yol: bazı köy içi yollar büyük '
    'kamyon için uygun değil, kış aylarında zemin sorun çıkarıyor. Çatalca taşımalarında '
    'araç boyutunu adresi gördükten sonra seçiyoruz.'),

'esenler': ('Esenler',
    ['Menderes', 'Fevzi Çakmak', 'Atışalanı', 'Kemer', 'Turgut Reis', 'Havaalanı', 'Nine Hatun', 'Oruçreis', 'Birlik'],
    ['bagcilar', 'bayrampasa', 'gungoren', 'sultangazi', 'basaksehir'],
    'Esenler’de otogar çevresi gün boyu hareketli; ana arterlerde araç bekletmek zor. '
    'Konut dokusunda asansörsüz blok oranı yüksek, merdivenler dar. Kentsel dönüşüm '
    'nedeniyle ilçede kısa mesafeli taşıma çok: aynı mahalle içinde bir binadan diğerine '
    'geçen taşımalarda parça eşya hizmetimiz komple araçtan belirgin şekilde uygun kalıyor.'),

'esenyurt': ('Esenyurt',
    ['Yeşilkent', 'Saadetdere', 'Balıkyolu', 'İnönü', 'Barbaros Hayrettin Paşa', 'Namık Kemal', 'Talatpaşa', 'Pınar', 'Cumhuriyet'],
    ['avcilar', 'beylikduzu', 'buyukcekmece', 'basaksehir', 'arnavutkoy'],
    'Esenyurt İstanbul’un en kalabalık ilçesi ve konut stoğunun büyük bölümü yüksek katlı '
    'sitelerden oluşuyor. Bu da şu demek: tek asansöre çok daire düşüyor. Taşıma gününde '
    'asansör sırası beklememek için yönetimden saat ayırtmak, mümkünse yük asansörünü '
    'kullanmak gerekiyor. Sitelerin bir kısmında akşam saatlerinde taşınma yasak.'),

'eyupsultan': ('Eyüpsultan',
    ['Alibeyköy', 'Kemerburgaz', 'Göktürk', 'Rami', 'Silahtarağa', 'Nişanca', 'Karadolap', 'Akşemsettin', 'Düğmeciler'],
    ['gaziosmanpasa', 'sultangazi', 'arnavutkoy', 'kagithane', 'beyoglu', 'sariyer', 'bayrampasa'],
    'Eyüpsultan Haliç kıyısından Kemerburgaz ormanlarına kadar uzanıyor ve bu iki uç bambaşka '
    'taşıma şartları demek. Alibeyköy ve Rami tarafında dar, yokuşlu sokaklar ve eski apartmanlar; '
    'Göktürk–Kemerburgaz tarafında geniş siteler ve villalar var. Aynı ilçe için iki farklı '
    'ekip ve araç planı kuruyoruz.'),

'fatih': ('Fatih',
    ['Fındıkzade', 'Aksaray', 'Çapa', 'Yedikule', 'Balat', 'Fener', 'Samatya', 'Cerrahpaşa', 'Kocamustafapaşa'],
    ['zeytinburnu', 'bayrampasa', 'eyupsultan', 'beyoglu'],
    'Tarihi yarımadada taşıma, İstanbul’un en özel işlerinden biri. Balat ve Fener’de sokaklar '
    'yokuşlu ve taş döşeli, binalar tarihi, merdivenler dar ve dönerli. Bazı sokaklara araç '
    'girişi saatle sınırlı. Fatih taşımalarında eşyanın büyük kısmını asansörlü araçla '
    'pencereden indiriyor, hassas parçaları elde taşıyoruz.'),

'gaziosmanpasa': ('Gaziosmanpaşa',
    ['Karayolları', 'Hürriyet', 'Sarıgöl', 'Merkez', 'Yıldıztabya', 'Karlıtepe', 'Bağlarbaşı', 'Yenidoğan', 'Pazariçi'],
    ['eyupsultan', 'sultangazi', 'bayrampasa', 'esenler'],
    'Gaziosmanpaşa’da arazi eğimli; birçok sokakta kamyonu bina hizasına çekmek mümkün olmuyor '
    've eşya bir miktar taşınarak araca ulaşıyor. Kentsel dönüşüm ilçede sürüyor, bu yüzden '
    'kısa mesafeli ve tarihi önceden belli olmayan taşımalar çok. Esnek tarih verebiliyorsanız '
    'taşıma maliyeti gözle görülür düşüyor.'),

'gungoren': ('Güngören',
    ['Haznedar', 'Merter', 'Güneştepe', 'Tozkoparan', 'Mareşal Çakmak', 'Akıncılar', 'Gençosman', 'Sanayi'],
    ['bahcelievler', 'bagcilar', 'esenler', 'zeytinburnu', 'bayrampasa'],
    'Güngören bizim kendi ilçemiz — ofisimiz Haznedar’da, Tevfik Fikret Sokak’ta. İlçedeki '
    'taşımalara genellikle otuz dakika içinde ulaşıyoruz. Güngören’de sokaklar dar ve konut '
    'ile iş yeri iç içe; Merter tarafında gündüz saatlerinde tekstil yüklemesi yapan araçlar '
    'sokakları kapatabiliyor. Bu ilçeyi en iyi bildiğimiz için taşıma saatini en isabetli '
    'burada planlıyoruz.'),

'kagithane': ('Kâğıthane',
    ['Seyrantepe', 'Gültepe', 'Çağlayan', 'Hamidiye', 'Talatpaşa', 'Nurtepe', 'Sultan Selim', 'Yahya Kemal', 'Ortabayır'],
    ['sisli', 'eyupsultan', 'beyoglu', 'sariyer'],
    'Kâğıthane dik yokuşlar ilçesi. Nurtepe, Gültepe ve Hamidiye taraflarında sokaklar hem dar '
    'hem eğimli; büyük araçla girmek çoğu zaman mümkün değil, eşya küçük araca aktarılarak '
    'taşınıyor. Seyrantepe ve Çağlayan tarafındaki yeni rezidanslarda ise yük asansörü ve '
    'randevu düzeni var. Kâğıthane’de fiyatı belirleyen şey mesafe değil, binaya erişim.'),

'kucukcekmece': ('Küçükçekmece',
    ['Halkalı', 'Sefaköy', 'Cennet', 'Kanarya', 'Atakent', 'İnönü', 'Yeşilova', 'Söğütlüçeşme', 'Kartaltepe'],
    ['avcilar', 'bahcelievler', 'bagcilar', 'basaksehir', 'bakirkoy', 'esenyurt'],
    'Küçükçekmece göl çevresinde geniş bir alana yayılıyor. Halkalı ve Atakent tarafında yeni '
    'siteler, Sefaköy ve Cennet taraflarında yoğun apartman dokusu var. Sefaköy’de sokaklar dar '
    've park sorunlu; Halkalı’da ise site kuralları belirleyici. İlçe içi taşımalarda bile '
    'iki adres arasında bambaşka yöntem gerekebiliyor.'),

'sariyer': ('Sarıyer',
    ['Maslak', 'Tarabya', 'Yeniköy', 'İstinye', 'Emirgan', 'Bahçeköy', 'Zekeriyaköy', 'Kilyos', 'Büyükdere', 'Ayazağa'],
    ['besiktas', 'sisli', 'kagithane', 'eyupsultan'],
    'Sarıyer’de villa ve müstakil ev oranı yüksek; Zekeriyaköy ve Bahçeköy taraflarında bahçeli '
    'evler, boğaz hattında ise dar ve dik yollara sahip yalı tipi yapılar var. Villalarda eşya '
    'birden çok kata dağıldığı için taşıma iki gün sürebiliyor. Sarıyer taşımalarında ekip '
    'sayısını baştan yüksek tutmak toplam süreyi kısaltıyor.'),

'silivri': ('Silivri',
    ['Selimpaşa', 'Gümüşyaka', 'Ortaköy', 'Alipaşa', 'Piri Mehmet Paşa', 'Değirmenköy', 'Fener', 'Kavaklı', 'Mimar Sinan'],
    ['catalca', 'buyukcekmece'],
    'Silivri şehir merkezine en uzak Avrupa yakası ilçelerinden. Buraya ya da buradan yapılan '
    'taşımalarda yol süresi işin en büyük kalemi; bu yüzden eşyayı tek seferde alacak araçla '
    'çıkıyoruz. Sahil şeridindeki yazlık sitelerde sezon dışında taşınma çok daha rahat '
    've maliyet belirgin şekilde düşüyor.'),

'sultangazi': ('Sultangazi',
    ['Cebeci', 'Habibler', 'Uğur Mumcu', '50. Yıl', 'Esentepe', 'Gazi', 'Yayla', 'Sultançiftliği', 'Zübeyde Hanım'],
    ['gaziosmanpasa', 'eyupsultan', 'arnavutkoy', 'basaksehir', 'esenler'],
    'Sultangazi’de arazi eğimli, sokaklar dar ve binaların çoğu asansörsüz. Cebeci ve Habibler '
    'taraflarında araç bina önüne çoğu zaman yanaşamıyor. İlçede kentsel dönüşüm nedeniyle '
    'geçici taşınmalar sık: eşyanın bir bölümünü depoya alıp kalanını yeni adrese taşıdığımız '
    'karma çözümler burada işe yarıyor.'),

'sisli': ('Şişli',
    ['Mecidiyeköy', 'Nişantaşı', 'Bomonti', 'Fulya', 'Esentepe', 'Teşvikiye', 'Kurtuluş', 'Feriköy', 'Halaskargazi', 'Gülbağ'],
    ['besiktas', 'kagithane', 'beyoglu', 'sariyer'],
    'Şişli’de asıl mesele trafik ve park. Mecidiyeköy, Nişantaşı ve Halaskargazi hattında '
    'gündüz araç bekletmek neredeyse imkânsız, birçok sokakta park yasağı var. Nişantaşı ve '
    'Teşvikiye’deki eski apartmanlarda merdivenler geniş ama asansörler küçük. Şişli '
    'taşımalarını mümkün olduğunca hafta içi erken saate ya da hafta sonuna alıyoruz.'),

'zeytinburnu': ('Zeytinburnu',
    ['Merkezefendi', 'Kazlıçeşme', 'Telsiz', 'Seyitnizam', 'Sümer', 'Veliefendi', 'Beştelsiz', 'Maltepe', 'Nuripaşa', 'Gökalp'],
    ['bakirkoy', 'bahcelievler', 'gungoren', 'bayrampasa', 'fatih'],
    'Zeytinburnu sahil ile sanayiyi birleştiren bir ilçe; konut dokusu yoğun ve sokaklar dar. '
    'Telsiz ve Beştelsiz taraflarında bina araları çok sıkışık, asansörlü araç kurmak için '
    'yer bulmak bazen komşu sokağı kullanmayı gerektiriyor. Sahil yolu üzerindeki binalarda '
    'ise rüzgâr, asansörlü taşımada dikkat ettiğimiz ayrı bir etken.'),
}

SSS = [
    ('Evden eve nakliyat fiyatı neye göre belirleniyor?',
     'Eşyanın hacmi, çıkış ve varış adresinin katı, asansör durumu, aradaki mesafe ve '
     'ambalajlama ihtiyacı fiyatı belirleyen beş ana kalem. Telefonda tahmini bir aralık '
     'söyleyebiliriz ama net fiyat için ücretsiz keşif yapıyoruz — eve gelip eşyayı görmeden '
     'verilen kesin fiyat, taşıma günü sürprize dönüşüyor.'),
    ('Ambalaj malzemesi ayrıca ücretli mi?',
     'Standart taşımalarda battaniye, streç film ve balonlu naylon hizmete dahildir. '
     'Özel koruma isteyen parçalar (piyano, büyük ekran televizyon, cam vitrin, tablo) '
     'için kullanılan özel sandık ve malzeme keşifte ayrıca konuşulur.'),
    ('Eşyalarım sigortalı mı?',
     'Evet. Taşıma sigortalıdır; eşyanız araca yüklendiği andan yeni adresinizde yerine '
     'yerleştirildiği ana kadar kapsam devam eder. Sigorta kapsamı ve tutarı sözleşmede yazılıdır.'),
    ('Asansörsüz binada ne yapıyorsunuz?',
     'Asansörlü taşıma aracı kuruyoruz; eşya pencereden ya da balkondan güvenle indirilip '
     'yükleniyor. Bu yöntem hem çok daha hızlı hem de merdivende çarpma riskini ortadan kaldırıyor. '
     'Sokakta araç kurmaya uygun yer olup olmadığını keşifte kontrol ediyoruz.'),
    ('Eşyalarımı sökme ve kurma işini siz mi yapıyorsunuz?',
     'Evet. Yatak odası, gardırop, salon takımı ve mutfak dolaplarının sökümü, taşınması ve '
     'yeni adreste kurulumu ekibimize aittir. Beyaz eşya bağlantıları da tarafımızca yapılır.'),
    ('Taşınma gününü ne kadar önceden haber vermeliyim?',
     'Hafta içi taşımalar için üç-dört gün genellikle yeterli. Ay sonu, hafta sonu ve okul '
     'dönemi başlangıcı yoğun olduğu için bu tarihlerde bir hafta önceden konuşmak daha güvenli. '
     'Acil durumlarda aynı gün çıktığımız da oluyor, arayın konuşalım.'),
    ('Sadece birkaç parça eşyam var, yine de geliyor musunuz?',
     'Geliyoruz. Parça eşya taşıma hizmetimizde komple araç ücreti ödemezsiniz; tek koltuk, '
     'buzdolabı ya da birkaç koli için de aynı özenle çalışıyoruz.'),
    ('Taşıma kaç saat sürer?',
     'Bir artı bir daire genellikle yarım günde biter. Üç artı bir ve üzeri evlerde ambalajlama '
     'dahil bir tam gün planlamak gerekir. Villa ve çok katlı evlerde iş iki güne yayılabilir; '
     'bunu keşifte netleştirip size gün veriyoruz.'),
]

ADIMLAR = [
    ('Arayın', 'Telefon ya da WhatsApp’tan ulaşın; taşınacak evi ve tarihi konuşalım.'),
    ('Ücretsiz keşif', 'Uygun bir saatte eve gelip eşyayı yerinde görür, net fiyat veririz.'),
    ('Ambalajlama', 'Taşıma günü eşyanız sökülür, koli ve battaniyeyle tek tek paketlenir.'),
    ('Taşıma ve kurulum', 'Yeni adreste eşya yerleştirilir, sökülen her şey yeniden kurulur.'),
]

# Her ilçe için tek bir pratik saha ipucu. Amaç sayfa doldurmak değil:
# o ilçede taşınacak birinin gerçekten işine yarayacak somut bir uyarı.
IPUCU = {
'arnavutkoy': 'Hadımköy ve Deliklikaya çevresindeki sanayi bölgelerinde gündüz saatlerinde '
    'TIR trafiği yoğun oluyor. Bu bölgelerde taşımayı sabah dokuzdan önce başlatmak, '
    'aracın bina önünde beklemeden yüklenmesini sağlıyor.',
'avcilar': 'Avcılar’da birçok apartmanın asansörü buzdolabı ve gardırop geçirmiyor. '
    'Taşınmadan önce asansör kapı genişliğini bir metreyle ölçüp bize söylerseniz, '
    'asansörlü araç gerekip gerekmediğini keşfe gelmeden bile söyleyebiliriz.',
'bagcilar': 'Bağcılar’da sokakların çoğu çift taraflı park nedeniyle daralıyor. '
    'Taşıma sabahı bina önünde iki araçlık yeri boş tutabilirseniz süre belirgin kısalıyor; '
    'apartman yönetimine bir gün önceden haber vermek genelde yetiyor.',
'bahcelievler': 'Şirinevler ve Yenibosna’da öğle saatleri en sıkışık zaman dilimi. '
    'Taşımayı sabah erken saate alırsanız hem araç park sorunu yaşamazsınız hem de '
    'aynı gün içinde yerleşmeyi bitirme şansınız artar.',
'bakirkoy': 'Ataköy ve çevresindeki sitelerin çoğu taşınma için yönetimden yazılı izin ve '
    'asansör randevusu istiyor. Bu izni birkaç gün önceden almak, taşıma günü kapıda '
    'beklemenin önüne geçen tek şey.',
'basaksehir': 'Kayaşehir ve Bahçeşehir’deki bloklarda yük asansörü genelde tek ve tüm siteye '
    'hizmet ediyor. Yönetimden saat ayırtmadan gelen ekipler saatlerce sıra bekliyor; '
    'biz randevuyu sizin adınıza da alabiliyoruz.',
'bayrampasa': 'Bayrampaşa’da konut sokakları gün ortasında ticari araç yüklemesiyle kapanıyor. '
    'Özellikle hafta ortası taşımalarda sabahın ilk saatleri, akşamüstünden çok daha rahat.',
'besiktas': 'Ortaköy, Bebek ve Arnavutköy sahilinde bazı sokaklara kamyon giremiyor; eşya '
    'küçük araca aktarılarak taşınıyor. Adresinizi keşifte görmemiz bu yüzden fiyattan '
    'önce yöntemi belirlemek için önemli.',
'beylikduzu': 'Beylikdüzü sitelerinin önemli bir kısmında hafta sonu taşınma yasak ya da '
    'saatle sınırlı. Tarih seçmeden önce site yönetiminin taşınma kuralını sormanız, '
    'sonradan gün değiştirmek zorunda kalmanızı önler.',
'beyoglu': 'Cihangir ve Galata’da bazı sokaklara araç girişi belirli saatlerle sınırlı. '
    'Taşınma gününü belirlemeden önce sokağınızın araç giriş saatini öğrenirseniz, '
    'ekibi ve asansörlü aracı doğru saate göre planlarız.',
'buyukcekmece': 'Sahil şeridindeki yazlık sitelerde sezonda taşınma hem zor hem pahalı. '
    'Tarihinizde esneklik varsa yaz ortası yerine sezon dışına almak, hem fiyatı '
    'düşürüyor hem de siteye giriş iznini kolaylaştırıyor.',
'catalca': 'Çatalca’da bazı köy içi yollar büyük kamyon için uygun değil ve yağışlı havada '
    'zemin sorun çıkarıyor. Adresi bize tarif ederken son iki yüz metrenin yol durumunu '
    'da söylerseniz aracı ona göre seçeriz.',
'esenler': 'Esenler’de kentsel dönüşüm nedeniyle çok sayıda kısa mesafeli taşıma oluyor. '
    'Aynı mahalle içinde taşınıyorsanız komple araç yerine parça eşya hizmetimizi sorun; '
    'çoğu durumda belirgin şekilde uygun kalıyor.',
'esenyurt': 'Esenyurt’ta bir asansöre çok daire düşüyor. Taşıma gününde asansör sırası '
    'beklememek için yönetimden saat ayırtın; mümkünse yük asansörünü kullanın. '
    'Bazı sitelerde akşam saatlerinde taşınma tamamen yasak.',
'eyupsultan': 'Alibeyköy ve Rami tarafındaki dar yokuşlarla Göktürk’teki geniş siteler '
    'bambaşka iki taşıma demek. Adresinizin hangi tarafta olduğunu baştan söylerseniz '
    'ekip ve araç planını doğru kurarız.',
'fatih': 'Balat ve Fener’de sokaklar taş döşeli ve yokuşlu; tarihi binalarda merdivenler dar '
    've dönerli. Bu bölgede eşyanın önemli kısmı asansörlü araçla pencereden iniyor, '
    'hassas parçalar elde taşınıyor — keşif olmadan fiyat vermek doğru olmuyor.',
'gaziosmanpasa': 'Gaziosmanpaşa’da eğim yüzünden aracı bina hizasına çekmek çoğu sokakta '
    'mümkün olmuyor. Bina önünde araç duracak düz bir alan varsa bunu keşifte söylemeniz '
    'hem süreyi hem fiyatı etkiliyor.',
'gungoren': 'Merter tarafında gündüz saatlerinde tekstil yüklemesi yapan araçlar sokakları '
    'kapatabiliyor. Kendi ilçemiz olduğu için burada taşıma saatini en isabetli biz '
    'planlıyoruz; tarihinizi söyleyin, en uygun saati birlikte seçelim.',
'kagithane': 'Nurtepe, Gültepe ve Hamidiye’de sokaklar hem dar hem dik; büyük araç çoğu yere '
    'giremiyor ve eşya küçük araca aktarılıyor. Bu aktarma işi süreye eklenir, '
    'bu yüzden taşımayı güne yaymak yerine erken başlatmak gerekiyor.',
'kucukcekmece': 'Sefaköy’de dar sokak ve park sorunu, Halkalı’da ise site kuralları belirleyici. '
    'İlçe içinde taşınıyor olsanız bile iki adres bambaşka yöntem gerektirebilir; '
    'keşifte her iki adresi de görmek istiyoruz.',
'sariyer': 'Zekeriyaköy ve Bahçeköy’deki bahçeli evlerde eşya birden çok kata dağıldığı için '
    'taşıma iki güne yayılabiliyor. Ekip sayısını baştan yüksek tutmak toplam süreyi '
    've dolayısıyla maliyeti düşürüyor.',
'silivri': 'Silivri’ye ya da Silivri’den yapılan taşımalarda yol süresi işin en büyük kalemi. '
    'Eşyayı tek seferde alacak araçla çıkmak, iki sefer yapmaktan neredeyse her zaman '
    'daha ucuza geliyor — hacmi doğru ölçmek bu yüzden önemli.',
'sultangazi': 'Cebeci ve Habibler’de araç bina önüne çoğu zaman yanaşamıyor. Kentsel dönüşüm '
    'nedeniyle geçici taşınma yapıyorsanız, eşyanın bir bölümünü depoya alıp kalanını '
    'yeni adrese taşıdığımız karma çözüm hem yer hem para kazandırıyor.',
'sisli': 'Mecidiyeköy, Nişantaşı ve Halaskargazi hattında gündüz araç bekletmek neredeyse '
    'imkânsız, birçok sokakta park yasağı var. Şişli taşımalarını hafta içi erken saate '
    'ya da hafta sonuna almak en pratik çözüm.',
'zeytinburnu': 'Telsiz ve Beştelsiz’de binalar çok sıkışık; asansörlü araç kuracak yer bulmak '
    'bazen komşu sokağı kullanmayı gerektiriyor. Sahil yolundaki yüksek binalarda ise '
    'rüzgâr, asansörlü taşımada dikkat ettiğimiz ayrı bir etken.',
}
