from drawbot_skia.drawbot import *
from math import pi, sin
from PIL import Image
import os

def lissajous(a, b, phase, radius):
    numSteps = 340
    points = []
    for i in range(numSteps):
        angle = 2 * pi * i / numSteps
        x = radius * sin(a * angle + phase)
        y = -radius * sin(b * angle)
        points.append((x, y))
    return points


canvasSize = 500
numFrames = 72
numShapes = 5
gridSize = canvasSize / numShapes
radius = 0.375 * gridSize

os.makedirs("output/frames", exist_ok=True)

for frame in range(numFrames):
    t = frame / numFrames
    newPage(canvasSize, canvasSize)

    fill(1)
    rect(0, 0, canvasSize, canvasSize)

    stroke(0)
    strokeWidth(2)
    lineJoin("round")
    fill(None)

    for a in range(1, numShapes + 1):
        for b in range(1, numShapes + 1):
            with savedState():
                translate(gridSize * a - 0.5 * gridSize,
                        canvasSize - gridSize * b + 0.5 * gridSize)
                points = lissajous(b, a, 2 * pi * t, radius)
                polygon(*points)

    saveImage(f"output/frames/frame_{frame:03d}.png")
    newDrawing()

# Stitch frames into animated GIF
frames = []
for i in range(numFrames):
    img = Image.open(f"output/frames/frame_{i:03d}.png")
    frames.append(img.copy())
    img.close()

frames[0].save(
    "output/LissajousGrid.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50,
    loop=0,
)

print(f"Saved animated GIF ({numFrames} frames)")

# Also save a single frame preview
saveImage("output/LissajousGrid.png")
print("Saved single frame PNG")
