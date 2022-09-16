import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php


# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Set buttom
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


x1 = 0
x2 = 0
y1=5
y2=30

def clockWise():
    # Draw a black filled box to clear the image.
    global x1, x2, y1, y2    
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if x1 < 130  and y1 == 5:
        x1 += 10
    elif y1 < 70 and x1 == 130 :
        y1 += 5
    elif y1 == 70 and x1 > 0:
        x1 -= 10
    elif x1 == 0 and y1 <= 70:
        y1 -= 5

    random_number = random.randint(10,30)

    font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", random_number)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py
    random_color= "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    draw.text((x1,y1), time.strftime("%a %d %H:%M" ), font=font1, fill=random_color)

def counterClockWise():
    # Draw a black filled box to clear the image.
    global x1, x2, y1, y2    
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    random_x = random.randint(5,15)
    random_y = random.randint(5,15)
    if x1 == 0 and y1 < 70:
        y1 += 5    
    elif y1 == 70 and x1 < 130:
        x1 += 10
    elif x1 <= 130 and y1 == 0:
        x1 -= 10
    elif y1 <= 70 and x1 == 130:
        y1 -= 5


    random_number = random.randint(10,30)

    font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", random_number)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py
    random_color= "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    draw.text((x1,y1), time.strftime("%a %d %H:%M" ), font=font1, fill=random_color)

while True:
    
    if not buttonA.value:
        clockWise()
    if not buttonB.value:
        counterClockWise()
    # Display image.
    disp.image(image, rotation)
    time.sleep(0.03)