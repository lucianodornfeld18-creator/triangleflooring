// Triangle Flooring — upload de fotos de projetos (singles + antes/depois)
// Fotos ficam no KV até o ingest_photos.py --remote puxar e apagar.

const CITIES = ["Bradenton", "Sarasota", "Lakewood Ranch", "Palmetto", "Parrish",
  "Venice", "St. Petersburg", "Tampa"];

const PAGE = (token) => `<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Triangle Flooring — Enviar Fotos</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#0F2A4E;color:#1B2939;padding:20px;min-height:100vh}
.wrap{max-width:520px;margin:0 auto}
h1{color:#fff;font-size:1.4rem;margin:8px 0 4px}
.sub{color:#9FC3E8;font-size:.9rem;margin-bottom:20px}
.card{background:#fff;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.card h2{font-size:1.05rem;color:#11335C;margin-bottom:4px}
.card p{font-size:.83rem;color:#5B6B7E;margin-bottom:14px}
label{display:block;font-size:.8rem;font-weight:700;color:#11335C;margin:10px 0 5px}
select{width:100%;padding:12px;border:1.5px solid #E2E8F0;border-radius:10px;font-size:1rem;background:#fff}
.drop{display:block;border:2px dashed #2E8DD9;border-radius:12px;padding:18px;text-align:center;color:#1A6FBF;font-weight:600;font-size:.95rem;cursor:pointer;background:#F0F7FE}
.drop.small{padding:14px}
.drop input{display:none}
.drop.has{border-style:solid;background:#E8F8EE;color:#0B7A43;border-color:#10B981}
.ba-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
button{width:100%;margin-top:16px;padding:15px;border:none;border-radius:12px;background:#E07A2B;color:#fff;font-size:1.05rem;font-weight:800;cursor:pointer}
button:disabled{background:#C9D4E2}
.msg{margin-top:10px;font-size:.9rem;font-weight:700;text-align:center}
.ok{color:#0B7A43}.err{color:#B91C1C}
.bar{height:8px;background:#E2E8F0;border-radius:99px;margin-top:12px;overflow:hidden;display:none}
.bar i{display:block;height:100%;width:0;background:#10B981;transition:width .3s}
</style></head><body><div class="wrap">
<h1>📸 Triangle Flooring — Enviar Fotos</h1>
<div class="sub">As fotos entram no banco de criativos e viram posts automaticamente.</div>

<div class="card">
<h2>Fotos de projetos</h2>
<p>Pode selecionar várias de uma vez.</p>
<label>Cidade do projeto</label>
<select id="city1">${["Não sei / outra", ...CITIES].map(c => `<option>${c}</option>`).join("")}</select>
<label>Fotos</label>
<label class="drop" id="d1">📷 Toque para escolher as fotos<input type="file" id="f1" accept="image/*" multiple></label>
<button id="b1">Enviar fotos</button>
<div class="bar" id="bar1"><i></i></div><div class="msg" id="m1"></div>
</div>

<div class="card">
<h2>Antes &amp; Depois</h2>
<p>Uma foto em cada campo — o sistema cria o post de antes/depois pareado, sem risco de trocar.</p>
<label>Cidade do projeto</label>
<select id="city2">${["Não sei / outra", ...CITIES].map(c => `<option>${c}</option>`).join("")}</select>
<div class="ba-grid">
<div><label>ANTES</label><label class="drop small" id="dB">🕐 Foto de antes<input type="file" id="fB" accept="image/*"></label></div>
<div><label>DEPOIS</label><label class="drop small" id="dA">✨ Foto de depois<input type="file" id="fA" accept="image/*"></label></div>
</div>
<button id="b2">Enviar par antes/depois</button>
<div class="bar" id="bar2"><i></i></div><div class="msg" id="m2"></div>
</div>
<script>
const T=${JSON.stringify(token)};
function mark(inp,drop){inp.addEventListener('change',()=>{const n=inp.files.length;
drop.classList.toggle('has',n>0);drop.firstChild.textContent=n? '✅ '+n+' foto'+(n>1?'s':'')+' selecionada'+(n>1?'s':''):drop.dataset.t;});drop.dataset.t=drop.firstChild.textContent;}
mark(f1,d1);mark(fB,dB);mark(fA,dA);
async function shrink(file){const bmp=await createImageBitmap(file);const M=1600;
const s=Math.min(1,M/Math.max(bmp.width,bmp.height));
const c=document.createElement('canvas');c.width=Math.round(bmp.width*s);c.height=Math.round(bmp.height*s);
c.getContext('2d').drawImage(bmp,0,0,c.width,c.height);
return new Promise(r=>c.toBlob(r,'image/jpeg',.85));}
async function send(btn,bar,msg,build){btn.disabled=true;msg.textContent='';bar.style.display='block';
try{await build(p=>{bar.firstChild.style.width=(p*100)+'%'});
msg.className='msg ok';msg.textContent='✅ Enviado! Pode fechar ou enviar mais.';}
catch(e){msg.className='msg err';msg.textContent='❌ Erro: '+e.message;}
btn.disabled=false;setTimeout(()=>{bar.style.display='none';bar.firstChild.style.width='0'},1500);}
b1.onclick=()=>send(b1,bar1,m1,async(prog)=>{
const fs=[...f1.files];if(!fs.length)throw new Error('escolha as fotos');
for(let i=0;i<fs.length;i++){const fd=new FormData();
fd.append('kind','single');fd.append('city',city1.value);fd.append('file',await shrink(fs[i]),'foto.jpg');
const r=await fetch('/upload?t='+T,{method:'POST',body:fd});if(!r.ok)throw new Error('upload falhou');
prog((i+1)/fs.length);}
f1.value='';d1.classList.remove('has');d1.firstChild.textContent=d1.dataset.t;});
b2.onclick=()=>send(b2,bar2,m2,async(prog)=>{
if(!fB.files[0]||!fA.files[0])throw new Error('precisa da foto de ANTES e da de DEPOIS');
const fd=new FormData();fd.append('kind','ba');fd.append('city',city2.value);
fd.append('before',await shrink(fB.files[0]),'antes.jpg');prog(.4);
fd.append('after',await shrink(fA.files[0]),'depois.jpg');
const r=await fetch('/upload?t='+T,{method:'POST',body:fd});if(!r.ok)throw new Error('upload falhou');prog(1);
fB.value='';fA.value='';[dB,dA].forEach(d=>{d.classList.remove('has');d.firstChild.textContent=d.dataset.t});});
</script></div></body></html>`;

