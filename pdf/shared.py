# -*- coding: utf-8 -*-
_uid=[0]
def bubbles(rating, d=13, gap=4, fill="#ffcc33", ring="#8a7550", ringw=1.4):
    n=5; W=n*d+(n-1)*gap; H=d; _uid[0]+=1; base=_uid[0]
    p=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;display:inline-block">']
    for i in range(n):
        cx=i*(d+gap)+d/2; cy=d/2; r=d/2-ringw
        f=max(0.0,min(1.0,rating-i))
        p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{ring}" stroke-width="{ringw}"/>')
        if f>0:
            cid=f"bb{base}_{i}"; x0=cx-r; w=f*(2*r)
            p.append(f'<clipPath id="{cid}"><rect x="{x0:.1f}" y="{cy-r:.1f}" width="{w:.2f}" height="{2*r:.1f}"/></clipPath>')
            p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" clip-path="url(#{cid})"/>')
    p.append('</svg>'); return ''.join(p)

# shared dark palette
PAL=dict(bg="#17100f", bg2="#20161a", panel="rgba(255,255,255,.035)", wine="#8a2733",
         cream="#f2e6d2", gold="#e3ad46", yellow="#ffcc33", mut="#a08b78",
         line="rgba(227,173,70,.16)", ink="#f2e6d2")
