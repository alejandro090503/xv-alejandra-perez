# -*- coding: utf-8 -*-
"""Aplica datos de Alejandra Pérez Treviño + paleta rosa oro/dorado sobre el clon de xv-paola-magdaleno."""
import re, sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = P.read_text(encoding="utf-8")

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if count is not None and n != count:
        sys.exit(f"[x] '{old[:70]}' aparece {n} veces (esperado {count})")
    s = s.replace(old, new)

# ---------- META ----------
rep("<title>Paola Fernanda &middot; Mis XV A&ntilde;os &middot; 22 Agosto 2026</title>",
    "<title>Alejandra &middot; Mis XV A&ntilde;os &middot; 1 Junio 2027</title>")
rep('content="Invitaci&oacute;n digital a los XV A&ntilde;os de Paola Fernanda Magdaleno Estrada &middot; 22 de Agosto de 2026 &middot; Zapopan, Jalisco &middot; Baile de M&aacute;scaras"',
    'content="Invitaci&oacute;n digital a los XV A&ntilde;os de Alejandra P&eacute;rez Trevi&ntilde;o &middot; 1 de Junio de 2027 &middot; Donna, Texas &middot; Cr&oacute;nica de Sociedad"')
rep('content="XV A&ntilde;os de Paola Fernanda &middot; 22 Agosto 2026"', 'content="XV A&ntilde;os de Alejandra &middot; 1 Junio 2027"')
rep('content="Queridos y gentiles lectores&hellip; El honor de tu presencia se solicita &middot; Zapopan, Jalisco &middot; 22 de Agosto de 2026"',
    'content="Queridos y gentiles lectores&hellip; El honor de su presencia se solicita &middot; Donna, Texas &middot; 1 de Junio de 2027"')
rep("https://xv-paola-magdaleno.vercel.app", "https://xv-alejandra-perez.vercel.app", count=None)
rep('content="XV A&ntilde;os Paola Fernanda"', 'content="XV A&ntilde;os Alejandra P&eacute;rez Trevi&ntilde;o"')

# ---------- SOBRE / LOADER ----------
rep('alt="Invitaci&oacute;n XV A&ntilde;os Paola Fernanda"', 'alt="Invitaci&oacute;n XV A&ntilde;os Alejandra"')
rep("Mis XV A&ntilde;os &middot; 22 Agosto 2026</div>", "Mis XV A&ntilde;os &middot; 1 Junio 2027</div>")
rep("var name='Paola';", "var name='Alejandra';")

# ---------- HERO / FECHA ----------
rep('<h1 class="hero-name" id="hNm">Paola Fernanda</h1>', '<h1 class="hero-name" id="hNm">Alejandra</h1>')
rep('<div class="fecha-txt">22 &middot; Agosto &middot; 2026</div>', '<div class="fecha-txt">1 &middot; Junio &middot; 2027</div>')

# ---------- CRÓNICA (firma: tinta dorada que se escribe sola) ----------
old_intro = s[s.index('      <div class="intro-whistle rv"'):s.index('    </div>\n  </section>\n\n  <!-- RETRATO')]
new_intro = '''      <div class="cr-mast rv" aria-hidden="true">
        <span class="cr-mast-rule"></span>
        <span class="cr-mast-txt">Edici&oacute;n especial &middot; Donna, Texas &middot; Temporada 2027</span>
        <span class="cr-mast-rule"></span>
      </div>
      <div class="intro-whistle rv" style="font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#7a5b1f;margin-bottom:16px;">Cr&oacute;nica de Sociedad</div>
      <div class="cr-letter" id="crLetter">
        <p class="intro-text cr-text" id="crText"><span class="intro-drop cr-drop" id="crDrop">Q</span>ueridos y gentiles lectores&hellip; Esta autora se complace en anunciar el acontecimiento m&aacute;s esperado de la temporada: la se&ntilde;orita *Alejandra* *P&eacute;rez* *Trevi&ntilde;o* har&aacute; su gran presentaci&oacute;n en sociedad al celebrar sus *quince* *a&ntilde;os.* Con el coraz&oacute;n lleno de ilusi&oacute;n, el honor de su presencia se solicita para acompa&ntilde;arla en esta velada de *gala,* digna de la m&aacute;s brillante de las temporadas. Que ninguna dama ni caballero de bien ose faltar.</p>
        <div class="cr-sign" id="crSign">
          <span class="cr-sign-pre">Su m&aacute;s fiel cronista,</span>
          <span class="cr-sign-name"><span class="cr-sign-ink">Lady Whistledown</span><i class="cr-nib" aria-hidden="true"></i></span>
        </div>
      </div>
'''
s = s.replace(old_intro, new_intro)

