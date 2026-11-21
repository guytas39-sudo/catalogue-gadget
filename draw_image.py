#!/usr/bin/env python3
"""TOAST & PRESS 3000 — a studio catalogue photograph of an impossible gadget.

A chrome toaster that toasts bread AND irons a shirt at the same time.
Drawn with Pillow: every element is vector geometry, so the render is
deterministic. Run: python3 draw_image.py  ->  entry.png (1024x1024).
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
FDIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(f"{FDIR}/{name}", size)

F_LABEL = font("DejaVuSans-Bold.ttf", 30)
F_BADGE = font("DejaVuSans-Bold.ttf", 22)
F_SMALL = font("DejaVuSans.ttf", 17)

# ---------- backdrop: soft studio gradient + floor ----------
img = Image.new("RGB", (W, H), (238, 238, 236))
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    g = int(240 - 22 * t)          # 240 -> 218, top to bottom
    d.line([(0, y), (W, y)], fill=(g, g, g - 2))
# floor: slightly darker band from y=830
d.rectangle([0, 830, W, H], fill=(216, 216, 214))
d.line([(0, 830), (W, 830)], fill=(196, 196, 194), width=2)
# soft contact shadow under the product
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ds = ImageDraw.Draw(sh)
ds.ellipse([255, 815, 775, 875], fill=(0, 0, 0, 70))
sh = sh.filter(ImageFilter.GaussianBlur(14))
img.paste(sh, (0, 0), sh)
d = ImageDraw.Draw(img)

# ---------- chrome toaster body (horizontal metallic gradient) ----------
BX0, BY0, BX1, BY1 = 300, 540, 724, 830
grad = Image.new("RGB", (BX1 - BX0, BY1 - BY0))
gd = ImageDraw.Draw(grad)
stops = [(0.00, (245, 245, 245)), (0.18, (205, 205, 205)),
         (0.38, (160, 160, 160)), (0.55, (225, 225, 225)),
         (0.72, (175, 175, 175)), (0.88, (235, 235, 235)),
         (1.00, (200, 200, 200))]
gw = BX1 - BX0
for x in range(gw):
    t = x / gw
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0
            col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
            break
    gd.line([(x, 0), (x, BY1 - BY0)], fill=col)
mask = Image.new("L", (gw, BY1 - BY0), 0)
dm = ImageDraw.Draw(mask)
dm.rounded_rectangle([0, 0, gw, BY1 - BY0], radius=28, fill=255)
img.paste(grad, (BX0, BY0), mask)
d = ImageDraw.Draw(img)
d.rounded_rectangle([BX0, BY0, BX1, BY1], radius=28, outline=(120, 120, 120), width=2)
# top highlight stripe
d.rounded_rectangle([BX0 + 14, BY0 + 10, BX1 - 14, BY0 + 26], radius=8,
                    fill=(255, 255, 255))
# feet
d.rounded_rectangle([330, BY1 - 4, 380, BY1 + 8], radius=6, fill=(60, 60, 60))
d.rounded_rectangle([644, BY1 - 4, 694, BY1 + 8], radius=6, fill=(60, 60, 60))

# ---------- slots + toast slices popping up ----------
for sx in (352, 556):
    d.rounded_rectangle([sx, 522, sx + 116, 546], radius=8, fill=(40, 40, 40))
for cx, ang in ((410, 5), (614, -4)):
    # one toast slice on its own layer so it can be tilted
    lay = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    dl.rounded_rectangle([45, 30, 155, 175], radius=18, fill=(196, 128, 52))
    dl.rounded_rectangle([55, 42, 145, 163], radius=12, fill=(232, 184, 106))
    dl.rounded_rectangle([55, 42, 145, 163], radius=12, outline=(176, 112, 44), width=3)
    lay = lay.rotate(ang, resample=Image.BICUBIC, center=(100, 100))
    img.paste(lay, (cx - 100, 395), lay)
d = ImageDraw.Draw(img)

# ---------- white shirt draped over the toaster's top, hanging down the front ----------
shirt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ds = ImageDraw.Draw(shirt)
# main cloth: shoulders at the top, gentle wavy hem
ds.polygon([(338, 548), (686, 548), (700, 700), (672, 716), (620, 700),
            (512, 712), (404, 700), (352, 716), (324, 700)],
           fill=(250, 250, 248, 255), outline=(190, 190, 188))
# collar: two triangles meeting at the neck
ds.polygon([(452, 548), (512, 606), (470, 612)], fill=(238, 238, 236, 255),
           outline=(170, 170, 168))
ds.polygon([(572, 548), (512, 606), (554, 612)], fill=(238, 238, 236, 255),
           outline=(170, 170, 168))
ds.polygon([(496, 590), (528, 590), (512, 606)], fill=(210, 210, 208, 255))
# button placket down the middle
ds.line([(512, 612), (512, 706)], fill=(200, 200, 198), width=3)
for by in (632, 662, 692):
    ds.ellipse([506, by, 518, by + 12], outline=(150, 150, 148), width=2)
# fold lines
ds.arc([360, 560, 470, 700], 20, 130, fill=(215, 215, 213), width=3)
ds.arc([560, 560, 680, 700], 50, 160, fill=(215, 215, 213), width=3)
ds.arc([430, 640, 600, 760], 10, 170, fill=(222, 222, 220), width=2)
img.paste(shirt, (0, 0), shirt)
d = ImageDraw.Draw(img)

# ---------- steam rising from toast + shirt ----------
steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dst = ImageDraw.Draw(steam)
for sx, ph in ((410, 0.0), (512, 1.4), (614, 2.6)):
    pts = []
    for i in range(41):
        yy = 430 - i * 6
        xx = sx + int(14 * math.sin(i * 0.35 + ph))
        pts.append((xx, yy))
    dst.line(pts, fill=(255, 255, 255, 110), width=7, joint="curve")
steam = steam.filter(ImageFilter.GaussianBlur(3))
img.paste(steam, (0, 0), steam)
d = ImageDraw.Draw(img)

# ---------- product label + badge + dial + lever ----------
# label plate is sized to the text: shrink the font until the name fits
plate = (368, 736, 640, 786)
label = "TOAST & PRESS 3000"
fsize = 30
while fsize > 16:
    fl = font("DejaVuSans-Bold.ttf", fsize)
    if d.textlength(label, font=fl) <= plate[2] - plate[0] - 16:
        break
    fsize -= 1
d.rounded_rectangle(plate, radius=8, fill=(28, 32, 40))
d.text(((plate[0] + plate[2]) // 2, 761), label, font=fl, fill=(245, 245, 240),
       anchor="mm")
# 2-IN-1 badge: small font so the text stays inside the circle
d.ellipse([648, 736, 700, 788], fill=(178, 34, 34), outline=(255, 255, 255), width=2)
d.text((674, 762), "2-IN-1", font=font("DejaVuSans-Bold.ttf", 15),
       fill=(255, 255, 255), anchor="mm")
# browning dial, clear of the label plate
d.ellipse([312, 742, 352, 782], fill=(70, 70, 70), outline=(220, 220, 220), width=2)
d.line([(332, 762), (332, 748)], fill=(240, 240, 240), width=3)
# side lever
d.rounded_rectangle([716, 620, 736, 668], radius=8, fill=(90, 90, 90),
                    outline=(200, 200, 200), width=2)
d.ellipse([712, 648, 740, 676], fill=(178, 34, 34), outline=(255, 255, 255), width=2)

# ---------- the one accessory: a necktie laid flat on the floor ----------
tie = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dt = ImageDraw.Draw(tie)
# knot + blade, lying horizontally, slightly angled
dt.polygon([(788, 836), (826, 822), (838, 846), (806, 862)],
           fill=(122, 28, 40, 255), outline=(90, 18, 28, 255))
dt.polygon([(826, 822), (960, 800), (982, 830), (968, 856), (838, 846)],
           fill=(146, 32, 48, 255), outline=(90, 18, 28, 255))
# diagonal stripes on the blade
for x0 in (860, 890, 920, 950):
    dt.line([(x0, 816), (x0 - 14, 852)], fill=(232, 190, 90, 255), width=6)
tie = tie.rotate(-4, resample=Image.BICUBIC, center=(880, 835))
img.paste(tie, (0, 0), tie)
d = ImageDraw.Draw(img)
# tie's soft shadow
sh2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d2 = ImageDraw.Draw(sh2)
d2.ellipse([790, 852, 985, 878], fill=(0, 0, 0, 40))
sh2 = sh2.filter(ImageFilter.GaussianBlur(6))
img.paste(sh2, (0, 0), sh2)

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
