# -*- coding: utf-8 -*-
"""
CSS ve JS kaynağı. build.py bunları assets/ altına yazar ve içerik SHA1'iyle damgalar.

⚠️ overflow-x YALNIZ html'de. body'ye de verilirse body kaydırma kabına dönüşür:
   sticky başlık ölür ve menü açıkken gövde kilidi tutmaz.
⚠️ picture varsayılan olarak satır içidir; yüzdelik yükseklik çözülemez → picture{display:block}.
⚠️ Ekranı geçen uzun bloklara .gel verme — IntersectionObserver geç tetikleniyor, içerik
   görünmüyormuş gibi oluyor.
"""

CSS = r"""
/* ── Yazı tipi ───────────────────────────────────────────── */
@font-face{
  font-family:'Plus Jakarta Sans';
  src:url('../fonts/pjs-var-tr.woff2') format('woff2-variations');
  font-weight:200 800; font-style:normal; font-display:swap;
}

/* ── Marka paleti (Umay kimlik dosyası) ───────────────────── */
:root{
  --sage:#8FA197;        /* logo yeşili */
  --sage-koyu:#6E756F;   /* ikincil metin, silik ögeler */
  --kurum:#3B3C39;       /* mürekkep, koyu şerit */
  --greige:#DAD5CC;      /* ana zemin */
  --krem:#F2F0EB;        /* açık bant, üst çubuk */

  --zemin:var(--greige);
  --zemin-ac:var(--krem);
  --kart:#fff;
  --murekkep:var(--kurum);
  --silik:var(--sage-koyu);
  --cizgi:var(--kurum);
  --bar:var(--kurum);
  /* Saç teli çizgiler mürekkebin şeffafından türetilir → her sıcak zeminde tutarlı durur. */
  --hat:rgba(59,60,57,.16);
  /* Buton gövde kalınlığı (3B çıkıntı) — düz renk olmalı, alfa gradyan üzerinde bulanıyor */
  --dg-kenar:#BEB7AA;      /* açık buton */
  --dg-kenar-koyu:#22231F; /* koyu buton */
  --mavi:#1A73E8;          /* arama eylemi — kullanıcı isteği */
  --mavi-kenar:#0F4FA8;
  /* Koyu şerit üzerindeki metin: soğuk gri yerine kremin şeffafı */
  --krem-yumusak:rgba(242,240,235,.78);
  --krem-silik:rgba(242,240,235,.55);

  --ust-h:88px;
  --sinir:1240px;
}

/* Kaydırınca üst çubuk incelir. Değişken :root'ta olduğu için mobil menünün
   `top` değeri ve logo yüksekliği kendiliğinden takip eder. */
html.kaydi{--ust-h:64px}

*,*::before,*::after{box-sizing:border-box}
html{
  overflow-x:hidden;           /* ⚠️ body'ye EKLEME — sticky başlık ölür */
  scroll-behavior:smooth;
  -webkit-text-size-adjust:100%;
}
@media (prefers-reduced-motion:reduce){ html{scroll-behavior:auto} }
body{
  margin:0; background:var(--zemin); color:var(--murekkep);
  font-family:'Plus Jakarta Sans',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  font-size:16px; line-height:1.65; -webkit-font-smoothing:antialiased;
}
img{max-width:100%; height:auto; display:block}
picture{display:block}          /* ⚠️ satır içi picture yüzdelik yüksekliği kırıyor */
a{color:inherit}
h1,h2,h3{line-height:1.12; letter-spacing:-.02em; margin:0}
p{margin:0 0 1em}

.sinir{max-width:var(--sinir); margin:0 auto; padding:0 24px}
.sinir.dar{max-width:820px}

.atla{position:absolute; left:-9999px; top:0; background:var(--kurum); color:var(--krem); padding:10px 16px; z-index:200}
.atla:focus{left:8px; top:8px}

/* Yer tutucu işareti — metin gelince data.py'de PH kalkar, bu da kaybolur */
.ph{background:#ffe8a3; color:#5b4300; padding:0 .25em; border-bottom:1px dashed #b58b00; font-style:italic}

/* ── Üst çubuk ───────────────────────────────────────────── */
.ust{
  position:sticky; top:0; z-index:100;
  background:var(--krem);
  /* ⚠️ .ust'e backdrop-filter VERME — mobil menü onun çocuğu; yığın bağlamı oluşunca
     menü açılır ama linkler tıklanmaz. Derinlik gölgeyle veriliyor. */
  border-bottom:1px solid var(--hat);
  box-shadow:0 1px 0 rgba(255,255,255,.6) inset;
  transition:box-shadow .32s ease, border-color .32s ease;
}
html.kaydi .ust{
  border-bottom-color:transparent;
  box-shadow:0 1px 0 rgba(255,255,255,.6) inset, 0 10px 30px -8px rgba(59,60,57,.22);
}
/* markanın yeşilinden ince bir aksan çizgisi — slab yerine iplik */
.ust::after{
  content:""; position:absolute; left:0; right:0; bottom:-1px; height:1px;
  background:linear-gradient(90deg,transparent,rgba(72,88,77,.55) 22%,rgba(72,88,77,.55) 78%,transparent);
  opacity:0; transition:opacity .32s ease;
}
html.kaydi .ust::after{opacity:1}
.ust-ic{
  max-width:var(--sinir); margin:0 auto; padding:0 28px;
  min-height:var(--ust-h); display:flex; align-items:center; gap:28px;
  transition:min-height .32s cubic-bezier(.4,0,.2,1);
}
.logo{text-decoration:none; display:flex; align-items:center}
/* Logo: gerçek marka varlığı (saydam WebP), oran 3,12:1.
   Yükseklik üst çubuğu belirler; genişlik orandan gelir. */
.logo-im{
  display:block; width:auto; height:calc(var(--ust-h) * .50);
  transition:height .32s cubic-bezier(.4,0,.2,1);
}
.logo:hover .logo-im{opacity:.82; transition:opacity .25s}
.logo-buyuk{height:72px}
@media (max-width:420px){ .logo-buyuk{height:56px} }

.menu{margin-left:auto}          /* ⚠️ mobilde .menu fixed olunca bu akıştan çıkar, aşağıda telafi var */
.menu ul{display:flex; gap:34px; list-style:none; margin:0; padding:0}
.menu ul{gap:38px}
.menu ul a{
  position:relative; display:block; padding:10px 2px;
  font-size:11px; font-weight:600; letter-spacing:.2em; text-transform:uppercase;
  text-decoration:none; color:var(--sage-koyu);
  transition:color .25s ease;
}
.menu ul a:hover,.menu ul a.etkin{color:var(--murekkep)}
/* ince alt çizgi ortadan açılır — 3px'lik slab yerine daha ölçülü bir işaret */
.menu ul a::after{
  content:""; position:absolute; left:0; right:0; bottom:0; height:1.5px;
  background:currentColor; transform:scaleX(0); transform-origin:center;
  transition:transform .32s cubic-bezier(.4,0,.2,1);
}
.menu ul a:hover::after,.menu ul a.etkin::after{transform:scaleX(1)}
.menu ul a.etkin{font-weight:700}

.hamburger{
  display:none; margin-left:auto; width:46px; height:46px; padding:14px 12px;
  background:#fff; border:1px solid var(--hat); cursor:pointer;
  flex-direction:column; justify-content:space-between; align-items:stretch;
  box-shadow:0 2px 8px rgba(59,60,57,.08); transition:box-shadow .25s,transform .2s;
}
.hamburger:active{transform:translateY(1px)}
.hamburger span{
  display:block; height:1.5px; background:var(--murekkep);
  transition:transform .32s cubic-bezier(.4,0,.2,1),opacity .2s,width .32s;
}
.hamburger span:nth-child(2){width:70%; align-self:flex-end}
.hamburger[aria-expanded="true"] span:nth-child(1){transform:translateY(7.5px) rotate(45deg)}
.hamburger[aria-expanded="true"] span:nth-child(2){opacity:0; width:100%}
.hamburger[aria-expanded="true"] span:nth-child(3){transform:translateY(-7.5px) rotate(-45deg)}

@media (max-width:880px){
  .hamburger{display:flex}
  .menu{
    position:fixed; inset:var(--ust-h) 0 auto 0; margin-left:0;
    background:var(--krem); border-bottom:1px solid var(--hat);
    box-shadow:0 24px 48px -16px rgba(59,60,57,.34);
    /* ⚠️ Yüzdelik öteleme panelin KENDİ yüksekliğine oranlıdır. Panel uzayınca
       (ör. alta iletişim bloğu eklenince) -104% yetmeyip panel başlığın altına taşıyor
       ve HAMBURGER TIKLANAMIYOR. Başlık yüksekliğini de düşerek kesin olarak çıkarıyoruz.
       visibility ayrıca kapalıyken tıklamayı ve erişilebilirlik ağacını kesiyor. */
    transform:translateY(calc(-100% - var(--ust-h)));
    visibility:hidden;
    transition:transform .42s cubic-bezier(.33,1,.68,1), visibility .42s;
    max-height:calc(100dvh - var(--ust-h)); overflow-y:auto;
  }
  .menu.acik{transform:translateY(0); visibility:visible}
  .menu ul{flex-direction:column; gap:0; padding:6px 28px 10px}
  .menu li{border-bottom:1px solid var(--hat)}
  .menu li:last-child{border-bottom:0}
  .menu ul a{
    padding:18px 0; font-size:12.5px; letter-spacing:.22em; color:var(--murekkep);
    display:flex; align-items:center; justify-content:space-between;
    opacity:0; transform:translateY(-8px);   /* açılışta sırayla süzülür */
    transition:opacity .32s ease,transform .32s ease,color .25s;
  }
  .menu.acik ul a{opacity:1; transform:none}
  .menu.acik li:nth-child(1) a{transition-delay:.06s}
  .menu.acik li:nth-child(2) a{transition-delay:.11s}
  .menu.acik li:nth-child(3) a{transition-delay:.16s}
  .menu.acik li:nth-child(4) a{transition-delay:.21s}
  .menu.acik li:nth-child(5) a{transition-delay:.26s}
  /* satır sonundaki ince ok, üzerine gelince uzar */
  .menu ul a::after{
    content:""; position:static; width:16px; height:1.5px; background:currentColor;
    opacity:.35; transform:none;
    transition:width .25s,opacity .25s;
  }
  .menu ul a:hover::after,.menu ul a.etkin::after{width:28px; opacity:1; transform:none}
  .menu ul a.etkin{font-weight:700}

  /* panel altındaki iletişim bloğu */
  .menu-ilt{
    display:flex; flex-direction:column; gap:10px;
    padding:16px 28px 22px; border-top:1px solid var(--hat);
    opacity:0; transform:translateY(-8px);
    transition:opacity .32s ease .3s,transform .32s ease .3s;
  }
  .menu.acik .menu-ilt{opacity:1; transform:none}
  .menu-ilt .dg{width:100%; text-align:center}
  .menu-ilt small{font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--sage-koyu)}
}
@media (min-width:881px){ .menu-ilt{display:none} }

/* ── Kahraman ────────────────────────────────────────────── */
.hero{position:relative; background:var(--greige); overflow:hidden}
.hero-gorsel img{
  width:100%; height:clamp(320px,62vh,620px); object-fit:cover; object-position:50% 8%;
  animation:heroOtur 2.2s cubic-bezier(.16,.84,.28,1) both;
}
@keyframes heroOtur{from{transform:scale(1.07)} to{transform:scale(1)}}

.hero-mono{
  position:absolute; inset:0; display:grid; place-content:center; justify-items:center;
  pointer-events:none;
}
.mono-maske{display:block; overflow:hidden; position:relative}   /* logo buradan yükselir */
.hero-logo{
  display:block; width:min(46vw,620px); height:auto;
  filter:drop-shadow(0 3px 34px rgba(0,0,0,.28));
  transform:translateY(106%); opacity:0;
  animation:logoYuksel 1.1s cubic-bezier(.16,.84,.28,1) .15s both;
}
@media (max-width:620px){ .hero-logo{width:74vw} }
@keyframes logoYuksel{
  from{transform:translateY(106%); opacity:0}
  to{transform:translateY(0); opacity:1}
}
/* logonun üzerinden bir kez geçen ışık */
.mono-maske::after{
  content:""; position:absolute; inset:0;
  background:linear-gradient(105deg,transparent 38%,rgba(255,255,255,.5) 50%,transparent 62%);
  mix-blend-mode:overlay; transform:translateX(-130%);
  animation:monoParla 1.3s ease-out 1s both;
}
@keyframes monoParla{to{transform:translateX(130%)}}

@media (prefers-reduced-motion:reduce){
  .hero-gorsel img,.mono-maske::after{animation:none}
  .hero-logo{animation:none; transform:none; opacity:1}
}

/* ── Başlıklar ───────────────────────────────────────────── */
.bolum-bas{
  text-align:center; font-size:clamp(26px,3.4vw,38px); font-weight:800; margin:0 0 14px;
}
.sol-bas{text-align:left}
.ust-baslik{
  text-align:center; font-size:11px; letter-spacing:.2em; text-transform:uppercase;
  color:var(--silik); font-weight:600; margin:0 0 26px;
}
.sol-bas + .ust-baslik{text-align:left}
.kural{display:block; width:58px; height:2px; background:var(--cizgi); margin:14px 0 18px}
.bolum-bas + .kural{margin-left:auto; margin-right:auto}

.giris,.sayfa-bas,.hizmetler-bolum,.projeler-bolum,.neden,.cta,.iletisim{padding:clamp(48px,7vw,92px) 0}
.sayfa-bas{padding-bottom:0}
.giris .metin p{font-size:17px; color:var(--murekkep)}
.giris .metin p:first-child{font-size:19px; font-weight:600; color:var(--murekkep)}

.dugmeler{display:flex; flex-wrap:wrap; gap:12px; margin-top:26px}
.bolum-bas ~ .dugmeler,.sinir.dar .dugmeler{justify-content:center}
.orta-baglanti{text-align:center; margin:38px 0 0}
/* ── Butonlar: fiziksel/3B his ───────────────────────────────
   Katmanlar: üstte iç ışık + altta iç gölge (yüzey eğimi), `0 Npx 0` ile gövde
   kalınlığı (çıkıntı), en altta yere düşen yumuşak gölge. Üzerine gelince yükselir,
   basınca çıkıntı kısalır ve düğme içeri çöker — kalınlık sabit kalsaydı his kaybolurdu. */
.dg{
  display:inline-block; padding:13px 26px; text-decoration:none;
  font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase;
  border:2px solid var(--cizgi);
  /* ⚠️ Saydam zemin greige üzerinde soluk kalıyordu — dock ve bildirimle aynı kural: NET BEYAZ. */
  background:linear-gradient(180deg,#fff 0%,#F6F4F0 100%); color:var(--murekkep);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.95),
    inset 0 -3px 0 rgba(59,60,57,.07),
    0 5px 0 var(--dg-kenar),
    0 11px 20px rgba(59,60,57,.20);
  transform:translateY(0);
  transition:background .22s,color .22s,transform .14s cubic-bezier(.2,.8,.3,1),box-shadow .14s;
}
.dg:hover{
  background:linear-gradient(180deg,#fff 0%,#EFECE6 100%);
  transform:translateY(-3px);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.95),
    inset 0 -3px 0 rgba(59,60,57,.07),
    0 8px 0 var(--dg-kenar),
    0 17px 28px rgba(59,60,57,.26);
}
.dg:active{
  transform:translateY(4px);
  box-shadow:
    inset 0 2px 4px rgba(59,60,57,.22),
    0 1px 0 var(--dg-kenar),
    0 3px 8px rgba(59,60,57,.18);
}
.dg-koyu{
  background:linear-gradient(180deg,#4A4B47 0%,var(--kurum) 100%); color:#fff;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.18),
    inset 0 -3px 0 rgba(0,0,0,.22),
    0 5px 0 var(--dg-kenar-koyu),
    0 11px 20px rgba(59,60,57,.34);
}
.dg-koyu:hover{
  background:linear-gradient(180deg,#545550 0%,#40413D 100%); color:#fff;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.22),
    inset 0 -3px 0 rgba(0,0,0,.22),
    0 8px 0 var(--dg-kenar-koyu),
    0 17px 28px rgba(59,60,57,.40);
}
.dg-ara{
  background:linear-gradient(180deg,#3B8BF0 0%,var(--mavi) 100%); color:#fff;
  border-color:var(--mavi-kenar);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.35),
    inset 0 -3px 0 rgba(0,0,0,.18),
    0 5px 0 var(--mavi-kenar),
    0 11px 20px rgba(26,115,232,.34);
}
.dg-ara:hover{
  background:linear-gradient(180deg,#4E97F5 0%,#1668D6 100%); color:#fff;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.4),
    inset 0 -3px 0 rgba(0,0,0,.18),
    0 8px 0 var(--mavi-kenar),
    0 17px 28px rgba(26,115,232,.42);
}
.dg-ara:active{
  box-shadow:
    inset 0 2px 5px rgba(0,0,0,.3),
    0 1px 0 var(--mavi-kenar),
    0 3px 8px rgba(26,115,232,.3);
}
.dg-koyu:active{
  box-shadow:
    inset 0 2px 5px rgba(0,0,0,.35),
    0 1px 0 var(--dg-kenar-koyu),
    0 3px 8px rgba(59,60,57,.3);
}
@media (max-width:620px){
  .dg{white-space:normal; text-align:center; flex:1 1 100%}  /* dar ekranda taşmasın */
}

/* ── Projeler: görselin üzerine kayan kart ───────────────── */
.projeler-bolum{background:var(--zemin)}
.proje{position:relative; margin:0 0 clamp(48px,7vw,86px)}
.proje:last-child{margin-bottom:0}
.proje-gorsel img{width:100%}
.proje-kart{
  background:var(--kart); padding:30px 32px; max-width:400px;
  box-shadow:0 18px 44px rgba(0,0,0,.07);
}
.proje-kart.kart-cerceve{background:var(--zemin); border:2px solid var(--cizgi); box-shadow:none}
.proje-kart h3{font-size:19px; font-weight:800}
.proje-kart p{font-size:15px; color:var(--murekkep); margin-bottom:.5em}
.proje-detay{font-size:11px !important; letter-spacing:.14em; text-transform:uppercase; color:var(--silik)}
.ok{display:block; width:64px; color:var(--murekkep); margin-top:18px; transition:transform .3s}
.proje:hover .ok{transform:translateX(8px)}

@media (min-width:900px){
  .proje{display:grid; grid-template-columns:repeat(12,1fr); align-items:center}
  .proje-gorsel{grid-row:1; grid-column:1/9}
  .proje-kart{grid-row:1; grid-column:7/13; justify-self:end; z-index:2}
  .proje.sag .proje-gorsel{grid-column:5/13}
  .proje.sag .proje-kart{grid-column:1/7; justify-self:start}
}
@media (max-width:899px){
  .proje-kart{margin:-48px 16px 0; max-width:none; position:relative; z-index:2}
}

/* ── Hizmetler ───────────────────────────────────────────── */
.hizmetler-bolum{background:var(--zemin-ac)}
.hizmet-akis{display:grid; gap:26px; grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.hizmet-akis .hizmet{background:var(--kart); padding:28px 26px; margin:0; border:1px solid var(--hat)}
.hizmet-akis .hizmet-metin h3{font-size:17px}
.hizmet-no{font-size:11px; font-weight:700; letter-spacing:.2em; color:var(--silik)}
.hizmet h3{font-size:22px; font-weight:800; margin-top:8px}
.hizmet p{font-size:15.5px; color:var(--murekkep)}

.hizmetler-bolum.tam .hizmet{
  display:grid; gap:clamp(24px,4vw,54px); align-items:center;
  padding:clamp(28px,4vw,44px) 0; border-top:1px solid var(--hat); margin:0;
}
.hizmetler-bolum.tam .hizmet:first-child{border-top:0}
@media (min-width:900px){
  .hizmetler-bolum.tam .hizmet{grid-template-columns:1fr 1.05fr}
  .hizmetler-bolum.tam .hizmet:nth-child(even) .hizmet-metin{order:2}
  /* Görseli olmayan hizmet iki sütunlu kalırsa sağ yarı boş görünüyor. */
  .hizmetler-bolum.tam .hizmet-tek{grid-template-columns:1fr}
  .hizmetler-bolum.tam .hizmet-tek .hizmet-metin{max-width:62ch}
}
.hizmet-gorsel{margin:0}
.hizmet-gorsel img{width:100%; border:1px solid var(--hat)}
.hizmet-gorsel figcaption{
  font-size:12px; color:var(--silik); margin-top:10px; line-height:1.5;
}

/* ── Neden birlikte çalışmalıyız ─────────────────────────── */
.neden{background:var(--zemin)}
.neden-izgara{display:grid; gap:22px; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); margin-top:32px}
.neden-kart{background:var(--kart); padding:30px 28px}
.neden-kart h3{font-size:17px; font-weight:800}
.neden-kart p{font-size:15px; color:var(--murekkep); margin:0}

/* ── Çağrı şeridi ────────────────────────────────────────── */
.cta{background:var(--bar); color:var(--krem)}
.cta .bolum-bas{color:var(--krem)}
.cta-metin{text-align:center; max-width:720px; margin:0 auto; color:var(--krem-yumusak)}
.cta .dg{
  background:linear-gradient(180deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,.04) 100%);
  border-color:#fff; color:#fff;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.3), 0 5px 0 rgba(0,0,0,.35), 0 11px 20px rgba(0,0,0,.34);
}
.cta .dg:hover{
  background:#fff; color:var(--bar);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9), 0 8px 0 rgba(0,0,0,.4), 0 17px 28px rgba(0,0,0,.4);
}
.cta .dg-koyu{
  background:linear-gradient(180deg,#fff 0%,#E8E5DE 100%); color:var(--bar);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.95), 0 5px 0 #9E988C, 0 11px 20px rgba(0,0,0,.38);
}
.cta .dg-koyu:hover{
  background:linear-gradient(180deg,#fff 0%,#DDD9D0 100%); color:var(--bar);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.95), 0 8px 0 #9E988C, 0 17px 28px rgba(0,0,0,.44);
}
.cta .dg:active,.cta .dg-ara{
  background:linear-gradient(180deg,#3B8BF0 0%,var(--mavi) 100%); color:#fff;
  border-color:var(--mavi-kenar);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.35),
    inset 0 -3px 0 rgba(0,0,0,.18),
    0 5px 0 var(--mavi-kenar),
    0 11px 20px rgba(26,115,232,.34);
}
.dg-ara:hover{
  background:linear-gradient(180deg,#4E97F5 0%,#1668D6 100%); color:#fff;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.4),
    inset 0 -3px 0 rgba(0,0,0,.18),
    0 8px 0 var(--mavi-kenar),
    0 17px 28px rgba(26,115,232,.42);
}
.dg-ara:active{
  box-shadow:
    inset 0 2px 5px rgba(0,0,0,.3),
    0 1px 0 var(--mavi-kenar),
    0 3px 8px rgba(26,115,232,.3);
}
.dg-koyu:active{
  transform:translateY(4px);
  box-shadow:inset 0 2px 5px rgba(0,0,0,.3), 0 1px 0 rgba(0,0,0,.35), 0 3px 8px rgba(0,0,0,.3);
}

/* ── İletişim ────────────────────────────────────────────── */
.iletisim{background:var(--zemin-ac)}
.ilt{margin:0}
.ilt-satir{display:grid; gap:4px 20px; padding:18px 0; border-top:1px solid var(--hat)}
.ilt-satir:first-child{border-top:0}
@media (min-width:640px){ .ilt-satir{grid-template-columns:190px 1fr; align-items:baseline} }
.ilt dt{font-size:11px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--silik)}
.ilt dd{margin:0; font-size:17px}
.ilt dd a{text-decoration:none; border-bottom:1px solid currentColor}

/* ── Alt bilgi ───────────────────────────────────────────── */
.alt{background:var(--zemin)}
.alt-gorsel img{width:100%; height:clamp(220px,34vh,360px); object-fit:cover}
.alt-kart{
  background:var(--kart); max-width:var(--sinir); margin:0 auto;
  padding:clamp(34px,5vw,52px) clamp(24px,4vw,56px);
}
.alt-logo{margin:0 0 4px; color:var(--kurum)}
.alt-kisi{font-weight:600; margin:0 0 14px}
.alt-sat{margin:0 0 6px; color:var(--murekkep)}
.alt-sat a{text-decoration:none; border-bottom:1px solid var(--hat)}
.alt-sos{margin:20px 0 0}
.sos{
  display:inline-flex; align-items:center; gap:9px; text-decoration:none;
  padding:9px 16px 9px 11px; background:#fff; border:1px solid var(--hat);
  color:var(--murekkep); font-size:13px; font-weight:600;
  box-shadow:0 3px 10px rgba(59,60,57,.08);
  transition:transform .22s,box-shadow .22s;
}
.sos:hover{transform:translateY(-2px); box-shadow:0 8px 20px rgba(59,60,57,.16)}
/* ⚠️ fill BURADA TANIMLANMAZ — ikon kendi marka degradesini <defs> içinden alıyor;
   CSS'teki fill sunum özniteliğini ezip ikonu tek renge düşürürdü. */
.sos svg{width:21px; height:21px; flex:0 0 21px}
.alt-serit{background:var(--bar); color:var(--krem-yumusak); text-align:center; padding:20px 24px 24px}
/* ⚠️ Mobilde sağ alt dock sabit duruyor; alt pay olmazsa imza onun altında kalıp
   tıklanamıyor. Pay dock yüksekliğinden (2 düğme + boşluk + 12px) fazla olmalı. */
@media (max-width:760px){ .alt-serit{padding-bottom:132px} }
.alt-serit p{margin:0 0 12px; font-size:13px}

/* ── Web4Medya imzası ────────────────────────────────────────
   ⚠️ Bağlantı SADECE marka adını sarar; rozeti <a> yapma.
   Mavi #0B57D0 koyu zeminde okunmuyor → aynı ailenin açık tonu.        */
.w4{--w4-mavi:#4D90FF; display:flex; justify-content:center; position:relative}
.w4::before{
  content:""; display:block; position:absolute; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),transparent); margin-top:-14px;
}
.w4-bag{
  display:inline-flex; align-items:center; gap:7px; padding:7px 15px; border-radius:999px;
  background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
  font-size:12px; letter-spacing:.02em; position:relative; overflow:hidden;
  transition:transform .3s,border-color .3s;
}
.w4-etiket{color:var(--krem-silik)}
.alt-serit a.w4-ad{color:#fff; text-decoration:none; font-weight:700; border:0; position:relative}
.w4-d{color:var(--w4-mavi); text-shadow:0 0 10px rgba(77,144,255,.55)}
.w4-ad::after{
  content:""; position:absolute; left:0; right:0; bottom:-3px; height:1px;
  background:var(--w4-mavi); transform:scaleX(0); transition:transform .3s;
}
.w4-bag:has(.w4-ad:hover){transform:translateY(-2px); border-color:rgba(77,144,255,.4)}
.w4-bag:has(.w4-ad:hover) .w4-ad::after{transform:scaleX(1)}
.w4-bag::after{
  content:""; position:absolute; top:0; bottom:0; width:40%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.14),transparent);
  transform:translateX(-160%);
}
.w4-bag:has(.w4-ad:hover)::after{animation:parla .8s ease}
@keyframes parla{to{transform:translateX(260%)}}

/* ── Yukarı çık (sol alt — sağ altı dock kullanıyor) ─────── */
.yukari{
  position:fixed; left:0; bottom:0; z-index:60;
  width:46px; height:46px; display:grid; place-items:center;
  background:rgba(110,117,111,.9); color:var(--krem); text-decoration:none;
  opacity:0; visibility:hidden; transition:opacity .3s,visibility .3s;
}
.yukari svg{width:22px}
.yukari.gorun{opacity:1; visibility:visible}

/* ── Sağ alt dock: WhatsApp + Hemen Ara ──────────────────── */
.dock{
  position:fixed; right:18px; bottom:18px; z-index:70;
  display:flex; flex-direction:column; gap:11px; align-items:flex-end;
  transition:transform .35s cubic-bezier(.4,0,.2,1);
}
.dock-dg{
  --renk:var(--bar);
  display:inline-flex; align-items:center; gap:10px;
  padding:12px 18px 12px 14px; border-radius:999px; text-decoration:none;
  background:#fff; color:var(--murekkep);
  border:1px solid rgba(0,0,0,.09);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.95),
    inset 0 -3px 0 rgba(59,60,57,.06),
    0 4px 0 var(--dg-kenar),
    0 12px 26px rgba(59,60,57,.24);
  font-size:13px; font-weight:700; letter-spacing:.01em; white-space:nowrap;
  transition:transform .25s,box-shadow .25s,background .25s;
  position:relative; overflow:hidden;
}
.dock-dg:hover{
  transform:translateY(-3px); background:#fff;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.95),
    inset 0 -3px 0 rgba(59,60,57,.06),
    0 7px 0 var(--dg-kenar),
    0 18px 34px rgba(59,60,57,.3);
}
.dock-dg:active{
  transform:translateY(3px);
  box-shadow:inset 0 2px 4px rgba(59,60,57,.2), 0 1px 0 var(--dg-kenar), 0 3px 8px rgba(59,60,57,.18);
}
.dock-ikon{
  width:30px; height:30px; flex:0 0 30px; border-radius:50%;
  display:grid; place-items:center; background:var(--renk); color:#fff;
}
.dock-ikon svg{width:17px; fill:currentColor}
.dock-wa{--renk:#25D366}
.dock-ara{--renk:#1A73E8}
/* nabız — dikkat çeker ama yormaz */
.dock-ara .dock-ikon::after{
  content:""; position:absolute; width:30px; height:30px; border-radius:50%;
  border:2px solid var(--renk); animation:nabiz 2.6s ease-out infinite;
}
@keyframes nabiz{
  0%{transform:scale(1); opacity:.55}
  70%,100%{transform:scale(1.85); opacity:0}
}
@media (prefers-reduced-motion:reduce){ .dock-ara .dock-ikon::after{animation:none} }
@media (max-width:520px){
  .dock{right:12px; bottom:12px; gap:9px}
  .dock-dg{padding:11px 16px 11px 12px; font-size:12.5px}
}

/* ── Çevrimiçi bildirimi (%50 kaydırmada) ────────────────── */
.bildirim{
  position:fixed; right:18px; bottom:18px; z-index:75; width:min(330px,calc(100vw - 36px));
  /* ⚠️ Net beyaz — krem zemin, krem bandın üzerinde eriyip belirginliğini yitiriyordu. */
  background:#fff; border:1px solid rgba(0,0,0,.09); border-radius:14px;
  box-shadow:0 22px 60px rgba(0,0,0,.26);
  padding:16px 40px 16px 18px;
  transform:translateY(24px) scale(.96); opacity:0; visibility:hidden;
  transition:transform .4s cubic-bezier(.2,.9,.3,1),opacity .4s,visibility .4s;
}
.bildirim.gorun{transform:none; opacity:1; visibility:visible}
.bildirim-bas{display:flex; align-items:center; gap:8px; font-weight:800; font-size:14px; margin:0 0 4px}
.nokta{
  width:9px; height:9px; border-radius:50%; background:#1F9D55; flex:0 0 9px;
  box-shadow:0 0 0 0 rgba(31,157,85,.6); animation:canli 2s infinite;
}
@keyframes canli{70%{box-shadow:0 0 0 9px rgba(31,157,85,0)} 100%{box-shadow:0 0 0 0 rgba(31,157,85,0)}}
@media (prefers-reduced-motion:reduce){ .nokta{animation:none} }
.bildirim p{margin:0 0 12px; font-size:14px; color:var(--murekkep); line-height:1.5}
.bildirim .dg{padding:10px 18px; font-size:11px; border-width:2px}
.bildirim-kapat{
  position:absolute; top:8px; right:8px; width:30px; height:30px; border:0; border-radius:50%;
  background:none; color:var(--sage-koyu); font-size:19px; line-height:1; cursor:pointer;
}
.bildirim-kapat:hover{background:var(--greige); color:var(--murekkep)}
/* Bildirim açıkken dock çakışmasın — yukarı kayar */
body.bildirim-acik .dock{transform:translateY(-168px)}
@media (max-width:520px){
  .bildirim{right:12px; bottom:12px}
  body.bildirim-acik .dock{transform:translateY(-176px)}
}

/* ── Görsel yer tutucu ───────────────────────────────────── */
.gorsel-yok{
  display:grid; place-items:center; aspect-ratio:4/3; background:var(--greige);
  color:var(--sage-koyu); font-size:12px; font-weight:700; letter-spacing:.16em; text-align:center;
}

/* ── Ortaya çıkış ────────────────────────────────────────────
   ⚠️ Yalnız html.js varken gizle; JS gecikirse içerik yine görünür.
   ⚠️ Ekrandan uzun bloklara .gel VERME (IntersectionObserver geç tetikleniyor).  */
.js .gel{opacity:0; transform:translateY(22px); transition:opacity .6s,transform .6s}
.js .gel.acildi{opacity:1; transform:none}
@media (prefers-reduced-motion:reduce){ .js .gel{opacity:1; transform:none} }
"""


JS = r"""
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
  var kok = document.documentElement;

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

    /* Üst çubuk kaydırınca incelir + gölge kazanır.
       ⚠️ Zemin HER DURUMDA opak krem — şeffaf yapıp JS'e bağlamak, betik gecikince
       kahramanın üzerinde okunmaz logo bırakır. Burada yalnız yükseklik/gölge değişiyor. */
    if (kok) kok.classList.toggle('kaydi', y > 24);

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
"""