# ---------- RETRATO ----------
rep('alt="Paola Fernanda Magdaleno Estrada"', 'alt="Alejandra P&eacute;rez Trevi&ntilde;o"')
rep('<div class="portrait-name rv">Paola Fernanda</div>', '<div class="portrait-name rv">Alejandra</div>')
rep('<div class="portrait-tag rv">XV A&ntilde;os &middot; 2026</div>', '<div class="portrait-tag rv">XV A&ntilde;os &middot; 2027</div>')
rep('alt="Paola de beb&eacute;"', 'alt="Alejandra de beb&eacute;"')
rep('alt="Paola de ni&ntilde;a"', 'alt="Alejandra de ni&ntilde;a"')
rep('alt="Paola en ballet"', 'alt="Alejandra"')
rep('alt="Paola adolescente"', 'alt="Alejandra"')
rep('<div class="pm-cap">So&ntilde;ando en puntas</div>', '<div class="pm-cap">So&ntilde;ando en grande</div>')

# ---------- UBICACIONES ----------
rep('<!-- UBICACION — solo recepción (sin ceremonia formal) -->', '<!-- UBICACIONES — misa (Donna) + recepción (Mission) -->')
rep('<div class="loc1-label">Ceremonia Religiosa</div>', '<div class="loc1-label">Misa de XV A&ntilde;os</div>')
rep('<div class="loc1-time">5:00 <span style="font-size:18px;letter-spacing:3px;">PM</span></div>',
    '<div class="loc1-time">4:00 <span style="font-size:18px;letter-spacing:3px;">PM</span></div>')
rep('margin:8px 6px 4px;">Templo de San Pedro Ap&oacute;stol</div>',
    'margin:8px 6px 4px;">St. Joseph Catholic Church</div><div class="loc1-addr">306 S Salinas Blvd<br>Donna, TX 78537</div>')
rep('https://maps.app.goo.gl/K44LaFL43CEdpdQh7', 'https://maps.app.goo.gl/MMwtWYqKjdtT5vDDA')
rep('<div class="loc1-time">7:00 <span style="font-size:18px;letter-spacing:3px;">PM</span></div>',
    '<div class="loc1-time">6:00 <span style="font-size:18px;letter-spacing:3px;">PM</span></div>')
rep('margin:8px 6px 4px;">Monet &mdash; Sal&oacute;n de Eventos</div>',
    'margin:8px 6px 4px;">Arelis Celebration Hall</div><div class="loc1-addr">1905 W Griffin Pkwy<br>Mission, TX 78572</div>')
rep('https://maps.app.goo.gl/kLcLTEQpdy7imvxc8', 'https://maps.app.goo.gl/N9c9qFmJ5mZhy5Pb9')

# ---------- ITINERARIO ----------
rep('    <!-- PENDIENTE: itinerario por confirmar con el cliente — horarios tentativos -->\n', '')
it = re.search(r'(<div class="itl" id="itl">\n)(.*?)(\n    </div>\n  </section>)', s, re.S)
items = it.group(2).split('\n')
gem = re.search(r'<div class="itl-gem">.*?</div>', items[0]).group(0)
def item(h, l):
    return f'      <div class="itl-item">{gem}<div class="itl-body"><div class="itl-time">{h}</div><div class="itl-label">{l}</div></div></div>'
