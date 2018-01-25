#!/usr/bin/python
from exchanges.bitfinex import Bitfinex
import time
from pykeyboard import PyKeyboard
import pygame

# initialise keyboard input
keyboard = PyKeyboard()

# initialise pygame for the graph
WIDTH = 100
HEIGHT = 50
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) # change screen size


# Previous and current value
prevPrevPrevPrice = 0
prevPrevPrice = 0
prevPrice = 0
curPrice = 0
priceUpDown = 0
prevPriceUpDown = 0
prevPrevPriceUpDown = 0

# Lookup table
# actual keypresses depend on the emulator
lut = [[], []]
lut[0] = [[[], []], [[], []]]
lut[1] = [[[], []], [[], []]]
lut[0][0][0] = 'r'
lut[0][0][1] = 'b'
lut[0][1][0] = 't'
lut[0][1][1] = 'a'
lut[1][0][0] = 'u'
lut[1][0][1] = 'd'
lut[1][1][0] = 'e'
lut[1][1][1] = 'l'


iterations = 0

thingsAreOk = True

# Query prices, make keypresses
done = False
while not done:
    time.sleep(1)

    # compute new values
    if thingsAreOk:
        prevPrevPrevPrice = prevPrevPrice
        prevPrevPrice = prevPrice
    
    prevPrice = curPrice

    try:
        curPrice = Bitfinex().get_current_price()
    except Exception as e:
        # if they don't like querying too much, wait a bit
        # What would be better is to read the http message and check the allowed rate
        # but eh for now
        time.sleep(60)

    if curPrice == prevPrice:
        thingsAreOk = False
        continue
    else:
        thingsAreOk = True


    if curPrice >= prevPrice:
        priceUpDown = 1
    else:
        priceUpDown = 0

    if prevPrice >= prevPrevPrice:
        prevPriceUpDown = 1
    else:
        prevPriceUpDown = 0

    if prevPrevPrice >= prevPrevPrevPrice:
        prevPrevPriceUpDown = 1
    else:
        prevPrevPriceUpDown = 0


    iterations += 1
    
    # Make keypress
    keyboard.press_key(lut[prevPrevPriceUpDown][prevPriceUpDown][priceUpDown])
    time.sleep(0.5)
    keyboard.release_key(lut[prevPrevPriceUpDown][prevPriceUpDown][priceUpDown])
    print("Current price: " + str(curPrice) + " - key: " + str(lut[prevPrevPriceUpDown][prevPriceUpDown][priceUpDown]))

    # Do pygame display
    screen.fill(0x000000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # scale the lines to fit in the screen
    point1 = (WIDTH-5, HEIGHT/2)
    point2 = (0.75*WIDTH, float(curPrice-prevPrice)+HEIGHT/2)
    point3 = (0.5*WIDTH, float(prevPrice-prevPrevPrice)+HEIGHT/2)
    point4 = (0.25*WIDTH, float(prevPrevPrice-prevPrevPrevPrice)+HEIGHT/2)
    point5 = (5, float(prevPrevPrice-prevPrevPrevPrice)+HEIGHT/2)
    points = [point1, point2, point3, point4, point5]
    pygame.draw.lines(screen, 0x00ff00, False, points, 2)

    pygame.display.update()
   # pygame.display.flip()
