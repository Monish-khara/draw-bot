from drawbot_skia.drawbot import *
from math import pi, sin, cos

W, H = 1000, 800
newPage(W, H)

fill(0)
rect(0, 0, W, H)

stroke(1)
strokeWidth(1.5)
fill(None)
lineCap("round")

apex_x, apex_y = 60, 320
axis_deg = 20
axis_rad = axis_deg * pi / 180

cone_length = 750
num_ellipses = 8
opening_ratio = 0.40
foreshorten = 0.26

perp_x = -sin(axis_rad)
perp_y = cos(axis_rad)
along_x = cos(axis_rad)
along_y = sin(axis_rad)

all_top = []
all_bot = []

for i in range(1, num_ellipses + 1):
    t = i / num_ellipses
    dist = cone_length * t

    cx = apex_x + dist * along_x
    cy = apex_y + dist * along_y

    semi_major = dist * opening_ratio
    semi_minor = semi_major * foreshorten

    num_pts = 200
    path = BezierPath()
    for j in range(num_pts + 1):
        angle = 2 * pi * j / num_pts
        px = cx + semi_major * cos(angle) * perp_x + semi_minor * sin(angle) * along_x
        py = cy + semi_major * cos(angle) * perp_y + semi_minor * sin(angle) * along_y
        if j == 0:
            path.moveTo((px, py))
        else:
            path.lineTo((px, py))
    path.closePath()
    drawPath(path)

    all_top.append((cx + semi_major * perp_x, cy + semi_major * perp_y))
    all_bot.append((cx - semi_major * perp_x, cy - semi_major * perp_y))

for edge in [all_top[-1], all_bot[-1]]:
    path = BezierPath()
    path.moveTo((apex_x, apex_y))
    path.lineTo(edge)
    drawPath(path)

saveImage("output/cone.png")
print("Saved cone.png")