new_items = '\n'.join([item('4:00 PM', 'Misa de XV A&ntilde;os'),
                       item('6:00 &ndash; 8:00 PM', 'Recepci&oacute;n y Cena'),
                       item('8:00 PM', 'Presentaci&oacute;n')])
s = s[:it.start(2)] + new_items + s[it.end(2):]
rep('.itl-item:nth-child(4).lit .itl-gem svg{animation-delay:1.95s}\n', '')

# ---------- DRESS CODE (dibujos se quedan; sin antifaz ni máscaras) ----------
rep('<div class="dc-subtitle rv">Baile de M&aacute;scaras</div>', '<div class="dc-subtitle rv">Gala de Sociedad</div>')
a = s.index('    <!-- MÁSCARA — invitación a llevar antifaz -->')
b = s.index('    <div class="dc-figures rv">')
s = s[:a] + s[b:]
rep('<span class="dc-avoid-lbl" style="color:#b3506f;">Tonos rosados reservados para la quincea&ntilde;era</span>',
    '<span class="dc-avoid-lbl" style="color:#9c5560;">Colores reservados para la quincea&ntilde;era</span>')
av = s.index('      <div class="dc-avoid-sw" style="gap:8px;">')
av_end = s.index('</div>', av) + len('</div>')
dots = ''.join(f'\n        <span class="dc-avoid-dot" style="background:{c};border:1px solid rgba(126,63,74,.30);"></span>'
               for c in ['#f9d3e0', '#f5d9ff', '#fe01ff', '#fcf0ff', '#ffccf7'])
s = s[:av] + '      <div class="dc-avoid-sw" style="gap:8px;">' + dots + '\n      </div>' + s[av_end:]
a = s.index('    <!-- COLORES SUGERIDOS -->')
b = s.index('    <div class="dc-hairline"></div>')
s = s[:a] + s[b:]

# ---------- FAMILIA ----------
rep('''          Fernando Magdaleno
          <span class="fam2-amp">&amp;</span>
          Daniela Estrada''', '''          Karla Alejandra Trevi&ntilde;o Cantu
          <span class="fam2-amp">&amp;</span>
          Juan Luis P&eacute;rez Garc&iacute;a''')
rep('''          Alondra Gonz&aacute;les
          <span class="fam2-amp">&amp;</span>
          Adolfo Hern&aacute;ndez''', '''          <span class="pend">Por confirmar</span>''')
fam = s.index('''      <div class="fam2-divider" aria-hidden="true">''', s.index('<span class="pend">Por confirmar</span>'))
fam_end = s.index('''    </div>
  </section>''', fam)
s = s[:fam] + s[fam_end:]

# ---------- REGALOS: monograma ----------
rep('fill="#6e2f47" opacity=".9">PF</text>', 'fill="#7e3f4a" opacity=".9">APT</text>')

# ---------- NOMBRES SIN SCRIPT ----------
rep('''<div style="font-family:'Great Vibes',cursive;font-size:44px;color:var(--gold);margin-top:22px;line-height:1;">Paola Fernanda</div>''',
    '''<div class="pie-name" style="font-family:'Cormorant Garamond',serif;font-weight:600;font-size:40px;letter-spacing:1px;color:#7e3f4a;margin-top:22px;line-height:1.1;">Alejandra</div>''')

# ---------- RSVP ----------
rep('<strong>21 de Agosto de 2026</strong>', '<strong>1 de Mayo de 2027</strong>')
rep('Fecha l&iacute;mite &middot; 21 Agosto 2026', 'Fecha l&iacute;mite &middot; 1 Mayo 2027')
rep('var DEADLINE  = new Date(2026, 7, 21, 23, 59, 59, 999);', 'var DEADLINE  = new Date(2027, 4, 1, 23, 59, 59, 999);')

# ---------- VINILO ----------
rep('<div class="vinyl-label-text">PF<small>2026</small></div>', '<div class="vinyl-label-text">APT<small>2027</small></div>')

