/* INSERTAR: antes de </body> */
/* (dentro de su propia etiqueta script, después de todos los demás scripts; usa GSAP + ScrollTrigger ya cargados) */
/* ═══ D · Luz Premium + brillo + itinerario · xv-alejandra-perez (Realeza / Bridgerton, rosa oro + foil dorado) ═══
   Orden: 1) LP_CONFIG  2) preparación del marcado (crea las capas del kit si el HTML no las trae)
          3) kit luz-premium.js COPIADO TAL CUAL  4) brillo de tarjetas, títulos e itinerario (adaptación D). */
window.LP_CONFIG = {
  flareMini: 'assets/flare-mini.webp',
  seda:    { sombra:'#4E2129', base:'#7E3F4A', luz:'#F0CFA8' },   /* rosa oro profundo */
  borde:   '#FFFDFB',                                            /* marfil: borde de TODAS las secciones claras */
  fundido: 220,
  cortina: { sombra:'#7E3F4A', base:'#B76E79', luz:'#F6DDA0' },   /* rosa oro metálico con luz de foil */
  niebla:  '246,228,224'
};

/* ── 2 · preparación: si el HTML ya trae la capa, no la duplica ── */
(function(){
  var D = document;
  var SPRITES = 'assets/caida-1.webp,assets/caida-2.webp,assets/caida-3.webp';
  function mk(tag, cls){ var e = D.createElement(tag); e.className = cls; e.setAttribute('aria-hidden', 'true'); return e; }
  function despues(ref, el){ ref.parentNode.insertBefore(el, ref.nextSibling); }

  /* portada: niebla baja (12) + caída 3D de pétalos (3) + un destello con fantasmas (1) + nombre cascada (10) y diamantes (2) */
  var hero = D.querySelector('section.hero');
  if (hero){
    var veil = hero.querySelector('.hero-veil') || hero.firstElementChild, ref = veil;
    if (!hero.querySelector('.lp-niebla')){ var n = mk('div', 'lp-niebla'); despues(ref, n); ref = n; }
    if (!hero.querySelector('.lp-caida')){ var c = mk('canvas', 'lp-caida'); c.setAttribute('data-sprites', SPRITES); despues(ref, c); }
    if (!hero.querySelector('.lp-flare')){ var f = mk('div', 'lp-flare'); f.setAttribute('data-x', '82%'); f.setAttribute('data-y', '15%'); f.setAttribute('data-s', '1'); hero.appendChild(f); }
    var nm = D.getElementById('hNm');
    if (nm && !nm.querySelector('.lp-cascada')){
      var t = nm.textContent.replace(/\s+/g, ' ').trim(), g = D.createElement('span'), s = D.createElement('span');
      g.className = 'lp-glints'; s.className = 'lp-cascada lp-claro'; s.textContent = t;
      nm.textContent = ''; g.appendChild(s); nm.appendChild(g); nm.setAttribute('aria-label', t);
    }
  }

  /* pie: niebla + caída + nombre con estela (cascada lenta, desfasada de la portada) */
  var pie = D.getElementById('smsg');
  if (pie){
    if (!pie.querySelector('.lp-caida')){ var c2 = mk('canvas', 'lp-caida'); c2.setAttribute('data-sprites', SPRITES); c2.setAttribute('data-n', innerWidth < 600 ? '10' : '14'); pie.insertBefore(c2, pie.firstChild); }
    if (!pie.querySelector('.lp-niebla')) pie.insertBefore(mk('div', 'lp-niebla'), pie.firstChild);
    var pn = pie.querySelector('[data-lp-nombre]') || pie.querySelector('.pie-name');
    if (!pn){ [].slice.call(pie.querySelectorAll('div')).some(function(d){ if (/Great Vibes/i.test(getComputedStyle(d).fontFamily) && d.children.length === 0){ pn = d; return true; } return false; }); }
    if (pn && !pn.classList.contains('lp-cascada')){ pn.classList.add('lp-cascada', 'lp-claro'); pn.style.setProperty('--lp-del', '-1.2s'); }
  }

  /* seda iluminada (14) alternada: cuenta regresiva, familia y RSVP */
  ['scd', 'sfam', 'srsvp'].forEach(function(id){
    var sec = D.getElementById(id);
    if (!sec) return;
    sec.classList.add('lp-osc');
    if (!sec.querySelector(':scope > canvas.lp-seda')) sec.insertBefore(mk('canvas', 'lp-seda'), sec.firstChild);
  });

  /* uniones: velo (15) al salir de la seda hacia Ubicaciones y Regalos; cortina (17) justo antes del RSVP */
  [['subic', 'velo'], ['sgifts', 'velo'], ['srsvp', 'seda']].forEach(function(u){
    var sec = D.getElementById(u[0]);
    if (sec && !sec.hasAttribute('data-lp-union')) sec.setAttribute('data-lp-union', u[1]);
  });
})();

