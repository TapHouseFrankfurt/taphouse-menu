#!/usr/bin/env python3
"""Regenerate the printed-menu QR codes from qr-routes.json.

WHY THIS EXISTS
---------------
The QR images used to be hand-made PNGs committed to pdf/qr/, with nothing tying
the picture to the URL it encoded. On 22 Aug 2026 the codes were repointed to
/qr/<slug> while those routes were never built, and because the image and the route
lived in two unrelated places, nothing caught it. Every scan 404'd for four days.

Now qr-routes.json is the only place a QR target is defined. build.mjs reads it to
emit the landing pages, this script reads it to draw the images, and the CI verify
job reads it to test them after every deploy. The image and the route cannot drift.

USAGE
-----
    python3 scripts/gen_qr.py            # rewrite pdf/qr/<slug>.png for every route
    python3 scripts/gen_qr.py --check    # verify on-disk PNGs match the table (exit 1 if not)

Only files named after a route are touched. google.png, tripadvisor.png and wifi.png
are unrelated and are deliberately left alone.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLE = os.path.join(ROOT, 'qr-routes.json')
QRDIR = os.path.join(ROOT, 'pdf', 'qr')
SIZE = 720  # px, matches the existing printed assets


def load_table():
    with open(TABLE, encoding='utf-8') as fh:
        data = json.load(fh)
    base = data['base'].rstrip('/')
    routes = {slug: f"{base}/qr/{slug}" for slug in data['routes']}
    style = data.get('style', {})
    # TapHouse print palette, NOT black on white. The printed menus have always used
    # crimson on cream; shipping default black/white would be a visible brand
    # regression on every menu, card and sticker.
    return routes, style.get('dark', '#6D1A28'), style.get('light', '#FFF8EC')


def draw(url, path, dark, light):
    import segno
    # error correction 'h' (~30%) so a code still scans through a beer ring,
    # a crease or dim bar lighting.
    qr = segno.make(url, error='h')
    border = 4                       # quiet zone in modules; below 4 scanners struggle
    modules = qr.symbol_size(scale=1, border=border)[0]
    scale = max(1, SIZE // modules)  # integer scale keeps modules crisp, never blurred
    qr.save(path, scale=scale, border=border, kind='png', light=light, dark=dark)
    # Re-save as RGB. segno emits a 1-bit palette PNG; the previous hand-made assets
    # were RGB and WeasyPrint has been proven against those, so stay byte-compatible
    # in format and avoid surprising the PDF renderer.
    from PIL import Image
    Image.open(path).convert('RGB').save(path)


def check(routes, dark, light):
    try:
        import cv2
    except ImportError:
        print('opencv not installed; cannot --check', file=sys.stderr)
        return 1
    det, bad = cv2.QRCodeDetector(), []
    for slug, url in routes.items():
        path = os.path.join(QRDIR, f'{slug}.png')
        if not os.path.exists(path):
            bad.append(f'{slug}: MISSING {path}')
            continue
        img = cv2.imread(path)
        decoded = det.detectAndDecode(img)[0] if img is not None else ''
        if decoded != url:
            bad.append(f'{slug}: encodes {decoded!r}, expected {url!r}')
            continue
        # Brand check: the printed codes are crimson on cream, not black on white.
        # A wrong-colour code still scans, so no URL check would ever catch it -- but
        # it is a visible regression on every printed menu, card and sticker.
        from PIL import Image
        with Image.open(path) as im:
            seen = {'#%02X%02X%02X' % rgb for _, rgb in im.convert('RGB').getcolors(65536)}
        for want in (dark.upper(), light.upper()):
            if want not in seen:
                bad.append(f'{slug}: wrong colour - missing {want}, found {sorted(seen)}')
    for line in bad:
        print('  MISMATCH', line)
    print(f'{len(routes) - len(bad)}/{len(routes)} QR images match qr-routes.json')
    return 1 if bad else 0


def main():
    routes, dark, light = load_table()
    if '--check' in sys.argv:
        return check(routes, dark, light)
    os.makedirs(QRDIR, exist_ok=True)
    for slug, url in routes.items():
        path = os.path.join(QRDIR, f'{slug}.png')
        draw(url, path, dark, light)
        print(f'  {slug:8s} -> {url}')
    print(f'Wrote {len(routes)} QR images to pdf/qr/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
