# -*- coding: utf-8 -*-
# Build the responsive HTML food menu (dark theme matching the drinks/beer menu).
# Skips print pages 1 (cover), 2 (story) and 8 (scan/QR back page).
import html, os, datetime, re

# Pull the real logos from the live build engine (build.mjs) so the food menu
# header matches the drinks menu exactly and stays in sync.
_bmjs_path = os.path.join(os.path.dirname(__file__), 'build.mjs')
if not os.path.exists(_bmjs_path):
    _bmjs_path = os.path.join(os.path.dirname(__file__), '..', 'build.mjs')
_BMJS = open(_bmjs_path).read()
def _grab(name):
    m = re.search(name + r'\s*=\s*"(data:[^"]+)"', _BMJS)
    if not m: raise SystemExit('logo %s not found in build.mjs' % name)
    return m.group(1)
CAMBA_LOGO = _grab('CAMBA_LOGO')   # Camba / TAP HOUSE badge (header left)
EMBLEM_HDR = _grab('EMBLEM_HDR')   # #EinfachCraftBier hop emblem (header right)
EMBLEM = EMBLEM_HDR                # reuse the same emblem in the footer

# ---- SINGLE SOURCE: parse the print menu.html for all dish data --------------
# The web food menu is generated FROM the print source (menu.html) so prices and
# dishes can never drift. Edit menu.html once -> regenerate PDF (WeasyPrint) AND
# this web menu (build_food.py). No dish data is duplicated here.
from bs4 import BeautifulSoup
MENU_CANDIDATES = [
    os.environ.get('FOOD_MENU_SRC', ''),
    '/sessions/vigilant-vibrant-curie/mnt/Claude CoWork/TapHouse Food Menu Source/menu.html',
    os.path.join(os.path.dirname(__file__), 'menu.html'),
    os.path.join(os.path.dirname(__file__), '..', 'menu.html'),
]
MENU = next((p for p in MENU_CANDIDATES if p and os.path.exists(p)), None)
if not MENU:
    raise SystemExit('menu.html (single source) not found; set FOOD_MENU_SRC')
_soup = BeautifulSoup(open(MENU, encoding='utf-8').read(), 'html.parser')

def _norm(s): return re.sub(r'\s+', ' ', (s or '').replace('\xa0', ' ')).strip()
def _txt(el): return _norm(el.get_text()) if el else ''

def _parse_dish(m):
    head = m.select_one('.dish-head'); name_el = head.select_one('.dish-name')
    pills = [_norm(p.get_text()) for p in name_el.select('.pill')]
    ne = BeautifulSoup(name_el.decode(), 'html.parser')
    for p in ne.select('.pill'): p.decompose()
    name = _norm(ne.get_text())
    pe = head.select_one('.price'); price = _norm(pe.get_text()) if pe else ''
    de = _txt(m.select_one('.desc-de')); en = _txt(m.select_one('.desc-en')); add = _txt(m.select_one('.addon'))
    ve = m.select_one('.variants'); var = _norm(''.join(str(c) for c in ve.contents)) if ve else ''
    pr = m.select_one('.pair'); pair = _norm(pr.select_one('b').get_text()) if (pr and pr.select_one('b')) else ''
    return dict(name=name, price=price, pills=pills, de=de, en=en, add=add, var=var, pair=pair)

def _subhead(m):
    frag = BeautifulSoup(m.decode(), 'html.parser'); span = frag.select_one('span'); sp = ''
    if span: sp = _norm(span.get_text()); span.decompose()
    main = _norm(frag.get_text())
    return (main + ' \u00b7 ' + sp.split('\u00b7')[0].strip()) if sp else main

# id + short tab label per content page, in document order (presentation only)
SECTION_META = [
    ('starters', 'Starters'),
    ('tandoor', 'Tandoor'),
    ('salads', 'Salads & Breads'),
    ('veg', 'Veg Mains'),
    ('mains', 'Chicken \u00b7 Gosht \u00b7 Prawns'),
]
_pages = []
for pg in _soup.select('div.page'):
    cl = pg.get('class', [])
    if 'cover' in cl or pg.select_one('.sx8'): continue          # skip cover + scan/QR back page
    sh = pg.select_one('.sec-head')
    if not sh or not pg.select('.dish'): continue                # skip the story page (no dishes)
    content = pg.select_one('.content')
    blocks = [{'head': '', 'dishes': []}]
    for mk in content.find_all('div', class_=['dish', 'subsec-title']):
        if 'subsec-title' in mk.get('class', []):
            blocks.append({'head': _subhead(mk), 'dishes': []})
        else:
            blocks[-1]['dishes'].append(_parse_dish(mk))
    en = _txt(sh.select_one('.sec-title-en')); de = _txt(sh.select_one('.sec-title'))
    _pages.append(dict(eyebrow=_txt(sh.select_one('.sec-eyebrow')),
                       title=(en or de), title_de=(de if en else ''),
                       note=_txt(sh.select_one('.sec-note')), blocks=blocks))
