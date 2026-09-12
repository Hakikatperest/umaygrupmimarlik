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
  /* Koyu şerit üzerindeki metin: soğuk gri yerine kremin şeffafı */
  --krem-yumusak:rgba(242,240,235,.78);
  --krem-silik:rgba(242,240,235,.55);

  --ust-h:64px;
  --sinir:1240px;
}

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
  background:var(--krem); border-bottom:3px solid var(--cizgi);
}
.ust-ic{
  max-width:var(--sinir); margin:0 auto; padding:0 24px;
  min-height:var(--ust-h); display:flex; align-items:center; gap:24px;
}
.logo{text-decoration:none; display:block; color:var(--kurum)}

/* ── Logo kilidi (işaret + UMAY / PROJE) ─────────────────────
   Kimlikteki dizilim: çizgisel ev markası, yanında geniş harf aralıklı UMAY,
   altında iki kısa çizgi arasında PROJE.                                    */
.logo-kilit{display:inline-flex; align-items:center; gap:11px}
.logo-im{width:auto; height:38px; flex:0 0 auto}
.logo-yazi{display:flex; flex-direction:column; line-height:1}
.logo-ad{
  font-size:21px; font-weight:600; letter-spacing:.26em; text-indent:.26em;
}
.logo-alt{
  display:flex; align-items:center; gap:6px; margin-top:4px;
  font-size:8.5px; font-weight:500; letter-spacing:.42em; text-indent:.42em;
}
.logo-alt i{flex:1 1 auto; height:1px; background:currentColor; opacity:.55; min-width:10px}

.logo-buyuk .logo-im{height:70px}
.logo-buyuk .logo-ad{font-size:34px}
.logo-buyuk .logo-alt{font-size:12px; margin-top:7px}

@media (max-width:420px){
  .logo-im{height:32px}
  .logo-ad{font-size:18px; letter-spacing:.2em; text-indent:.2em}
  .logo-alt{font-size:7.5px}
}
.menu{margin-left:auto}          /* ⚠️ mobilde .menu fixed olunca bu akıştan çıkar, aşağıda telafi var */
.menu ul{display:flex; gap:34px; list-style:none; margin:0; padding:0}
.menu a{
  position:relative; display:block; padding:22px 0;
  font-size:11px; font-weight:600; letter-spacing:.18em; text-transform:uppercase;
  text-decoration:none; color:var(--murekkep);
}
.menu a::before{
  content:""; position:absolute; top:0; left:0; right:0; height:3px;
  background:var(--cizgi); transform:scaleX(0); transition:transform .25s;
}
.menu a:hover::before,.menu a.etkin::before{transform:scaleX(1)}

.hamburger{
  display:none; margin-left:auto; width:42px; height:42px; padding:9px;
  background:none; border:0; cursor:pointer; flex-direction:column; justify-content:space-between;
}
.hamburger span{display:block; height:2px; background:var(--murekkep); transition:transform .3s,opacity .2s}
.hamburger[aria-expanded="true"] span:nth-child(1){transform:translateY(10px) rotate(45deg)}
.hamburger[aria-expanded="true"] span:nth-child(2){opacity:0}
.hamburger[aria-expanded="true"] span:nth-child(3){transform:translateY(-10px) rotate(-45deg)}

