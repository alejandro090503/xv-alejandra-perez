import sys, json
from playwright.sync_api import sync_playwright
SIL="HTMLMediaElement.prototype.play=function(){this.muted=true;this.pause();return Promise.resolve();};document.querySelectorAll('audio,video').forEach(m=>{m.muted=true;m.pause();});"
shots=sys.argv[1:] or ['sintro','hero','sgifts']
with sync_playwright() as pw:
    b=pw.chromium.launch(); c=b.new_context(viewport={'width':375,'height':740}); c.add_init_script(SIL)
    p=c.new_page(); errs=[]
    p.on('pageerror',lambda e:errs.append(str(e))); p.on('console',lambda m:m.type=='error' and errs.append(m.text))
    p.goto(''+(__import__('os').environ.get('URL','http://localhost:5731'))+'/?noauto'); p.evaluate(SIL); p.wait_for_timeout(1500)
    p.mouse.click(187,370); p.wait_for_timeout(10000); p.evaluate(SIL)
    r=p.evaluate("()=>({sw:document.documentElement.scrollWidth,iw:innerWidth,h:document.documentElement.scrollHeight,open:document.body.classList.contains('al-open'),words:document.querySelectorAll('#crText .w').length})")
    print(json.dumps(r))
    for s in shots:
        if s=='hero': p.evaluate("scrollTo(0,0)")
        elif ':' in s:
            sid,off=s.split(':'); p.evaluate(f"(()=>{{const e=document.getElementById('{sid}');scrollTo(0,e.offsetTop+{off})}})()")
        else: p.evaluate(f"(()=>{{const e=document.getElementById('{s}');scrollTo(0,e.offsetTop-20)}})()")
        p.wait_for_timeout(1800); p.evaluate(SIL)
        p.screenshot(path=f'_src/shot-{s.replace(":","_")}.png')
    print('ERR',errs[:8]); b.close()
