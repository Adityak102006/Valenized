#!/usr/bin/env python3
"""Render 5 page mockups of the VALENIZED portfolio as PNGs."""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = '/home/user/site/_previews'
os.makedirs(OUT, exist_ok=True)

W = 1200
PAD = 64
BG = (5, 5, 7)
BG2 = (10, 10, 16)
INK = (244, 243, 247)
INK_DIM = (154, 152, 168)
INK_LOW = (74, 72, 86)
LINE = (255, 255, 255, 22)
ACCENT = (168, 85, 247)
ACCENT_2 = (124, 58, 237)

fonts_dir = '/usr/share/fonts/truetype/dejavu' \
    if os.path.isdir('/usr/share/fonts/truetype/dejavu') \
    else '/usr/share/fonts/truetype'
serif_bold = os.path.join(fonts_dir, 'DejaVuSerif-Bold.ttf')
serif = os.path.join(fonts_dir, 'DejaVuSerif.ttf')
serif_it = os.path.join(fonts_dir, 'DejaVuSerif-Italic.ttf')
sans = os.path.join(fonts_dir, 'DejaVuSans.ttf')
sans_bold = os.path.join(fonts_dir, 'DejaVuSans-Bold.ttf')

def f(size, path=sans):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def mono(s):
    # best mono available on system
    for name in ['DejaVuSansMono-Bold.ttf', 'DejaVuSansMono.ttf']:
        p = os.path.join(fonts_dir, name)
        if os.path.exists(p): return p
    return sans

def F(size, kind='sans', w=400):
    if kind == 'serif':    return f(size, serif)
    if kind == 'serif_i':  return f(size, serif_it)
    if kind == 'serif_b':  return f(size, serif_bold)
    if kind == 'bold':     return f(size, sans_bold)
    if kind == 'mono':     return f(size, mono(size))

def text_w(draw, s, font):
    b = draw.textbbox((0,0), s, font=font)
    return b[2] - b[0]

