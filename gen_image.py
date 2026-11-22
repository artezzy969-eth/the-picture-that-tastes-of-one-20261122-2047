#!/usr/bin/env python3
"""Procedural hero-ingredient food picture: glistening ramen bowl.
1024x1024 PNG, no text. Pillow 10.2.0, no network.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)
W = H = 1024
img = Image.new("RGB", (W, H), (18, 10, 8))
d = ImageDraw.Draw(img, "RGBA")

# ---- dark warm background: radial glow behind bowl ----
bg = Image.new("RGB", (W, H), (16, 9, 7))
bd = ImageDraw.Draw(bg)
for r in range(520, 0, -4):
    t = r / 520
    c = (int(16 + 70 * (1 - t) ** 2), int(9 + 38 * (1 - t) ** 2), int(7 + 18 * (1 - t) ** 2))
    bd.ellipse([512 - r, 540 - r, 512 + r, 540 + r], fill=c)
img = bg
d = ImageDraw.Draw(img, "RGBA")

cx, cy = 512, 560  # bowl center
# ---- table shadow ----
d.ellipse([cx - 430, cy + 300, cx + 430, cy + 420], fill=(0, 0, 0, 160))

# ---- bowl outer (dark ceramic, warm rim light) ----
d.ellipse([cx - 420, cy - 300, cx + 420, cy + 330], fill=(28, 16, 12, 255))
d.ellipse([cx - 420, cy - 300, cx + 420, cy + 330], outline=(150, 80, 40, 180), width=6)
# rim highlight arc (top-left warm light)
for a in range(180, 360, 2):
    x = cx + 415 * math.cos(math.radians(a)); y = cy + 8 + 300 * math.sin(math.radians(a))
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 190, 110, 90))
# bowl inner shadow ring
d.ellipse([cx - 385, cy - 268, cx + 385, cy + 295], fill=(12, 7, 5, 255))
# broth surface
d.ellipse([cx - 360, cy - 245, cx + 360, cy + 272], fill=(146, 74, 22, 255))

# broth radial gloss: lighter amber center-left
broth = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bdr = ImageDraw.Draw(broth)
for r in range(360, 0, -3):
    t = r / 360
    col = (int(146 + 90 * (1 - t)), int(74 + 55 * (1 - t)), int(22 + 18 * (1 - t)), 255)
    bdr.ellipse([cx - r, cy - int(r * 0.72), cx + r, cy + int(r * 0.72)], fill=col)
img.paste(Image.alpha_composite(img.convert("RGBA"), broth).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# oil sheen blobs on broth
for (ox, oy, orad, alpha) in [(-150, -120, 90, 70), (120, -160, 70, 60), (200, 40, 60, 50), (-220, 60, 55, 45)]:
    d.ellipse([cx + ox - orad, cy + oy - orad // 2, cx + ox + orad, cy + oy + orad // 2],
              fill=(255, 200, 90, alpha))

# ---- noodles: many curved golden strokes ----
noodle_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(noodle_layer)
for i in range(260):
    a0 = random.uniform(0, 2 * math.pi)
    rr = random.uniform(40, 330)
    nx = cx + rr * math.cos(a0) * 0.98
    ny = cy + rr * math.sin(a0) * 0.70
    ln = random.uniform(25, 70)
    ang = random.uniform(0, 2 * math.pi)
    x2 = nx + ln * math.cos(ang); y2 = ny + ln * math.sin(ang) * 0.6
    shade = random.choice([(232, 178, 84), (245, 205, 120), (214, 150, 55), (250, 220, 150)])
    nd.line([nx, ny, (nx + x2) / 2, (ny + y2) / 2 - 6, x2, y2], fill=shade + (235,), width=random.choice([5, 6, 7]))
    nd.line([nx, ny + 2, x2, y2 + 2], fill=(120, 70, 20, 120), width=2)
noodle_layer = noodle_layer.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(img.convert("RGBA"), noodle_layer)
d = ImageDraw.Draw(img, "RGBA")

# ---- chashu slices: two overlapping glossy pork rounds ----
def chashu(px, py, pr, rot):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.ellipse([px - pr, py - pr * 0.85, px + pr, py + pr * 0.85], fill=(178, 92, 58, 255))
    ld.ellipse([px - pr * 0.72, py - pr * 0.6, px + pr * 0.72, py + pr * 0.6], fill=(232, 178, 140, 255))
    ld.ellipse([px - pr * 0.45, py - pr * 0.38, px + pr * 0.45, py + pr * 0.38], fill=(196, 110, 72, 255))
    # fat marbling arcs
    for k in range(5):
        a0 = random.uniform(0, 360); a1 = a0 + random.uniform(40, 110)
        ld.arc([px - pr * 0.6, py - pr * 0.5, px + pr * 0.6, py + pr * 0.5], a0, a1,
               fill=(250, 225, 200, 200), width=4)
    # gloss highlight
    ld.ellipse([px - pr * 0.5, py - pr * 0.6, px - pr * 0.15, py - pr * 0.35], fill=(255, 235, 210, 55))
    lay = lay.rotate(rot, center=(px, py), resample=Image.BICUBIC)
    return lay

img = Image.alpha_composite(img, chashu(cx - 170, cy + 60, 130, 12))
img = Image.alpha_composite(img, chashu(cx + 185, cy + 95, 118, -18))
d = ImageDraw.Draw(img, "RGBA")

# ---- soft egg halves: white + glossy orange yolk ----
def egg(px, py, pr):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.ellipse([px - pr, py - pr * 0.78, px + pr, py + pr * 0.78], fill=(248, 240, 225, 255))
    ld.ellipse([px - pr, py - pr * 0.78, px + pr, py + pr * 0.78], outline=(210, 190, 160, 255), width=3)
    # yolk: radial orange
    for r in range(int(pr * 0.52), 0, -2):
        t = r / (pr * 0.52)
        col = (int(255 - 40 * t), int(150 - 30 * t), int(30 + 20 * t), 255)
        ld.ellipse([px - r, py - int(r * 0.8), px + r, py + int(r * 0.8)], fill=col)
    # yolk gloss dot
    ld.ellipse([px - int(pr * 0.28), py - int(pr * 0.42), px - int(pr * 0.05), py - int(pr * 0.18)],
               fill=(255, 230, 170, 200))
    return lay

img = Image.alpha_composite(img, egg(cx - 60, cy - 130, 105))
img = Image.alpha_composite(img, egg(cx + 130, cy - 150, 92))
d = ImageDraw.Draw(img, "RGBA")

# ---- scallion rings ----
for i in range(46):
    a0 = random.uniform(0, 2 * math.pi); rr = random.uniform(60, 320)
    sx = cx + rr * math.cos(a0); sy = cy + rr * math.sin(a0) * 0.7
    sr = random.uniform(9, 16)
    d.ellipse([sx - sr, sy - sr * 0.7, sx + sr, sy + sr * 0.7], outline=(60, 160, 60, 255), width=4)
    d.ellipse([sx - sr * 0.45, sy - sr * 0.3, sx + sr * 0.45, sy + sr * 0.3], fill=(140, 210, 90, 220))

# ---- sesame seeds scattered on broth ----
for i in range(70):
    a0 = random.uniform(0, 2 * math.pi); rr = random.uniform(80, 330)
    sx = cx + rr * math.cos(a0); sy = cy + rr * math.sin(a0) * 0.7
    d.ellipse([sx - 4, sy - 2, sx + 4, sy + 2], fill=(245, 225, 180, 230))

# ---- nori sheet (top right, dark green, matte) ----
nori = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd2 = ImageDraw.Draw(nori)
nd2.rounded_rectangle([cx + 150, cy - 260, cx + 330, cy - 60], radius=18, fill=(18, 42, 26, 235))
nd2.rounded_rectangle([cx + 150, cy - 260, cx + 330, cy - 60], radius=18, outline=(60, 110, 70, 200), width=3)
nori = nori.rotate(-14, center=(cx + 240, cy - 160), resample=Image.BICUBIC)
img = Image.alpha_composite(img, nori)
d = ImageDraw.Draw(img, "RGBA")

# ---- steam wisps ----
steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(steam)
for sx0, amp, ph in [(380, 26, 0), (512, 34, 2.1), (640, 24, 4.2)]:
    pts = []
    for y in range(60, 330, 8):
        x = sx0 + amp * math.sin(y / 55 + ph)
        pts.append((x, y))
    sd.line(pts, fill=(255, 250, 240, 95), width=34)
    sd.line(pts, fill=(255, 250, 240, 75), width=16)
steam = steam.filter(ImageFilter.GaussianBlur(11))
img = Image.alpha_composite(img, steam)
d = ImageDraw.Draw(img, "RGBA")

# ---- warm rim light on bowl edge + vignette ----
d.arc([cx - 420, cy - 300, cx + 420, cy + 330], 200, 340, fill=(255, 180, 100, 160), width=8)
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
for r in range(720, 380, -6):
    vd.ellipse([512 - r, 512 - r, 512 + r, 512 + r], outline=(0, 0, 0, 26), width=6)
vig = vig.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img, vig)

out = img.convert("RGB")
out.save("entry.png", optimize=True)
print("saved entry.png", out.size)