# ---------- JS: countdown, calendario ----------
rep("/* COUNTDOWN — 22 agosto 2026 17:00 Zapopan (UTC-6) */", "/* COUNTDOWN — 1 junio 2027 16:00 Donna TX (CDT, UTC-5) */")
rep("new Date('2026-08-22T17:00:00-06:00')", "new Date('2027-06-01T16:00:00-05:00')")
rep("encodeURIComponent('XV Años de Paola Fernanda Magdaleno Estrada')", "encodeURIComponent('XV Años de Alejandra Pérez Treviño')")
rep("encodeURIComponent('Misa de XV: 5:00 PM · Recepción: 7:00 PM — Baile de Máscaras — Zapopan, Jalisco')",
    "encodeURIComponent('Misa de XV: 4:00 PM · St. Joseph Catholic Church, Donna TX — Recepción: 6:00 PM · Arelis Celebration Hall, Mission TX')")
rep("encodeURIComponent('Zapopan, Jalisco')", "encodeURIComponent('St. Joseph Catholic Church, 306 S Salinas Blvd, Donna, TX 78537')")
rep("dates=20260822T230000Z/20260823T060000Z", "dates=20270601T210000Z/20270602T050000Z")

# ---------- MÚSICA: canción propia en el repo ----------
rep("https://bsjoelxktbvlavfoozhk.supabase.co/storage/v1/object/public/fotos-clientes/audio/xv-paola-magdaleno/cancion.mp3", "cancion.mp3")
rep("var FALLBACK='https://boda-isaac-y-claudia.vercel.app/cancion.mp3';", "var FALLBACK='https://xv-alejandra-perez.vercel.app/cancion.mp3';")

# ---------- PALETA (rosa oro + dorado sobre marfil) ----------
pal = [
    ('#fdf6f4', '#fffdfb'), ('#fbf3f1', '#fffaf8'), ('#fbf6f3', '#fffcfa'),
    ('#b3506f', '#9c5560'), ('#6e2f47', '#7e3f4a'), ('#7a3242', '#7e3f4a'), ('#b06277', '#b76e79'), ('#d18a9c', '#d9a3aa'),
    ('#fbd3d9', '#f6e3e5'), ('#fd86b0', '#b76e79'), ('#f5bec7', '#e9c9cc'),
    ('#d0aa58', '#d4af37'), ('#e8cf92', '#ecd58a'), ('#7d5f28', '#7a5b1f'), ('#f0d59a', '#f0d58a'), ('#e3cc94', '#ead28a'),
    ('#a88860', '#a8862a'), ('#e8ddd8', '#f3e9e6'), ('#4a2736', '#4e2a31'), ('#3a1f2c', '#3e2228'),
    ('rgba(199,125,151', 'rgba(183,110,121'), ('rgba(208,170,88', 'rgba(212,175,55'), ('rgba(110,47,71', 'rgba(126,63,74'),
    ('rgba(179,80,111', 'rgba(156,85,96'), ('rgba(251,211,217', 'rgba(246,227,229'), ('rgba(245,190,199', 'rgba(233,201,204'),
    ('rgba(253,246,244', 'rgba(255,253,251'), ('rgba(251,240,243', 'rgba(255,248,246'), ('rgba(251,246,243', 'rgba(255,252,250'),
    ('rgba(246,210,218', 'rgba(240,222,224'), ('rgba(226,205,166', 'rgba(236,214,140'), ('rgba(125,95,40', 'rgba(122,91,31'),
    ('rgba(247,250,244', 'rgba(255,251,249'),
]
for o, n in pal:
    s = re.sub(re.escape(o), n, s, flags=re.I)

