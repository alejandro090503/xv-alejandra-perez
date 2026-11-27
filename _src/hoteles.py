# -*- coding: utf-8 -*-
"""Reemplaza #shotel con los hoteles de _src/hoteles.json (tarjetas con carrusel + mapa horizontal sin rutas)."""
import json, pathlib, re, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "index.html"
s = P.read_text(encoding="utf-8")
d = json.loads((ROOT / "_src/hoteles.json").read_text(encoding="utf-8"))
H = d["hoteles"]
e = lambda t: html.escape(str(t or ""), quote=True)

cards = []
for i, h in enumerate(H):
    imgs = "".join(f'<img src="{e(f)}" class="{"on" if j == 0 else ""}" alt="{e(h["nombre"])}" loading="lazy">' for j, f in enumerate(h.get("fotos", [])))
    dist = ""
    if h.get("mi") is not None:
        dist = f'<div class="ht-dist">{e(h["mi"])} mi &middot; {e(h["min"])} min en auto al sal&oacute;n</div>'
    cards.append(f'''
      <div class="ht-card rv">
        <div class="ht-lev">
          <div class="hcar">{imgs}<div class="hcar-dots"></div></div>
          <div class="ht-body">
            <div class="ht-type">{e(h.get("tipo") or "Hotel")}</div>
            <div class="ht-name">{e(h["nombre"])}</div>
            <div class="ht-addr">{e(h.get("direccion"))}</div>
            {dist}
            <div class="ht-btns">
              <a class="btn" href="{e(h.get("reservar"))}" target="_blank" rel="noopener">Reservar</a>
              <a class="btn" href="{e(h.get("ubicacion"))}" target="_blank" rel="noopener">Ver ubicaci&oacute;n</a>
            </div>
          </div>
        </div>
      </div>''')

sec = f'''<section class="rv" id="shotel">
    <div class="eyebrow eyebrow-gold rv">Para tu Estad&iacute;a</div>
    <h2 class="sec-title rv">Hospedaje</h2>
    <p class="ht-intro rv">Si vienes de fuera, te sugerimos estos hoteles cerca del sal&oacute;n en Mission y McAllen, Texas.</p>
    <div class="al-map rv" id="alMap" aria-label="Mapa de hoteles y sal&oacute;n"></div>
    <div class="ht-list">{"".join(cards)}
    </div>
  </section>'''

a = s.index('<section class="rv" id="shotel">')
b = s.index('</section>', a) + len('</section>')
s = s[:a] + sec + s[b:]

css = r'''
/* === HOSPEDAJE (3 hoteles reales) === */
.ht-intro{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:17px;line-height:1.6;color:#4a3236;text-align:center;max-width:330px;margin:-10px auto 20px}
.al-map{height:200px;max-width:360px;margin:0 auto 26px;border-radius:18px;overflow:hidden;border:1px solid rgba(212,175,55,.45);box-shadow:0 10px 30px rgba(126,63,74,.12);z-index:0}
.ht-list{display:flex;flex-direction:column;gap:26px;max-width:360px;margin:0 auto}
.ht-lev{background:linear-gradient(158deg,#fff,#fff8f6);border-radius:22px;border:1px solid rgba(212,175,55,.38);box-shadow:0 12px 40px rgba(126,63,74,.12);overflow:hidden}
.ht-card .hcar{position:relative;width:100%;height:210px;overflow:hidden;background:#f3e9e6}
.ht-card .hcar img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1.1s ease}
.ht-card .hcar img.on{opacity:1}
.ht-card .hcar-dots{position:absolute;bottom:10px;left:0;right:0;display:flex;justify-content:center;gap:7px;z-index:2}
.ht-card .hcar-dots i{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.6)}
.ht-card .hcar-dots i.on{background:#f0d58a;transform:scale(1.3)}
.ht-body{padding:16px 22px 24px;text-align:center}
.ht-type{font-family:'Lato',sans-serif;font-weight:700;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:#7a5b1f;margin-bottom:6px}
.ht-name{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:25px;line-height:1.2;color:#7e3f4a;margin-bottom:6px}
.ht-addr{font-family:'Lato',sans-serif;font-weight:700;font-size:15px;line-height:1.5;color:#5b4146}
.ht-dist{font-family:'Lato',sans-serif;font-weight:700;font-size:14px;color:#9c5560;margin-top:6px}
.ht-btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.al-pin{width:14px;height:14px;border-radius:50%;background:#d4af37;border:2px solid #fff;box-shadow:0 0 0 2px rgba(126,63,74,.5),0 2px 8px rgba(0,0,0,.25)}
.al-pin.venue{width:18px;height:18px;background:#7e3f4a}
'''
if "/* === HOSPEDAJE (3 hoteles reales) === */" not in s:
    last = s.rindex('</style>', 0, s.index('</head>'))
    s = s[:last] + css + s[last:]
    s = s.replace('</head>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">\n</head>', 1)

pts = [{"lat": h["lat"], "lng": h["lng"], "n": h["nombre"], "v": 0} for h in H]
rc = d.get("recepcion")
if rc: pts.append({"lat": rc["lat"], "lng": rc["lng"], "n": rc.get("nombre", "Recepción"), "v": 1})
js = '''
<!-- HOSPEDAJE:JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
(function(){
  document.querySelectorAll('#shotel .hcar').forEach(function(c){
    var im=c.querySelectorAll('img'),dots=c.querySelector('.hcar-dots'),k=0;if(im.length<2)return;
    im.forEach(function(_,i){var d=document.createElement('i');if(!i)d.className='on';dots.appendChild(d);});
    var ds=dots.querySelectorAll('i');
    setInterval(function(){if(document.hidden)return;var r=c.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;
      im[k].classList.remove('on');ds[k].classList.remove('on');k=(k+1)%im.length;im[k].classList.add('on');ds[k].classList.add('on');},3800);
  });
  var P=__PTS__,el=document.getElementById('alMap');if(!el||!window.L)return;
  var m=L.map(el,{zoomControl:false,attributionControl:true,scrollWheelZoom:false,dragging:!L.Browser.mobile,tap:false});
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',{maxZoom:16,attribution:'Esri'}).addTo(m);
  var b=[];P.forEach(function(p){var mk=L.marker([p.lat,p.lng],{icon:L.divIcon({className:'',html:'<div class="al-pin'+(p.v?' venue':'')+'"></div>',iconSize:[18,18],iconAnchor:[9,9]})}).addTo(m);mk.bindTooltip(p.n);b.push([p.lat,p.lng]);});
  m.fitBounds(b,{padding:[26,26]});
})();
</script>
'''.replace("__PTS__", json.dumps(pts, ensure_ascii=False))
if "<!-- HOSPEDAJE:JS -->" in s:
    s = re.sub(r"<!-- HOSPEDAJE:JS -->.*?</script>\n</script>", "", s, flags=re.S)
s = s.replace('</body>', js + '</body>', 1)
P.write_text(s, encoding="utf-8")
print("hoteles:", [h["nombre"] for h in H])
