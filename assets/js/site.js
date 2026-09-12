
(function(){
  'use strict';

  /* ── Menü ─────────────────────────────────────────────── */
  var ham = document.querySelector('.hamburger');
  var menu = document.getElementById('menu');
  if (ham && menu) {
    ham.addEventListener('click', function(){
      var acik = menu.classList.toggle('acik');
      ham.setAttribute('aria-expanded', acik ? 'true' : 'false');
      ham.setAttribute('aria-label', acik ? 'Menüyü kapat' : 'Menüyü aç');
    });
    menu.addEventListener('click', function(ev){
      if (ev.target.closest('a')) {
        menu.classList.remove('acik');
        ham.setAttribute('aria-expanded','false');
      }
    });
    document.addEventListener('keydown', function(ev){
      if (ev.key === 'Escape' && menu.classList.contains('acik')) {
        menu.classList.remove('acik');
        ham.setAttribute('aria-expanded','false');
        ham.focus();
      }
    });
  }

  /* ── Ortaya çıkış ─────────────────────────────────────── */
  var gelenler = document.querySelectorAll('.gel');
  if (gelenler.length && 'IntersectionObserver' in window) {
    var go = new IntersectionObserver(function(girisler){
      girisler.forEach(function(g){
        if (!g.isIntersecting) return;
        var kap = g.target.parentElement;
        var kardes = kap ? Array.prototype.indexOf.call(kap.children, g.target) : 0;
        g.target.style.transitionDelay = Math.min(kardes, 4) * 70 + 'ms';
        g.target.classList.add('acildi');
        go.unobserve(g.target);
      });
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.04});
    gelenler.forEach(function(el){ go.observe(el); });
    /* Güvenlik ağı: 2,5 sn sonra görünür alanda gizli kalan varsa aç. */
    setTimeout(function(){
      document.querySelectorAll('.gel:not(.acildi)').forEach(function(el){
        if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('acildi');
      });
    }, 2500);
  }

  /* ── Yukarı çık ───────────────────────────────────────── */
  var yukari = document.querySelector('.yukari');

  /* ── Çevrimiçi bildirimi (%50 kaydırma) ───────────────── */
  var bildirim = document.querySelector('.bildirim');
  var kapatildi = false;
  try { kapatildi = sessionStorage.getItem('ugm-bildirim') === 'kapali'; } catch(e) {}

  var kapat = bildirim && bildirim.querySelector('.bildirim-kapat');
  if (kapat) {
    kapat.addEventListener('click', function(){
      kapatildi = true;
      bildirim.classList.remove('gorun');
      document.body.classList.remove('bildirim-acik');
      try { sessionStorage.setItem('ugm-bildirim','kapali'); } catch(e) {}
    });
  }

  var bekliyor = false;
  function kaydirma(){
    bekliyor = false;
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var toplam = document.documentElement.scrollHeight - window.innerHeight;
    var oran = toplam > 0 ? y / toplam : 0;

    if (yukari) yukari.classList.toggle('gorun', y > 500);

    if (bildirim && !kapatildi) {
      /* ⚠️ Sayfa dibinde GÖSTERME: sabit bildirim alt bilgideki Web4Medya imzasının üstünü
         örtüyor ve mobilde imza tıklanamıyor. Dibe yaklaşınca gizlenince dock da yerine iner. */
      var dibeKalan = toplam - y;
      var ac = oran >= 0.5 && dibeKalan > 280;
      bildirim.classList.toggle('gorun', ac);
      document.body.classList.toggle('bildirim-acik', ac);
    }
  }
  window.addEventListener('scroll', function(){
    if (bekliyor) return;
    bekliyor = true;
    window.requestAnimationFrame(kaydirma);
  }, {passive:true});
  kaydirma();
})();
