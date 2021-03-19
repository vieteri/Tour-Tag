from flask import Flask
from flask import render_template, request
import time
import colorsys
import time
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd

FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)

lines = ["aloitus",
         "5",
         "4",
         "3",
         "2",
         "1"]


    








app = Flask(__name__)

def hat(lines):
    colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x / float(len(lines)), 1.0, 1.0)]) for x in range(len(lines))]
    unicornhathd.rotation(270)
    unicornhathd.brightness(0.6)

    width, height = unicornhathd.get_shape()

    text_x = width
    text_y = 2

    font_file, font_size = FONT

    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = width, 0
    try:
        
        for line in lines:
            w, h = font.getsize(line)
            text_width += w + width
            text_height = max(text_height, h)

        text_width += width + text_x + 1

        image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        offset_left = 0

        for index, line in enumerate(lines):
            draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

            offset_left += font.getsize(line)[0] + width

        for scroll in range(text_width - width):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x + scroll, y))
                    r, g, b = [int(n) for n in pixel]
                    unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

            unicornhathd.show()
            time.sleep(0.01)

    except : #KeyboardInterrupt
        unicornhathd.off()

    finally:
        unicornhathd.off()
        return 'true'
    
aloitus=hat(lines)
print ("DOne")

a=1
@app.route("/")
def index():
    return render_template('test.html')

@app.route('/kokkola')
def left_side():
    data1="LEFT"
    print (data1)
    lines=["Kokkola"]
    hat (lines)
    return 'true'

@app.route('/pori')
def right_side():
   data1="RIGHT"
   lines=["Pori"]
   hat (lines)
   return 'true'

@app.route('/vaasa')
def up_side():
   data1="FORWARD"
   lines=["Vaasa"]
   hat (lines)
   return 'true'

@app.route('/oulu')
def down_side():
   data1="BACK"
   lines=["Oulu"]
   hat (lines)
   return 'true'

@app.route('/stop')
def stop():
   data1="STOP"

   return  'true'

if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)
