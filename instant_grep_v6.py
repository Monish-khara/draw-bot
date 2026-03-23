"""instant-grep v6: Morphing accent — a colored V-shape morphs through all 8 cone positions."""
from drawbot_skia.drawbot import *
from PIL import Image
import os

SVG_W, SVG_H = 2216.53, 1076.42
CANVAS_W, CANVAS_H = 2400, 1260
PADDING = 96
scale_x = (CANVAS_W - 2 * PADDING) / SVG_W
scale_y = (CANVAS_H - 2 * PADDING) / SVG_H
off_x = PADDING
off_y = PADDING

ACCENT = (0xFF / 255, 0x62 / 255, 0x00 / 255)


def tx(x, y):
    return (x * scale_x + off_x, CANVAS_H - (y * scale_y + off_y))


def lerp(a, b, t):
    return a + (b - a) * t


def ease_in_out(t):
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


POLYLINES = [
    [(555.26, 1074.21), (2.26, 2.21), (2214.26, 1074.21)],
    [(1661.26, 1074.21), (2.26, 2.21), (1108.26, 1074.21)],
    [(1661.26, 1074.21), (2214.26, 2.21), (2.26, 1074.21)],
    [(555.26, 1074.21), (2214.26, 2.21), (1108.26, 1074.21)],
    [(1661.26, 2.21), (2214.26, 1074.21), (2.26, 2.21)],
    [(555.26, 2.21), (2214.26, 1074.21), (1108.26, 2.21)],
    [(555.26, 2.21), (2.26, 1074.21), (2214.26, 2.21)],
    [(1661.26, 2.21), (2.26, 1074.21), (1108.26, 2.21)],
]

FLAT = []
for pts in POLYLINES:
    FLAT.append((pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1]))

numFrames = 120
numCones = len(FLAT)
os.makedirs("output/frames_instant_grep_v6", exist_ok=True)

for frame in range(numFrames):
    t = frame / numFrames

    newPage(CANVAS_W, CANVAS_H)
    fill(1)
    rect(0, 0, CANVAS_W, CANVAS_H)

    stroke(0)
    strokeWidth(2)
    lineJoin("miter")
    fill(None)
    for pts in POLYLINES:
        path = BezierPath()
        path.moveTo(tx(*pts[0]))
        path.lineTo(tx(*pts[1]))
        path.lineTo(tx(*pts[2]))
        drawPath(path)

    progress = t * numCones
    idx = int(progress) % numCones
    local_t = progress - int(progress)
    eased = ease_in_out(local_t)

    a = FLAT[idx]
    b = FLAT[(idx + 1) % numCones]

    cur = tuple(lerp(a[i], b[i], eased) for i in range(6))

    fade = 1.0
    if local_t < 0.1:
        fade = local_t / 0.1
    elif local_t > 0.9:
        fade = (1.0 - local_t) / 0.1
    fade = max(0.0, min(1.0, fade))

    stroke(*ACCENT, fade)
    strokeWidth(4)
    fill(None)

    path = BezierPath()
    path.moveTo(tx(cur[0], cur[1]))
    path.lineTo(tx(cur[2], cur[3]))
    path.lineTo(tx(cur[4], cur[5]))
    drawPath(path)

    saveImage(f"output/frames_instant_grep_v6/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_instant_grep_v6/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/instant_grep_v6.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,
    loop=0,
)
print(f"Saved instant_grep_v6.gif ({numFrames} frames)")
