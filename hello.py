from drawbot_skia.drawbot import *

newPage(1000, 1000)

# background
fill(0.05, 0.05, 0.1)
rect(0, 0, 1000, 1000)

# circle
fill(1, 0.35, 0.2)
oval(300, 300, 400, 400)

# text
fill(1)
font("Helvetica")
fontSize(72)
text("hello drawbot", (160, 150))

saveImage("output/hello.png")
print("Saved to output/hello.png")