if len(_pages) != len(SECTION_META):
    raise SystemExit('expected %d content pages, found %d' % (len(SECTION_META), len(_pages)))
SECTIONS = []
for (sid, tab), pdata in zip(SECTION_META, _pages):
    d = dict(id=sid, tab=tab); d.update(pdata); SECTIONS.append(d)

# ---- allergen legend ---------------------------------------------------------
LEGEND = (
 "<b>V</b> vegetarisch · <b>VG</b> vegan · <b>VG*</b> auf Wunsch vegan / vegan on request<br>"
 "Allergene / Allergens: <b>A</b> Gluten · <b>B</b> Krebstiere · <b>C</b> Eier · <b>D</b> Fisch · "
 "<b>E</b> Erdnüsse · <b>F</b> Soja · <b>G</b> Milch · <b>H</b> Schalenfrüchte · <b>I</b> Sellerie · "
 "<b>J</b> Senf · <b>K</b> Sesam · <b>L</b> Sulfite · <b>M</b> Lupinen · <b>N</b> Weichtiere<br>"
 "Zusatzstoffe / Additives: <b>1</b> Farbstoff · <b>2</b> Konservierungsstoff · <b>3</b> Antioxidationsmittel · "
 "<b>4</b> Koffein · <b>5</b> Geschmacksverstärker · <b>7</b> Süßungsmittel · <b>9</b> Phosphat — "
 "Details bei unserem Team / full details from our team<br>"
 "Flaschenbiere & Getränke: digitale Karte – QR-Code am Tisch scannen · Bottled beers & drinks on our digital menu."
)

# ---- rendering ---------------------------------------------------------------
def esc(s): return s  # content already contains intended entities/plain text

def render_code(de):
    # wrap "(A, G)" style codes in a muted span
    import re
    return re.sub(r'\(([^)]*[A-N0-9][^)]*)\)', r'<span class="code">(\1)</span>', de)

def dish_html(d):
    pills = ''.join(f'<span class="vpill">{p}</span>' for p in d['pills'])
    price = f'<span class="d-price">{d["price"]} €</span>' if d['price'] else ''
    parts = [f'<div class="d-top"><span class="d-name">{d["name"]}{pills}</span>{price}</div>']
    if d['de']: parts.append(f'<div class="d-de">{render_code(d["de"])}</div>')
    if d['en']: parts.append(f'<div class="d-en">{d["en"]}</div>')
    if d['var']: parts.append(f'<div class="d-var">{d["var"]} €</div>')
    if d['add']: parts.append(f'<div class="d-add">{d["add"]}</div>')
    if d['pair']: parts.append(f'<div class="pair"><span class="dia"></span>Passt zu / Pairs with <b>{d["pair"]}</b></div>')
    return '<div class="dish">' + ''.join(parts) + '</div>'

def section_html(s, active):
    blocks = []
    head = f'<div class="sec-head"><div class="eyebrow">{s["eyebrow"]}</div>'
    head += f'<div class="sec-title">{s["title"]}</div>'
    if s.get('title_de'): head += f'<div class="sec-title-de">{s["title_de"]}</div>'
    head += '<div class="sec-bar"></div>'
    if s['note']: head += f'<div class="sec-note">{s["note"]}</div>'
    head += '</div>'
    blocks.append(head)
    for b in s['blocks']:
        if b['head']:
            blocks.append(f'<div class="subhead">{b["head"]}</div>')
        blocks.append('<div class="catblock">' + ''.join(dish_html(d) for d in b['dishes']) + '</div>')
    return f'<section id="{s["id"]}" class="panel">' + ''.join(blocks) + '</section>'

tabs = ''.join(
    f'<button class="tabbtn{" active" if i==0 else ""}" data-t="{s["id"]}">{s["tab"]}</button>'
    for i,s in enumerate(SECTIONS))
panels = ''.join(section_html(s, i==0) for i,s in enumerate(SECTIONS))
updated = datetime.date.today().strftime('%-d %b %Y')