const slug = (c) => (c && !c.startsWith("Não") ? c : "florida")
  .toLowerCase().replace(/\./g, "").replace(/\s+/g, "-");

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.searchParams.get("t") !== env.TOKEN) return new Response("forbidden", { status: 403 });

    if (req.method === "GET" && url.pathname === "/")
      return new Response(PAGE(env.TOKEN), { headers: { "content-type": "text/html;charset=utf-8" } });

    if (req.method === "POST" && url.pathname === "/upload") {
      const fd = await req.formData();
      const city = slug(fd.get("city"));
      const ts = Date.now();
      if (fd.get("kind") === "ba") {
        const id = `${ts}-${city}`;
        await env.PHOTOS.put(`ba/${id}/before.jpg`, await fd.get("before").arrayBuffer());
        await env.PHOTOS.put(`ba/${id}/after.jpg`, await fd.get("after").arrayBuffer());
        return Response.json({ ok: true, pair: id });
      }
      const f = fd.get("file");
      const key = `single/${ts}-${Math.random().toString(36).slice(2, 7)}-${city}.jpg`;
      await env.PHOTOS.put(key, await f.arrayBuffer());
      return Response.json({ ok: true, key });
    }

    if (req.method === "GET" && url.pathname === "/list") {
      const singles = (await env.PHOTOS.list({ prefix: "single/" })).keys.map(k => k.name);
      const baKeys = (await env.PHOTOS.list({ prefix: "ba/" })).keys.map(k => k.name);
      const pairs = {};
      for (const k of baKeys) {
        const [, id, which] = k.match(/^ba\/(.+)\/(before|after)\.jpg$/) || [];
        if (id) (pairs[id] = pairs[id] || {})[which] = k;
      }
      return Response.json({
        singles,
        pairs: Object.entries(pairs).filter(([, p]) => p.before && p.after)
          .map(([id, p]) => ({ id, ...p })),
      });
    }

    if (req.method === "GET" && url.pathname === "/file") {
      const v = await env.PHOTOS.get(url.searchParams.get("key"), "arrayBuffer");
      return v ? new Response(v, { headers: { "content-type": "image/jpeg" } })
               : new Response("not found", { status: 404 });
    }

    if (req.method === "POST" && url.pathname === "/delete") {
      const { keys } = await req.json();
      for (const k of keys) await env.PHOTOS.delete(k);
      return Response.json({ ok: true, deleted: keys.length });
    }

    return new Response("not found", { status: 404 });
  },
};
