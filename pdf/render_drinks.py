# -*- coding: utf-8 -*-
# Renders the 3 light-print drinks PDFs (Tap / Bottle / Other) that match the Food
# menu look. Data comes from public/_drinks.json (live Untappd feed via build.mjs);
# curated descriptions + spirits/wine/soft/coffee come from data.py. Falls back to the
# curated snapshot in data.py if _drinks.json is missing. Output -> public/*.pdf.
import html, urllib.parse, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data as D          # data.py merges public/_drinks.json over its curated snapshot
from shared import bubbles as _bub
from weasyprint import HTML

def esc(s): return html.escape(str(s))
def fpath(rel): return "file://" + os.path.join(HERE, rel)
PUB = os.path.abspath(os.path.join(HERE, '..', 'public'))
os.makedirs(PUB, exist_ok=True)

CRIM="#6D1A28"; DEEP="#4A1019"; GOLD="#C9963A"; SOFTG="#E3C88F"; CREAM="#FFF8EC"; INK="#1A1209"; MUT="#8a7256"; YEL="#E7A81E"

def bub_img(rating,d=12,gap=3):
    svg=_bub(rating,d=d,gap=gap,fill="#E7A81E",ring="#c9a86a",ringw=1.3)
    W=5*d+4*gap
    return '<img src="data:image/svg+xml;utf8,'+urllib.parse.quote(svg)+'" width="%d" height="%d" style="vertical-align:middle"/>'%(W,d)

def _teaser(desc, n=66):
    """One clean line for print: truncate long descriptions at a word boundary with an ellipsis."""
    desc=desc.strip()
    if len(desc)<=n:
        return desc
    return desc[:n].rsplit(' ',1)[0].rstrip(' ,;:—-')+'…'

def tap_items(pred=lambda n: True):
    """Render tap cards whose real tap number satisfies pred(n). Core = 1-7, rotating = 8+."""
    out=[]
    for idx,(name,origin,style,abv,ibu,desc,prices) in enumerate(D.TAP):
        _tn = getattr(D, 'TAP_NUM', None)
        tapno = _tn[idx] if (_tn and idx < len(_tn)) else idx+1
        if not pred(tapno):
            continue
        meta=" · ".join([x for x in [style,(abv+" ABV" if abv else ""),(ibu+" IBU" if ibu else "")] if x])
        pr="   ".join('%s <b>€%s</b>'%(esc(sz),esc(p)) for sz,p in prices)
        d='<div class="d">%s</div>'%esc(_teaser(desc)) if desc else ''
        sc,cnt=(D.TAP_RATING[idx] if idx < len(D.TAP_RATING) else (0,0))
        rate=''
        if sc:
            rate='<div class="rate">%s <span class="rs">%.2f</span> <span class="rc">%s ratings</span></div>'%(bub_img(sc),sc,D.kfmt(cnt))
        out.append('<div class="item"><div class="n"><span class="num">%d</span>%s</div>%s<div class="m">%s · %s</div>%s<div class="p">%s</div></div>'%(tapno,esc(name),rate,esc(meta),esc(origin),d,pr))
    return "".join(out)

def tap_html():   # full list (kept for reference / any non-split use)
    return tap_items()

def bottle_html():
    out=[]
    for cat,items in D.BOTTLE.items():
        rows=[]
        for name,origin,style,abv,size,price in items:
            rows.append('<div class="brow"><div class="bl"><span class="bn">%s</span><span class="bm">%s · %s · %s</span></div><div class="br"><span class="bs">%s</span><span class="bp">€%s</span></div></div>'%(esc(name),esc(style),esc(abv),esc(origin),esc(size),esc(price)))
        out.append('<div class="cat"><h3>%s <span class="cc">%d</span></h3>%s</div>'%(esc(cat),len(items),"".join(rows)))
    return "".join(out)

