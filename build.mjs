import { getDocument } from 'pdfjs-dist/legacy/build/pdf.mjs';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
const __dir = dirname(fileURLToPath(import.meta.url));
const ROOT = __dir;  // build.mjs runs from repo root
const PUB = join(ROOT, 'public');

const URLS = {
  tap:    'https://untp.beer/JE8zq',
  bottle: 'https://untp.beer/AXmAK',
  other:  'https://untp.beer/KpBxa'   // reserved; 'other' uses maintained data for now
};

// ---------- fetch + extract ----------
async function fetchPdf(url){
  const r = await fetch(url, { redirect:'follow', headers:{'User-Agent':'Mozilla/5.0 TapHouseMenuBot'} });
  console.log('FETCH',url,'->',r.status,r.headers.get('content-type'));
  if(!r.ok) throw new Error('fetch '+url+' -> '+r.status);
  return new Uint8Array(await r.arrayBuffer());
}
async function extractLines(data){
  const pdf = await getDocument({ data, useSystemFonts:true }).promise;
  const lines = [];
  for(let p=1; p<=pdf.numPages; p++){
    const tc = await (await pdf.getPage(p)).getTextContent();
    let last=null, cur='';
    for(const it of tc.items){
      const y = it.transform[5];
      if(last!==null && Math.abs(y-last)>3){ if(cur.trim()) lines.push(cur.trim()); cur=''; }
      cur += it.str; last = y;
    }
    if(cur.trim()) lines.push(cur.trim());
  }
  return lines;
}

const JUNK = /^\+\d|www\.|Mendelssohn|BEERS ON TAP|Beers on Tap|Optional: Beer|Card payments|Girocard|Page \d|Subscribe|---PAGE|Untappd Rating/i;
const hasMeta = s => / • /.test(s);
const hasPrice = s => /€/.test(s);
const isStart = s => /^\d+\.\s+/.test(s);

// ---------- TAP ----------
function parseTap(lines){
  const L = lines.filter(l => l && !JUNK.test(l));
  const items=[]; let i=0;
  while(i<L.length){
    if(!isStart(L[i])){ i++; continue; }
    const m = L[i].match(/^(\d+)\.\s+(.*)/); let num=+m[1], name=m[2]; i++;
    while(i<L.length && !hasMeta(L[i]) && !hasPrice(L[i]) && !isStart(L[i])){ name+=' '+L[i]; i++; }
    let meta=''; if(i<L.length && hasMeta(L[i])){ meta=L[i]; i++; }
    while(i<L.length && !hasPrice(L[i]) && !isStart(L[i])) i++;   // skip description
    let price=''; if(i<L.length && hasPrice(L[i])){ price=L[i]; i++; }
    const segs = meta.split(' • ').map(s=>s.trim()).filter(Boolean);
    const loc = segs[0]||'';
    const style = segs[1]||'';
    const abvM = meta.match(/([\d.]+)%\s*ABV/); const abv = abvM?abvM[1]+'%':'';
    const ibuM = meta.match(/(\d+)\s*IBU/); const ibu = ibuM?ibuM[1]:'';
    const prices=[]; let pm; const re=/(\d+ml[^€]*?)€\s*([\d.]+)/g;
    while((pm=re.exec(price))){
      let sz = pm[1].replace(/Draft/ig,'').replace(/\(flight only\)/ig,'(flight)').replace(/\s+/g,' ').trim();
      prices.push([sz, pm[2]]);
    }
    items.push({ num, name:name.replace(/\s+/g,' ').trim(), loc, style, abv, ibu, prices });
  }
  return items;
}

