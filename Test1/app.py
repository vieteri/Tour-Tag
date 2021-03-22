from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
import time
import colorsys
import time
from sys import exit
from functools import wraps
from datetime import datetime

# try:
#     from PIL import Image, ImageDraw, ImageFont
# except ImportError:
#     exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

#import unicornhathd

FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)
global currentroute
currentroute=[]
lines = ["aloitus",
         "5",
         "4",
         "3",
         "2",
         "1"]

# basic Flask functions from https://circuitdigest.com/microcontroller-projects/web-controlled-raspberry-pi-surveillance-robot
# login functions from https://github.com/realpython/discover-flask
    


app = Flask(__name__)

#sercret key is required by login funtionality
app.secret_key="my toutag" #This should be imported from separate config file and be random key

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

############################################################################
# def hat(lines):
#     colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x / float(len(lines)), 1.0, 1.0)]) for x in range(len(lines))]
#     unicornhathd.rotation(270)
#     unicornhathd.brightness(0.6)

#     width, height = unicornhathd.get_shape()

#     text_x = width
#     text_y = 2

#     font_file, font_size = FONT

#     font = ImageFont.truetype(font_file, font_size)

#     text_width, text_height = width, 0
#     try:
        
#         for line in lines:
#             w, h = font.getsize(line)
#             text_width += w + width
#             text_height = max(text_height, h)

#         text_width += width + text_x + 1

#         image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
#         draw = ImageDraw.Draw(image)

#         offset_left = 0

#         for index, line in enumerate(lines):
#             draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

#             offset_left += font.getsize(line)[0] + width

#         for scroll in range(text_width - width):
#             for x in range(width):
#                 for y in range(height):
#                     pixel = image.getpixel((x + scroll, y))
#                     r, g, b = [int(n) for n in pixel]
#                     unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

#             unicornhathd.show()
#             time.sleep(0.01)

#     except : #KeyboardInterrupt
#         unicornhathd.off()

#     finally:
#         unicornhathd.off()
#         return 'true'
    
# aloitus=hat(lines)
##########################################################################
print ("DOne")
stopssouth=['oulu','kokkola','vaasa','pori','turku','helsinki','hamina']

a=1
@app.route("/")
@login_required
def index():
    return render_template('test.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route("/login", methods=['GET','POST'])
def login():
  error=None
  if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
      error ='Invalid credentials. Please try again.'
    else: 
      session['logged_in'] = True
      flash('You were just logged in')
      return redirect(url_for('index'))

  return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
  session.pop('logged_in', None)
  flash('You were just logged out')
  return redirect(url_for('welcome'))

#############################################################################################################################################################
""" Functions for starting the tour and selecting the to go and come back route """

# Start of the tour function and storing of the time 

starting_times = []
@app.route('/StartTour')
@login_required
def start_tour():
    global  starting_times
    now = datetime.now()
    print ('Tour start time is ',now)
    starting_times =  starting_times.append(now)   
    return  'true'

# Way to go and way back route selection 
ctrl = 0 
@app.route('/Input Route to go')
@login_required
def Input_Route():
    global ctrl
    ctrl = 1
    return 'true'

@app.route('/Input return Route')
@login_required
def Return_Route():
    ctrl = 2
    return 'true'

# Two lists are created where to store the route to go and come back 

global go_route 
global back_route 


#######################################################################################################################################################################
@app.route('/setroute' , methods=['POST'])
@login_required
def setroute():
    
    print ('setroute')
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        sourceindex=stopssouth.index(source)
        print ('source index ',sourceindex)
        destinationidex=stopssouth.index(destination)
        print ('destination index ',destinationidex)
        currentroute=[]
        i=1
        direction=[]
        if sourceindex > destinationidex:
          direction.append('north')

          i=sourceindex
          while i != destinationidex-1:
            x=stopssouth[i]
            currentroute.append(x)
            print (i)
            i-=1

        else:
          direction.append('south')

          i=sourceindex
          while i != destinationidex+1:
            x=stopssouth[i]
            print (x)
            currentroute.append(x)
            print (i)
            i+=1
        print (currentroute)


    print ('source')
    lines=currentroute
    #    hat (lines)
         
   ################################################################################    Added 
    if ctrl == 1:  # in this way it would be possible to store the two routes 
         go_route = go_route.append("Kokkola")
    elif ctrl == 2: 
         back_route = back_route.append("Kokkola")
    ##############################################################################  
         
    return redirect(url_for('start_tour'))



############################################################################################################################################################################
""" Timer function when stopping at the port. Asks the user to input the port at which they are stopping and then
stores the name of the port and time into two lists, also a countdown timer of 2h (stoppage time at the port) is started and should be printed to the LED matrix """

port_stops_time = []
stop_port = []
@app.route('/Port Stop',  methods=['POST'])
@login_required
def Port_stop(): 
    global port_stops_time
    global stop_port 
         
    now = datetime.now()
    port_stops_time =  port_stops_time.append(now)   
    port = request.form['port']
    stop_port = stop_port.append(port)
    t =  7200
    t = int(t)
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        data1="FORWARD"
        lines =[timer] # this should print the timer to the LEDs 
        #hat (lines)
        time.sleep(1) 
        t -= 1
    return 'true'


""" Uploading the data to the database """
@app.route('/End tour ~ Upload the data')
@login_required
def end_tour():
         # starting_times
         # port_stops_time 
         # stop_port  
         # go_route
         # back_route 
   return  'true'

##############################################################################################################################################################################
if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010, debug=True)