/* ── 3 · kit luz-premium.js (COPIA TAL CUAL de kit-efectos-elysium/luz) ── */
/* ═══ Luz Premium Elysium · aprobados (1, 2, 3, 8, 10, 12, 14) ═══
   Copiar TAL CUAL al final del <body> (después del HTML de las secciones).
   Configuración por invitación, ANTES de este script:
     window.LP_CONFIG = {
       flareMini: 'assets/flare-mini.webp',
       seda:    { sombra:'#3B2F4A', base:'#B9A6C9', luz:'#FFF4E6' },  // 3 tonos de la paleta (oscuro, medio, brillo)
       borde:   '#F6F2EC',      // color de borde que comparten TODAS las secciones claras (la seda se funde desde aquí)
       fundido: 220,            // alto en px del fundido de la seda
       cortina: { sombra:'#7A5A33', base:'#C9A86E', luz:'#FFF4DC' },  // metálico para data-lp-union="seda"
       niebla:  '236,240,246',  // r,g,b de la niebla
       causticas: '#FFF8E4'     // color de la luz de las cáusticas
     };
   Todo se pausa fuera de pantalla y con la pestaña oculta; con prefers-reduced-motion queda en un cuadro fijo. */
(function(){
  var C=window.LP_CONFIG||{}, reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function vis(el,cb){if(!('IntersectionObserver' in window)){cb(true);return}new IntersectionObserver(function(es){es.forEach(function(e){cb(e.isIntersecting)})},{rootMargin:'120px'}).observe(el)}
  function hidden(){return document.hidden}
  function hex(h){h=h.replace('#','');if(h.length===3)h=h.split('').map(function(c){return c+c}).join('');return[parseInt(h.slice(0,2),16)/255,parseInt(h.slice(2,4),16)/255,parseInt(h.slice(4,6),16)/255]}
  function fit(c,scale,max){var r=c.getBoundingClientRect(),d=Math.min(max||2,devicePixelRatio||1)*(scale||1);c.width=Math.max(1,Math.round(r.width*d));c.height=Math.max(1,Math.round(r.height*d));return d}
  function img(s){var i=new Image();i.src=s;return i}
  var FM=img(C.flareMini||'assets/flare-mini.webp');

  /* 1 · destello + fantasmas a lo largo del eje que cruza el centro del contenedor */
  document.querySelectorAll('.lp-flare').forEach(function(host,idx){
    var box=host.parentElement, wrap=document.createElement('div');wrap.className='lp-flare-wrap';box.appendChild(wrap);host.remove();
    var del=(-idx*2.9)+'s', s=parseFloat(host.dataset.s||1);
    function build(){wrap.innerHTML='';var W=box.clientWidth,H=box.clientHeight,fx=W*parseFloat(host.dataset.x||18)/100,fy=H*parseFloat(host.dataset.y||20)/100,cx=W/2,cy=H/2;
      var f=document.createElement('div');f.className='lp-fl';f.style.cssText='left:'+fx+'px;top:'+fy+'px;--s:'+s+';--del:'+del;f.innerHTML='<b></b>';wrap.appendChild(f);
      [[.55,14,'255,236,200',.4,0],[.85,34,'170,220,255',.28,1],[1.15,10,'255,255,255',.45,0],[1.4,56,'255,190,210',.22,1],[1.7,22,'200,255,230',.3,0]].forEach(function(q){
        var g=document.createElement('i');g.className='lp-ghost'+(q[4]?' hex':'');var k=q[0]*1.67,x=fx+(cx-fx)*k,y=fy+(cy-fy)*k,z=q[1]*s;
        g.style.cssText='left:'+(x-z/2)+'px;top:'+(y-z/2)+'px;width:'+z+'px;height:'+z+'px;--o:'+q[3]+';--del:'+del+';background:radial-gradient(circle,rgba('+q[2]+',.9) 0 40%,transparent 72%)';wrap.appendChild(g)})}
    build();addEventListener('resize',build)});

  /* 2 · chispas de diamante en el filo superior de las letras, una a la vez */
  document.querySelectorAll('.lp-glints').forEach(function(gb,idx){var on=false;vis(gb,function(v){on=v});
    function glint(){ if(on&&!reduce&&!hidden()){var w=gb.clientWidth,h=gb.clientHeight,d=document.createElement('i');d.className='lp-glint';
      d.style.left=(w*.12+Math.random()*w*.76)+'px';d.style.top=(h*.22+Math.random()*h*.3)+'px';gb.appendChild(d);
      d.animate([{opacity:0,transform:'scale(.2) rotate(-25deg)'},{opacity:1,transform:'scale(1) rotate(0)'},{opacity:0,transform:'scale(.2) rotate(25deg)'}],{duration:1100,easing:'ease-in-out'}).onfinish=function(){d.remove()}}
      setTimeout(glint,700+Math.random()*900)}
    setTimeout(glint,idx*400)});

  /* 3 · caída temática: giro 3D + destello cuando la cara mira a la luz */
  document.querySelectorAll('.lp-caida').forEach(function(c){
    var x=c.getContext('2d'),d=fit(c),on=false,S=(c.dataset.sprites||'').split(',').filter(Boolean).map(img),n=parseInt(c.dataset.n||(innerWidth<600?14:20)),P=[];
    for(var i=0;i<n;i++){var z=Math.random();P.push({x:Math.random(),y:Math.random()*1.1-.1,z:z,v:.025+z*.035,s:16+z*22,r:Math.random()*6.28,sp:(Math.random()-.5)*.8,a:Math.random()*6.28,w:1.2+Math.random()*1.8,k:i,ph:Math.random()*6.28})}
    vis(c,function(v){on=v});addEventListener('resize',function(){d=fit(c)});
    (function loop(t){ if(on&&!hidden()&&S.length){var W=c.width,H=c.height;x.clearRect(0,0,W,H);
      P.forEach(function(p){ if(!reduce){p.y+=p.v/60;if(p.y>1.1){p.y=-.1;p.x=Math.random()}p.a+=p.w/60;p.r+=p.sp/60}
        var im=S[p.k%S.length];if(!im.complete||!im.naturalWidth)return;
        var X=(p.x+Math.sin(t/1800+p.ph)*.03)*W,Y=p.y*H,sz=p.s*d,ar=im.naturalHeight/im.naturalWidth,fl=Math.cos(p.a),face=Math.pow(Math.max(0,fl),14);
        x.save();x.translate(X,Y);x.rotate(p.r);x.scale(Math.max(.14,Math.abs(fl))*(fl<0?-1:1),1);
        x.globalAlpha=.5+p.z*.4;x.drawImage(im,-sz/2,-sz*ar/2,sz,sz*ar);
        if(face>.05){x.globalCompositeOperation='lighter';x.globalAlpha=face*.7;x.drawImage(im,-sz/2,-sz*ar/2,sz,sz*ar);x.globalCompositeOperation='source-over'}
        x.restore();
        if(face>.7&&FM.complete){x.globalAlpha=(face-.7)/.3;var zz=sz*1.6;x.drawImage(FM,X-zz/2+sz*.15,Y-zz/2-sz*.15,zz,zz)}});
      x.globalAlpha=1} requestAnimationFrame(loop)})(0)});

  /* WebGL: utilidades */
  function prog(gl,fs){var vs='attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
    function sh(t,s){var o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return o}
    var pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
    var b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
    var l=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,2,gl.FLOAT,false,0,0);return pr}
  var HP='#ifdef GL_FRAGMENT_PRECISION_HIGH\nprecision highp float;\n#else\nprecision mediump float;\n#endif\n';

  /* 8 · cáusticas en GPU (una sola canvas por escena) */
  document.querySelectorAll('.lp-causticas').forEach(function(c){
    var gl=c.getContext('webgl',{premultipliedAlpha:true,alpha:true,antialias:false});if(!gl){c.remove();return}
    var pr=prog(gl,HP+'uniform vec2 res;uniform float t;uniform vec3 col;void main(){vec2 uv=gl_FragCoord.xy/res;float time=t*.35+23.;vec2 p=uv*6.28318*vec2(1.4*res.x/res.y/1.5,1.)-250.;vec2 i=p;float c=1.;float inten=.005;'+
      'for(int n=0;n<5;n++){float tt=time*(1.-(3.5/float(n+1)));i=p+vec2(cos(tt-i.x)+sin(tt+i.y),sin(tt-i.y)+cos(tt+i.x));c+=1./length(vec2(p.x/(sin(i.x+tt)/inten),p.y/(cos(i.y+tt)/inten)));}'+
      'c/=5.;c=1.17-pow(c,1.4);float v=clamp(pow(abs(c),8.),0.,1.);gl_FragColor=vec4(col*v,v*.92);}');
    var uR=gl.getUniformLocation(pr,'res'),uT=gl.getUniformLocation(pr,'t'),uC=gl.getUniformLocation(pr,'col'),on=false,col=hex(C.causticas||'#FFF8E4');
    function size(){fit(c,.75,1.5);gl.viewport(0,0,c.width,c.height)}size();addEventListener('resize',size);vis(c,function(v){on=v});
    (function loop(t){ if((on&&!hidden())||t===0){gl.uniform2f(uR,c.width,c.height);gl.uniform1f(uT,reduce?0:t/1000);gl.uniform3f(uC,col[0],col[1],col[2]);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)}
      requestAnimationFrame(loop)})(0)});

  /* 10 · cascada: separa el texto en letras */
  document.querySelectorAll('.lp-cascada').forEach(function(el){var t=el.textContent;el.textContent='';el.setAttribute('aria-label',t);
    t.split('').forEach(function(ch,i){var s=document.createElement('span');s.setAttribute('aria-hidden','true');s.style.setProperty('--i',i);if(ch===' '){s.className='sp';s.innerHTML='&nbsp;'}else s.textContent=ch;el.appendChild(s)})});

  /* 12 · niebla: textura generada UNA vez y compartida por todas las capas */
  var nieblas=document.querySelectorAll('.lp-niebla');
  if(nieblas.length){var w=512,h=160,cv=document.createElement('canvas');cv.width=w;cv.height=h;var g=cv.getContext('2d'),tono=C.niebla||'236,240,246';
    function blob(x,y,r,a){var gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,'rgba('+tono+','+a+')');gr.addColorStop(1,'rgba('+tono+',0)');g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,6.29);g.fill()}
    /* blobs dentro del alto de la textura: ninguna orilla queda cortada en seco */
    for(var i=0;i<150;i++){var X=Math.random()*w,Y=h*.32+Math.random()*h*.36,R=16+Math.random()*(Math.min(Y,h-Y)-6),A=.05+Math.random()*.12;blob(X,Y,R,A);blob(X-w,Y,R,A);blob(X+w,Y,R,A)}
    var url='url('+cv.toDataURL()+')';nieblas.forEach(function(n){for(var k=0;k<3;k++){var l=document.createElement('i');l.style.backgroundImage=url;n.appendChild(l)}})}

  /* 15 · velo de luz y 17 · cortina de seda en la unión: data-lp-union="velo" | "seda" en la sección de ABAJO */
  var velos=[];
  document.querySelectorAll('[data-lp-union]').forEach(function(sec){
    var tipo=sec.getAttribute('data-lp-union'),u=document.createElement('div');u.className='lp-union lp-union--'+tipo;u.setAttribute('aria-hidden','true');
    if(getComputedStyle(sec).position==='static')sec.style.position='relative';
    if(tipo==='seda'){var cs=C.cortina||{},cv=document.createElement('canvas');cv.className='lp-seda';
      if(cs.sombra)cv.dataset.sombra=cs.sombra;if(cs.base)cv.dataset.base=cs.base;if(cs.luz)cv.dataset.luz=cs.luz;u.appendChild(cv)}
    else velos.push(u);
    sec.insertBefore(u,sec.firstChild)});
  if(velos.length){var vt=0;function velo(){vt=0;var mid=innerHeight/2;velos.forEach(function(v){var r=v.getBoundingClientRect(),c=r.top+r.height/2,d=Math.abs(c-mid)/(innerHeight*.5);v.style.opacity=reduce?.5:Math.max(0,1-d*1.4).toFixed(3)})}
    addEventListener('scroll',function(){if(!vt)vt=requestAnimationFrame(velo)},{passive:true});addEventListener('resize',velo);velo()}

  /* 14b · fundido de la seda: la transición va COMPLETA dentro de la sección con seda, desde el color EXACTO del borde
     de la sección vecina (LP_CONFIG.borde, p. ej. el marfil que comparten todas las secciones claras) → transparente.
     Así la línea de unión es del mismo color de los dos lados y no queda franja gris ni corte.
     Por sección: data-lp-borde-top / data-lp-borde-bot = otro color o "none" (sin fundido de ese lado). */
  /* el color viaja del borde hacia el tono medio de la seda mientras se vuelve transparente: no pasa por gris */
  function smooth(col,dir,tint){var c=col.split(',').map(Number),b=(tint||col).split(',').map(Number),st=[];
    for(var i=0;i<=8;i++){var t=i/8,a=1-t*t*(3-2*t),k=t*.7,m=c.map(function(v,j){return Math.round(v+(b[j]-v)*k)}).join(',');st.push('rgba('+m+','+a.toFixed(3)+') '+(t*100).toFixed(1)+'%')}
    return 'linear-gradient('+dir+','+st.join(',')+')'}
  function rgb(c){if(!c)return null;if(c.indexOf('rgb')===0)return c.replace(/rgba?\(|\)/g,'').split(',').slice(0,3).map(function(x){return x.trim()}).join(',');var h=hex(c);return h.map(function(v){return Math.round(v*255)}).join(',')}
  document.querySelectorAll('.lp-seda').forEach(function(cv){var sec=cv.parentElement;if(!sec||sec.classList.contains('lp-union'))return;
    /* en secciones cortas el fundido no pasa del 30% del alto, para que la seda se siga viendo */
    var fades=[];function alto(){var h=Math.round(Math.min(C.fundido||220,sec.offsetHeight*.3))+'px';fades.forEach(function(f){f.style.height=h})}
    addEventListener('resize',alto);setTimeout(alto,0);addEventListener('load',alto);
    var H=(C.fundido||220)+'px';[['top','to bottom'],['bot','to top']].forEach(function(s){
      var v=sec.getAttribute('data-lp-borde-'+s[0]);if(v==='none')return;var col=rgb(v||C.borde);if(!col)return;
      var tint=rgb(cv.dataset.base||(C.seda||{}).base);
      var f=document.createElement('div');f.className='lp-sfade lp-sfade--'+s[0];f.setAttribute('aria-hidden','true');f.style.height=H;f.style.backgroundImage=smooth(col,s[1],tint);sec.insertBefore(f,cv.nextSibling);fades.push(f)});alto()});

  /* 14 · seda iluminada: UN contexto WebGL compartido que dibuja cada sección visible y la copia a su canvas 2D */
  var sedas=[].slice.call(document.querySelectorAll('.lp-seda'));
  if(sedas.length){var G=document.createElement('canvas'),gl=G.getContext('webgl',{preserveDrawingBuffer:true,antialias:false});
    if(!gl){sedas.forEach(function(s){s.remove()})}else{
      var pr=prog(gl,HP+'uniform vec2 res;uniform float t;uniform float seed;uniform vec3 cS,cB,cL;'+
        'float h(vec2 p){return sin(p.x*3.1+p.y*1.3+t*.6)*.55+sin(p.x*1.7-p.y*2.2-t*.45)*.35+sin(p.x*5.3+p.y*.7+t*.8)*.12;}'+
        'void main(){vec2 uv=gl_FragCoord.xy/res;vec2 p=vec2(uv.x*2.,uv.y*1.4*(res.y/res.x)*1.4)+seed;float e=.01;'+
        'float hx=(h(p+vec2(e,0.))-h(p-vec2(e,0.)))/(2.*e),hy=(h(p+vec2(0.,e))-h(p-vec2(0.,e)))/(2.*e);'+
        'vec3 n=normalize(vec3(-hx*.35,-hy*.35,1.));vec3 l=normalize(vec3(cos(t*.25)*.7,.5,.6));float dif=max(0.,dot(n,l));'+
        'vec3 hv=normalize(l+vec3(0.,0.,1.));float spec=pow(max(0.,dot(n,hv)),40.);'+
        'vec3 col=mix(cS,cB,.25+dif*.75)+cL*spec*.32+cL*pow(dif,8.)*.06;gl_FragColor=vec4(min(col,vec3(1.)),1.);}');
      var u={r:gl.getUniformLocation(pr,'res'),t:gl.getUniformLocation(pr,'t'),s:gl.getUniformLocation(pr,'seed'),S:gl.getUniformLocation(pr,'cS'),B:gl.getUniformLocation(pr,'cB'),L:gl.getUniformLocation(pr,'cL')};
      var items=sedas.map(function(cv,i){var pal=Object.assign({sombra:'#4A3B2E',base:'#C9A97E',luz:'#FFF4E0'},C.seda||{},{sombra:cv.dataset.sombra||(C.seda||{}).sombra,base:cv.dataset.base||(C.seda||{}).base,luz:cv.dataset.luz||(C.seda||{}).luz});
        Object.keys(pal).forEach(function(k){if(!pal[k])delete pal[k]});pal=Object.assign({sombra:'#4A3B2E',base:'#C9A97E',luz:'#FFF4E0'},pal);
        var it={cv:cv,x:cv.getContext('2d'),on:false,seed:i*3.7,S:hex(pal.sombra),B:hex(pal.base),L:hex(pal.luz),first:true};
        function sz(){var r=cv.getBoundingClientRect();cv.width=Math.max(2,Math.round(r.width*.5));cv.height=Math.max(2,Math.round(r.height*.5))}sz();addEventListener('resize',function(){sz();it.first=true});
        vis(cv,function(v){it.on=v});return it});
      var fr=0;
      (function loop(t){ if(!hidden()&&((fr++&1)===0)){items.forEach(function(it){ if(!(it.on||it.first))return; if(reduce&&!it.first)return; it.first=false;
          var w=it.cv.width,h=it.cv.height;if(G.width!==w||G.height!==h){G.width=w;G.height=h}gl.viewport(0,0,w,h);
          gl.uniform2f(u.r,w,h);gl.uniform1f(u.t,reduce?0:t/1000);gl.uniform1f(u.s,it.seed);gl.uniform3fv(u.S,it.S);gl.uniform3fv(u.B,it.B);gl.uniform3fv(u.L,it.L);
          gl.drawArrays(gl.TRIANGLE_STRIP,0,4);it.x.drawImage(G,0,0)})}
        requestAnimationFrame(loop)})(0)}}
})();

