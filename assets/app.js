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
          k.target.classList.add('gorundu');
          g.unobserve(k.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      gelenler.forEach(function (e) { g.observe(e); });
    }
  }

  /* ── Kahraman görselinde 3B eğim ─────────────────────────────────────
     Yalnızca fare olan cihazlarda; dokunmatikte sabit açı kalır.        */
  var sahne = document.querySelector('.sahne'), egik = document.querySelector('.egik');
  if (sahne && egik && !azHareket && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var bekleyen = null;
    sahne.addEventListener('pointermove', function (e) {
      if (bekleyen) return;
      bekleyen = requestAnimationFrame(function () {
        bekleyen = null;
        var k = sahne.getBoundingClientRect();
        var x = (e.clientX - k.left) / k.width - 0.5;
        var y = (e.clientY - k.top) / k.height - 0.5;
        egik.style.setProperty('--ry', (-9 + x * 13).toFixed(2) + 'deg');
        egik.style.setProperty('--rx', (7 - y * 11).toFixed(2) + 'deg');
      });
    });
    sahne.addEventListener('pointerleave', function () {
      egik.style.removeProperty('--ry');
      egik.style.removeProperty('--rx');
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

  /* ── Yıl ─────────────────────────────────────────────────────────────── */
  var yil = document.getElementById('yil');
  if (yil) yil.textContent = new Date().getFullYear();
})();
