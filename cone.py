from drawbot_skia.drawbot import *
from math import pi, cos
from PIL import Image
import re
import os

SVG_W, SVG_H = 2057.65, 1821.5
CANVAS = 1000
PADDING = 50

scale_x = (CANVAS - 2 * PADDING) / SVG_W
scale_y = (CANVAS - 2 * PADDING) / SVG_H
sc = min(scale_x, scale_y)

off_x = (CANVAS - SVG_W * sc) / 2
off_y = (CANVAS - SVG_H * sc) / 2

def tx(x, y):
    return (x * sc + off_x, CANVAS - (y * sc + off_y))

APEX = (2.0, 1007.94)

ellipse_paths = [
    "M1879.78 1703.59C1978.01 1638.47 1822.34 1230.72 1532.08 792.842C1241.82 354.968 926.88 52.789 828.645 117.908C730.411 183.026 886.081 590.783 1176.34 1028.66C1466.61 1466.53 1781.55 1768.71 1879.78 1703.59Z",
    "M1235.25 1466.01C1295.41 1426.13 1189.55 1160.54 998.809 872.794C808.068 585.051 604.671 384.119 544.511 423.998C484.35 463.878 590.207 729.469 780.949 1017.21C971.691 1304.95 1175.09 1505.89 1235.25 1466.01Z",
    "M746.563 1282.13C787.946 1254.69 728.347 1091.94 613.443 918.6C498.54 745.263 371.844 626.984 330.461 654.417C289.077 681.849 348.677 844.606 463.58 1017.94C578.483 1191.28 705.179 1309.56 746.563 1282.13Z",
    "M368.271 1142.53C388.466 1129.14 359.377 1049.71 303.3 965.118C247.223 880.523 185.393 822.797 165.198 836.184C145.003 849.571 174.092 929.001 230.169 1013.6C286.246 1098.19 348.076 1155.92 368.271 1142.53Z",
]

line_paths = [
    "M819.38 125.988L2.00007 1007.94L1780.48 1693.17",
    "M1827.97 1329.46L2.00007 1007.94L1301.85 479.208",
    "M1593.53 888.378L2.00007 1007.94",
]

def parse_ellipse_points(d):
    tokens = re.findall(r'[MCLZmclz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d)
    points = []
    i = 0
    while i < len(tokens):
        cmd = tokens[i]
        i += 1
        if cmd == 'M':
            points.append((float(tokens[i]), float(tokens[i+1])))
            i += 2
        elif cmd == 'C':
            points.append((float(tokens[i]), float(tokens[i+1])))
            points.append((float(tokens[i+2]), float(tokens[i+3])))
            points.append((float(tokens[i+4]), float(tokens[i+5])))
            i += 6
        elif cmd == 'Z':
            pass
    return points

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_points(pts_a, pts_b, t):
    return [(lerp(a[0], b[0], t), lerp(a[1], b[1], t)) for a, b in zip(pts_a, pts_b)]

def draw_ellipse_from_points(pts, do_tx=True):
    path = BezierPath()
    p = [tx(x, y) if do_tx else (x, y) for x, y in pts]
    path.moveTo(p[0])
    path.curveTo(p[1], p[2], p[3])
    path.curveTo(p[4], p[5], p[6])
    path.curveTo(p[7], p[8], p[9])
    path.curveTo(p[10], p[11], p[0])
    path.closePath()
    drawPath(path)

def draw_svg_path(d):
    tokens = re.findall(r'[MCLZmclz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d)
    path = BezierPath()
    i = 0
    while i < len(tokens):
        cmd = tokens[i]
        i += 1
        if cmd == 'M':
            x, y = float(tokens[i]), float(tokens[i+1])
            path.moveTo(tx(x, y))
            i += 2
        elif cmd == 'C':
            x1, y1 = float(tokens[i]), float(tokens[i+1])
            x2, y2 = float(tokens[i+2]), float(tokens[i+3])
            x3, y3 = float(tokens[i+4]), float(tokens[i+5])
            path.curveTo(tx(x1, y1), tx(x2, y2), tx(x3, y3))
            i += 6
        elif cmd == 'L':
            x, y = float(tokens[i]), float(tokens[i+1])
            path.lineTo(tx(x, y))
            i += 2
        elif cmd == 'Z':
            path.closePath()
    drawPath(path)

def ease_out_cubic(t):
    return 1.0 - (1.0 - t) ** 3

# smallest to largest
ellipse_data = [parse_ellipse_points(d) for d in reversed(ellipse_paths)]
apex_points = [APEX] * 12

# keyframes: apex -> ellipse0 -> ellipse1 -> ellipse2 -> ellipse3
keyframes = [apex_points] + ellipse_data

numFrames = 60
os.makedirs("output/frames_cone", exist_ok=True)

for frame in range(numFrames):
    t = frame / (numFrames - 1)

    newPage(CANVAS, CANVAS)

    fill(0)
    rect(0, 0, CANVAS, CANVAS)

    stroke(1)
    strokeWidth(2)
    lineJoin("round")
    fill(None)

    for d in ellipse_paths:
        draw_svg_path(d)
    for d in line_paths:
        draw_svg_path(d)

    eased = ease_out_cubic(t)
    progress = eased * (len(keyframes) - 1)
    idx = min(int(progress), len(keyframes) - 2)
    local_t = progress - idx
    current_pts = lerp_points(keyframes[idx], keyframes[idx + 1], local_t)

    fade_in = min(t / 0.05, 1.0)
    fade_out = max(0, 1.0 - (t - 0.80) / 0.20) if t > 0.80 else 1.0
    alpha = fade_in * fade_out

    stroke(0xFF/255, 0x62/255, 0x00/255, alpha)
    strokeWidth(3)
    fill(None)
    draw_ellipse_from_points(current_pts, do_tx=True)

    saveImage(f"output/frames_cone/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_cone/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/cone.gif",
    save_all=True,
    append_images=frames[1:],
    duration=33,
    loop=0,
)

print(f"Saved cone.gif ({numFrames} frames)")
