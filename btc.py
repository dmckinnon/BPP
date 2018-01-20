#!/usr/bin/python
from exchanges.bitfinex import Bitfinex
import time

# Previous and current value
prevPrice = 0
curPrice = 0

# Previous and current 1st derivative
prevGrad = 0
curGrad = 0

# Previous and current 2nd derivative
prevConc = 0
curConc = 0

# Right now, just print out price every 1/2 second

while(True):
	time.sleep(2)

	# compute new values
	prevPrice = curPrice
	try:
		curPrice = Bitfinex().get_current_price()
	except Exception as e:
		time.sleep(60)
	

	prevGrad = curGrad
	curGrad = curPrice - prevPrice

	prevConc = curConc
	curConc =- curGrad - prevGrad 
	
	# Print stats
	print ("Current price: " + str(curPrice))
	dir = "up"
	if (curPrice <= prevPrice):
		dir = "down"
	print ("Price has gone " + dir)