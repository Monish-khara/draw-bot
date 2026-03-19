from drawbot_skia.drawbot import *
from math import pi, sin, cos
from PIL import Image
import os

def lissajous_points(a, b, phase, radius, numSteps=600):
    points = []
    for i in range(numSteps):
        angle = 2 * pi * i / numSteps
        x = radius * sin(a * angle + phase)
        y = -radius * sin(b * angle)
        points.append((x, y))
    return points

def lerp(a, b, t):
    return a + (b - a) * t

canvasSize = 1000
numFrames = 120
radius = canvasSize * 0.4
numSteps = 600
trimLength = 0.75

orange = (0xFF/255, 0x62/255, 0x00/255)
white = (1.0, 1.0, 1.0)

os.makedirs("output/frames_v2", exist_ok=True)

for frame in range(numFrames):
    t = frame / numFrames
    newPage(canvasSize, canvasSize)

    fill(0x31/255, 0x29/255, 0x28/255)
    rect(0, 0, canvasSize, canvasSize)

    lineCap("round")
    lineJoin("round")
    fill(None)

    with savedState():
        translate(canvasSize / 2, canvasSize / 2)
        points = lissajous_points(3, 5, 2 * pi * t, radius, numSteps)

        trimStart = int((t * numSteps * 2) % numSteps)
        segCount = int(trimLength * numSteps)

        for i in range(segCount - 1):
            idx0 = (trimStart + i) % numSteps
            idx1 = (trimStart + i + 1) % numSteps

            frac = i / (segCount - 1)
            r = lerp(orange[0], white[0], frac)
            g = lerp(orange[1], white[1], frac)
            b = lerp(orange[2], white[2], frac)

            stroke(r, g, b)
            strokeWidth(3)

            path = BezierPath()
            path.moveTo(points[idx0])
            path.lineTo(points[idx1])
            drawPath(path)

    saveImage(f"output/frames_v2/frame_{frame:03d}.png")
    newDrawing()

frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames_v2/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/Lissajous_solo.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50,
    loop=0,
)

print(f"Saved Lissajous_solo.gif ({numFrames} frames)")
