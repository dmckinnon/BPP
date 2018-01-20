#!/usr/bin/python
from exchanges.bitfinex import Bitfinex
import time
from pykeyboard import PyKeyboard

# initialise keyboard input
keyboard = PyKeyboard()

# Previous and current value
prevPrice = 0
curPrice = 0
priceUpDown = 0

# Previous and current 1st derivative
prevGrad = 0
curGrad = 0
gradUpDown = 0

# Previous and current 2nd derivative
prevConc = 0
curConc = 0
concUpDown = 0

# Lookup table
# actual keypresses depend on the emulator
lut[] = {[], []}
lut[0] = {[[], []], [[], []]}
lut[1] = {[[], []], [[], []]}
lut[0][0][0] = 'a'
lut[0][0][1] = 
lut[0][1][0] = 
lut[0][1][1] = 
lut[1][0][0] = 
lut[1][0][1] = 
lut[1][1][0] = 
lut[1][1][1] = 


# Query prices, make keypresses
while(True):
    time.sleep(2)

    # compute new values
    prevPrice = curPrice
    try:
        curPrice = Bitfinex().get_current_price()
    except Exception as e:
        # if they don't like querying too much, wait a bit
        # What would be better is to read the http message and check the allowed rate
        # but eh for now
        time.sleep(60)
    

    prevGrad = curGrad
    curGrad = curPrice - prevPrice

    prevConc = curConc
    curConc =- curGrad - prevGrad 
    
    # Make keypress

    # Print stats
    print ("Current price: " + str(curPrice))
    dir = "up"
    if (curPrice <= prevPrice):
        dir = "down"
        keyboard.tap_key('d')
    else:
        keyboard.tap_key('u')
    print ("Price has gone " + dir)