def other_html():
    def sp(items):
        r=[]
        for name,abv,p4,p2 in items:
            m='<span class="bm">%s</span>'%esc(abv) if abv else ''
            r.append('<div class="brow"><div class="bl"><span class="bn">%s</span>%s</div><div class="br"><span class="bp">4cl €%s</span><span class="bsub">2cl €%s</span></div></div>'%(esc(name),m,esc(p4),esc(p2)))
        return "".join(r)
    spirit="".join('<div class="cat"><h3>%s</h3>%s</div>'%(esc(c),sp(i)) for c,i in D.SPIRITS.items())
    afrows="".join('<div class="brow"><div class="bl"><span class="bn">%s</span><span class="bm">%s · non-alcoholic</span></div><div class="br"><span class="bp2">€%s</span></div></div>'%(esc(n),esc(a),esc(p)) for n,a,p in D.AF_COCKTAILS)
    afblock='<div class="cat"><h3>Alcohol-Free Cocktails — ISH</h3>%s</div>'%afrows
    def wn(items):
        r=[]
        for name,abv,g1,g2,bo in items:
            pp=" · ".join(x for x in [('0.1l €'+g1) if g1 else '',('0.2l €'+g2) if g2 else '',('Bottle €'+bo) if bo else ''] if x)
            m='<span class="bm">%s</span>'%esc(abv) if abv else ''
            r.append('<div class="brow"><div class="bl"><span class="bn">%s</span>%s</div><div class="br"><span class="bp2">%s</span></div></div>'%(esc(name),m,esc(pp)))
        return "".join(r)
    wine='<div class="cat"><h3>Wine</h3>%s%s</div><div class="cat"><h3>Alcohol-Free Wine</h3>%s</div>'%(wn(D.WINE),wn(D.WINE_SPECIAL),wn(D.WINE_NA))
    def sm(items): return "".join('<div class="brow"><div class="bl"><span class="bn">%s</span></div><div class="br"><span class="bp2">%s</span></div></div>'%(esc(n),esc(p)) for n,p in items)
    return '<div class="note">%s. Spirit prices: 4cl (single) / 2cl.</div><div class="cols2">%s%s<div class="cat"><h3>Softdrinks</h3>%s</div><div class="cat"><h3>Coffee</h3>%s</div></div>'%(esc(D.MIXERS),spirit+afblock,wine,sm(D.SOFT),sm(D.COFFEE))

EMBLEM=fpath('emblem.png')
PAY=('<div class="paystrip"><div class="pl1">Kartenzahlung willkommen · Bargeld sowieso &nbsp;/&nbsp; Card payments welcome · Cash, of course</div>'
     '<div class="pl2">Girocard ab 10&#8201;€ · Debit-/Kreditkarten ab 15&#8201;€ – sorry, AMEX · Internationale &amp; Business-Karten ggf. mit geringem Aufschlag / small surcharge may apply. &nbsp;·&nbsp; #SpiceCraft · #EinfachCraftBier · Untappd: TapHouse Frankfurt</div></div>')
CONTACT=('<div class="contact"><img class="cemb" src="%s"/>'
         '<div class="cright"><div class="cbrand">TapHouse Frankfurt</div>'
         '<div class="ctag">Craft Beer Bar with Indian Kitchen</div>'
         '<div class="caddr">Mendelssohnstraße 51 · 60325 Frankfurt am Main</div>'
         '<div class="caddr">+49 69 60660989 · taphousefrankfurt.com</div>'
         '<div class="csoc">Folgen Sie uns: <b>Instagram</b> · <b>Facebook</b> · <b>Untappd</b> @taphousefrankfurt</div>'
         '</div></div>')%EMBLEM

FONTS='''
@font-face{font-family:'Cormorant';src:url('%s');font-weight:400}
@font-face{font-family:'Cormorant';src:url('%s');font-weight:600}
@font-face{font-family:'Cormorant';src:url('%s');font-weight:700}
@font-face{font-family:'Jost';src:url('%s');font-weight:400}
@font-face{font-family:'Jost';src:url('%s');font-weight:500}
@font-face{font-family:'Jost';src:url('%s');font-weight:600}
'''%(fpath('cormorant-400.woff2'),fpath('cormorant-600.woff2'),fpath('cormorant-700.woff2'),
     fpath('jost-400.woff2'),fpath('jost-500.woff2'),fpath('jost-600.woff2'))

