# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import math

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont
from time import sleep


# Raspberry reset Pi pin configuration:
RST = 4

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3c)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 128
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('VCR_OSD_MONO.ttf', 50)

# Write two lines of text.

def display_playing(current_track, max_track, percentage):

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    font = ImageFont.truetype('VCR_OSD_MONO.ttf', 50)
    if (current_track < 10):
        draw.text((x+25, top+5), str(current_track),  font=font, fill=255)
    else:
        draw.text((x+0, top+5), str(current_track),  font=font, fill=255)
    font = ImageFont.truetype('VCR_OSD_MONO.ttf', 25)
    draw.text((x+65, top+25), "/ " + str(max_track),  font=font, fill=255)
    
    #Draw the progressbar
    percentage = percentage*1.28
    percentage = math.trunc(percentage)
    draw.rectangle((0, 57, percentage, bottom), outline=1010, fill=1)
    
    disp.image(image)
    disp.display()

def show_counting():
    counter = 0


    while (counter < 20):
        counter=counter+1
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        font = ImageFont.truetype('VCR_OSD_MONO.ttf', 50)
        if (counter < 10):
            draw.text((x+25, top+5), str(counter),  font=font, fill=255)
        else:
            draw.text((x+0, top+5), str(counter),  font=font, fill=255)
        font = ImageFont.truetype('VCR_OSD_MONO.ttf', 25)
        draw.text((x+65, top+25), "/ 20",  font=font, fill=255)
        #draw.line((x, bottom, x+shape_width, top), fill=255)
        draw.rectangle((x, 59, x+shape_width, bottom), outline=255, fill=1)
        
        disp.image(image)
        disp.display()
        sleep(1)



