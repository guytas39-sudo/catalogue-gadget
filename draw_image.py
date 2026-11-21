#!/usr/bin/env python3
"""Draw the entry image: a studio catalogue photograph of an impossible gadget.

The TOAST & PRESS 3000 — a chrome toaster that toasts bread AND irons a shirt
at the same time. A white dress shirt is draped over the toaster being pressed,
two golden toast slices pop from the slots, steam rises, and exactly one
accessory lies beside it: a burgundy striped necktie, freshly pressed.

Drawn with Pillow: every shape is a fixed coordinate, so running this twice
produces identical bytes. Run: python3 draw_image.py  ->  writes entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)


F_BADGE = font("DejaVuSans-Bold.ttf", 14)

img = Image.new("RGB", (W, H), (247, 247, 245))
d = ImageDraw.Draw(img)

# ---- studio backdrop: soft vertical gradient, floor below y=780 ----
for y in range(H):
    if y < 780:
        t = y / 780
        c = tuple(int(247 + (218 - 247) * t) for _ in range(3))
    else:
        t = (y - 780) / 244
        c = tuple(int(218 - (218 - 196) * t) for _ in range(3))
    d.line([(0, y), (W, y)], fill=c)
d.line([(0, 780), (W, 780)], fill=(190, 190, 188), width=2)

# ---- soft contact shadow under the product (RGBA overlay) ----
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
od.ellipse([300, 772, 760, 812], fill=(60, 60, 60, 70))
od.ellipse([740, 788, 990, 820], fill=(60, 60, 60, 45))
img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
d = ImageDraw.Draw(img)

# ---- toast slices popping from the slots ----
def toast(x0, y0, x1, y1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(178, 118, 44))
    d.rounded_rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 6], radius=13,
                        fill=(246, 205, 107))
    # light toasting marks
    d.ellipse([x0 + 26, y0 + 40, x0 + 52, y0 + 78], fill=(226, 170, 80))
    d.ellipse([x1 - 52, y0 + 30, x1 - 26, y0 + 66], fill=(226, 170, 80))

toast(372, 300, 478, 500)
toast(546, 292, 652, 500)

# ---- toaster body: chrome with a bright highlight stripe ----
d.rounded_rectangle([300, 470, 724, 790], radius=28, fill=(176, 176, 176),
                    outline=(110, 110, 110), width=3)
# chrome bands: bright stripe left, dark edge right
d.rounded_rectangle([300, 470, 352, 790], radius=28, fill=(224, 224, 224))
d.rounded_rectangle([352, 470, 392, 790], radius=4, fill=(240, 240, 240))
d.rounded_rectangle([668, 470, 724, 790], radius=28, fill=(128, 128, 128))
# top slots (dark, behind the toast)
d.rounded_rectangle([360, 466, 492, 486], radius=8, fill=(52, 52, 52))
d.rounded_rectangle([532, 466, 664, 486], radius=8, fill=(52, 52, 52))
# right side cap with browning dial and lever
d.ellipse([680, 620, 720, 660], fill=(96, 96, 96), outline=(70, 70, 70),
          width=2)
d.line([(700, 640), (700, 626)], fill=(245, 245, 245), width=3)
d.rounded_rectangle([700, 668, 716, 724], radius=6, fill=(90, 90, 90))

# ---- dress shirt draped over the toaster top, being pressed ----
# The drape covers only the top third of the front face, so the chrome body
# below it stays visible and the toaster reads as the hero.
d.rounded_rectangle([330, 440, 694, 610], radius=16, fill=(255, 255, 255),
                    outline=(178, 178, 178), width=2)
# shading on the right half of the drape
d.rounded_rectangle([560, 440, 694, 610], radius=16, fill=(232, 232, 232))
d.rounded_rectangle([330, 440, 560, 610], radius=16, fill=(255, 255, 255))
# fold lines
d.line([(400, 450), (388, 600)], fill=(198, 198, 198), width=2)
d.line([(624, 450), (636, 600)], fill=(198, 198, 198), width=2)
# collar: two triangles meeting at the centre V
d.polygon([(452, 440), (512, 440), (512, 498), (468, 470)], fill=(250, 250, 250),
          outline=(160, 160, 160))
d.polygon([(572, 440), (512, 440), (512, 498), (556, 470)], fill=(250, 250, 250),
          outline=(160, 160, 160))
# placket and buttons down the middle
d.line([(512, 498), (512, 602)], fill=(190, 190, 190), width=3)
for by in (520, 556, 592):
    d.ellipse([504, by, 520, by + 16], fill=(214, 214, 214),
              outline=(150, 150, 150), width=2)

# ---- product label plate + 2-IN-1 badge (on the chrome front, below the shirt) ----
d.rounded_rectangle([330, 700, 600, 744], radius=8, fill=(38, 38, 38))
label = "TOAST & PRESS 3000"
size = 20
f = font("DejaVuSans-Bold.ttf", size)
while d.textlength(label, font=f) > 252 and size > 12:
    size -= 1
    f = font("DejaVuSans-Bold.ttf", size)
tw = d.textlength(label, font=f)
d.text((465 - tw / 2, 722 - size / 2 - 2), label, font=f, fill=(245, 245, 245))
# circular badge
d.ellipse([624, 694, 680, 750], fill=(178, 34, 34), outline=(120, 20, 20),
          width=2)
bt = "2-IN-1"
btw = d.textlength(bt, font=F_BADGE)
d.text((652 - btw / 2, 722 - 7), bt, font=F_BADGE, fill=(255, 255, 255))

# ---- steam rising from the shirt: smooth sine curves, not zigzags ----
import math
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
for x0, top in ((420, 250), (512, 230), (604, 250)):
    pts = []
    for i in range(31):
        yy = 430 - i * (430 - top) / 30
        xx = x0 + 9 * math.sin(i * 0.55)
        pts.append((xx, yy))
    od.line(pts, fill=(150, 150, 150, 100), width=4)
img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
d = ImageDraw.Draw(img)

# ---- exactly one accessory: a burgundy striped necktie, laid flat ----
# Drawn upright on its own layer (knot + blade + tip + stripes), then
# rotated, so it reads as a real tie instead of a flat wedge.
tie = Image.new("RGBA", (300, 90), (0, 0, 0, 0))
td = ImageDraw.Draw(tie)
# blade
td.polygon([(46, 26), (238, 26), (272, 45), (238, 64), (46, 64)],
           fill=(122, 31, 43))
# diagonal stripes, kept inside the blade rectangle
for i in range(7):
    x = 62 + i * 26
    td.line([(x, 26), (x + 12, 64)], fill=(156, 51, 64), width=7)
# knot
td.polygon([(6, 18), (46, 18), (54, 72), (0, 72)], fill=(96, 22, 32))
td.polygon([(46, 26), (238, 26), (272, 45), (238, 64), (46, 64)],
           outline=(70, 14, 20), width=2)
td.polygon([(6, 18), (46, 18), (54, 72), (0, 72)], outline=(70, 14, 20))
tie = tie.rotate(-16, expand=True, resample=Image.BICUBIC)
img.paste(tie, (730, 748), tie)

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