// ---------- BOTTLE ----------
const CATN = {1:'Alcohol-Free',2:'Gluten-Free',3:'Lager',4:'Pale Ale',5:'Session IPA',6:'IPA',7:'NEIPA',8:'Dark / Stout',9:'Wheat',10:'Fruity',11:'Sour',12:'Trappist / Belgian',13:'Bock',14:'Cider',15:'Other'};
function parseBottle(lines){
  const L = lines.filter(l => l && !JUNK.test(l) && !/Alcohol Free 2\.|BOTTLED BEERS|takeaway/i.test(l));
  const items=[]; let i=0;
  while(i<L.length){
    if(!isStart(L[i])){ i++; continue; }
    const m = L[i].match(/^(\d+)\.\s+(.*)/); const cat=+m[1]; let name=m[2]; i++;
    while(i<L.length && !hasMeta(L[i]) && !hasPrice(L[i]) && !isStart(L[i])){ name+=' '+L[i]; i++; }
    let meta=''; while(i<L.length && !hasPrice(L[i]) && !isStart(L[i])){ meta+=(meta?' ':'')+L[i]; i++; }
    let price=''; if(i<L.length && hasPrice(L[i])){ price=L[i]; i++; }
    const segs = meta.split(' • ').map(s=>s.trim()).filter(Boolean);
    const style = segs[0]||'';
    const abvM = meta.match(/([\d.]+)%\s*ABV/); const abv = abvM?abvM[1]+'%':'';
    const loc = segs.filter((s,idx)=>idx>0 && !/ABV|IBU|CAL/.test(s)).join(', ').replace(/\s+•/,'').trim();
    const pm = price.match(/(\d+(?:ml|cl)|[\d.]+\s*L)\s*(?:Bottle|Can|Draft)?.*?€\s*([\d.]+)/i);
    items.push({ cat:CATN[cat]||'Other', name:name.replace(/\s+/g,' ').trim(), style, abv, loc:loc.replace(/\s+/g,' ').trim(),
                 size: pm?pm[1].replace(/\s+/g,''):'', price: pm?pm[2]:'' });
  }
  // group by category, preserving first-seen order
  const groups = {};
  for(const it of items){ (groups[it.cat] ||= []).push(it); }
  return groups;
}

// ---------- ratings ----------
function norm(s){
  return s.toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g,'')
    .replace(/ß/g,'ss').replace(/[’']/g,'')
    .replace(/\([^)]*\)/g,'')
    .replace(/[^a-z0-9 ,/\-]/g,'')
    .replace(/\s+/g,' ').trim();
}
export { parseTap, parseBottle, norm };

// ============ GENERATOR (dark digital) ============
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
let _uid=0;
function bubbles(rating,d=13,gap=4,fill='#ffcc33',ring='#8a7550',rw=1.4){
  const n=5,W=n*d+(n-1)*gap,H=d; _uid++; const base=_uid;
  let p=[`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;display:inline-block">`];
  for(let i=0;i<n;i++){
    const cx=i*(d+gap)+d/2, cy=d/2, r=d/2-rw, f=Math.max(0,Math.min(1,rating-i));
    p.push(`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r.toFixed(1)}" fill="none" stroke="${ring}" stroke-width="${rw}"/>`);
    if(f>0){ const id=`bb${base}_${i}`, x0=cx-r, w=f*2*r;
      p.push(`<clipPath id="${id}"><rect x="${x0.toFixed(1)}" y="${(cy-r).toFixed(1)}" width="${w.toFixed(2)}" height="${(2*r).toFixed(1)}"/></clipPath>`);
      p.push(`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r.toFixed(1)}" fill="${fill}" clip-path="url(#${id})"/>`);
    }
  }
  p.push('</svg>'); return p.join('');
}
const kfmt = n => n>=1000 ? (n/1000).toFixed(1).replace(/\.0$/,'')+'k' : ''+n;

