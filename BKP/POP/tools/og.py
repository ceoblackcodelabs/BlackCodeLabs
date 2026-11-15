"""Generate 1200x630 Open Graph share images (WhatsApp / Facebook / X / LinkedIn previews)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
F = lambda n, s: ImageFont.truetype(os.path.join(HERE, 'fonts', n), s)
W, H = 1200, 630
INK = (26, 20, 17); GOLD = (214, 169, 58); GOLD2 = (239, 199, 101)

def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * 0.4)
    return im.crop((x, y, x + w, y + h))

def wrap(d, text, font, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def make(out, bg_stem, kicker, title, foot=''):
    bgp = os.path.join(ROOT, 'assets/img', bg_stem + '.webp')
    bg = cover(Image.open(bgp).convert('RGB'), W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(0.6))
    ov = Image.new('RGBA', (W, H))
    px = ov.load()
    for x in range(W):                       # left-to-right dark gradient for legibility
        a = int(235 - 150 * (x / W) ** 0.9)
        for y in range(H):
            b = int(40 * (y / H))             # extra darkening towards the bottom
            px[x, y] = INK + (min(250, a + b),)
    im = Image.alpha_composite(bg.convert('RGBA'), ov)
    d = ImageDraw.Draw(im)
    # gold edge
    d.rectangle([0, 0, 14, H], fill=GOLD)
    # logo tile
    lg = Image.open(os.path.join(ROOT, 'assets/img/logo.png')).convert('RGBA')
    lg.thumbnail((78, 104))
    tile = Image.new('RGBA', (lg.width + 28, lg.height + 24), (255, 253, 249, 255))
    m = Image.new('L', tile.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, tile.width - 1, tile.height - 1], 20, fill=255)
    im.paste(tile, (64, 56), m); im.paste(lg, (64 + 14, 56 + 12), lg)
    d = ImageDraw.Draw(im)
    d.text((64 + tile.width + 22, 70), 'POCKET OF PARADISE', font=F('Poppins-SemiBold.ttf', 26), fill=(255, 255, 255))
    d.text((64 + tile.width + 22, 106), 'Boutique safaris & beach escapes', font=F('Poppins-Medium.ttf', 22), fill=GOLD2)
    # kicker + title
    kf = F('Poppins-SemiBold.ttf', 24)
    y = 228
    if kicker:
        d.rectangle([64, y + 13, 104, y + 15], fill=GOLD)
        d.text((120, y), kicker.upper(), font=kf, fill=GOLD2)
        y += 56
    size = 60
    while True:
        tf = F('Poppins-ExtraBold.ttf', size)
        lines = wrap(d, title, tf, 760)
        if len(lines) <= 3 or size <= 44: break
        size -= 4
    for ln in lines[:3]:
        d.text((64, y), ln, font=tf, fill=(255, 255, 255)); y += int(size * 1.16)
    if foot:
        d.rounded_rectangle([64, H - 92, 64 + d.textlength(foot, font=F('Poppins-SemiBold.ttf', 26)) + 48, H - 40], 26, fill=GOLD)
        d.text((88, H - 86), foot, font=F('Poppins-SemiBold.ttf', 26), fill=INK)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.convert('RGB').save(out, 'JPEG', quality=84, optimize=True, progressive=True)
