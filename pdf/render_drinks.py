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

def tap_html():
    out=[]
    for idx,(name,origin,style,abv,ibu,desc,prices) in enumerate(D.TAP):
        meta=" · ".join([x for x in [style,(abv+" ABV" if abv else ""),(ibu+" IBU" if ibu else "")] if x])
        pr="   ".join('%s <b>€%s</b>'%(esc(sz),esc(p)) for sz,p in prices)
        d='<div class="d">%s</div>'%esc(desc) if desc else ''
        sc,cnt=(D.TAP_RATING[idx] if idx < len(D.TAP_RATING) else (0,0))
        rate=''
        if sc:
            rate='<div class="rate">%s <span class="rs">%.2f</span> <span class="rc">%s ratings</span></div>'%(bub_img(sc),sc,D.kfmt(cnt))
        out.append('<div class="item"><div class="n"><span class="num">%d</span>%s</div>%s<div class="m">%s · %s</div>%s<div class="p">%s</div></div>'%(idx+1,esc(name),rate,esc(meta),esc(origin),d,pr))
    return "".join(out)

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
@page{size:A4;margin:14mm 13mm 18mm 13mm;
 @bottom-center{content:"Hops. Heat. Frankfurt.  ·  #SpiceCraft · #EinfachCraftBier  ·  Untappd: TapHouse Frankfurt";font-family:"Jost";font-size:7.2pt;color:#9a805e;letter-spacing:.4pt}
 @bottom-right{content:"Seite " counter(page) "/" counter(pages);font-family:"Jost";font-size:7pt;color:#b09b78}}
*{box-sizing:border-box;margin:0;padding:0}
.bg{position:fixed;top:-14mm;left:-13mm;width:210mm;height:297mm;background:'''+CREAM+''';z-index:-2}
.bgband{position:fixed;top:-14mm;left:-13mm;width:210mm;height:66mm;background:linear-gradient(180deg,#fbf1dd,'''+CREAM+''');z-index:-1}
body{font-family:"Jost";color:'''+INK+''';font-size:8.6pt;line-height:1.4}
.note{font-size:8pt;color:'''+MUT+''';font-style:italic;margin:0 0 8pt;border-left:2.5pt solid '''+GOLD+''';padding-left:8pt}
.cols2{column-count:2;column-gap:15pt}
.item{break-inside:avoid;margin-bottom:6.5pt;padding-bottom:5.5pt;border-bottom:.5pt solid #ecdcbf}
.item .n{font-family:"Cormorant";font-weight:700;font-size:12.5pt;color:'''+CRIM+''';line-height:1.05}
.item .num{display:inline-block;min-width:15pt;color:'''+GOLD+'''}
.rate{margin:2.5pt 0 1pt}
.rate .rs{font-family:"Jost";font-weight:600;font-size:8.4pt;color:#a9781a;vertical-align:middle}
.rate .rc{font-size:6.6pt;color:'''+MUT+''';vertical-align:middle}
.item .m{font-size:7.3pt;color:'''+DEEP+''';margin-top:1.5pt;font-weight:500}
.item .d{font-size:7.3pt;color:#5a4a34;margin-top:2.5pt;line-height:1.32;font-style:italic}
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
.contact{display:flex;justify-content:space-between;align-items:center;gap:16pt;border-top:1.5pt solid #C9963A;padding-top:9pt}
.cemb{height:50pt}
.cright{text-align:right}
.cbrand{font-family:"Cormorant";font-weight:700;font-size:19pt;color:#6D1A28;line-height:1}
.ctag{font-family:"Cormorant";font-style:italic;font-size:11pt;color:#C9963A;margin-top:1pt}
.caddr{font-family:"Jost";font-size:8pt;color:#4A1019;margin-top:3pt}
.csoc{font-family:"Jost";font-size:8pt;color:#6D1A28;margin-top:3pt}
.csoc b{color:#6D1A28}
.paystrip{background:#C9963A;border-radius:6pt;padding:8pt 12pt;text-align:center;margin:0 0 10pt;break-inside:avoid}
.pl1{font-family:"Cormorant";font-weight:700;font-size:12pt;color:#4A1019}
.pl2{font-family:"Jost";font-size:7.6pt;color:#4A1019;margin-top:2pt;line-height:1.35}
.head{padding:0 0 9pt;margin-bottom:9pt;border-bottom:1.5pt solid #C9963A;text-align:left}
.hrow{display:flex;justify-content:space-between;align-items:flex-start;gap:14pt}
.hl{flex:0 0 auto}
.hr{flex:0 0 auto;text-align:right}
.hc{flex:1;text-align:center;padding-top:2pt}
.llogo{height:92pt}
.emblem{height:64pt;margin-top:6pt}
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

def build(kind, outname):
    cfg={
     'tap':('Beers on Tap', tap_html, '“Spice amplifies hops. Hops cut spice.”',
            '<div class="note">Tasting flight — choose any five 100&#8201;ml pours from our twenty taps. Ratings are live from Untappd.</div>'),
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