function tapPanel(items, rmap){
  const cards = items.map(it=>{
    const meta=[it.style, it.abv?it.abv+' ABV':'', it.ibu?it.ibu+' IBU':''].filter(Boolean).join(' · ');
    const pills = it.prices.map(([s,p])=>`<span class="pill">${esc(s)} <b>€${esc(p)}</b></span>`).join('');
    const r = rmap[norm(it.name)];
    const rate = r ? `<div class="rate">${bubbles(r[0])}<span class="rscore">${r[0].toFixed(2)}</span><span class="rcount">${kfmt(r[1])} ratings</span></div>` : '';
    return `<div class="card"><div class="cardhead"><h3><span class="tnum">${it.num}</span>${esc(it.name)}</h3></div>${rate}<div class="meta">${esc(meta)}</div><div class="origin">◍ ${esc(it.loc)}</div><div class="prices">${pills}</div></div>`;
  }).join('');
  return `<div class="tapnote"><b>🍺 Tasting flight</b> — choose any five 100&nbsp;ml pours from our twenty taps. Ratings are live from Untappd.</div>${cards}`;
}
function bottlePanel(groups){
  const cats=Object.keys(groups);
  const chips='<button class="chip active" data-cat="all">All</button>'+cats.map(c=>`<button class="chip" data-cat="c${c.replace(/[^a-z0-9]/gi,'')}">${esc(c)}</button>`).join('');
  const blocks=cats.map(c=>{
    const rows=groups[c].map(it=>`<div class="brow" data-name="${esc((it.name+' '+it.style+' '+it.loc).toLowerCase())}"><div class="binfo"><div class="bname">${esc(it.name)}</div><div class="bmeta">${esc(it.style)} · ${esc(it.abv)} · ${esc(it.loc)}</div></div><div class="bright"><span class="bsize">${esc(it.size)}</span><span class="bprice">€${esc(it.price)}</span></div></div>`).join('');
    return `<section class="catblock" data-cat="c${c.replace(/[^a-z0-9]/gi,'')}"><h2 class="cathead">${esc(c)} <span class="catcount">${groups[c].length}</span></h2>${rows}</section>`;
  }).join('');
  return `<div class="toolbar"><input class="search" id="bsearch" placeholder="Search bottles — name, style, brewery…" autocomplete="off"><div class="chips" id="bchips">${chips}</div></div><div class="tapnote" style="margin-top:4px">All bottles available for takeaway at a reduced price.</div><div id="blist">${blocks}</div><div class="empty" id="bempty">No matches — try another search.</div>`;
}
function otherPanel(o){
  const sp=items=>items.map(([n,a,p4,p2])=>`<div class="brow"><div class="binfo"><div class="bname">${esc(n)}</div>${a?`<span class="bmeta">${esc(a)}</span>`:''}</div><div class="bright"><span class="bprice">4cl €${esc(p4)}</span><span class="bsub">2cl €${esc(p2)}</span></div></div>`).join('');
  const spirit=Object.entries(o.spirits).map(([c,i])=>`<section class="catblock"><h2 class="cathead">${esc(c)}</h2>${sp(i)}</section>`).join('');
  const af=o.af_cocktails.map(([n,a,p])=>`<div class="brow"><div class="binfo"><div class="bname">${esc(n)}</div><span class="bmeta">${esc(a)} · non-alcoholic</span></div><div class="bright"><span class="bprice">€${esc(p)}</span></div></div>`).join('');
  const afblock=`<section class="catblock"><h2 class="cathead">Alcohol-Free Cocktails — ISH</h2>${af}</section>`;
  const wn=items=>items.map(([n,a,g1,g2,bo])=>{const pj=[g1?`0.1l €${g1}`:'',g2?`0.2l €${g2}`:'',bo?`Bottle €${bo}`:''].filter(Boolean).join(' · ');return `<div class="brow"><div class="binfo"><div class="bname">${esc(n)}</div>${a?`<span class="bmeta">${esc(a)}</span>`:''}</div><div class="bright"><span class="bprice2">${esc(pj)}</span></div></div>`;}).join('');
  const wine=`<section class="catblock"><h2 class="cathead">Wine</h2>${wn(o.wine)}${wn(o.wine_special)}</section><section class="catblock"><h2 class="cathead">Alcohol-Free Wine</h2>${wn(o.wine_na)}</section>`;
  const sm=items=>items.map(([n,p])=>`<div class="brow"><div class="binfo"><div class="bname">${esc(n)}</div></div><div class="bright"><span class="bprice2">${esc(p)}</span></div></div>`).join('');
  const soft=`<section class="catblock"><h2 class="cathead">Softdrinks</h2>${sm(o.soft)}</section>`;
  const coffee=`<section class="catblock"><h2 class="cathead">Coffee</h2>${sm(o.coffee)}</section>`;
  return `<div class="mixnote">${esc(o.mixers)}. <b>Spirit prices: 4cl (single) / 2cl.</b></div><h2 class="cathead spirits">Spirits</h2>${spirit}${afblock}${wine}${soft}${coffee}`;
}

