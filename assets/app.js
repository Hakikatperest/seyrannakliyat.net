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
      }, { rootMargin: '0px 0px -4% 0px', threshold: 0 });
      gelenler.forEach(function (e) { g.observe(e); });

      /* Güvenlik ağı: gözlemci herhangi bir sebeple tetiklenmezse içerik
         gizli kalmamalı. Uzun bloklarda 3B döndürme sınır kutusunu da
         döndürdüğü için tetikleme gecikip "beyaz ekran" oluşuyordu. */
      setTimeout(function () {
        document.querySelectorAll('.gel:not(.gorundu)').forEach(function (el) {
          var k = el.getBoundingClientRect();
          if (k.top < innerHeight * 1.5) el.classList.add('gorundu');
        });
      }, 2500);
      addEventListener('load', function () {
        setTimeout(function () {
          document.querySelectorAll('.gel:not(.gorundu)').forEach(function (el) {
            if (el.getBoundingClientRect().top < innerHeight) el.classList.add('gorundu');
          });
        }, 300);
      });
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
  /* Eğim YALNIZCA fareli masaüstünde. Mobilde görsel dümdüz durur —
     kaydırmaya bağlı eğim ve cihaz eğimi denendi, kullanıcı "resim yamuk
     kalıyor" diye iki kez bildirdi. Mobildeki derinlik açılış animasyonu,
     gölge ve perspektiften geliyor; görselin kendisi eğilmiyor. */
  if (sahne && egik && !azHareket &&
      matchMedia('(hover: hover) and (pointer: fine)').matches &&
      matchMedia('(min-width:1001px)').matches) {
    var bekleyen = null, sonX = 0, sonY = 0;

    function ciz() {
      bekleyen = null;
      egik.style.setProperty('--rx', (7 - sonY * 11).toFixed(2) + 'deg');
      egik.style.setProperty('--ry', (-9 + sonX * 13).toFixed(2) + 'deg');
    }
    function iste() { if (!bekleyen) bekleyen = requestAnimationFrame(ciz); }

    sahne.addEventListener('pointermove', function (e) {
      var k = sahne.getBoundingClientRect();
      sonX = (e.clientX - k.left) / k.width - 0.5;
      sonY = (e.clientY - k.top) / k.height - 0.5;
      iste();
    });
    sahne.addEventListener('pointerleave', function () {
      egik.style.removeProperty('--rx');
      egik.style.removeProperty('--ry');
    });
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

  /* ── Çevrimiçi bildirimi ─────────────────────────────────────────────
     Sayfanın yarısına inilince bir kez açılır. Kapatılırsa oturum boyunca
     tekrar gelmez — her kaydırmada yüzüne çıkan bildirim rahatsız eder. */
  var bldrm = document.getElementById('bildirim');
  if (bldrm) {
    var kapali = false;
    try { kapali = sessionStorage.getItem('sn-bildirim') === 'kapali'; } catch (e) {}
    var acildi = false;

    function bildirimBak() {
      if (acildi || kapali) return;
      var toplam = document.documentElement.scrollHeight - innerHeight;
      if (toplam > 0 && scrollY / toplam >= 0.5) {
        acildi = true;
        bldrm.classList.add('acik');
        removeEventListener('scroll', bildirimBak);
      }
    }
    if (!kapali) addEventListener('scroll', bildirimBak, { passive: true });

    document.getElementById('bildirimKapat').addEventListener('click', function () {
      bldrm.classList.remove('acik');
      kapali = true;
      try { sessionStorage.setItem('sn-bildirim', 'kapali'); } catch (e) {}
    });
  }

  /* ── Yıl ─────────────────────────────────────────────────────────────── */
  var yil = document.getElementById('yil');
  if (yil) yil.textContent = new Date().getFullYear();
})();
