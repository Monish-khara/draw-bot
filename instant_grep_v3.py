"""instant-grep v3: Cones fan open from closed (rays overlapping) to final spread."""
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


def tx(x, y):
    return (x * scale_x + off_x, CANVAS_H - (y * scale_y + off_y))


def lerp(a, b, t):
    return a + (b - a) * t


def ease_in_out_cubic(t):
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


def angle_from_apex(apex, pt):
    return math.atan2(pt[1] - apex[1], pt[0] - apex[0])


def point_at_angle(apex, angle, length):
    return (apex[0] + math.cos(angle) * length, apex[1] + math.sin(angle) * length)


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


numFrames = 72
os.makedirs("output/frames_instant_grep_v3", exist_ok=True)

for frame in range(numFrames):
    t = frame / (numFrames - 1)
    progress = ease_in_out_cubic(t)

    newPage(CANVAS_W, CANVAS_H)
    fill(1)
    rect(0, 0, CANVAS_W, CANVAS_H)
    stroke(0)
    strokeWidth(2)
    lineJoin("miter")
    fill(None)

    for pts in POLYLINES:
        apex = pts[1]
        end0 = pts[0]
        end2 = pts[2]

        a0 = angle_from_apex(apex, end0)
        a2 = angle_from_apex(apex, end2)
        mid_angle = (a0 + a2) / 2

        if abs(a0 - a2) > math.pi:
            mid_angle += math.pi

        cur_a0 = lerp(mid_angle, a0, progress)
        cur_a2 = lerp(mid_angle, a2, progress)

        len0 = dist(apex, end0)
        len2 = dist(apex, end2)

        cur_end0 = point_at_angle(apex, cur_a0, len0)
        cur_end2 = point_at_angle(apex, cur_a2, len2)

        p_apex = tx(*apex)
        p0 = tx(*cur_end0)
        p2 = tx(*cur_end2)

        path = BezierPath()
        path.moveTo(p0)
        path.lineTo(p_apex)
        path.lineTo(p2)
        drawPath(path)

    saveImage(f"output/frames_instant_grep_v3/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_instant_grep_v3/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/instant_grep_v3.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,
    loop=0,
)
print(f"Saved instant_grep_v3.gif ({numFrames} frames)")
