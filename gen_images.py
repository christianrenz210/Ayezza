import os

from PIL import Image, ImageDraw, ImageFont

W, H = 800, 1236
ACCENT = (227, 197, 103)
GOLD = (201, 162, 39)
MUTED = (168, 168, 160)


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/Georgia.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/ARIAL.TTF",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_icon(d, cx, cy):
    w, h = 220, 160
    x0, y0 = cx - w // 2, cy - h // 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=14, outline=ACCENT, width=10)
    d.ellipse([x0 + 25, y0 + 30, x0 + 61, y0 + 66], outline=ACCENT, width=10)
    pts = [
        (x0 + 12, y0 + 142),
        (x0 + 82, y0 + 72),
        (x0 + 142, y0 + 132),
        (x0 + 188, y0 + 82),
        (x0 + 208, y0 + 142),
    ]
    d.line(pts, fill=ACCENT, width=10, joint="curve")


def make(label, sub, top, bottom, out):
    img = Image.new("RGB", (W, H), bottom)
    d = ImageDraw.Draw(img)
    grad_steps = 200
    for i in range(grad_steps):
        t = i / grad_steps
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        d.rectangle([0, i * H // grad_steps, W, (i + 1) * H // grad_steps], fill=(r, g, b))
    d.rectangle([24, 24, W - 24, H - 24], outline=GOLD, width=2)
    draw_icon(d, W // 2, H // 2 - 120)
    f_title = font(72, bold=True)
    d.text((W // 2, H // 2 + 40), label, font=f_title, fill=ACCENT, anchor="mm")
    f_sub = font(26)
    d.text((W // 2, H // 2 + 92), sub, font=f_sub, fill=MUTED, anchor="mm")
    img.save(out, "JPEG", quality=90)
    print("wrote", out)


base = os.path.join(os.path.dirname(__file__), "static", "img")
make("AYEZZA 0", "IMAGE FRAME", (35, 50, 58), (18, 24, 28), os.path.join(base, "ayezza(0).jpg"))
make("AYEZZA 1", "IMAGE FRAME", (58, 35, 51), (28, 18, 24), os.path.join(base, "ayezza(1).jpg"))
