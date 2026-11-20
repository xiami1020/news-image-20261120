#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261120.
Deterministic: fixed text, fixed fonts, no time, no random, no network.
Run: python3 generate.py  -> writes entry.png (1024x1024, <1MiB).
The submitted program (main.py) only copies entry.png to /output.
Headlines verified 2026-11-20 from BBC / OneTurn / SimpleLife news listings.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, color, max_w, lh=None):
    lh = lh or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y

img = Image.new("RGB", (W, H), "#F7F2E6")
d = ImageDraw.Draw(img)

# ---- header ----
d.rectangle([0, 0, W, 118], fill="#10243E")
d.text((28, 22), "WORLD NEWS", font=font(62), fill="white")
d.text((28, 88), "FRIDAY  •  THE DAY IN ONE PICTURE", font=font(20), fill="#F2C14E")
d.text((700, 30), "20 NOV", font=font(52), fill="white")
d.text((700, 88), "2026", font=font(28), fill="#F2C14E")

# ---- main story: Shenzhen summit ----
d.rounded_rectangle([24, 138, 624, 560], radius=14, fill="white", outline="#10243E", width=3)
d.text((44, 156), "SHENZHEN  •  SUMMIT", font=font(20), fill="#B03A2E")
text_block(d, 44, 186, "TRUMP, XI & PUTIN MEET", font(34), "#10243E", 540)
text_block(d, 44, 262, "First three-way summit ends with a joint peace declaration.", font(24, False), "#222222", 540)
# globe + three flags
d.ellipse([70, 360, 250, 540], fill="#2E6FB7", outline="#10243E", width=3)
d.ellipse([110, 390, 210, 510], outline="white", width=2)
d.line([160, 360, 160, 540], fill="white", width=2)
d.line([70, 450, 250, 450], fill="white", width=2)
for i, (c1, c2, label) in enumerate([("#B22234", "#FFFFFF", "US"), ("#DE2910", "#FFDE00", "CHINA"), ("#FFFFFF", "#0039A6", "RUSSIA")]):
    x = 290 + i * 105
    d.rectangle([x, 380, x + 88, 440], fill=c1, outline="#10243E", width=2)
    d.rectangle([x, 440, x + 88, 470], fill=c2, outline="#10243E", width=2)
    d.text((x + 8, 482), label, font=font(18), fill="#10243E")
d.text((290, 520), "US  •  CHINA  •  RUSSIA", font=font(18), fill="#555555")

# ---- right column: ICJ + Anthropic ----
d.rounded_rectangle([644, 138, 1000, 340], radius=14, fill="#10243E")
d.text((664, 156), "THE HAGUE  •  JUSTICE", font=font(19), fill="#F2C14E")
text_block(d, 664, 186, "World Court: Myanmar committed genocide against the Rohingya.", font(24), "white", 316)
d.text((664, 296), "ICJ  •  9–6 RULING", font=font(19), fill="#9FC3E8")
d.rounded_rectangle([644, 360, 1000, 560], radius=14, fill="white", outline="#10243E", width=3)
d.text((664, 378), "NEW YORK  •  MARKETS", font=font(19), fill="#B03A2E")
text_block(d, 664, 406, "Anthropic debuts on Nasdaq: shares close +17% at about $97.", font(23), "#10243E", 316)
# rising chart
pts = [(670, 545), (730, 532), (790, 538), (850, 520), (910, 505), (975, 492)]
d.line(pts, fill="#1E7A34", width=5, joint="curve")
for x, y in pts:
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill="#1E7A34")

# ---- bottom row: three stories ----
panels = [
    ("CRIMEA  •  CONFLICT", "Ukraine strikes the Crimea Bridge for the 3rd time in 4 days; rail halted.", "#B03A2E"),
    ("RIYADH  •  CONFLICT", "Houthi missile damages Saudi wealth-fund tower in Riyadh.", "#B03A2E"),
    ("MARKETS  •  ECONOMY", "Stocks fall a 5th day; Nikkei drops 4.8% as Asia slides.", "#B03A2E"),
]
for i, (kicker, body, kc) in enumerate(panels):
    x0 = 24 + i * 330
    d.rounded_rectangle([x0, 580, x0 + 310, 820], radius=14, fill="white", outline="#10243E", width=3)
    d.text((x0 + 18, 600), kicker, font=font(17), fill=kc)
    text_block(d, x0 + 18, 634, body, font(23), "#10243E", 274)
    d.rectangle([x0 + 18, 780, x0 + 292, 786], fill="#F2C14E")

# ---- footer strip ----
d.rectangle([0, 860, W, 1024], fill="#10243E")
text_block(d, 28, 884, "Also: US Senate rejects Iran war-powers measure 51–48  •  Trump pardons Pete Rose  •  UK pledges 1,000+ drones for Ukraine  •  Taiwan stocks plunge", font(22), "white", 968)
d.text((28, 972), "20 NOVEMBER 2026  •  SOURCES: BBC / ICJ / NASDAQ  •  ONE IMAGE, ONE DAY", font=font(18), fill="#F2C14E")

img.save("entry.png", "PNG", optimize=True)
print("wrote entry.png", img.size)