const STYLE = `
:root{--bg:#17100f;--bg2:#20161a;--panel:rgba(255,255,255,.035);--wine:#8a2733;--cream:#f2e6d2;--gold:#e3ad46;--yellow:#ffcc33;--mut:#a08b78;--line:rgba(227,173,70,.16);}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--cream);-webkit-font-smoothing:antialiased}
.wrap{max-width:680px;margin:0 auto;min-height:100vh;background:radial-gradient(1200px 380px at 50% -60px, rgba(138,39,51,.55), transparent 70%),linear-gradient(180deg,#1c1310 0%, #17100f 40%, #140d0c 100%);}
header.top{padding:30px 18px 20px;text-align:center;position:relative}
header.top .logo{font-family:'Oswald';font-weight:600;letter-spacing:4px;font-size:11px;color:var(--gold);text-transform:uppercase}
header.top h1{font-family:'Anton',sans-serif;font-weight:400;font-size:40px;letter-spacing:.5px;margin:4px 0 2px;text-transform:uppercase;color:var(--cream);line-height:.98}
header.top h1 span{color:var(--gold)}
header.top .tag{font-family:'Oswald';font-weight:500;letter-spacing:2px;font-size:11.5px;color:var(--yellow);margin-top:5px;text-transform:uppercase}
header.top .sub{font-family:'Oswald';font-weight:500;letter-spacing:3px;font-size:12px;color:var(--cream);opacity:.75;margin-top:9px;text-transform:uppercase}
header.top .bar{width:58px;height:3px;background:linear-gradient(90deg,var(--gold),var(--yellow));margin:12px auto 0;border-radius:3px}
header.top .addr{font-size:11px;color:var(--mut);margin-top:10px}
nav.tabs{position:sticky;top:0;z-index:20;display:flex;background:rgba(20,13,12,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.tabs button{flex:1;border:0;background:transparent;color:var(--mut);font-family:'Oswald';font-weight:600;letter-spacing:1px;font-size:13px;padding:14px 4px;cursor:pointer;text-transform:uppercase;border-bottom:3px solid transparent}
nav.tabs button.active{color:var(--cream);border-bottom:3px solid var(--gold)}
.panel{display:none;padding:16px 14px 70px}
.panel.active{display:block}
.standalone .panel{display:block}
.tapnote,.mixnote{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:10px;padding:11px 13px;font-size:12.5px;color:var(--mut);margin-bottom:14px}
.tapnote b,.mixnote b{color:var(--cream)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:15px 16px;margin-bottom:12px}
.cardhead h3{font-family:'Oswald';font-weight:600;font-size:18px;line-height:1.18;color:var(--cream)}
.tnum{display:inline-block;min-width:22px;color:var(--gold);font-weight:700}
.rate{display:flex;align-items:center;gap:8px;margin-top:8px}
.rscore{font-family:'Oswald';font-weight:600;font-size:14px;color:var(--yellow)}
.rcount{font-size:10.5px;color:var(--mut);letter-spacing:.3px}
.meta{font-size:12.5px;font-weight:500;margin-top:8px;color:var(--gold)}
.origin{font-size:11.5px;color:var(--mut);margin-top:2px}
.prices{margin-top:12px;display:flex;flex-wrap:wrap;gap:7px}
.pill{background:rgba(227,173,70,.08);border:1px solid var(--line);border-radius:20px;padding:5px 12px;font-size:12px;color:var(--mut)}
.pill b{color:var(--yellow);font-weight:700}
.toolbar{position:sticky;top:49px;z-index:15;background:linear-gradient(180deg,#160f0e,#160f0ecc);padding:12px 0 8px;margin:-4px 0 6px}
.standalone .toolbar{top:0}
.search{width:100%;border:1px solid var(--line);border-radius:22px;padding:11px 16px;font-size:14px;font-family:inherit;background:rgba(255,255,255,.04);color:var(--cream)}
.search::placeholder{color:#8a7663}
.search:focus{outline:none;border-color:var(--gold)}
.chips{display:flex;gap:7px;overflow-x:auto;padding:11px 2px 4px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;border:1px solid var(--line);background:rgba(255,255,255,.03);color:var(--mut);border-radius:20px;padding:7px 13px;font-size:12px;font-weight:600;font-family:'Oswald';letter-spacing:.5px;cursor:pointer;white-space:nowrap}
.chip.active{background:linear-gradient(180deg,var(--gold),#c8922f);color:#1a120f;border-color:var(--gold)}
.catblock{margin-bottom:22px}
.cathead{font-family:'Oswald';font-weight:600;font-size:15px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);padding:6px 0 8px;border-bottom:1px solid var(--line);margin-bottom:4px;display:flex;align-items:center;gap:8px}
.cathead.spirits{font-size:17px;color:var(--cream)}
.catcount{background:rgba(227,173,70,.14);color:var(--gold);font-size:11px;border-radius:12px;padding:1px 8px;font-weight:500}
.brow{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:11px 4px;border-bottom:1px solid rgba(227,173,70,.1)}
.brow:last-child{border-bottom:0}
.bname{font-size:13.5px;font-weight:600;line-height:1.25;color:var(--cream)}
.bmeta{font-size:11px;color:var(--mut);margin-top:2px}
.bright{text-align:right;flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-end;gap:1px}
.bsize{font-size:10.5px;color:var(--mut)}
.bprice{font-family:'Oswald';font-weight:600;font-size:15px;color:var(--yellow)}
.bsub{font-size:11px;color:var(--mut);margin-top:1px}
.bprice2{font-size:11.5px;color:var(--yellow);font-weight:600;text-align:right;line-height:1.45}
.empty{text-align:center;color:var(--mut);padding:30px;font-size:13px;display:none}
footer{text-align:center;padding:30px 16px 54px;color:var(--mut);font-size:11px;border-top:1px solid var(--line)}
.femblem{height:56px;margin-bottom:8px;opacity:.95}
.fbrand{font-family:'Oswald';font-weight:600;font-size:19px;color:var(--cream);letter-spacing:.5px}
.ftag{font-family:'Oswald';font-weight:500;font-size:11px;color:var(--gold);letter-spacing:2px;text-transform:uppercase;margin-top:2px}
.faddr{font-size:11px;color:var(--mut);margin-top:8px}
.fsoc{font-size:11px;color:var(--cream);margin-top:5px}.fsoc b{color:var(--gold)}
.fpay{font-size:10px;color:var(--mut);margin-top:10px;line-height:1.6}
.updated{font-size:9.5px;color:#6f5f4d;margin-top:8px}
`;
const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Anton&family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">`;
function header(sub){ return `<header class="top"><div class="logo">Camba · Brauerei Handwerk</div><h1>Tap<span>House</span> Frankfurt</h1><div class="tag">#SpiceCraft</div><div class="sub">${esc(sub)}</div><div class="bar"></div><div class="addr">Mendelssohnstraße 51 · Frankfurt am Main · taphousefrankfurt.com</div></header>`; }
function footer(emblem, stamp){ return `<footer><img class="femblem" src="${emblem}"/><div class="fbrand">TapHouse Frankfurt</div><div class="ftag">Craft Beer Bar with Indian Kitchen</div><div class="faddr">Mendelssohnstraße 51 · 60325 Frankfurt am Main · +49 69 60660989 · taphousefrankfurt.com</div><div class="fsoc">Follow us: <b>Instagram</b> · <b>Facebook</b> · <b>Untappd</b> @taphousefrankfurt</div><div class="fpay">Card payments welcome · Girocard from €10 · Debit/Credit from €15 — no AMEX<br>#SpiceCraft · #EinfachCraftBier · Prices in € incl. VAT</div><div class="updated">Menu auto-updated ${stamp}</div></footer>`; }
const TABS_JS=`document.querySelectorAll('nav.tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('nav.tabs button').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.tab).classList.add('active');window.scrollTo(0,0);});const h=location.hash.replace('#','');if(['tap','bottle','other'].includes(h)){const t=document.querySelector('nav.tabs button[data-tab="'+h+'"]');if(t)t.click();}`;
const FILTER_JS=`(function(){const chips=document.getElementById('bchips'),search=document.getElementById('bsearch');if(!chips)return;let cur='all';function apply(){const q=search.value.trim().toLowerCase();let any=false;document.querySelectorAll('#blist .catblock').forEach(bl=>{const ok=cur==='all'||bl.dataset.cat===cur;let sh=0;bl.querySelectorAll('.brow').forEach(r=>{const m=ok&&(!q||r.dataset.name.includes(q));r.style.display=m?'flex':'none';if(m)sh++;});bl.style.display=(ok&&sh>0)?'block':'none';if(sh>0)any=true;});document.getElementById('bempty').style.display=any?'none':'block';}chips.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{chips.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));c.classList.add('active');cur=c.dataset.cat;apply();});search.addEventListener('input',apply);})();`;
function page(title, body, js){ return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title>${FONTS}<style>${STYLE}</style></head><body>${body}<script>${js}</script></body></html>`; }

function build(tap, bottle, other, rmap, emblem, stamp){
  const T=tapPanel(tap,rmap), B=bottlePanel(bottle), O=otherPanel(other);
  const combined=page('TapHouse Frankfurt — Drinks', `<div class="wrap">${header('Drinks Menu')}<nav class="tabs"><button data-tab="tap" class="active">On Tap</button><button data-tab="bottle">Bottles</button><button data-tab="other">Other Drinks</button></nav><div id="tap" class="panel active">${T}</div><div id="bottle" class="panel">${B}</div><div id="other" class="panel">${O}</div>${footer(emblem,stamp)}</div>`, TABS_JS+FILTER_JS);
  const mk=(sub,panel,js)=>page('TapHouse Frankfurt — '+sub, `<div class="wrap standalone">${header(sub)}<div class="panel active">${panel}</div>${footer(emblem,stamp)}</div>`, js);
  return {
    'index.html': combined,
    'tap-beers/index.html': mk('Tap Beers', T, ''),
    'bottle-beers/index.html': mk('Bottled Beers', B, FILTER_JS),
    'other-drinks/index.html': mk('Other Than Beer', O, '')
  };
}

async function main(){
  mkdirSync(PUB,{recursive:true});
  const rmapRaw={"camba bavaria hell": [3.43, 16621], "camba bavaria pils": [3.37, 865], "camba bavaria jager weisse / simcoe weisse": [3.64, 9032], "camba bavaria chiemsee pale": [3.64, 4107], "camba bavaria island": [3.78, 4574], "camba bavaria chiemsee hopla": [3.46, 10753], "camba bavaria chiemsee black": [3.54, 3127], "orca brau algorithmusfrei - double west coast red ale": [3.95, 342], "kinn sjelefred": [3.4, 11101], "pivovar matuska zlata raketa 17": [3.87, 8090], "faselbrau - zum wohl brauerei peach cream cider": [4.15, 53], "kuehn kunz rosen howlsome": [3.76, 375], "vogelsang karmingimpel": [3.57, 224], "strassenbrau too hop to handle": [3.8, 343], "two chefs exotic getaway - mango guave passionfruit sour": [3.3, 6294], "atelier vrai i did, did i": [4.19, 114], "camba bavaria bavarian summer": [3.82, 70], "fuerst wiacek berlin fire": [3.84, 1356], "blech.brut tentapod": [4.09, 269], "sudden death smokin in ohio": [4.1, 512]};
  const rmap={}; for(const k in rmapRaw) rmap[norm(k)]=rmapRaw[k];
  const other={"mixers": "All mixers 3.20 € — Water, Cola / Cola Light / Cola Zero, TH Tonic Water, TH Bitter Lemon, TH Spicy Ginger", "spirits": {"Gin": [["Stobbe 1776 – Premium London Dry Gin", "", "8.40", "5.40"]], "Rum": [["Old Monk XXX 7 Y.O. Vatted (Mohan Meakin)", "40%", "8.40", "5.40"], ["The Kraken Black Spiced Rum", "35%", "9.40", "5.90"], ["Camikara 8 Y.O. Cask Aged Indian Rum", "", "10.90", "6.90"], ["Ron Zacapa Centenario Solera 23 Gran Reserva", "40%", "14.90", "8.90"]], "Bourbon": [["Maker's Mark Kentucky Straight Bourbon", "43%", "8.40", "5.40"]], "Single Malt Whisky": [["Monkey Shoulder Batch 27 Blended Malt", "40%", "9.90", "6.40"], ["Indri 'Trini – The Three Wood' Indian Single Malt", "46%", "10.90", "6.90"], ["Caol Ila 12 Y.O. Single Malt Scotch", "43%", "11.90", "7.40"], ["The Glenlivet 18 Y.O. Single Malt Scotch", "40%", "16.90", "10.90"]], "Shots": [["Berliner Luft Pfefferminzlikör", "", "5.40", "3.90"], ["Jose Cuervo Especial Gold Reposado Tequila", "38%", "7.90", "4.90"], ["Herradura Reposado Tequila", "40%", "9.90", "6.90"]]}, "af_cocktails": [["Daiquiri", "0.0%", "8.90"], ["Espresso Martini", "0.0%", "8.90"], ["Spritz", "0.2%", "8.90"], ["Paloma", "0.3%", "8.90"], ["G&T", "0.4%", "8.90"], ["Mojito", "0.5%", "8.90"]], "wine": [["Prinz von Hessen – Rosé", "11.5%", "5.40", "8.40", "27.90"], ["Prinz von Hessen – Landgraf Feinherb Riesling", "11.5%", "5.40", "8.40", "27.90"], ["Weingut Groh – Sauvignon Blanc", "11.5%", "5.40", "8.40", "27.90"], ["Weingut Knipser – Sauvignon Blanc Trocken", "12%", "6.40", "9.40", "29.90"], ["Tenuta Ca' Bolani – Merlot Friuli Aquileia", "13%", "5.90", "8.90", "28.90"], ["Bodegas Montecillo – Crianza", "13.5%", "6.90", "9.90", "30.90"], ["Masseria Altemura 'Sasseo' – Primitivo Salento IGT", "14.5%", "6.90", "9.90", "30.90"]], "wine_special": [["Wine Schorle", "", "", "6.90", ""], ["Aperol Spritz", "", "", "8.90", ""]], "wine_na": [["SOBERCIETY 'Missed You' Sauvignon Blanc", "0.5%", "6.90", "9.90", "30.90"], ["Kolonne Null – Riesling", "0.0%", "5.90", "8.90", "28.90"]], "soft": [["H2O – Vio (medium / still)", "0.25l 3.40  ·  0.75l 7.90"], ["Apfelschorle", "0.3l 3.90"], ["Orangensaft (100% Direktsaft, no added sugar)", "0.3l 4.90"], ["Hausgemachte Limonade Schorle — Maracuja-Minze / Mango-Rosmarin / Himbeere-Hibiskus / Zitrone-Basilikum", "0.4l 5.90"], ["Coca-Cola / Cola Light / Cola Zero / Fanta", "0.2l 3.90"], ["Thomas Henry – Bitter Lemon / Spicy Ginger", "0.2l 3.90"]], "coffee": [["Espresso", "single 3.90  ·  double 5.40"], ["Americano", "4.90"], ["Cappuccino / Flat White", "5.90"]]};
  const emblem="data:image/png;base64,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";
  const stamp=new Date().toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric',timeZone:'Europe/Berlin'});

  let tap, bottle;
  if(process.env.SELFTEST){
    ({tap,bottle}=JSON.parse(readFileSync(join(__dir,'_fixture.json'),'utf8')));
  } else {
    const [tb,bb]=await Promise.all([fetchPdf(URLS.tap),fetchPdf(URLS.bottle)]);
    tap=parseTap(await extractLines(tb));
    bottle=parseBottle(await extractLines(bb));
  }
  console.log(`Parsed: ${tap.length} taps, ${Object.values(bottle).reduce((a,b)=>a+b.length,0)} bottles in ${Object.keys(bottle).length} categories`);
  if(tap.length<5 || Object.keys(bottle).length<5) throw new Error('Parse looks wrong — aborting so we never publish an empty menu.');
  const files=build(tap,bottle,other,rmap,emblem,stamp);
  for(const [name,html] of Object.entries(files)){ const fp=join(PUB,name); mkdirSync(dirname(fp),{recursive:true}); writeFileSync(fp,html); }
  console.log('Wrote', Object.keys(files).join(', '), '-> public/');
}
if(process.argv[1] && process.argv[1].endsWith('build.mjs')) main().catch(e=>{console.error('BUILD FAILED:',e.message); process.exit(1);});