def css():
    return FONTS+'''
@page{size:A4;margin:14mm 13mm 14mm 13mm;
 @bottom-right{content:"Seite " counter(page) "/" counter(pages);font-family:"Jost";font-size:7pt;color:#b09b78}}
*{box-sizing:border-box;margin:0;padding:0}
.bg{position:fixed;top:-14mm;left:-13mm;width:210mm;height:297mm;background:'''+CREAM+''';z-index:-2}
.bgband{position:fixed;top:-14mm;left:-13mm;width:210mm;height:66mm;background:linear-gradient(180deg,#fbf1dd,'''+CREAM+''');z-index:-1}
body{font-family:"Jost";color:'''+INK+''';font-size:8.6pt;line-height:1.4}
.note{font-size:8pt;color:'''+MUT+''';font-style:italic;margin:0 0 6pt;border-left:2.5pt solid '''+GOLD+''';padding-left:8pt}
.cols2{column-count:2;column-gap:15pt}
.item{break-inside:avoid;margin-bottom:5pt;padding-bottom:4pt;border-bottom:.5pt solid #ecdcbf}
.item .n{font-family:"Cormorant";font-weight:700;font-size:12.5pt;color:'''+CRIM+''';line-height:1.05}
.item .num{display:inline-block;min-width:15pt;color:'''+GOLD+'''}
.rate{margin:2.5pt 0 1pt}
.rate .rs{font-family:"Jost";font-weight:600;font-size:8.4pt;color:#a9781a;vertical-align:middle}
.rate .rc{font-size:6.6pt;color:'''+MUT+''';vertical-align:middle}
.item .m{font-size:7.3pt;color:'''+DEEP+''';margin-top:1.5pt;font-weight:500}
.item .d{font-size:7.2pt;color:#5a4a34;margin-top:2pt;line-height:1.3;font-style:italic;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.item .p{font-size:8pt;margin-top:3pt;color:'''+MUT+'''}
.item .p b{color:'''+CRIM+'''}
.cat{break-inside:avoid;margin-bottom:8pt}
.cat h3{font-family:"Cormorant";font-weight:700;font-size:12pt;letter-spacing:.5pt;color:'''+CRIM+''';border-bottom:1pt solid '''+SOFTG+''';padding-bottom:2pt;margin-bottom:3pt}
.cat h3 .cc{color:'''+GOLD+''';font-size:8.5pt;font-family:"Jost"}
.brow{display:flex;justify-content:space-between;gap:6pt;align-items:baseline;padding:2.3pt 0;border-bottom:.4pt dotted #e2cfa8}
.bl{flex:1}
.bn{font-size:8pt;font-weight:600;color:'''+INK+'''}
.bm{display:block;font-size:6.9pt;color:'''+MUT+''';margin-top:.5pt}
.br{text-align:right;white-space:nowrap}
.bs{font-size:6.7pt;color:#b09b78;margin-right:4pt}
.bp{font-family:"Cormorant";font-weight:700;font-size:10.5pt;color:'''+CRIM+'''}
.bsub{display:block;font-size:7pt;color:'''+MUT+''';margin-top:.5pt}
.bp2{font-size:7.4pt;color:'''+CRIM+''';font-weight:600}
.content{padding-bottom:60mm}
.bottomgroup{position:absolute;left:0;right:0;bottom:0}
.sheet{display:flex;flex-direction:column;min-height:265mm}
.sheet.brk{break-before:page}
.fill{flex:1 0 auto}
.footwrap{flex:0 0 auto;margin-top:8pt;break-inside:avoid}
.foot{border-top:.6pt solid '''+GOLD+''';padding-top:5pt;display:flex;justify-content:space-between;align-items:baseline;gap:10pt}
.foot .fl{font-family:"Jost";font-size:7.2pt;color:'''+DEEP+'''}
.foot .fc{font-family:"Cormorant";font-style:italic;font-weight:600;font-size:9.5pt;color:'''+CRIM+'''}
.foot .fr{font-family:"Jost";font-size:7.2pt;color:'''+MUT+''';letter-spacing:.3pt}
.qrzone{break-inside:avoid;margin-top:6pt}
.qrhead{font-family:"Cormorant";font-weight:700;font-size:13pt;color:'''+CRIM+''';text-align:center;letter-spacing:.5pt;border-bottom:1pt solid '''+SOFTG+''';padding-bottom:3pt;margin-bottom:8pt}
.qrrow{display:flex;justify-content:space-between;gap:10pt;align-items:flex-start}
.qrrev{justify-content:center;gap:46pt;margin-top:4pt}
.qrcell{flex:0 0 auto;text-align:center}
.qrrow .qrcell img{width:62pt;height:62pt;display:block;margin:0 auto;border:1pt solid #e7d3ab;border-radius:4pt}
.qrrev .qrcell img{width:74pt;height:74pt}
.minicontact{font-family:"Jost";font-size:7.4pt;color:'''+DEEP+''';text-align:center;margin-top:6pt}
.qcap{font-family:"Jost";font-weight:600;font-size:8pt;color:'''+CRIM+''';margin-top:3pt}
.qsub{font-family:"Jost";font-size:6.6pt;color:'''+MUT+''';font-style:italic;margin-top:.5pt}
.qrprompt{text-align:center;font-family:"Cormorant";font-style:italic;font-size:11pt;color:'''+DEEP+''';margin:5pt 0 4pt;padding:0 10pt}
.contact{display:flex;justify-content:space-between;align-items:center;gap:16pt;border-top:1.5pt solid #C9963A;padding-top:9pt}
.cemb{height:50pt}
.cright{text-align:right}
.cbrand{font-family:"Cormorant";font-weight:700;font-size:19pt;color:#6D1A28;line-height:1}
.ctag{font-family:"Cormorant";font-style:italic;font-size:11pt;color:#C9963A;margin-top:1pt}
.caddr{font-family:"Jost";font-size:8pt;color:#4A1019;margin-top:3pt}
.csoc{font-family:"Jost";font-size:8pt;color:#6D1A28;margin-top:3pt}
.csoc b{color:#6D1A28}
.paystrip{background:#C9963A;border-radius:6pt;padding:6pt 12pt;text-align:center;margin:8pt 0 0;break-inside:avoid}
.pl1{font-family:"Cormorant";font-weight:700;font-size:12pt;color:#4A1019}
.pl2{font-family:"Jost";font-size:7.6pt;color:#4A1019;margin-top:2pt;line-height:1.35}
.head{padding:0 0 9pt;margin-bottom:9pt;border-bottom:1.5pt solid #C9963A;text-align:left}
.hrow{display:flex;justify-content:space-between;align-items:flex-start;gap:14pt}
.hl{flex:0 0 auto}
.hr{flex:0 0 auto;text-align:right}
.hc{flex:1;text-align:center;padding-top:2pt}
.llogo{height:80pt}
.emblem{height:56pt;margin-top:6pt}
.hc h1{font-family:"Cormorant";font-weight:700;font-size:31pt;color:#6D1A28;line-height:1;margin:0 0 1pt}
.hc .st{font-family:"Cormorant";font-weight:600;font-size:15pt;color:#4A1019;font-style:italic}
.hc .tl{font-family:"Jost";font-size:8pt;color:#8a7256;letter-spacing:.5pt;margin-top:4pt}
'''

