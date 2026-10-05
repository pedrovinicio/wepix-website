"""Render a 1080x1350 Instagram post in WePix's brand.

Usage: python3 make_post.py '<json spec>' out.jpg

Spec keys:
  layout     "photo" | "phone" | "card"   (default "photo")
  bg         photo layout only: beach | city | nature   (WePix's own group-cover art)
  bg_y       0-1 vertical crop of the photo (default 0.5)
  kicker     short label in the pill, e.g. "NOVIDADE", "VOCÊ SABIA?", "SUA VEZ"
  headline   <= 8 words
  highlight  words of the headline drawn in the accent colour
  sub        one short sentence (optional)
  hsize      headline font size (default 92; card layout default 104)

Self-contained: brand art lives in ./assets, Sora + DM Sans (OFL) in ./fonts.
"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
M = 80
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
FONTS = os.path.join(HERE, 'fonts')

# WePix palette (docs/design/color-schema.md + website css)
PRIMARY = (93, 180, 232)       # #5DB4E8
PRIMARY_DARK = (58, 159, 219)  # #3A9FDB
PRIMARY_LIGHT = (142, 205, 244)  # #8ECDF4
DARK = (15, 23, 42)            # #0F172A
ACCENT = (245, 158, 11)        # #F59E0B
WHITE = (255, 255, 255)
SOFT = (226, 236, 245)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name + '.ttf'), size)


def asset(name):
    return Image.open(os.path.join(ASSETS, name))


def gradient(w, h, stops):
    """Diagonal gradient (top-left -> bottom-right) through colour stops."""
    small = Image.new('RGB', (64, 64))
    px = small.load()
    for y in range(64):
        for x in range(64):
            t = (x + y) / 126
            for i in range(len(stops) - 1):
                a, b = i / (len(stops) - 1), (i + 1) / (len(stops) - 1)
                if a <= t <= b:
                    f = (t - a) / (b - a)
                    c1, c2 = stops[i], stops[i + 1]
                    px[x, y] = tuple(int(c1[k] + (c2[k] - c1[k]) * f) for k in range(3))
                    break
    return small.resize((w, h), Image.BICUBIC)


def cover(im, w, h, y=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    ox = (im.width - w) // 2
    oy = int((im.height - h) * y)
    return im.crop((ox, oy, ox + w, oy + h))


def wrap(d, text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def norm(w):
    return w.strip('.,!?;:"“”\'').lower()


def draw_headline(d, x, y, lines, f, hl_words, base, hl_col, lh):
    sp = d.textlength(' ', font=f)
    for line in lines:
        cx = x
        for w in line.split():
            col = hl_col if norm(w) in hl_words else base
            d.text((cx, y), w, font=f, fill=col)
            cx += d.textlength(w, font=f) + sp
        y += lh
    return y


def pill(d, x, y, text, fill, color):
    f = font('sora-700', 26)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + tw + 44, y + 52), 26, fill=fill)
    d.text((x + 22, y + 11), text, font=f, fill=color)


def logo(im, x, y, height, white=True):
    lg = asset('logo-white.png' if white else 'logo.png').convert('RGBA')
    lg = lg.resize((int(lg.width * height / lg.height), height), Image.LANCZOS)
    im.paste(lg, (x, y), lg)


def phone(shot_h):
    """App screenshot with rounded corners and a soft shadow."""
    shot = asset('app-sample.png').convert('RGBA')
    w = int(shot.width * shot_h / shot.height)
    shot = shot.resize((w, shot_h), Image.LANCZOS)
    r = 46
    mask = Image.new('L', shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, shot_h - 1), r, fill=255)
    frame = Image.new('RGBA', (w + 24, shot_h + 24), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle((0, 0, w + 23, shot_h + 23), r + 12, fill=(15, 23, 42, 255))
    frame.paste(shot, (12, 12), mask)
    pad = 60
    out = Image.new('RGBA', (frame.width + 2 * pad, frame.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad + 10, pad + 30, pad + frame.width + 10, pad + frame.height + 30), r + 12, fill=(10, 30, 60, 110))
    out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(28)))
    out.alpha_composite(frame, (pad, pad))
    return out


def diamonds(im, cx, cy, size, alpha):
    """Faint version of the WePix icon motif (four rounded diamonds)."""
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = size
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        x, y = cx + dx * s * 0.62, cy + dy * s * 0.62
        pts = [(x, y - s / 2), (x + s / 2, y), (x, y + s / 2), (x - s / 2, y)]
        d.line(pts + [pts[0]], fill=(255, 255, 255, alpha), width=max(6, int(s / 9)), joint='curve')
    im.alpha_composite(layer)


def make(spec, out):
    layout = spec.get('layout', 'photo')
    hl_words = {norm(w) for w in spec.get('highlight', '').split()}
    kicker = spec.get('kicker', '').upper()

    if layout == 'photo':
        bg = asset(spec.get('bg', 'beach') + '.jpg').convert('RGB')
        im = cover(bg, W, H, spec.get('bg_y', 0.5)).convert('RGBA')
        ov = Image.new('RGBA', (W, H))
        od = ImageDraw.Draw(ov)
        for y in range(H):
            t = max(0.0, (y / H - 0.30) / 0.70)
            od.line((0, y, W, y), fill=DARK + (int(240 * t ** 0.85),))
        for y in range(260):  # top scrim so the logo stays legible
            od.line((0, y, W, y), fill=DARK + (int(110 * (1 - y / 260)),))
        im = Image.alpha_composite(im, ov)
        d = ImageDraw.Draw(im)
        logo(im, M, M - 6, 92)
        hf = font('sora-800', spec.get('hsize', 92))
        sf = font('dm-sans-500', 40)
        hl = wrap(d, spec['headline'], hf, W - 2 * M)
        sl = wrap(d, spec.get('sub', ''), sf, W - 2 * M) if spec.get('sub') else []
        lh, sh = int(hf.size * 1.12), int(sf.size * 1.38)
        y = H - M - len(sl) * sh - (34 if sl else 0) - len(hl) * lh
        if kicker:
            pill(d, M, y - 86, kicker, PRIMARY, WHITE)
        y = draw_headline(d, M, y, hl, hf, hl_words, WHITE, PRIMARY_LIGHT, lh) + 34
        for l in sl:
            d.text((M, y), l, font=sf, fill=SOFT)
            y += sh

    elif layout == 'phone':
        im = gradient(W, H, [PRIMARY_DARK, PRIMARY, PRIMARY_LIGHT]).convert('RGBA')
        diamonds(im, W - 120, 250, 260, 34)
        ph = phone(860)
        im.alpha_composite(ph, (W - ph.width + 70, H - ph.height + 250))
        # dark fade behind the text column for contrast
        ov = Image.new('RGBA', (W, H))
        od = ImageDraw.Draw(ov)
        for x in range(W):
            od.line((x, 0, x, H), fill=DARK + (int(120 * max(0, 1 - x / 760) ** 1.2),))
        im = Image.alpha_composite(im, ov)
        d = ImageDraw.Draw(im)
        logo(im, M, M - 6, 92)
        colw = 560
        hf = font('sora-800', spec.get('hsize', 76))
        sf = font('dm-sans-500', 36)
        hl = wrap(d, spec['headline'], hf, colw)
        sl = wrap(d, spec.get('sub', ''), sf, colw - 20) if spec.get('sub') else []
        lh, sh = int(hf.size * 1.14), int(sf.size * 1.4)
        y = 330
        if kicker:
            pill(d, M, y, kicker, WHITE, PRIMARY_DARK)
            y += 96
        y = draw_headline(d, M, y, hl, hf, hl_words, WHITE, DARK, lh) + 30
        for l in sl:
            d.text((M, y), l, font=sf, fill=WHITE)
            y += sh

    else:  # card — big question / tip on brand gradient
        im = gradient(W, H, [PRIMARY_DARK, PRIMARY, PRIMARY_LIGHT]).convert('RGBA')
        diamonds(im, W - 150, H - 230, 300, 40)
        d = ImageDraw.Draw(im)
        logo(im, M, M - 6, 92)
        hf = font('sora-800', spec.get('hsize', 104))
        sf = font('dm-sans-500', 42)
        hl = wrap(d, spec['headline'], hf, W - 2 * M)
        sl = wrap(d, spec.get('sub', ''), sf, W - 2 * M - 40) if spec.get('sub') else []
        lh, sh = int(hf.size * 1.1), int(sf.size * 1.4)
        block = (96 if kicker else 0) + len(hl) * lh + (40 + len(sl) * sh if sl else 0)
        y = max(260, (H - block) // 2)
        if kicker:
            pill(d, M, y, kicker, DARK, WHITE)
            y += 96
        y = draw_headline(d, M, y, hl, hf, hl_words, WHITE, DARK, lh) + 40
        for l in sl:
            d.text((M, y), l, font=sf, fill=WHITE)
            y += sh

    im.convert('RGB').save(out, quality=92)


if __name__ == '__main__':
    make(json.loads(sys.argv[1]), sys.argv[2])