# ─────────────────────────────────────────
# Common primitives
# ─────────────────────────────────────────
def chrome_orb(draw, cx, cy, r):
    # outer purple ring
    for i in range(8, 0, -1):
        a = int(8 * i / 8)
        draw.ellipse((cx-r-i*3, cy-r-i*3, cx+r+i*3, cy+r+i*3),
                     outline=(*ACCENT, int(255 * 0.05 * a/8)))
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(26, 26, 34))
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=ACCENT)
    # inner highlight (concentric)
    steps = 30
    for j in range(steps, 0, -1):
        inset = r - (j * r // steps)
        if inset <= 0: continue
        alpha = int(255 * 0.30 * (1 - j/steps))
        draw.ellipse((cx-inset, cy-inset, cx+inset, cy+inset),
                     outline=(*ACCENT, alpha), width=2)

def draw_nav(draw, y=0, active='Index'):
    draw.rectangle((0, y, W, y+64), fill=(*BG, 230))
    draw.line((PAD, y+64, W-PAD, y+64), fill=(ACCENT[0], ACCENT[1], ACCENT[2], 60))
    draw.text((PAD, y+22), 'VALENIZED', font=F(20, 'serif_i'), fill=INK)
    # dot
    bbox = draw.textbbox((PAD, y+22), 'VALENIZED', font=F(20, 'serif_i'))
    draw.ellipse((bbox[2]+2, bbox[3]-6, bbox[2]+8, bbox[3]), fill=ACCENT)
    items = ['Index', 'About', 'Works', 'Contact', 'Terms']
    x = 700
    for nm in items:
        col = ACCENT if nm == active else INK_DIM
        draw.text((x, y+24), nm.upper(), font=F(10, 'mono', 700), fill=col)
        w = text_w(draw, nm.upper(), F(10, 'mono', 700))
        if nm == active:
            draw.line((x, y+48, x+w, y+48), fill=ACCENT, width=1)
        x += w + 32

def draw_footer(draw, y):
    h = 250
    draw.rectangle((0, y, W, y+h), fill=BG2)
    draw.line((PAD, y, W-PAD, y), fill=(255,255,255,30))

    draw.text((PAD, y+30), '— STUDIO', font=F(10, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, y+58), 'Valenized', font=F(58, 'serif_i'), fill=INK)
    draw.ellipse((PAD+250, y+90, PAD+260, y+100), fill=ACCENT)
    draw.text((PAD, y+136), 'Lorem ipsum dolor sit amet, consectetur',
              font=F(13, 'sans'), fill=INK_DIM)
    draw.text((PAD, y+154), 'adipiscing elit. Sed do eiusmod tempor.',
              font=F(13, 'sans'), fill=INK_DIM)

    draw.text((720, y+30), '— NAVIGATE', font=F(10, 'mono', 700), fill=INK_DIM)
    for i, lab in enumerate(['Index','About','Works','Contact','Terms']):
        draw.text((720, y+58 + i*22), lab, font=F(14, 'sans'), fill=(*INK, 180))

    draw.text((960, y+30), '— CONTACT', font=F(10, 'mono', 700), fill=INK_DIM)
    for i, lab in enumerate(['inquire@valenized.com', '@valenized.studio', 'are.na/valenized']):
        draw.text((960, y+58 + i*22), lab, font=F(13, 'sans'), fill=(*INK, 180))

    draw.line((PAD, y+200, W-PAD, y+200), fill=(255,255,255,30))
    draw.text((PAD, y+225), '© 2026 VALENIZED STUDIO — ALL RIGHTS RESERVED.',
              font=F(10, 'mono', 700), fill=INK_DIM)
    draw.text((W-PAD, y+225), 'DESIGNED IN-HOUSE · TERMS', font=F(10, 'mono', 700),
              fill=INK_DIM, anchor='rt')
    return y + h

# ─────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────
def render_home():
    H = 4200
    img = Image.new('RGB', (W, H), BG)
    # subtle purple blob
    img.paste((168, 85, 247, 18), (W//2-200, 0, W//2+200, H//2), mask=Image.new('L',(400,H//2),0))
    draw = ImageDraw.Draw(img, 'RGBA')

    draw_nav(draw, active='Index')

    # eyebrow
    draw.text((PAD, 170), '— LOREM IPSUM DOLOR SIT', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((W-PAD, 170), '21:48:02', font=F(11, 'mono', 700), fill=ACCENT, anchor='rt')

    # title - large italic
    y_title = 320
    draw.text((PAD, y_title),     'Lorem ipsum',       font=F(120, 'serif_i'), fill=INK)
    draw.text((PAD, y_title+135), 'dolor sit amet,',   font=F(120, 'serif_i'), fill=INK)
    # accent on "dolor"
    bbox = draw.textbbox((PAD, y_title+135), 'dolor sit amet,', font=F(120, 'serif_i'))
    draw.text((PAD, y_title+135), 'dolor', font=F(120, 'serif_i'), fill=ACCENT)
    # outline "consectetur"
    draw.text((PAD, y_title+270), 'consectetur.',
              font=F(120, 'serif_i'), fill=None)
    for ox in range(-2,3):
        for oy in range(-2,3):
            if ox or oy:
                w_ = text_w(draw, 'consectetur.', F(120, 'serif_i'))
                draw.text((PAD+ox, y_title+270+oy), 'consectetur.',
                          font=F(120, 'serif_i'), fill=INK)

    # chrome orb (right side)
    chrome_orb(draw, W-220, 480, 160)

    # meta block right-bottom
    draw.text((W-PAD, 880), 'N° LOREM / IPSUM', font=F(10, 'mono', 700), fill=INK_DIM, anchor='rt')
    draw.text((W-PAD, 904), 'FILED · [ LOREM · IPSUM · DOLOR ]', font=F(10, 'mono', 700), fill=INK_DIM, anchor='rt')
    draw.text((W-PAD, 928), 'SCROLL ↓', font=F(10, 'mono', 700), fill=INK_DIM, anchor='rt')

    # CTAs
    draw.rounded_rectangle((PAD, 980, PAD+200, 1024), radius=22, outline=INK_DIM)
    draw.text((PAD+100, 1003), 'VIEW WORKS →', font=F(11, 'mono', 700), fill=INK, anchor='mm')
    draw.rounded_rectangle((PAD+220, 980, PAD+440, 1024), radius=22, fill=ACCENT)
    draw.text((PAD+330, 1003), 'START A PROJECT →', font=F(11, 'mono', 700), fill=INK, anchor='mm')

    # ─── MARQUEE ───
    my = 1140
    draw.line((0, my, W, my), fill=(255,255,255,30))
    draw.text((30, my+50), '  Lorem  ✦  Ipsum  ✦  Dolor  ✦  Sit  ✦  Amet  ✦  Lorem  ✦',
              font=F(58, 'serif_i'), fill=None)
    for ox in range(-1,2):
        for oy in range(-1,2):
            if ox or oy:
                draw.text((30+ox, my+50+oy),
                          '  Lorem  ✦  Ipsum  ✦  Dolor  ✦  Sit  ✦  Amet  ✦  Lorem  ✦',
                          font=F(58, 'serif_i'), fill=INK)
    draw.line((0, my+180, W, my+180), fill=(255,255,255,30))

    # ─── INTRO ───
    iy = 1380
    draw.text((PAD, iy), '— MANIFESTO, LOREM', font=F(11, 'mono', 700), fill=ACCENT)
    draw.text((PAD, iy+50),  'Lorem ipsum,',    font=F(64, 'serif_i'), fill=INK)
    draw.text((PAD, iy+120), 'dolor sit amet.',  font=F(64, 'serif_i'), fill=INK)
    # accent on italic parts
    draw.text((PAD+260, iy+50),  'ipsum,',    font=F(64, 'serif_i'), fill=ACCENT)
    draw.text((PAD+150, iy+120), 'sit amet.', font=F(64, 'serif_i'), fill=ACCENT)

    # right side
    rx = 720
    for i, (line, dim) in enumerate([
        ('Lorem ipsum dolor sit amet,', False),
        ('consectetur adipiscing elit.', False),
        ('Sed do eiusmod tempor incididunt.', True),
        ('Duis aute irure dolor in reprehenderit', True),
        ('in voluptate velit esse cillum dolore.', True),
        ('Excepteur sint occaecat cupidatat.', True)
    ]):
        col = INK if not dim else INK_DIM
        draw.text((rx, iy+30+i*30), line, font=F(17, 'sans'), fill=col)

    # stats
    sy = iy + 280
    draw.line((rx, sy-20, rx+420, sy-20), fill=(255,255,255,30))
    for i, (n, l) in enumerate([('24+','LOREM IPSUM'), ('06','DOLOR SIT'), ('07','AMET CONSECT')]):
        draw.text((rx+i*150, sy+20),  n, font=F(48, 'serif_i'), fill=ACCENT)
        draw.text((rx+i*150, sy+58),  l, font=F(9, 'mono', 700), fill=INK_DIM)

    # ─── SERVICES ───
    sy0 = 1860
    draw.text((PAD, sy0), '— DISCIPLINES', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, sy0+50), 'What I', font=F(64, 'serif_i'), fill=INK)
    draw.text((PAD, sy0+118), 'craft.', font=F(64, 'serif_i'), fill=ACCENT)

    # 3 cards
    cw, gap = 380, 20
    cy1 = sy0 + 200
    for i, (n, t, desc) in enumerate([
        ('01', 'Illustration',
         'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod.'),
        ('02', '3D + Motion',
         'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.'),
        ('03', 'Apparel',
         'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.'),
    ]):
        x = PAD + i*(cw+gap)
        # glass card
        draw.rounded_rectangle((x, cy1, x+cw, cy1+280), radius=20,
                               fill=(*INK, 8), outline=(255,255,255,40))
        # icon tile
        draw.rounded_rectangle((x+20, cy1+20, x+72, cy1+72), radius=14, fill=ACCENT)
        draw.text((x+46, cy1+47), n, font=F(22, 'serif_i'), fill=INK, anchor='mm')
        # title
        draw.text((x+20, cy1+120), t, font=F(32, 'serif_i'), fill=INK)
        # desc
        draw.text((x+20, cy1+155), desc.split(',')[0]+',', font=F(14, 'sans'), fill=INK_DIM)
        if ',' in desc:
            draw.text((x+20, cy1+178), ','.join(desc.split(',')[1:]).strip(),
                      font=F(14, 'sans'), fill=INK_DIM)
        # tags
        for j, tg in enumerate(['LOREM','IPSUM','DOLOR']):
            tw = text_w(draw, tg, F(9, 'mono', 700))
            tx = x+20+j*(tw+16)
            draw.rounded_rectangle((tx, cy1+240, tx+tw+12, cy1+260), radius=10,
                                   outline=(255,255,255,40))
            draw.text((tx+6, cy1+251), tg, font=F(9, 'mono', 700), fill=INK_DIM)

    # ─── GALLERY ───
    gy = 2400
    draw.text((PAD, gy),  '— SELECTED PIECES', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, gy+50),  'From the archive.',  font=F(56, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, gy+50), 'From the archive.', font=F(56, 'serif_i'))
    draw.text((PAD+185, gy+50), 'archive.', font=F(56, 'serif_i'), fill=ACCENT)

    # all-works btn
    draw.rounded_rectangle((W-PAD-180, gy+30, W-PAD, gy+74), radius=22, outline=(255,255,255,60))
    draw.text((W-PAD-90, gy+52), 'ALL WORKS →', font=F(11, 'mono', 700), fill=INK, anchor='mm')

    # tiles — placeholder boxes
    # row 1: big tile (12 col)
    tr = 140
    gx, gy1 = PAD, gy + tr
    draw.rounded_rectangle((gx, gy1, W-PAD, gy1+260), radius=18,
                           fill=(15,15,22), outline=(255,255,255,40))
    draw.text(((gx+W-PAD)//2, gy1+130), '[ chrome sculpture — 1920×1350 image ]',
              font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')
    draw.text((gx+20, gy1+230), 'Lorem Ipsum №01', font=F(20, 'serif_i'), fill=INK)
    draw.text((W-PAD-20, gy1+30), '/01', font=F(10, 'mono', 700), fill=ACCENT, anchor='rt')

    # row 2: 2 medium tiles
    th = 280
    tlx = gx
    tw2 = (W - PAD - PAD - 16) // 2
    draw.rounded_rectangle((tlx, gy1+280, tlx+tw2, gy1+280+th), radius=18,
                           fill=(15,15,22), outline=(255,255,255,40))
    draw.text((tlx+tw2//2, gy1+410), '[ samurai image ]',
              font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')
    draw.text((tlx+20, gy1+530), 'Dolor Sit Amet', font=F(20, 'serif_i'), fill=INK)
    draw.text((tlx+tw2-20, gy1+310), '/02', font=F(10, 'mono', 700), fill=ACCENT, anchor='rt')

    tlx2 = tlx + tw2 + 16
    draw.rounded_rectangle((tlx2, gy1+280, tlx2+tw2, gy1+280+th), radius=18,
                           fill=(15,15,22), outline=(255,255,255,40))
    draw.text((tlx2+tw2//2, gy1+410), '[ miku header image ]',
              font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')
    draw.text((tlx2+20, gy1+530), 'Consectetur / 39', font=F(20, 'serif_i'), fill=INK)
    draw.text((tlx2+tw2-20, gy1+310), '/03', font=F(10, 'mono', 700), fill=ACCENT, anchor='rt')

    # row 3: 8 + 4 split
    thb = 300
    tw4 = (W - PAD - PAD - 16) * 4 // 12 * 2
    tw8 = (W - PAD - PAD - 16) - tw4 - 16
    yy = gy1 + 280 + th + 16
    draw.rounded_rectangle((gx, yy, gx+tw8, yy+thb), radius=18,
                           fill=(15,15,22), outline=(255,255,255,40))
    draw.text((gx+tw8//2, yy+150), '[ tribal tee image ]',
              font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')
    draw.text((gx+20, yy+270), 'Adipiscing — Series 08', font=F(20, 'serif_i'), fill=INK)
    draw.text((gx+tw8-20, yy+30), '/04', font=F(10, 'mono', 700), fill=ACCENT, anchor='rt')
    draw.rounded_rectangle((gx+tw8+16, yy, gx+tw8+16+tw4, yy+thb), radius=18,
                           fill=(15,15,22), outline=(255,255,255,40))
    draw.text((gx+tw8+16+tw4//2, yy+150), '[ silver sculpt ]',
              font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')
    draw.text((gx+tw8+36, yy+270), 'Elit Tempor', font=F(20, 'serif_i'), fill=INK)
    draw.text((gx+tw8+16+tw4-20, yy+30), '/05', font=F(10, 'mono', 700), fill=ACCENT, anchor='rt')

    # ─── CTA STRIP ───
    csy = yy + thb + 80
    draw.line((0, csy-30, W, csy-30), fill=(255,255,255,30))
    draw.text((W//2, csy), '— LOREM IPSUM?', font=F(10, 'mono', 700), fill=INK_DIM, anchor='mm')
    draw.text((W//2, csy+50),  'let\'s make', font=F(58, 'serif_i'), fill=INK, anchor='mm')
    draw.text((W//2, csy+115), 'lorem ipsum.', font=F(58, 'serif_i'), fill=ACCENT, anchor='mm')

    # btns centered
    bw = 250
    cx0 = W//2 - bw - 12
    draw.rounded_rectangle((cx0, csy+170, cx0+bw, csy+220), radius=25, fill=ACCENT)
    draw.text((cx0+bw//2, csy+195), 'START A PROJECT →', font=F(11, 'mono', 700), fill=INK, anchor='mm')
    cx1 = W//2 + 12
    draw.rounded_rectangle((cx1, csy+170, cx1+bw, csy+220), radius=25, outline=(255,255,255,80))
    draw.text((cx1+bw//2, csy+195), 'EMAIL DIRECTLY →',  font=F(11, 'mono', 700), fill=INK, anchor='mm')

    # footer
    draw_footer(draw, csy + 280)

    # Crop off anything unused
    content_end = csy + 280 + 250
    img = img.crop((0, 0, W, content_end))
    img.save(f'{OUT}/home.png')
    print(f'→ home.png  ({img.size[0]}×{img.size[1]})')


# ─────────────────────────────────────────
# ABOUT PAGE
# ─────────────────────────────────────────
def render_about():
    H = 3800
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img, 'RGBA')
    draw_nav(draw, active='About')

    y0 = 200
    # Left text
    draw.text((PAD, y0+10), '— ABOUT', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, y0+90), 'Lorem ipsum', font=F(80, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, y0+90), 'Lorem ipsum', font=F(80, 'serif_i'))
    draw.text((bbox[2]+12, y0+90), 'dolor', font=F(80, 'serif_i'), fill=ACCENT)
    draw.text((PAD, y0+180), 'sit amet consectetur adipiscing elit.',
              font=F(80, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, y0+180), 'sit amet consectetur adipiscing elit.',
                          font=F(80, 'serif_i'))
    draw.text((bbox[2]+12, y0+180), 'adipiscing', font=F(80, 'serif_i'), fill=ACCENT)

    # paragraphs
    py = y0 + 320
    for line, dim in [
        ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod',
         False),
        ('tempor incididunt ut labore et dolore magna aliqua.', False),
        ('', False),
        ('Duis aute irure dolor in reprehenderit in voluptate velit esse cillum',
         True),
        ('dolore eu fugiat nulla pariatur excepteur sint.', True),
        ('', True),
        ('Sed ut perspiciatis unde omnis iste natus error sit voluptatem',
         True),
    ]:
        col = INK if not dim else INK_DIM
        draw.text((PAD, py), line, font=F(17, 'sans'), fill=col)
        py += 30

    # btns
    py += 20
    draw.rounded_rectangle((PAD, py, PAD+200, py+44), radius=22, outline=INK_DIM)
    draw.text((PAD+100, py+22), 'WORK WITH ME →', font=F(11, 'mono', 700), fill=INK, anchor='mm')
    draw.rounded_rectangle((PAD+220, py, PAD+420, py+44), radius=22, outline=INK_DIM)
    draw.text((PAD+320, py+22), 'SEE THE ARCHIVE →', font=F(11, 'mono', 700), fill=INK, anchor='mm')

    # Right image (placeholder)
    rx = W//2 + 30
    rw = W - rx - PAD
    ry = 280
    rh = 600
    draw.rounded_rectangle((rx, ry, rx+rw, ry+rh), radius=20,
                           fill=(15,15,22), outline=(255,255,255,40))
    draw.text((rx+rw//2, ry+rh//2), '[ samurai portrait ]',
              font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')

    # gradient overlay bottom-left
    for i in range(80):
        a = int(60 * (1 - i/80))
        draw.ellipse((rx+i, ry+rh-160+i, rx+rw-i, ry+rh+i),
                     outline=(*ACCENT, int(a/4)))
    # badge
    draw.rounded_rectangle((rx+24, ry+rh-90, rx+260, ry+rh-30), radius=14,
                           fill=(*BG2, 220), outline=(255,255,255,40))
    draw.text((rx+38, ry+rh-72), 'STUDIO ACTIVE', font=F(9, 'mono', 700), fill=INK_DIM)
    draw.text((rx+38, ry+rh-50), 'Lorem', font=F(22, 'serif_i'), fill=ACCENT)

    # ─── TOOLKIT ───
    ty = 1080
    draw.line((0, ty-60, W, ty-60), fill=(255,255,255,30))
    draw.text((PAD, ty), '— TOOLKIT',   font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, ty+50),  'Pillars of',  font=F(56, 'serif_i'), fill=INK)
    draw.text((PAD, ty+115), 'practice.',   font=F(56, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, ty+115), 'practice.', font=F(56, 'serif_i'))
    draw.text((bbox[2]+12, ty+115), 'practice', font=F(56, 'serif_i'), fill=ACCENT)

    skill_y = ty + 200
    sw, sgap = 260, 16
    for i, (n, name, items) in enumerate([
        ('/01 — IMAGE', 'Illustration', ['Photoshop','Procreate','CSP','Krita']),
        ('/02 — VOLUME','3D & Motion',  ['Blender','Houdini','After FX','C4D']),
        ('/03 — SURFACE','Apparel',     ['Illustrator','Screen prints','Airbrush','DTG']),
        ('/04 — CODE',  'Web',          ['HTML/CSS/JS','WebGL/Three','GSAP','Spline']),
    ]):
        x = PAD + i*(sw+sgap)
        draw.rounded_rectangle((x, skill_y, x+sw, skill_y+280), radius=18,
                               fill=(*INK, 8), outline=(255,255,255,40))
        draw.text((x+20, skill_y+20), n, font=F(9, 'mono', 700), fill=ACCENT)
        draw.text((x+20, skill_y+50), name, font=F(24, 'serif_i'), fill=INK)
        for j, it in enumerate(items):
            draw.text((x+20, skill_y+100+j*36), it, font=F(13, 'mono'), fill=INK_DIM)
            if j < 3:
                draw.line((x+20, skill_y+125+j*36, x+sw-20, skill_y+125+j*36),
                          fill=(255,255,255,20))

    # ─── TIMELINE ───
    tl_y = skill_y + 360
    draw.rectangle((0, tl_y-60, W, H-PAD-260), fill=BG2)
    draw.text((PAD, tl_y), '— TIMELINE', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, tl_y+50),  'A short walk backwards.', font=F(56, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, tl_y+50), 'A short walk', font=F(56, 'serif_i'))
    draw.text((bbox[2]+12, tl_y+50), 'backwards.', font=F(56, 'serif_i'), fill=ACCENT)

    # timeline rail
    rx_t = PAD + 40
    draw.line((rx_t, tl_y+140, rx_t, tl_y+560), fill=ACCENT)
    items = [
        ('2025 — Present',     'Independent · Studio',
         'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod.'),
        ('2022 — 2025',        'Senior Designer · Bureau',
         'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.'),
        ('2019 — 2022',        'Junior Artist · Atelier',
         'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui.'),
        ('2018',               'First commissioned piece',
         'Lorem ipsum dolor sit amet, consectetur adipiscing elit, printed.'),
    ]
    for i, (yr, h, d) in enumerate(items):
        yy = tl_y+160+i*120
        draw.ellipse((rx_t-7, yy-8, rx_t+7, yy+8), fill=ACCENT)
        draw.ellipse((rx_t-15, yy-15, rx_t+15, yy+15), outline=(*ACCENT, 60))
        draw.text((rx_t+30, yy-10), yr, font=F(11, 'mono', 700), fill=ACCENT)
        draw.text((rx_t+30, yy+10), h, font=F(22, 'serif_i'), fill=INK)
        draw.text((rx_t+30, yy+40), d, font=F(14, 'sans'), fill=INK_DIM)

    # CTA
    cy = tl_y + 730
    draw.text((W//2, cy), 'enjoyed the lorem?', font=F(36, 'serif_i'), fill=INK, anchor='mm')
    draw.text((W//2, cy+45), 'say hello', font=F(36, 'serif_i'), fill=ACCENT, anchor='mm')
    bx = W//2-100
    draw.rounded_rectangle((bx, cy+90, bx+200, cy+134), radius=22, fill=ACCENT)
    draw.text((bx+100, cy+112), 'SEND A BRIEF →', font=F(10, 'mono', 700), fill=INK, anchor='mm')

    draw_footer(draw, cy + 180)
    img = img.crop((0, 0, W, cy + 180 + 250))
    img.save(f'{OUT}/about.png')
    print(f'→ about.png  ({img.size[0]}×{img.size[1]})')


# ─────────────────────────────────────────
# WORKS PAGE
# ─────────────────────────────────────────
def render_works():
    H = 4400
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img, 'RGBA')
    draw_nav(draw, active='Works')

    # page header
    ph = 350
    y0 = 100
    draw.text((PAD, y0), '— THE ARCHIVE', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, y0+60),  'Selected', font=F(100, 'serif_i'), fill=INK)
    draw.text((PAD, y0+160), 'works,', font=F(100, 'serif_i'), fill=INK)
    draw.text((PAD, y0+260), 'Lorem ipsum.', font=F(100, 'serif_i'), fill=INK)
    # accent dot
    bbox = draw.textbbox((PAD+330, y0+160), 'works,', font=F(100, 'serif_i'))
    draw.ellipse((bbox[2]+4, bbox[3]-50, bbox[2]+18, bbox[3]-36), fill=ACCENT)
    bbox = draw.textbbox((PAD+650, y0+260), 'Lorem ipsum.', font=F(100, 'serif_i'))
    draw.ellipse((bbox[2]+4, bbox[3]-50, bbox[2]+18, bbox[3]-36), fill=ACCENT)

    # right meta
    mx = W - PAD - 200
    for i, lab in enumerate(['TOTAL WORKS · 07', 'LAST UPDATED · AUG 2026', 'DISCIPLINES · 04']):
        draw.text((mx, y0+60+i*30), lab, font=F(10, 'mono', 700), fill=INK_DIM)

    # filter bar
    fy = ph + 70
    draw.line((0, fy, W, fy), fill=(255,255,255,30))
    draw.line((0, fy+70, W, fy+70), fill=(255,255,255,30))
    chips = ['ALL · 07', 'MOTION · 02', '3D · 03', 'ILLUSTRATION · 02',
             'APPAREL · 01', 'EDITORIAL · 02', 'PHOTOGRAPHY · 01']
    cx = PAD
    for i, ch in enumerate(chips):
        w = text_w(draw, ch, F(10, 'mono', 700)) + 24
        if i == 0:
            draw.rounded_rectangle((cx, fy+15, cx+w, fy+55), radius=20, fill=ACCENT)
            draw.text((cx+w//2, fy+35), ch, font=F(10, 'mono', 700), fill=INK, anchor='mm')
        else:
            draw.rounded_rectangle((cx, fy+15, cx+w, fy+55), radius=20,
                                   outline=(255,255,255,30))
            draw.text((cx+w//2, fy+35), ch, font=F(10, 'mono', 700), fill=INK_DIM, anchor='mm')
        cx += w + 8

    # 7 tiles masonry - simpler arrangement
    tx0 = PAD
    ty0 = fy + 110
    tw = (W - PAD*2 - 12) // 2

    positions = [
        (tx0,         ty0,           W-PAD-tx0, 380, 'CHROME SCULPTURE', 'Lorem Ipsum №01', '/01'),
        (tx0,         ty0+400,       tw,         380, 'SILVER SCULPTURE', 'Dolor Sit Amet',  '/02'),
        (tx0+tw+12,   ty0+400,       tw,         380, 'BLUE ABSTRACT',    'Consectetur Elit','/03'),
        (tx0,         ty0+800,       tw,         380, 'SAMURAI',          'Sed Tempor',      '/04'),
        (tx0+tw+12,   ty0+800,       tw,         380, 'MIKU HEADER',      'Magna Labore/39', '/05'),
        (tx0,         ty0+1200,      tw,         380, 'OCEAN',            'Ut Enim Minim',   '/06'),
        (tx0+tw+12,   ty0+1200,      W-PAD-tx0-tw-12, 380, 'TRIBAL TEE',      'Veniam Quis',  '/07'),
    ]
    for (x, y, w, h, ph, ti, idx) in positions:
        draw.rounded_rectangle((x, y, x+w, y+h), radius=18,
                               fill=(15,15,22), outline=(255,255,255,40))
        draw.text((x+w//2, y+h//2), f'[ {ph} ]',
                  font=F(11, 'mono', 700), fill=INK_LOW, anchor='mm')
        draw.text((x+20, y+h-32), ti, font=F(20, 'serif_i'), fill=INK)
        draw.text((x+w-20, y+30), idx, font=F(11, 'mono', 700), fill=ACCENT, anchor='rt')

    # bottom marquee
    my = ty0 + 1700
    draw.line((0, my, W, my), fill=(255,255,255,30))
    draw.text((30, my+60), '  Lorem  ✦  Ipsum  ✦  Dolor  ✦  Sit  ✦  Amet  ✦  Lorem  ✦',
              font=F(54, 'serif_i'), fill=None)
    for ox in range(-1,2):
        for oy in range(-1,2):
            if ox or oy:
                draw.text((30+ox, my+60+oy),
                          '  Lorem  ✦  Ipsum  ✦  Dolor  ✦  Sit  ✦  Amet  ✦  Lorem  ✦',
                          font=F(54, 'serif_i'), fill=INK)
    draw.line((0, my+170, W, my+170), fill=(255,255,255,30))

    draw_footer(draw, my + 220)
    img = img.crop((0, 0, W, my + 220 + 250))
    img.save(f'{OUT}/works.png')
    print(f'→ works.png  ({img.size[0]}×{img.size[1]})')


# ─────────────────────────────────────────
# CONTACT PAGE
# ─────────────────────────────────────────
def render_contact():
    H = 3200
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img, 'RGBA')
    draw_nav(draw, active='Contact')

    # header
    yh = 100
    draw.text((PAD, yh), '— SAY HELLO', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, yh+60),  'Start a brief', font=F(100, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, yh+60), 'Start a brief', font=F(100, 'serif_i'))
    draw.ellipse((bbox[2]+6, bbox[3]-50, bbox[2]+22, bbox[3]-36), fill=ACCENT)
    # right meta
    for i, lab in enumerate(['RESPONSE · LOREM IPSUM', 'STATUS · LOREM SIT']):
        draw.text((W-PAD-200, yh+60+i*30), lab, font=F(10, 'mono', 700), fill=INK_DIM)

    # left: 4 info cards stacked
    ix = PAD
    iy0 = yh + 280
    iw = 340
    ih = 100
    gap = 16
    info = [
        ('EMAIL', 'inquire@valenized.com'),
        ('DIRECT', '@valenized.studio'),
        ('BASED',  'Remote / Lorem'),
        ('HOURS',  'Lorem ipsum'),
    ]
    for i, (lbl, val) in enumerate(info):
        y = iy0 + i*(ih+gap)
        # glass
        draw.rounded_rectangle((ix, y, ix+iw, y+ih), radius=18,
                               fill=(*INK, 8), outline=(255,255,255,30))
        # icon
        draw.rounded_rectangle((ix+20, y+20, ix+68, y+68), radius=12,
                               fill=(*ACCENT, 28), outline=ACCENT)
        draw.text((ix+44, y+44), '✉', font=F(22), fill=ACCENT, anchor='mm')
        draw.text((ix+88, y+30), lbl, font=F(9, 'mono', 700), fill=INK_DIM)
        draw.text((ix+88, y+52), val, font=F(18, 'serif_i'), fill=INK)

    # urgent note
    uny = iy0 + 4*(ih+gap)
    draw.rounded_rectangle((ix, uny, ix+iw, uny+120), radius=18,
                           fill=(*INK, 8), outline=(255,255,255,30))
    draw.text((ix+20, uny+22), '— FOR LOREM', font=F(9, 'mono', 700), fill=ACCENT)
    desc = 'Add [URGENT] to your subject'
    draw.text((ix+20, uny+52), 'line. Lorem ipsum dolor sit amet,',
              font=F(14, 'sans'), fill=INK_DIM)
    draw.text((ix+20, uny+72), 'consectetur adipiscing elit.',
              font=F(14, 'sans'), fill=INK_DIM)

    # right: glass form
    fx, fy = PAD + iw + 50, iy0
    fw = W - PAD - fx
    fh = 720
    draw.rounded_rectangle((fx, fy, fx+fw, fy+fh), radius=22,
                           fill=(*INK, 8), outline=(255,255,255,40))
    # subtle glow top-right
    for r in range(20, 0, -1):
        draw.ellipse((fx+fw-r*4, fy-r*4, fx+fw+r*4, fy+r*4),
                     outline=(*ACCENT, int(8 * (20-r)/20)))

    row_y = fy + 30
    # row 1: Name | Company
    ff_w = (fw - 60) // 2
    for j, (l, v) in enumerate([('NAME', 'Your name'),
                                 ('COMPANY / PROJECT', 'Optional')]):
        x0 = fx + 20 + j*(ff_w + 20)
        draw.text((x0, row_y), l, font=F(9, 'mono', 700), fill=INK_DIM)
        draw.rounded_rectangle((x0, row_y+24, x0+ff_w, row_y+76),
                               radius=12, fill=(255,255,255,12),
                               outline=(255,255,255,40))
        draw.text((x0+15, row_y+56), v, font=F(15, 'sans'), fill=INK_DIM)

    row_y = fy + 130
    for j, (l, v) in enumerate([('EMAIL', 'hello@example.com'),
                                 ('DISCIPLINE', 'Illustration ▾')]):
        x0 = fx + 20 + j*(ff_w + 20)
        draw.text((x0, row_y), l, font=F(9, 'mono', 700), fill=INK_DIM)
        draw.rounded_rectangle((x0, row_y+24, x0+ff_w, row_y+76),
                               radius=12, fill=(255,255,255,12),
                               outline=(255,255,255,40))
        draw.text((x0+15, row_y+56), v, font=F(15, 'sans'), fill=INK_DIM)

    # budget pills
    draw.text((fx+20, row_y+110), 'BUDGET RANGE',
              font=F(9, 'mono', 700), fill=INK_DIM)
    by = row_y + 132
    cx = fx + 20
    pills = ['< $1K', '$1-5K', '$5-15K', '$15-50K', '$50K+']
    for i, p in enumerate(pills):
        w = text_w(draw, p, F(9, 'mono', 700)) + 24
        if i == 2:  # selected
            draw.rounded_rectangle((cx, by, cx+w, by+28), radius=14, fill=ACCENT)
            draw.text((cx+w//2, by+14), p, font=F(9, 'mono', 700), fill=INK, anchor='mm')
        else:
            draw.rounded_rectangle((cx, by, cx+w, by+28), radius=14,
                                   outline=(255,255,255,40))
            draw.text((cx+w//2, by+14), p, font=F(9, 'mono', 700), fill=INK_DIM, anchor='mm')
        cx += w + 8

    # brief
    draw.text((fx+20, by+60), 'THE BRIEF',
              font=F(9, 'mono', 700), fill=INK_DIM)
    draw.rounded_rectangle((fx+20, by+80, fx+fw-20, by+220),
                            radius=12, fill=(255,255,255,12),
                            outline=(255,255,255,40))
    draw.text((fx+35, by+105), 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Tell me about the work.',
              font=F(15, 'sans'), fill=INK_DIM)

    # submit
    sx, sw_ = fx + 20, fw - 40
    draw.rounded_rectangle((sx, by+250, sx+sw_, by+302), radius=22, fill=ACCENT)
    draw.text((sx+sw_//2, by+276), 'SEND INQUIRY →',
              font=F(11, 'mono', 700), fill=INK, anchor='mm')

    draw_footer(draw, fy + fh + 60)
    img = img.crop((0, 0, W, fy + fh + 60 + 250))
    img.save(f'{OUT}/contact.png')
    print(f'→ contact.png  ({img.size[0]}×{img.size[1]})')


# ─────────────────────────────────────────
# TERMS PAGE
# ─────────────────────────────────────────
def render_terms():
    H = 5200
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img, 'RGBA')
    draw_nav(draw, active='Terms')

    # header
    yh = 100
    draw.text((PAD, yh), '— LEGAL', font=F(11, 'mono', 700), fill=INK_DIM)
    draw.text((PAD, yh+60),  'Terms of', font=F(100, 'serif_i'), fill=INK)
    draw.text((PAD, yh+160), 'service.', font=F(100, 'serif_i'), fill=INK)
    bbox = draw.textbbox((PAD, yh+160), 'service.', font=F(100, 'serif_i'))
    draw.ellipse((bbox[2]+4, bbox[3]-50, bbox[2]+18, bbox[3]-36), fill=ACCENT)

    # right meta
    for i, lab in enumerate(['VERSION · v1.0', 'UPDATED · AUG 2026']):
        draw.text((W-PAD-200, yh+60+i*30), lab, font=F(10, 'mono', 700), fill=INK_DIM)

    # sticky TOC (left)
    tx = PAD
    ty = yh + 320
    tw_ = 240
    draw.text((tx, ty), '— CONTENTS', font=F(10, 'mono', 700), fill=INK_DIM)
    sections = ['Acceptance','Scope','Fees','Timeline','IP',
                'Cancellation','Liability','Confidentiality',
                'Governing law','Contact']
    for i, s in enumerate(sections):
        y = ty + 40 + i*36
        idx = f'{i+1:02d}'
        active = i == 0
        col = ACCENT if active else INK_DIM
        draw.text((tx, y), idx, font=F(11, 'mono', 700), fill=col)
        draw.text((tx+30, y), s, font=F(13, 'sans'),
                  fill=INK if active else INK)
        draw.line((tx, y+24, tx+tw_, y+24), fill=(255,255,255,20))

    # right: legal doc
    dx_ = tx + tw_ + 60
    draw.text((dx_, ty), '— LAST UPDATED · 21.08.2026 · EFFECTIVE IMMEDIATELY',
              font=F(9, 'mono', 700), fill=ACCENT)

    ty2 = ty + 60
    sections_data = [
        ('01. Acceptance',
         ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor',
          'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.',
          'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.']),
        ('02. Scope of work',
         ['Lorem ipsum dolor sit amet, consectetur adipiscing elit — anything not in',
          'the brief is not assumed to be included.',
          'Ut enim ad minim veniam, quis nostrud exercitation.']),
        ('03. Fees & payment',
         ['Lorem ipsum dolor sit amet, consectetur:',
          '— 50% deposit, lorem ipsum dolor sit amet',
          '— 50% balance, sed do eiusmod tempor',
          'Duis aute irure dolor in reprehenderit.']),
        ('04. Timeline & revisions',
         ['Lorem ipsum dolor sit amet — timelines begin counting from receipt of',
          'cleared deposit. Two rounds of revisions included per deliverable.',
          'Client delays pause the timeline.']),
        ('05. Intellectual property',
         ['Lorem ipsum dolor sit amet — upon full payment, client receives a',
          'non-exclusive, transferable license. The Studio retains:',
          '— source files, working files, underlying techniques',
          '— right to display in portfolio, social, editorial channels',
          '— right to be credited as author']),
        ('06. Cancellation',
         ['Lorem ipsum dolor sit amet. Either party may cancel with 7 days notice.',
          'If cancelled by Client after work begun, deposit non-refundable.']),
        ('07. Liability',
         ['Lorem ipsum dolor sit amet. Studio\'s total liability capped at total fee.',
          'Not liable for indirect, incidental, or consequential losses.']),
        ('08. Confidentiality',
         ['Lorem ipsum dolor sit amet. Both parties agree to keep confidential any',
          'information marked as such.']),
        ('09. Governing law',
         ['Lorem ipsum dolor sit amet. Governed by local law. Disputes resolved by',
          'good-faith mediation, then arbitration.']),
        ('10. Contact',
         ['Lorem ipsum — write to inquire@valenized.com. Response within five',
          'working days. Sed do eiusmod tempor incididunt.']),
    ]
    for title, paras in sections_data:
        draw.text((dx_, ty2), title, font=F(34, 'serif_i'), fill=INK)
        ty2 += 50
        for p in paras:
            draw.text((dx_, ty2), p, font=F(15, 'sans'), fill=INK_DIM)
            ty2 += 26
        ty2 += 30

    draw_footer(draw, ty2 + 100)
    img = img.crop((0, 0, W, ty2 + 100 + 250))
    img.save(f'{OUT}/terms.png')
    print(f'→ terms.png  ({img.size[0]}×{img.size[1]})')


# ─────────────────────────────────────────
render_home()
render_about()
render_works()
render_contact()
render_terms()