CSS = """
:root{--bg:#17100f;--bg2:#20161a;--panel:rgba(255,255,255,.035);--wine:#8a2733;--cream:#f2e6d2;--gold:#e3ad46;--yellow:#ffcc33;--mut:#a08b78;--line:rgba(227,173,70,.16);}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg)}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;color:var(--cream);-webkit-font-smoothing:antialiased}
.wrap{max-width:680px;margin:0 auto;min-height:100vh;background:radial-gradient(1200px 380px at 50% -60px, rgba(138,39,51,.55), transparent 70%),linear-gradient(180deg,#1c1310 0%, #17100f 40%, #140d0c 100%);}
header.top{padding:26px 16px 16px;text-align:center;position:relative}
.top .hrow{display:flex;align-items:center;justify-content:space-between;gap:8px}
.top .cam{height:64px;width:auto;max-width:240px;border-radius:6px;flex:0 0 auto}
.top .emb{height:84px;width:auto;flex:0 0 auto}
.top .mid{flex:1;min-width:0;text-align:center}
.top .mid h1{font-family:'Cormorant Garamond',serif;font-weight:700;font-size:31px;letter-spacing:.3px;margin:1px 0 2px;color:var(--cream);line-height:1.03;text-transform:none;white-space:nowrap}
.top .mid h1 span{color:var(--gold)}
.top .mid .tag{font-family:'Oswald';font-weight:500;letter-spacing:.4px;font-size:11px;color:var(--gold);text-transform:none;margin-top:3px}
.top .mid .sub{font-family:'Oswald';font-weight:500;letter-spacing:2.5px;font-size:11px;color:var(--cream);opacity:.8;margin-top:4px;text-transform:uppercase}
.top .mid .bar{width:46px;height:3px;background:linear-gradient(90deg,var(--gold),var(--yellow));margin:8px auto 0;border-radius:3px}
.top .addr{font-size:11px;color:var(--mut);margin-top:10px}
@media(max-width:520px){
  header.top{padding:12px 12px 8px}
  .top .hrow{gap:7px}
  .top .cam{height:34px;max-width:100px}
  .top .emb{display:none}
  .top .mid h1{font-size:19px;white-space:normal;line-height:1.05}
  .top .mid .tag{font-size:9px;margin-top:2px}
  .top .mid .sub{font-size:9px;letter-spacing:1.6px;margin-top:2px}
  .top .mid .bar{width:32px;margin-top:4px}
  .top .addr{display:none}
}
nav.tabs{position:sticky;top:0;z-index:20;display:flex;gap:2px;overflow-x:auto;background:rgba(20,13,12,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);scrollbar-width:none}
nav.tabs::-webkit-scrollbar{display:none}
nav.tabs button{flex:0 0 auto;border:0;background:transparent;color:var(--mut);font-family:'Oswald';font-weight:600;letter-spacing:1px;font-size:12.5px;padding:14px 15px;cursor:pointer;text-transform:uppercase;border-bottom:3px solid transparent;white-space:nowrap}
nav.tabs button.active{color:var(--cream);border-bottom:3px solid var(--gold)}
.panel{display:block;padding:22px 15px 8px;scroll-margin-top:56px}
.panel + .panel{border-top:1px solid var(--line)}
.sec-head{text-align:center;margin-bottom:14px}
.eyebrow{font-family:'Oswald';font-weight:500;letter-spacing:2.5px;font-size:10.5px;text-transform:uppercase;color:var(--gold)}
.sec-title{font-family:'Oswald';font-weight:600;font-size:24px;color:var(--cream);margin-top:4px;letter-spacing:.5px}
.sec-title-de{font-family:'Oswald';font-weight:400;font-size:13px;color:var(--mut);margin-top:2px;letter-spacing:1px}
.sec-bar{width:52px;height:3px;background:linear-gradient(90deg,var(--gold),var(--yellow));margin:11px auto 0;border-radius:3px}
.sec-note{font-size:11.5px;color:var(--mut);margin-top:10px;line-height:1.5;max-width:560px;margin-left:auto;margin-right:auto}
.subhead{font-family:'Oswald';font-weight:600;font-size:15px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);padding:14px 0 6px;border-bottom:1px solid var(--line);margin:20px 0 2px}
.catblock{margin-bottom:6px}
.dish{padding:13px 2px;border-bottom:1px solid rgba(227,173,70,.1)}
.dish:last-child{border-bottom:0}
.d-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.d-name{font-family:'Oswald';font-weight:600;font-size:15.5px;color:var(--cream);line-height:1.22}
.vpill{display:inline-block;font-family:'Oswald';font-size:9.5px;font-weight:600;letter-spacing:.5px;color:var(--gold);border:1px solid var(--line);border-radius:20px;padding:1px 6px;margin-left:6px;vertical-align:2px;text-transform:uppercase}
.d-price{font-family:'Oswald';font-weight:600;font-size:15px;color:var(--yellow);white-space:nowrap}
.d-de{font-size:12.5px;color:#d3c0a6;margin-top:5px;line-height:1.42}
.d-de .code{color:var(--mut);font-size:11px}
.d-en{font-size:12px;font-style:italic;color:var(--mut);margin-top:3px;line-height:1.4}
.d-var{font-size:12.5px;margin-top:5px;color:var(--cream)}
.d-var b{color:var(--yellow);font-weight:600}
.d-add{font-size:11.5px;color:var(--gold);margin-top:5px}
.pair{margin-top:7px;font-family:'Oswald';font-weight:500;font-size:10.5px;letter-spacing:1.2px;text-transform:uppercase;color:var(--gold)}
.pair b{color:var(--yellow);font-weight:600}
.pair .dia{display:inline-block;width:5px;height:5px;background:var(--gold);transform:rotate(45deg);margin-right:7px;vertical-align:1px}
.legend{margin:6px 15px 0;background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:10px;padding:12px 14px;font-size:10.5px;color:var(--mut);line-height:1.65}
.legend b{color:var(--cream);font-weight:600}
footer{text-align:center;padding:26px 16px 40px;color:var(--mut);font-size:11px;border-top:1px solid var(--line);margin-top:18px}
.femblem{height:54px;margin-bottom:8px;opacity:.95}
.fbrand{font-family:'Oswald';font-weight:600;font-size:19px;color:var(--cream);letter-spacing:.5px}
.ftag{font-family:'Oswald';font-weight:500;font-size:11px;color:var(--gold);letter-spacing:2px;text-transform:uppercase;margin-top:2px}
.faddr{font-size:11px;color:var(--mut);margin-top:8px}
.fpay{font-size:10px;color:var(--mut);margin-top:10px;line-height:1.6}
.updated{font-size:9.5px;color:#6f5f4d;margin-top:8px}
@media(max-width:420px){
  header.top h1{font-size:34px}
  nav.tabs button{font-size:11.5px;padding:13px 11px}
  .sec-title{font-size:21px}
  .d-name{font-size:14.5px}
}
"""

