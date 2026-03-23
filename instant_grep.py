from drawbot_skia.drawbot import *
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

os.makedirs("output", exist_ok=True)

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

saveImage("output/instant_grep.png")
print("Saved output/instant_grep.png")