# ---------- CSS nuevo (crónica, nombres serif, extras) ----------
css = r'''
/* === ALEJANDRA · nombres en serif (sin script) === */
.ld-name{font-family:'Cormorant Garamond',serif !important;font-weight:600;font-size:64px !important;letter-spacing:2px}
.hero-name{font-family:'Cormorant Garamond',serif !important;font-weight:600 !important;font-size:clamp(54px,16vw,78px) !important;letter-spacing:2px !important;line-height:1.1 !important;
  background:linear-gradient(160deg,#7e3f4a 0%,#9c5560 22%,#b76e79 42%,#d4af37 58%,#b76e79 76%,#7e3f4a 100%) !important;-webkit-background-clip:text !important;background-clip:text !important}
.portrait-name{font-family:'Cormorant Garamond',serif !important;font-weight:600;font-size:38px !important;letter-spacing:2px}
.loc1-addr{font-family:'Lato',sans-serif;font-weight:700;font-size:15px;line-height:1.5;color:#5b4146;margin:2px 6px 6px}
.pend{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;color:#9c5560;opacity:.9}

/* === FIRMA · Crónica de Sociedad que se escribe sola en tinta dorada === */
.cr-mast{display:flex;align-items:center;gap:10px;justify-content:center;margin:0 auto 14px;max-width:340px}
.cr-mast-rule{flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.75),transparent)}
.cr-mast-txt{font-family:'Lato',sans-serif;font-weight:700;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#7a5b1f;white-space:nowrap}
.cr-letter{position:relative;max-width:360px;margin:0 auto}
.cr-text{font-size:19px !important;line-height:1.8 !important;color:#3b2a2d !important;text-align:center}
.cr-text .w{display:inline;opacity:.13;transition:opacity .45s ease,color .9s ease,text-shadow .9s ease}
.cr-text .w.on{opacity:1;color:#3b2a2d}
.cr-text .w.ink{color:#a8862a;text-shadow:0 0 10px rgba(236,213,138,.75)}
.cr-text .w.gold{font-weight:600;background:linear-gradient(100deg,#8a6a1c 0%,#d4af37 30%,#f6e7b0 48%,#d4af37 64%,#9c5560 100%);
  background-size:220% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none}
.cr-text .w.gold.on{animation:crFoil 3.2s ease-out 1 both}
@keyframes crFoil{from{background-position:100% 0}to{background-position:0 0}}
.cr-drop{position:relative;font-family:'Cormorant Garamond',serif !important;font-weight:600 !important;font-size:3.1em !important;line-height:.8 !important;float:left;margin:6px 8px 0 0 !important;
  background:linear-gradient(160deg,#8a6a1c 0%,#d4af37 28%,#f8ecbf 46%,#d4af37 62%,#b76e79 100%) !important;background-size:200% 200% !important;
  -webkit-background-clip:text !important;background-clip:text !important;-webkit-text-fill-color:transparent !important;opacity:.18;transition:opacity .8s ease;filter:none !important}
.cr-drop.on{opacity:1;animation:crFoil 2.6s ease-out 1 both}
.cr-drop::after{content:"";position:absolute;left:50%;top:42%;width:46px;height:46px;margin:-23px 0 0 -23px;pointer-events:none;opacity:0;
  background:radial-gradient(closest-side,rgba(255,250,228,.95),rgba(236,213,138,.55) 35%,rgba(212,175,55,0) 70%);transform:scale(.3)}
.cr-drop.on::after{animation:crFlare 1.6s ease-out .25s 1 both}
@keyframes crFlare{0%{opacity:0;transform:scale(.3) rotate(0)}35%{opacity:1;transform:scale(1.15) rotate(25deg)}100%{opacity:0;transform:scale(1.6) rotate(60deg)}}
.cr-sign{margin-top:26px;text-align:right;padding-right:6px}
.cr-sign-pre{display:block;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;font-size:16px;color:#7e3f4a;opacity:0;transition:opacity .8s ease}
.cr-sign.on .cr-sign-pre{opacity:.9}
.cr-sign-name{position:relative;display:inline-block;margin-top:4px}
.cr-sign-ink{display:inline-block;font-family:'Great Vibes',cursive;font-size:40px;line-height:1.25;padding:0 6px 4px 2px;
  background:linear-gradient(100deg,#8a6a1c,#d4af37 40%,#b76e79 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
  clip-path:inset(0 100% 0 0);transition:clip-path 2.4s cubic-bezier(.45,.05,.35,1) .35s}
.cr-sign.on .cr-sign-ink{clip-path:inset(0 0 0 0)}
.cr-nib{position:absolute;top:58%;left:0;width:7px;height:7px;border-radius:50%;opacity:0;pointer-events:none;
  background:radial-gradient(circle,#fffbe8 0%,#ecd58a 45%,rgba(212,175,55,0) 75%);box-shadow:0 0 14px 4px rgba(236,213,138,.75)}
.cr-sign.on .cr-nib{animation:crNib 2.4s cubic-bezier(.45,.05,.35,1) .35s 1 both}
@keyframes crNib{0%{opacity:0;transform:translate(0,0)}8%{opacity:1}25%{transform:translate(calc(var(--nw,240px)*.25),-6px)}50%{transform:translate(calc(var(--nw,240px)*.5),4px)}
  75%{transform:translate(calc(var(--nw,240px)*.75),-5px)}92%{opacity:1}100%{opacity:0;transform:translate(var(--nw,240px),0)}}
@media (prefers-reduced-motion:reduce){.cr-text .w,.cr-drop,.cr-sign-pre{opacity:1 !important;transition:none}.cr-sign-ink{clip-path:none;transition:none}.cr-nib,.cr-drop::after{display:none}}
'''
last = s.rindex('</style>', 0, s.index('</head>'))
s = s[:last] + css + s[last:]

