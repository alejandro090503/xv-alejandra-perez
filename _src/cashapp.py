# -*- coding: utf-8 -*-
"""Inserta la tarjeta CashApp en #sgifts. Si se pasa el $cashtag, genera cashapp-qr.png local y lo activa.
Uso: python -X utf8 _src/cashapp.py            (placeholder 'por confirmar')
     python -X utf8 _src/cashapp.py '$AleCash'  (QR real)"""
import sys, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "index.html"
s = P.read_text(encoding="utf-8")
tag = sys.argv[1].strip() if len(sys.argv) > 1 else ""
if tag and not tag.startswith("$"):
    tag = "$" + tag

if tag:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage  # noqa
    q = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12)
    q.add_data("https://cash.app/" + tag)
    q.make(fit=True)
    img = q.make_image(fill_color="#7e3f4a", back_color="white").convert("RGB")
    img.save(ROOT / "cashapp-qr.png")
    qr_html = f'<img class="ca-qr-img" src="cashapp-qr.png?v={tag[1:]}" alt="QR de CashApp {tag}" width="176" height="176">'
    tag_html = tag
    btns = (f'<a class="btn ca-btn" href="https://cash.app/{tag}" target="_blank" rel="noopener">Abrir CashApp</a>'
            f'<button class="btn ca-btn ca-copy" type="button" data-tag="{tag}">Copiar {tag}</button>')
else:
    qr_html = '<div class="ca-qr-pend"><span>QR de CashApp</span><em>por confirmar</em></div>'
    tag_html = '<span class="pend">$cashtag por confirmar</span>'
    btns = ''

card = f'''<!-- CASHAPP:INI -->
    <div class="ca-card rv" id="caCard">
      <div class="ca-eyebrow">Regalo en efectivo &middot; CashApp</div>
      <div class="ca-qr">{qr_html}</div>
      <div class="ca-tag">{tag_html}</div>
      <p class="ca-note">Escanea el c&oacute;digo con la c&aacute;mara de tu celular o desde la app de CashApp.</p>
      <div class="ca-btns">{btns}</div>
    </div>
    <!-- CASHAPP:FIN -->'''

if "<!-- CASHAPP:INI -->" in s:
    s = re.sub(r"<!-- CASHAPP:INI -->.*?<!-- CASHAPP:FIN -->", card, s, flags=re.S)
else:
    anchor = '    <p class="env-tap-hint">Toca el sobre</p>\n    </div>\n'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + "    " + card + "\n")
    css = r'''
/* === CASHAPP (petición de la clienta) === */
.ca-card{position:relative;max-width:340px;margin:34px auto 0;padding:28px 24px 26px;text-align:center;border-radius:22px;
  background:linear-gradient(158deg,#ffffff,#fff8f6);border:1px solid rgba(212,175,55,.45);box-shadow:0 12px 40px rgba(126,63,74,.12)}
.ca-eyebrow{font-family:'Lato',sans-serif;font-weight:700;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#7a5b1f;margin-bottom:16px}
.ca-qr{display:flex;justify-content:center;margin-bottom:14px}
.ca-qr-img{width:176px;height:176px;border-radius:14px;border:1px solid rgba(212,175,55,.5);padding:6px;background:#fff}
.ca-qr-pend{width:176px;height:176px;border-radius:14px;border:1.5px dashed rgba(183,110,121,.6);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;
  background:repeating-linear-gradient(45deg,rgba(246,227,229,.35) 0 8px,rgba(255,255,255,.6) 8px 16px)}
.ca-qr-pend span{font-family:'Lato',sans-serif;font-weight:700;font-size:14px;color:#7e3f4a}
.ca-qr-pend em{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;font-size:17px;color:#9c5560}
.ca-tag{font-family:'Lato',sans-serif;font-weight:700;font-size:20px;letter-spacing:.04em;color:#7e3f4a;margin-bottom:8px}
.ca-note{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:16px;line-height:1.55;color:#4a3236;margin-bottom:14px}
.ca-btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.ca-btns:empty{display:none}
'''
    last = s.rindex('</style>', 0, s.index('</head>'))
    s = s[:last] + css + s[last:]
    js = r'''
<script>
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.ca-copy');if(!b)return;
  var t=b.getAttribute('data-tag'),o=b.textContent;
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).catch(function(){var i=document.createElement('input');i.value=t;document.body.appendChild(i);i.select();document.execCommand('copy');i.remove();})
  .finally(function(){b.textContent='¡Copiado!';setTimeout(function(){b.textContent=o},1800);});});
</script>
'''
    s = s.replace('</body>', js + '</body>', 1)
P.write_text(s, encoding="utf-8")
print("CashApp:", tag or "placeholder")
