"""instant-grep v5: Traveling pulses — colored segments zip along each ray."""
from drawbot_skia.drawbot import *
from PIL import Image
import os
import math

SVG_W, SVG_H = 2216.53, 1076.42
CANVAS_W, CANVAS_H = 2400, 1260
PADDING = 96
scale_x = (CANVAS_W - 2 * PADDING) / SVG_W
scale_y = (CANVAS_H - 2 * PADDING) / SVG_H
off_x = PADDING
off_y = PADDING

ACCENT = (0xFF / 255, 0x62 / 255, 0x00 / 255)
PULSE_LEN = 0.12


def tx(x, y):
    return (x * scale_x + off_x, CANVAS_H - (y * scale_y + off_y))


def lerp(a, b, t):
    return a + (b - a) * t


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

RAYS = []
for i, pts in enumerate(POLYLINES):
    apex = pts[1]
    RAYS.append((apex, pts[0], i * 2))
    RAYS.append((apex, pts[2], i * 2 + 1))

numFrames = 90
os.makedirs("output/frames_instant_grep_v5", exist_ok=True)

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

    strokeWidth(4)
    lineJoin("round")
    fill(None)
    for apex, endpoint, idx in RAYS:
        stagger = (idx / len(RAYS)) * 0.4
        local_t = ((t - stagger) % 1.0) / (1.0 - 0.0)
        local_t = max(0.0, min(1.0, local_t))

        head = local_t
        tail = max(0.0, head - PULSE_LEN)

        fade = 1.0
        if head < PULSE_LEN:
            fade = head / PULSE_LEN
        if head > 1.0 - PULSE_LEN:
            fade = (1.0 - head) / PULSE_LEN
        fade = max(0.0, min(1.0, fade))

        if fade <= 0:
            continue

        stroke(*ACCENT, fade)

        p_tail = tx(lerp(apex[0], endpoint[0], tail),
                     lerp(apex[1], endpoint[1], tail))
        p_head = tx(lerp(apex[0], endpoint[0], head),
                     lerp(apex[1], endpoint[1], head))

        path = BezierPath()
        path.moveTo(p_tail)
        path.lineTo(p_head)
        drawPath(path)

    saveImage(f"output/frames_instant_grep_v5/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_instant_grep_v5/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/instant_grep_v5.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,
    loop=0,
)
print(f"Saved instant_grep_v5.gif ({numFrames} frames)")
