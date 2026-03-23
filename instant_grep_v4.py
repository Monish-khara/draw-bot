"""instant-grep v4: Radar sweep — colored beams rotate through each corner's cone angle."""
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
BEAM_LENGTH = math.hypot(SVG_W, SVG_H)


def tx(x, y):
    return (x * scale_x + off_x, CANVAS_H - (y * scale_y + off_y))


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

CORNERS = {}
for pts in POLYLINES:
    apex = pts[1]
    if apex not in CORNERS:
        CORNERS[apex] = []
    CORNERS[apex].append(pts[0])
    CORNERS[apex].append(pts[2])

SWEEPS = []
for apex, endpoints in CORNERS.items():
    angles = [math.atan2(ep[1] - apex[1], ep[0] - apex[0]) for ep in endpoints]
    SWEEPS.append((apex, min(angles), max(angles)))

numFrames = 90
os.makedirs("output/frames_instant_grep_v4", exist_ok=True)

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

    stroke(*ACCENT)
    strokeWidth(3)
    fill(None)
    for apex, min_a, max_a in SWEEPS:
        mid = (min_a + max_a) / 2
        half = (max_a - min_a) / 2
        angle = mid + half * math.sin(2 * math.pi * t)

        end = (apex[0] + math.cos(angle) * BEAM_LENGTH,
               apex[1] + math.sin(angle) * BEAM_LENGTH)

        p_apex = tx(*apex)
        p_end = tx(*end)
        path = BezierPath()
        path.moveTo(p_apex)
        path.lineTo(p_end)
        drawPath(path)

    saveImage(f"output/frames_instant_grep_v4/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_instant_grep_v4/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/instant_grep_v4.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,
    loop=0,
)
print(f"Saved instant_grep_v4.gif ({numFrames} frames)")