js = r'''
<script>
/* === FIRMA · Crónica que se escribe sola (Text Reveal en tinta dorada) === */
(function(){
  var p=document.getElementById('crText'),drop=document.getElementById('crDrop'),sign=document.getElementById('crSign');
  if(!p)return;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nodes=[].slice.call(p.childNodes),frag=document.createDocumentFragment(),spans=[];
  nodes.forEach(function(n){
    if(n.nodeType!==3){frag.appendChild(n);return;}
    n.textContent.split(/(\s+)/).forEach(function(t){
      if(!t)return;
      if(/^\s+$/.test(t)){frag.appendChild(document.createTextNode(t));return;}
      var sp=document.createElement('span');sp.className='w';
      if(t.charAt(0)==='*'){t=t.replace(/\*/g,'');sp.className+=' gold';}
      sp.textContent=t;frag.appendChild(sp);spans.push(sp);
    });
  });
  p.textContent='';p.appendChild(frag);
  var ink=sign&&sign.querySelector('.cr-sign-ink');
  function setW(){if(ink&&sign)sign.style.setProperty('--nw',ink.offsetWidth+'px');}
  setW();window.addEventListener('resize',setW);
  if(reduce){spans.forEach(function(s){s.classList.add('on')});drop&&drop.classList.add('on');sign&&sign.classList.add('on');return;}
  var lit=0,ticking=false;
  function upd(){
    ticking=false;
    var r=p.getBoundingClientRect(),vh=innerHeight;
    var pr=(vh*0.86-r.top)/(r.height+vh*0.30);pr=Math.max(0,Math.min(1,pr));
    var n=Math.round(pr*spans.length*1.04);
    if(n>lit){
      for(var i=lit;i<n&&i<spans.length;i++){(function(sp){sp.classList.add('on');if(!/gold/.test(sp.className)){sp.classList.add('ink');setTimeout(function(){sp.classList.remove('ink')},650);}})(spans[i]);}
      lit=Math.min(n,spans.length);
    }
    if(drop&&pr>0.01)drop.classList.add('on');
    if(sign&&lit>=spans.length)sign.classList.add('on');
  }
  function onS(){if(!ticking){ticking=true;requestAnimationFrame(upd);}}
  window.addEventListener('scroll',onS,{passive:true});
  upd();
})();
</script>
'''
s = s.replace('</body>', js + '</body>', 1)
P.write_text(s, encoding="utf-8")
print("OK", len(s))
