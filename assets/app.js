/* =============================================================================
   Seyran Nakliyat — tek betik (26 sayfa paylaşır)

   Kural: hiçbir dış kütüphane yok, hiçbir üçüncü parti istek yok. Ağır olan
   her şey (video, harita) kullanıcı isteyene kadar YÜKLENMEZ.
   ========================================================================== */
(function () {
  'use strict';
  var azHareket = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Üst bar: sayfa kayınca camlaşır ─────────────────────────────────── */
  var ust = document.querySelector('.ust');
  if (ust) {
    var yapisikYaz = function () {
      ust.classList.toggle('yapisik', window.scrollY > 12);
    };
    yapisikYaz();
    addEventListener('scroll', yapisikYaz, { passive: true });
  }

  /* ── Mobil menü ──────────────────────────────────────────────────────── */
  var dug = document.querySelector('.menu-dug'), menu = document.querySelector('.menu');
  if (dug && menu) {
    dug.addEventListener('click', function () {
      var acik = menu.classList.toggle('acik');
      dug.setAttribute('aria-expanded', acik ? 'true' : 'false');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('acik');
        dug.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ── Görünürlükte belirme ────────────────────────────────────────────── */
  var gelenler = document.querySelectorAll('.gel');
  if (gelenler.length) {
    if (azHareket || !('IntersectionObserver' in window)) {
      gelenler.forEach(function (e) { e.classList.add('gorundu'); });
    } else {
      var g = new IntersectionObserver(function (kayitlar) {
        kayitlar.forEach(function (k) {
          if (!k.isIntersecting) return;
          /* Aynı kaptaki kardeşler sırayla kalksın — tek tek değil, dalga hâlinde. */
          var kardesler = Array.prototype.filter.call(
            k.target.parentElement ? k.target.parentElement.children : [],
            function (c) { return c.classList.contains('gel'); });
          var i = kardesler.indexOf(k.target);
          if (i > 0) k.target.style.transitionDelay = Math.min(i, 6) * 70 + 'ms';
          k.target.classList.add('gorundu');
          g.unobserve(k.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      gelenler.forEach(function (e) { g.observe(e); });
    }
  }

  /* ── Kahraman görselinde 3B ───────────────────────────────────────────
     Üç kaynak: fare (masaüstü), sayfa kaydırma (her cihaz) ve cihaz eğimi
     (telefonu yatırınca — Android'de izinsiz çalışır). Üçü de aynı iki CSS
     değişkenini yazar, hepsi rAF ile tek kareye indirilir. */
  var sahne = document.querySelector('.sahne'), egik = document.querySelector('.egik');
  if (egik) {
    /* Açılış animasyonu bitince bırak: fill-mode "both" ile asılı kalırsa
       CSS transition'ı ezer ve fare/eğim hareketi sert görünür. */
    egik.addEventListener('animationend', function (e) {
      if (e.animationName === 'egikAc') egik.classList.add('acildi');
    });
  }
  if (sahne && egik && !azHareket) {
    var temelRX = 7, temelRY = -9;
    if (matchMedia('(max-width:1000px)').matches) { temelRX = 5; temelRY = -6; }

    var fareX = 0, fareY = 0, egimX = 0, egimY = 0, kaydirma = 0, bekleyen = null;

    function ciz() {
      bekleyen = null;
      var rx = temelRX - fareY * 11 - egimX + kaydirma * 9;
      var ry = temelRY + fareX * 13 + egimY;
      egik.style.setProperty('--rx', rx.toFixed(2) + 'deg');
      egik.style.setProperty('--ry', ry.toFixed(2) + 'deg');
    }
    function iste() { if (!bekleyen) bekleyen = requestAnimationFrame(ciz); }

    if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
      sahne.addEventListener('pointermove', function (e) {
        var k = sahne.getBoundingClientRect();
        fareX = (e.clientX - k.left) / k.width - 0.5;
        fareY = (e.clientY - k.top) / k.height - 0.5;
        iste();
      });
      sahne.addEventListener('pointerleave', function () { fareX = fareY = 0; iste(); });
    }

    /* Kaydırdıkça görsel hafifçe arkaya yatar — mobilde asıl derinlik burada. */
    addEventListener('scroll', function () {
      var k = sahne.getBoundingClientRect();
      if (k.bottom < 0 || k.top > innerHeight) return;
      kaydirma = Math.max(-1, Math.min(1, -k.top / innerHeight));
      iste();
    }, { passive: true });

    /* Cihaz eğimi: iOS izin istediği için yalnızca izin gerektirmeyen
       tarayıcılarda (Android) bağlanıyor; istem çıkarıp kullanıcıyı
       rahatsız etmiyoruz. */
    if (window.DeviceOrientationEvent &&
        typeof DeviceOrientationEvent.requestPermission !== 'function' &&
        matchMedia('(hover: none)').matches) {
      addEventListener('deviceorientation', function (e) {
        if (e.beta === null && e.gamma === null) return;
        egimX = Math.max(-8, Math.min(8, ((e.beta || 0) - 45) * 0.16));
        egimY = Math.max(-9, Math.min(9, (e.gamma || 0) * 0.20));
        iste();
      }, { passive: true });
    }
  }

  /* ── Sayaçlar ────────────────────────────────────────────────────────── */
  var sayaclar = document.querySelectorAll('[data-sayac]');
  if (sayaclar.length && 'IntersectionObserver' in window) {
    var sg = new IntersectionObserver(function (kayitlar) {
      kayitlar.forEach(function (k) {
        if (!k.isIntersecting) return;
        sg.unobserve(k.target);
        var el = k.target, hedef = parseInt(el.dataset.sayac, 10) || 0, sonek = el.dataset.sonek || '';
        if (azHareket) { el.textContent = hedef + sonek; return; }
        var t0 = performance.now(), sure = 1100;
        (function adim(t) {
          var o = Math.min(1, (t - t0) / sure);
          o = 1 - Math.pow(1 - o, 3);
          el.textContent = Math.round(hedef * o) + sonek;
          if (o < 1) requestAnimationFrame(adim);
        })(t0);
      });
    }, { threshold: 0.4 });
    sayaclar.forEach(function (e) { sg.observe(e); });
  }

  /* ── Video: tıklanana kadar tek bayt inmez ───────────────────────────── */
  document.querySelectorAll('.vid-dug').forEach(function (b) {
    b.addEventListener('click', function () {
      var kutu = b.parentElement, kaynak = b.dataset.video;
      if (!kaynak) return;
      var v = document.createElement('video');
      v.src = kaynak; v.controls = true; v.autoplay = true; v.playsInline = true;
      v.preload = 'auto';
      v.setAttribute('poster', b.dataset.poster || '');
      kutu.innerHTML = '';
      kutu.appendChild(v);
      v.play().catch(function () {});
    });
  });

  /* ── Yıl ─────────────────────────────────────────────────────────────── */
  var yil = document.getElementById('yil');
  if (yil) yil.textContent = new Date().getFullYear();
})();
