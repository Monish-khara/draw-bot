"""instant-grep v1: All lines grow from apex simultaneously with ease-out."""
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


def tx(x, y):
    return (x * scale_x + off_x, CANVAS_H - (y * scale_y + off_y))


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


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

numFrames = 60
os.makedirs("output/frames_instant_grep_v1", exist_ok=True)

for frame in range(numFrames):
    t = frame / (numFrames - 1)
    progress = ease_out_cubic(t)

    newPage(CANVAS_W, CANVAS_H)
    fill(1)
    rect(0, 0, CANVAS_W, CANVAS_H)
    stroke(0)
    strokeWidth(2)
    lineJoin("miter")
    fill(None)

    for pts in POLYLINES:
        apex = tx(*pts[1])
        end0 = tx(*pts[0])
        end2 = tx(*pts[2])

        cur0 = (lerp(apex[0], end0[0], progress), lerp(apex[1], end0[1], progress))
        cur2 = (lerp(apex[0], end2[0], progress), lerp(apex[1], end2[1], progress))

        path = BezierPath()
        path.moveTo(cur0)
        path.lineTo(apex)
        path.lineTo(cur2)
        drawPath(path)

    saveImage(f"output/frames_instant_grep_v1/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_instant_grep_v1/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/instant_grep_v1.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,
    loop=0,
)
print(f"Saved instant_grep_v1.gif ({numFrames} frames)")