@media (max-width:880px){
  .hamburger{display:flex}
  .menu{
    position:fixed; inset:var(--ust-h) 0 auto 0; margin-left:0;
    background:var(--krem); border-bottom:3px solid var(--cizgi);
    transform:translateY(-120%); transition:transform .35s cubic-bezier(.4,0,.2,1);
    max-height:calc(100dvh - var(--ust-h)); overflow-y:auto;
  }
  .menu.acik{transform:translateY(0)}
  .menu ul{flex-direction:column; gap:0; padding:8px 24px 20px}
  .menu a{padding:15px 0; font-size:13px; border-bottom:1px solid var(--hat)}
  .menu a::before{display:none}
  .menu a.etkin{font-weight:800}
}

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
.mono-satir{display:flex; position:relative}  /* ::after ışığı buna göre konumlanır */
.mono-harf{
  display:block; overflow:hidden;              /* maske: harf buradan yükselir */
  line-height:.86; padding:0 .012em;
}
.mono-harf i{
  display:block; font-style:normal;
  font-size:clamp(88px,20vw,220px); font-weight:800; letter-spacing:-.05em;
  color:var(--krem); text-shadow:0 2px 40px rgba(0,0,0,.14);
  transform:translateY(108%); filter:blur(9px);
  animation:monoYuksel .95s cubic-bezier(.16,.84,.28,1) both;
  animation-delay:var(--g,0ms);
}
@keyframes monoYuksel{
  from{transform:translateY(108%); filter:blur(9px); opacity:0}
  60%{filter:blur(0); opacity:1}
  to{transform:translateY(0); filter:blur(0); opacity:.94}
}
/* harflerin üzerinden bir kez geçen ışık */
.mono-satir::after{
  content:""; position:absolute; inset:0;
  background:linear-gradient(105deg,transparent 38%,rgba(255,255,255,.55) 50%,transparent 62%);
  mix-blend-mode:overlay; transform:translateX(-130%);
  animation:monoParla 1.3s ease-out .85s both;
}
@keyframes monoParla{to{transform:translateX(130%)}}
.mono-cizgi{
  display:block; width:clamp(74px,13vw,150px); height:3px; background:var(--krem); margin-top:.22em;
  transform:scaleX(0); transform-origin:center;
  animation:monoCizgi .8s cubic-bezier(.16,.84,.28,1) .62s both; opacity:.9;
}
@keyframes monoCizgi{to{transform:scaleX(1)}}

@media (prefers-reduced-motion:reduce){
  .hero-gorsel img,.mono-satir::after{animation:none}
  .mono-harf i{animation:none; transform:none; filter:none; opacity:.94}
  .mono-cizgi{animation:none; transform:scaleX(1)}
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
.dg{
  display:inline-block; padding:13px 26px; text-decoration:none;
  font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase;
  border:2px solid var(--cizgi); background:transparent; color:var(--murekkep);
  transition:background .22s,color .22s,transform .22s;
}
.dg:hover{background:var(--cizgi); color:var(--krem); transform:translateY(-2px)}
.dg-koyu{background:var(--cizgi); color:var(--krem)}
.dg-koyu:hover{background:transparent; color:var(--murekkep)}
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
.cta .dg{border-color:var(--krem); color:var(--krem)}
.cta .dg:hover{background:var(--krem); color:var(--bar)}
.cta .dg-koyu{background:var(--krem); color:var(--bar)}
.cta .dg-koyu:hover{background:transparent; color:var(--krem)}

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
.alt-sos{margin:18px 0 0}
.sos{display:inline-block; width:26px; color:var(--murekkep)}
.sos svg{width:100%; fill:currentColor}
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
  background:rgba(242,240,235,.82); color:var(--murekkep);
  border:1px solid rgba(0,0,0,.09);
  box-shadow:0 10px 28px rgba(0,0,0,.16), inset 0 1px 0 rgba(255,255,255,.9);
  font-size:13px; font-weight:700; letter-spacing:.01em; white-space:nowrap;
  transition:transform .25s,box-shadow .25s,background .25s;
  position:relative; overflow:hidden;
  -webkit-backdrop-filter:blur(14px) saturate(160%); backdrop-filter:blur(14px) saturate(160%);
}
.dock-dg:hover{transform:translateY(-3px); box-shadow:0 16px 36px rgba(0,0,0,.22); background:var(--krem)}
.dock-ikon{
  width:30px; height:30px; flex:0 0 30px; border-radius:50%;
  display:grid; place-items:center; background:var(--renk); color:#fff;
}
.dock-ikon svg{width:17px; fill:currentColor}
.dock-wa{--renk:#25D366}
.dock-ara{--renk:var(--kurum)}
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
  background:var(--krem); border:1px solid var(--hat); border-radius:14px;
  box-shadow:0 22px 60px rgba(0,0,0,.2);
  padding:16px 40px 16px 18px;
  transform:translateY(24px) scale(.96); opacity:0; visibility:hidden;
  transition:transform .4s cubic-bezier(.2,.9,.3,1),opacity .4s,visibility .4s;
}
.bildirim.gorun{transform:none; opacity:1; visibility:visible}
.bildirim-bas{display:flex; align-items:center; gap:8px; font-weight:800; font-size:14px; margin:0 0 4px}
.nokta{
  width:9px; height:9px; border-radius:50%; background:var(--sage); flex:0 0 9px;
  box-shadow:0 0 0 0 rgba(143,161,151,.65); animation:canli 2s infinite;
}
@keyframes canli{70%{box-shadow:0 0 0 9px rgba(143,161,151,0)} 100%{box-shadow:0 0 0 0 rgba(143,161,151,0)}}
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
"""