CAMBA=fpath('camba.png')
def header(section, tagline):
    tl='<div class="tl">%s</div>'%esc(tagline) if tagline else ''
    return ('<div class="head"><div class="hrow">'
            '<div class="hl"><img class="llogo" src="%s"/></div>'
            '<div class="hc"><h1>TapHouse Frankfurt</h1><div class="st">%s</div>%s</div>'
            '<div class="hr"><img class="emblem" src="%s"/></div>'
            '</div></div>')%(CAMBA, esc(section), tl, EMBLEM)

def qr_cell(img, cap, sub=''):
    s='<div class="qsub">%s</div>'%esc(sub) if sub else ''
    return '<div class="qrcell"><img src="%s"/><div class="qcap">%s</div>%s</div>'%(fpath('qr/'+img),esc(cap),s)

QR_BLOCK = ('<div class="qrzone">'
    '<div class="qrhead">Scan for more &nbsp;·&nbsp; Mehr entdecken</div>'
    '<div class="qrrow">'
    + qr_cell('tap.png','Tap Beers','Bierkarte · live')
    + qr_cell('food.png','Food Menu','Speisekarte')
    + qr_cell('bottle.png','Bottled Beers','Flaschenbiere')
    + qr_cell('other.png','Other Drinks','Weitere Getränke')
    + qr_cell('wifi.png','Free WiFi','Gäste-WLAN')
    + '</div>'
    '<div class="qrprompt">Enjoyed your visit? A quick review means the world to us. &nbsp;/&nbsp; Hat es geschmeckt? Eine kurze Bewertung hilft uns sehr.</div>'
    '<div class="qrrow qrrev">'
    + qr_cell('google.png','Review on Google')
    + qr_cell('tripadvisor.png','Review on Tripadvisor')
    + '</div></div>')

