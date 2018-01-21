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
lut = [[], []]
lut[0] = [[[], []], [[], []]]
lut[1] = [[[], []], [[], []]]
lut[0][0][0] = 'r'
lut[0][0][1] = 'b'
lut[0][1][0] = 't'
lut[0][1][1] = 'l'
lut[1][0][0] = 'u'
lut[1][0][1] = 'd'
lut[1][1][0] = 'l'
lut[1][1][1] = 'a'


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

    if curPrice >= prevPrice:
        priceUpDown = 1
    else:
        priceUpDown = 0

    prevGrad = curGrad
    curGrad = curPrice - prevPrice
    if curGrad >= prevGrad:
        gradUpDown = 1
    else:
        gradUpDown = 0

    prevConc = curConc
    curConc = curGrad - prevGrad
    if curConc >= prevConc:
        concUpDown = 1
    else:
        concUpDown = 0

    
    # Make keypress
    keyboard.press_key(lut[priceUpDown][gradUpDown][concUpDown])
    time.sleep(0.5)
    keyboard.release_key(lut[priceUpDown][gradUpDown][concUpDown])
    print("Current price: " + str(curPrice) + " - key: " + str(lut[priceUpDown][gradUpDown][concUpDown]))
