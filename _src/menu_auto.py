# -*- coding: utf-8 -*-
"""principal.md §4 y §5: un solo botón Menú abajo al centro + recorrido automático sin botón."""
import pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = P.read_text(encoding="utf-8")
assert "id=\"alMenuBtn\"" not in s

css = r'''
/* === MENÚ (único flotante junto al vinilo) === */
#scroll-hint{display:none !important}
.al-menu-btn{position:fixed;left:50%;bottom:calc(18px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:997;height:46px;min-width:104px;padding:0 20px;
  display:flex;align-items:center;gap:10px;justify-content:center;border-radius:999px;cursor:pointer;opacity:0;pointer-events:none;transition:opacity .8s ease;
  background:rgba(255,253,251,.78);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border:1px solid rgba(212,175,55,.65);box-shadow:0 8px 24px rgba(126,63,74,.16)}
.al-menu-btn.show{opacity:1;pointer-events:auto}
.al-menu-btn i{display:flex;flex-direction:column;gap:4px}
.al-menu-btn i b{display:block;width:16px;height:1.5px;background:#7e3f4a;border-radius:2px}
.al-menu-btn i b:nth-child(2){width:11px}
.al-menu-btn span{font-family:'Lato',sans-serif;font-weight:700;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#7e3f4a}
.vinyl-btn{bottom:calc(18px + env(safe-area-inset-bottom)) !important;right:16px !important;width:56px !important;height:56px !important;transition:opacity .8s ease}
body:not(.al-open) .vinyl-btn{opacity:0;pointer-events:none}
.al-menu{position:fixed;inset:0;z-index:12000;background:#fffdfb;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .5s ease}
.al-menu.open{opacity:1;pointer-events:auto}
.al-menu-x{position:absolute;top:calc(14px + env(safe-area-inset-top));right:16px;width:46px;height:46px;border:none;background:none;font:300 34px/1 'Cormorant Garamond',serif;color:#7e3f4a;cursor:pointer}
.al-menu-rule{width:120px;height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:0 auto 18px}
.al-menu ul{list-style:none;text-align:center}
.al-menu li a{display:block;padding:9px 18px;font-family:'Cormorant Garamond',serif;font-weight:600;font-size:23px;color:#7e3f4a;text-decoration:none;letter-spacing:.5px}
.al-menu li a:active{color:#b76e79}
.wrap{padding-bottom:84px}
'''
html = '''
<!-- MENÚ -->
<button class="al-menu-btn" id="alMenuBtn" type="button" aria-label="Abrir men&uacute;"><i><b></b><b></b><b></b></i><span>Men&uacute;</span></button>
<nav class="al-menu" id="alMenu" aria-hidden="true">
  <button class="al-menu-x" id="alMenuX" type="button" aria-label="Cerrar men&uacute;">&times;</button>
  <div class="al-menu-rule"></div>
  <ul>
    <li><a href="#sintro">Cr&oacute;nica</a></li>
    <li><a href="#sportrait">La Festejada</a></li>
    <li><a href="#scd">Cuenta Regresiva</a></li>
    <li><a href="#subic">Ubicaciones</a></li>
    <li><a href="#siti">Itinerario</a></li>
    <li><a href="#sdc">C&oacute;digo de Vestimenta</a></li>
    <li><a href="#sfam">Mi Familia</a></li>
    <li><a href="#sgifts">Regalos</a></li>
    <li><a href="#salbum">&Aacute;lbum</a></li>
    <li><a href="#shotel">Hospedaje</a></li>
    <li><a href="#srsvp">Confirmar Asistencia</a></li>
  </ul>
  <div class="al-menu-rule" style="margin:18px auto 0"></div>
</nav>
<script>
(function(){
  var btn=document.getElementById('alMenuBtn'),m=document.getElementById('alMenu'),x=document.getElementById('alMenuX');
  var auto={on:false,stopped:false,v:0,acc:0,last:0,raf:0};
  function stopAuto(){auto.stopped=true;auto.on=false;cancelAnimationFrame(auto.raf);document.documentElement.style.scrollBehavior='';}
  window.__alStopAuto=stopAuto;
  function open(){stopAuto();m.classList.add('open');m.setAttribute('aria-hidden','false');}
  function close(){m.classList.remove('open');m.setAttribute('aria-hidden','true');}
  btn.addEventListener('click',open);x.addEventListener('click',close);
  m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();close();
    var t=document.querySelector(a.getAttribute('href'));if(t){var y=t.getBoundingClientRect().top+scrollY-10;window.scrollTo({top:y,behavior:'smooth'});}});});
  /* stop al primer gesto */
  ['wheel','touchstart','pointerdown','keydown'].forEach(function(ev){window.addEventListener(ev,function(e){
    if(!auto.on)return; if(e.target&&e.target.closest&&e.target.closest('#envelope-screen'))return; stopAuto();},{passive:true,capture:true});});
  var expected=-1;
  window.addEventListener('scroll',function(){if(auto.on&&expected>=0&&Math.abs(scrollY-expected)>40)stopAuto();},{passive:true});
  function slowZone(){var y=innerHeight*.5,sel=['.hero','#sintro','#siti','#sportrait'];
    for(var i=0;i<sel.length;i++){var el=document.querySelector(sel[i]);if(!el)continue;var r=el.getBoundingClientRect();if(r.top<y&&r.bottom>y)return true;}return false;}
  function step(t){
    if(!auto.on)return;
    var dt=auto.last?Math.min(64,t-auto.last):16;auto.last=t;
    if(document.hidden){auto.raf=requestAnimationFrame(step);return;}
    var target=slowZone()?24:38,max=document.documentElement.scrollHeight-innerHeight;
    if(scrollY>=max-2){target=0;}
    auto.v+=(target-auto.v)*Math.min(1,dt/1000*2.2);
    auto.acc+=auto.v*dt/1000;
    var px=Math.floor(auto.acc);
    if(px>=1){auto.acc-=px;window.scrollBy(0,px);expected=scrollY;}
    if(scrollY>=max-2&&auto.v<1){stopAuto();return;}
    auto.raf=requestAnimationFrame(step);
  }
  function startAuto(){
    var q=new URLSearchParams(location.search);
    if(auto.stopped||q.has('noauto')||location.hash||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))return;
    document.documentElement.style.scrollBehavior='auto';auto.on=true;auto.last=0;expected=scrollY;auto.raf=requestAnimationFrame(step);
  }
  window.__alOnOpen=function(){
    document.body.classList.add('al-open');btn.classList.add('show');
    setTimeout(startAuto,2500);
  };
  /* abrir lightbox, sobre de regalos, mapa o RSVP detiene el recorrido */
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.env-interactive,#srsvp,.hcar,.al-map,a'))stopAuto();},true);
  var lp=window.launchPage;
  if(typeof lp==='function'){window.launchPage=function(){lp.apply(this,arguments);window.__alOnOpen();};}
})();
</script>
'''
last = s.rindex('</style>', 0, s.index('</head>'))
s = s[:last] + css + s[last:]
s = s.replace('</body>', html + '</body>', 1)
P.write_text(s, encoding="utf-8")
print("menu+auto OK")