# Gold-line branding row (mirrors the food-menu footer): gold border-top + contact / tagline / hashtags
FOOT_ROW = ('<div class="foot">'
            '<span class="fl">TapHouse Frankfurt · Mendelssohnstraße 51 · 60325 Frankfurt · +49 69 60660989</span>'
            '<span class="fc">Hops. Heat. Frankfurt.</span>'
            '<span class="fr">#SpiceCraft · #EinfachCraftBier</span>'
            '</div>')

def tap_body():
    core = tap_items(lambda n: n <= 7)
    rot  = tap_items(lambda n: n >= 8)
    note1='<div class="note">Tasting flight — choose any five 100&#8201;ml pours from our twenty taps. Ratings are live from Untappd.</div>'
    note2='<div class="note">Rotating taps 8–20 — our ever-changing tap selection, updated as kegs change. Scan any code on page&nbsp;1 for the always-current list.</div>'
    # Page 1: no card-payments strip (frees space); branding + gold line bottom-aligned.
    sheet1=('<div class="sheet">'+header('Beers on Tap','“Spice amplifies hops. Hops cut spice.”')
            +'<div class="fill">'+note1+'<div class="cols2">'+core+'</div>'+QR_BLOCK+'</div>'
            +'<div class="footwrap">'+FOOT_ROW+'</div></div>')
    # Page 2: branding gold line + card-payments strip, bottom-aligned.
    sheet2=('<div class="sheet brk">'+header('Beers on Tap — Rotating','Taps 8–20 · changes often')
            +'<div class="fill">'+note2+'<div class="cols2">'+rot+'</div></div>'
            +'<div class="footwrap">'+FOOT_ROW+PAY+'</div></div>')
    return '<div class="bg"></div><div class="bgband"></div>'+sheet1+sheet2

def build(kind, outname):
    if kind=='tap':
        body=tap_body()
    else:
        cfg={
         'bottle':('Bottled Beers', bottle_html, '',
                '<div class="note">150+ varieties · all bottles available for takeaway at a reduced price.</div>'),
         'other':('Other Than Beer', other_html, '', ''),
        }[kind]
        section, fn, tagline, note = cfg
        inner=fn()
        content = inner if kind=='other' else note+'<div class="cols2">'+inner+'</div>'
        body=('<div class="bg"></div><div class="bgband"></div>'+header(section,tagline)+'<div class="content">'+content+'</div>'+'<div class="bottomgroup">'+PAY+CONTACT+'</div>')
    doc="<!DOCTYPE html><html><head><meta charset='utf-8'><style>"+css()+"</style></head><body>"+body+"</body></html>"
    out=os.path.join(PUB, outname)
    HTML(string=doc, base_url=HERE).write_pdf(out)
    print(outname, os.path.getsize(out), "bytes")

if __name__ == '__main__':
    build('tap','tap-beers.pdf')
    build('bottle','bottle-beers.pdf')
    build('other','other-drinks.pdf')
