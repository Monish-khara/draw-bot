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

BG = (0x4A / 255, 0x44 / 255, 0x3B / 255)
ACCENT = (0xF5 / 255, 0x4E / 255, 0x00 / 255)
LINE_COLOR = (1, 1, 1)
PULSE_LEN = 0.25
TRAIL_SEGMENTS = 8


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
    fill(*BG)
    rect(0, 0, CANVAS_W, CANVAS_H)

    stroke(*LINE_COLOR)
    strokeWidth(2)
    lineJoin("miter")
    fill(None)
    for pts in POLYLINES:
        path = BezierPath()
        path.moveTo(tx(*pts[0]))
        path.lineTo(tx(*pts[1]))
        path.lineTo(tx(*pts[2]))
        drawPath(path)

    lineJoin("round")
    fill(None)
    for apex, endpoint, idx in RAYS:
        stagger = (idx / len(RAYS)) * 0.7
        local_t = ((t - stagger) % 1.0)
        local_t = max(0.0, min(1.0, local_t))

        head = local_t
        tail = max(0.0, head - PULSE_LEN)

        if head <= 0:
            continue

        for seg in range(TRAIL_SEGMENTS):
            frac = seg / TRAIL_SEGMENTS
            seg_start = lerp(tail, head, frac)
            seg_end = lerp(tail, head, (seg + 1) / TRAIL_SEGMENTS)

            color_t = frac ** 0.3
            r = lerp(LINE_COLOR[0], ACCENT[0], color_t)
            g = lerp(LINE_COLOR[1], ACCENT[1], color_t)
            b = lerp(LINE_COLOR[2], ACCENT[2], color_t)

            edge_fade = 1.0
            if head < PULSE_LEN:
                edge_fade = head / PULSE_LEN
            if head > 1.0 - PULSE_LEN * 0.5:
                edge_fade = (1.0 - head) / (PULSE_LEN * 0.5)
            edge_fade = max(0.0, min(1.0, edge_fade))

            stroke(r, g, b, edge_fade)
            strokeWidth(2)

            p0 = tx(lerp(apex[0], endpoint[0], seg_start),
                     lerp(apex[1], endpoint[1], seg_start))
            p1 = tx(lerp(apex[0], endpoint[0], seg_end),
                     lerp(apex[1], endpoint[1], seg_end))

            path = BezierPath()
            path.moveTo(p0)
            path.lineTo(p1)
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