HTML = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Food Menu · TapHouse Frankfurt — Craft Beer Bar & Indian Kitchen</title>
<meta name="description" content="TapHouse Frankfurt food menu — tandoori specialities, curries, snacks, salads, wraps and dessert from our Indian kitchen in the Westend. Craft beer pairings for every dish.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Cormorant+Garamond:wght@600;700&family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div class="hrow">
    <img class="cam" src="{CAMBA_LOGO}" alt="Camba Bavaria TapHouse logo"/>
    <div class="mid">
      <h1>Tap<span>House</span> Frankfurt</h1>
      <div class="tag">Craft Beer Bar with Indian Kitchen (#SpiceCraft)</div>
      <div class="sub">Food Menu</div>
      <div class="bar"></div>
    </div>
    <img class="emb" src="{EMBLEM_HDR}" alt="#EinfachCraftBier logo"/>
  </div>
  <div class="addr">Mendelssohnstraße 51 · 60325 Frankfurt am Main · Craft Beer Bar &amp; Indian Kitchen · taphousefrankfurt.com</div>
</header>
<nav class="tabs" id="tabs">{tabs}</nav>
{panels}
<div class="legend">{LEGEND}</div>
<footer>
  <img class="femblem" src="{EMBLEM}" alt="TapHouse Frankfurt emblem"/>
  <div class="fbrand">TapHouse Frankfurt</div>
  <div class="ftag">Craft Beer Bar with Indian Kitchen</div>
  <div class="faddr">Mendelssohnstraße 51 · 60325 Frankfurt am Main · +49 69 60660989 · taphousefrankfurt.com</div>
  <div class="fpay">Kartenzahlung willkommen · Girocard ab 10 € · Debit/Kredit ab 15 € — kein AMEX<br>#SpiceCraft · #EinfachCraftBier · Preise in € inkl. MwSt.</div>
  <div class="updated">Aktualisiert · {updated}</div>
</footer>
</div>
<script>
(function(){{
  var nav=document.getElementById('tabs');
  var btns=[].slice.call(nav.querySelectorAll('button'));
  function setActive(b){{ btns.forEach(function(x){{x.classList.toggle('active',x===b);}});
    if(b) b.scrollIntoView({{inline:'center',block:'nearest',behavior:'smooth'}}); }}
  // click a section button -> smooth-scroll to that section (nothing is hidden)
  nav.addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b) return;
    var el=document.getElementById(b.getAttribute('data-t'));
    if(el) el.scrollIntoView({{behavior:'smooth',block:'start'}});
    setActive(b);
  }});
  // scrollspy: highlight the section currently in view
  var map={{}}; btns.forEach(function(b){{ map[b.getAttribute('data-t')]=b; }});
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(entries){{
      entries.forEach(function(en){{ if(en.isIntersecting) setActive(map[en.target.id]); }});
    }},{{rootMargin:'-45% 0px -50% 0px',threshold:0}});
    document.querySelectorAll('.panel').forEach(function(p){{io.observe(p);}});
  }}
}})();
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(__file__), '..', 'public', 'food.html')
out = os.path.abspath(out)
open(out,'w').write(HTML)
print("wrote", out, len(HTML), "bytes")