/* ── 4 · D-brillo (tarjetas y títulos) + D-itinerario · adaptación de kit-efectos-elysium/brillo.js e itinerario.js ── */
(function(){
  var D = document, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, nf = 0;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);

  /* pausa de las animaciones CSS fuera de pantalla */
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function(es){
    es.forEach(function(e){ e.target.classList.toggle('lp-pausa', !e.isIntersecting); });
  }, { rootMargin: '150px' }) : null;
  function vigila(el){ if (io) io.observe(el); }

  /* destello con proporción áurea: nunca florecen dos juntos */
  function flare(padre, x, y, s, mini){
    var f = D.createElement('i'), b = D.createElement('b');
    f.className = 'lpb-fl' + (mini ? ' is-mini' : '');
    f.setAttribute('aria-hidden', 'true');
    f.style.setProperty('--x', x); f.style.setProperty('--y', y); f.style.setProperty('--s', s || 1);
    var dur = mini ? 5.5 + (nf % 3) * .9 : 8 + (nf % 3);
    f.style.setProperty('--dur', dur + 's');
    f.style.setProperty('--del', (-((nf * .618034) % 1) * dur).toFixed(2) + 's');
    f.appendChild(b); padre.appendChild(f); nf++;
  }
  function capa(padre, cl, conHijo, del){
    var e = D.createElement('i');
    e.className = cl; e.setAttribute('aria-hidden', 'true');
    if (conHijo){ var h = D.createElement('i'); if (del) h.style.setProperty('--del', del); e.appendChild(h); }
    padre.appendChild(e); return e;
  }

  /* ── Tarjetas: ubicación, RSVP, regalos y hotel (B: pon data-lp-filo en la tarjeta de hotel si su clase no está aquí) ── */
  var SEL = '.loc1-card,.rsvp-card,.ca-card,[data-lp-filo],#shotel .hotel-card,#shotel .htl-card,#shotel .hcard';
  D.querySelectorAll(SEL).forEach(function(c, k){
    if (c.classList.contains('lpb-card')) return;
    c.classList.add('lpb-card');
    if (getComputedStyle(c).position === 'static') c.style.position = 'relative';
    var r = parseFloat(getComputedStyle(c).borderTopLeftRadius) || 0;
    c.style.setProperty('--r', Math.max(r, 2) + 'px');
    capa(c, 'lpb-halo');
    capa(c, 'lpb-sheen', true, (-(k * 3.1)).toFixed(1) + 's');
    capa(c, 'lpb-line');
    capa(c, 'lpb-rim');
    ['t', 'r', 'b', 'l'].forEach(function(lado){ capa(c, 'lpb-run ' + lado, true, (-(k * 2.7)).toFixed(1) + 's'); });
    var chica = c.offsetWidth < 260;
    flare(c, '7%', '0', chica ? .8 : 1);          /* grande arriba a la izquierda (150–220 px) */
    flare(c, '90%', '100%', chica ? .5 : .62);     /* mediano en la esquina opuesta */
    vigila(c);
  });

  /* ── Títulos: foil / enciende / vertical, repartidos sin repetir dos seguidos ── */
  var TIPOS = ['foil', 'enciende', 'vertical'], titulos = [];
  [].slice.call(D.querySelectorAll('.sec-title')).filter(function(h){ return !h.closest('#sintro') && !h.classList.contains('lpt'); })
    .forEach(function(h, i){
      var tipo = TIPOS[i % 3], txt = h.textContent.replace(/\s+/g, ' ').trim();
      h.classList.add('lpt', 'lpt--' + tipo);
      h.setAttribute('aria-label', txt);
      h.textContent = '';
      var inn = D.createElement('span'), base = D.createElement('span'), win = D.createElement('span'), hi = D.createElement('span');
      inn.className = 'lpt-in'; base.className = 'lpt-base'; win.className = 'lpt-win'; hi.className = 'lpt-hi';
      inn.setAttribute('aria-hidden', 'true'); win.setAttribute('aria-hidden', 'true');
      base.textContent = txt; hi.textContent = txt;
      win.appendChild(hi); inn.appendChild(base); inn.appendChild(win); h.appendChild(inn);
      flare(inn, '6%', '34%', .42);                      /* ~80 px sobre la primera letra */
      if (tipo === 'foil') flare(inn, '96%', '30%', 1, true);  /* mini al final */
      vigila(h);
      titulos.push({ h: h, tipo: tipo, base: base, win: win, hi: hi, i: i, tl: null });
    });

  function mide(t){
    var bx = t.base.offsetLeft, by = t.base.offsetTop, bw = t.base.offsetWidth, bh = t.base.offsetHeight;
    var W = t.win.style, H = t.hi.style;
    H.width = bw + 'px'; H.height = bh + 'px';
    if (t.tipo === 'foil'){ W.left = bx + 'px'; W.top = by + 'px'; W.width = (bw * .42) + 'px'; W.height = bh + 'px'; }
    else if (t.tipo === 'vertical'){ W.left = bx + 'px'; W.top = by + 'px'; W.width = bw + 'px'; W.height = (bh * .45) + 'px'; }
    else { W.left = bx + 'px'; W.top = by + 'px'; W.width = bw + 'px'; W.height = bh + 'px'; }
  }
  function anima(t){
    if (!hasGsap || reduce) return;
    var d0 = -(((t.i * .618034) % 1) * 3);
    var tl = gsap.timeline({ repeat: -1, paused: true, delay: 0 });
    if (t.tipo === 'foil'){
      /* banda de foil horizontal; ventana y texto se mueven en sentidos opuestos: el texto no se desplaza */
      tl.fromTo(t.win, { xPercent: -100 }, { xPercent: 240, duration: 2.6, ease: 'power1.inOut' }, 0)
        .fromTo(t.hi, { xPercent: 42 }, { xPercent: -100.8, duration: 2.6, ease: 'power1.inOut' }, 0)
        .to({}, { duration: 4.4 });
    } else if (t.tipo === 'vertical'){
      tl.fromTo(t.win, { yPercent: -100 }, { yPercent: 222, duration: 2.2, ease: 'power1.inOut' }, 0)
        .fromTo(t.hi, { yPercent: 45 }, { yPercent: -99.9, duration: 2.2, ease: 'power1.inOut' }, 0)
        .to({}, { duration: 5.3 });
    } else {
      /* enciende: la copia de foil prende y se apaga, como lámpara */
      tl.to(t.win, { opacity: 1, duration: 1.1, ease: 'power2.out' })
        .to(t.win, { opacity: .25, duration: 1.6, ease: 'power1.inOut' }, '+=.6')
        .to(t.win, { opacity: 0, duration: 1.4, ease: 'power1.in' }, '+=2.2')
        .to({}, { duration: 1.6 });
    }
    tl.progress(((d0 % tl.duration()) + tl.duration()) % tl.duration() / tl.duration());
    t.tl = tl;
    ScrollTrigger.create({ trigger: t.h, start: 'top bottom', end: 'bottom top',
      onToggle: function(s){ if (s.isActive){ if (t.tipo === 'enciende') tl.restart(); else tl.play(); } else tl.pause(); } });
  }
  function mideTodo(){ titulos.forEach(mide); }
  mideTodo(); titulos.forEach(anima);
  var rz = 0; addEventListener('resize', function(){ clearTimeout(rz); rz = setTimeout(mideTodo, 120); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(function(){ mideTodo(); if (hasGsap) ScrollTrigger.refresh(); });
  addEventListener('load', mideTodo);

  /* ── Itinerario con luz: horas en Bodoni Moda y estela guiada por el scroll ── */
  var itl = D.getElementById('itl');
  if (!itl || itl.dataset.luz) return;
  itl.dataset.luz = '1';
  itl.classList.add('lpi');
  if (!D.querySelector('link[href*="Bodoni+Moda"]')){
    var lk = D.createElement('link'); lk.rel = 'stylesheet';
    lk.href = 'https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;1,6..96,500&display=swap';
    D.head.appendChild(lk);
  }
  var rows = [].slice.call(itl.querySelectorAll('.itl-item'));
  itl.querySelectorAll('.itl-time').forEach(function(h){
    var t = h.textContent.replace(/\s+/g, ' ').trim(), m = t.match(/^(.*?)\s*([ap])\.?\s*m\.?$/i);
    if (!m) return;
    h.setAttribute('aria-label', t);
    h.textContent = '';
    var a = D.createElement('span'), b = D.createElement('span');
    a.className = 'lpi-n'; b.className = 'lpi-m';
    a.textContent = m[1]; b.textContent = m[2].toLowerCase() + 'm';
    h.appendChild(a); h.appendChild(b);
  });
  if (reduce || !hasGsap){ rows.forEach(function(r){ r.classList.add('lpi-lit'); }); return; }

  function el(cl){ var e = D.createElement('i'); e.className = cl; e.setAttribute('aria-hidden', 'true'); itl.appendChild(e); return e; }
  var prog = el('lpi-prog'), colas = [{ e: el('lpi-tail t1'), px: 118 }, { e: el('lpi-tail t2'), px: 74 }, { e: el('lpi-tail t3'), px: 34 }];
  var head = el('lpi-head'); head.appendChild(D.createElement('b'));
  vigila(itl);

  /* geometría: del centro del primer punto al del último (offset*, sin transformaciones del reveal) */
  var x0 = 0, y0 = 0, L = 1, hitos = [];
  function geo(){
    hitos = rows.map(function(r){
      var g = r.querySelector('.itl-gem') || r;
      return { x: r.offsetLeft + g.offsetLeft + g.offsetWidth / 2, y: r.offsetTop + g.offsetTop + g.offsetHeight / 2 };
    });
    if (!hitos.length) return;
    x0 = hitos[0].x; y0 = hitos[0].y; L = Math.max(1, hitos[hitos.length - 1].y - y0);
    prog.style.left = (x0 - .75) + 'px'; prog.style.top = y0 + 'px'; prog.style.height = L + 'px';
    colas.forEach(function(c){ var w = parseFloat(getComputedStyle(c.e).width) || 2; c.e.style.left = (x0 - w / 2) + 'px'; c.e.style.top = '0px'; c.e.style.height = c.px + 'px'; });
    head.style.left = x0 + 'px'; head.style.top = '0px';
  }
  var meta = 0, p = -1, giro = 90, raf = 0, last = 0;
  function pinta(vel){
    var d = p * L, y = y0 + d;
    prog.style.transform = 'scaleY(' + p.toFixed(4) + ')';
    colas.forEach(function(c){
      var k = Math.min(d, c.px) / c.px;
      c.e.style.transform = 'translate3d(0,' + (y - c.px).toFixed(2) + 'px,0) scaleY(' + k.toFixed(3) + ')';
      c.e.style.opacity = p > .002 ? 1 : 0;
    });
    /* el destello gira hacia donde va la luz: baja = 90°, sube = -90° */
    var objetivo = vel < -.0004 ? -90 : (vel > .0004 ? 90 : giro);
    giro += (objetivo - giro) * .14;
    var esc = .8 + Math.min(.42, Math.abs(vel) * 7);
    head.style.transform = 'translate3d(0,' + y.toFixed(2) + 'px,0) rotate(' + giro.toFixed(2) + 'deg) scale(' + esc.toFixed(3) + ')';
    head.classList.toggle('is-on', p > .003);
    rows.forEach(function(r, i){ var h = hitos[i]; r.classList.toggle('lpi-lit', !!h && p > .001 && y >= h.y - 2); });
  }
  function loop(now){
    raf = 0;
    var dt = last ? Math.min((now - last) / 1000, .05) : .016;
    last = now;
    var dv = meta - p;
    p += dv * (1 - Math.exp(-dt / .17));
    var quieto = Math.abs(meta - p) < .0005;
    if (quieto) p = meta;
    pinta(quieto ? 0 : dv);
    if (!quieto) raf = requestAnimationFrame(loop);
    else last = 0;
  }
  function kick(){ if (!raf && !D.hidden) raf = requestAnimationFrame(loop); }
  geo();
  ScrollTrigger.create({
    trigger: itl, start: 'top 78%', end: 'bottom 58%',
    onUpdate: function(s){ meta = s.progress; kick(); },
    onRefresh: function(s){ geo(); meta = s.progress; if (p < 0) p = meta; kick(); }
  });
  addEventListener('resize', function(){ geo(); kick(); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(function(){ geo(); kick(); });
  requestAnimationFrame(function(){ if (p < 0) p = 0; geo(); pinta(0); });
})();
