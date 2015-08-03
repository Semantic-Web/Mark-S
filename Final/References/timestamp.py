#!/usr/bin/env python2.7
# import necessary modules
import datetime, csv
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# write header for timestamp event file
ts_fieldnames = ['date', 'event', 'value']
occ_state = False
tv_state = False
with open('TIMESTAMPS_ALL_EVENTS_2015_07_19.csv', 'w') as tsfile:
    ts_writer = csv.DictWriter(tsfile, fieldnames=ts_fieldnames)
    ts_writer.writeheader()
    
    
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected
# write timestamp event to timestamp event file, console
def occ_callback(channel):
    global occ_state
    occ_state  = not occ_state
    print "ocupancy event " + str(int(occ_state)) + " detected at " + str(datetime.datetime.now())
    with open('TIMESTAMPS_ALL_EVENTS_2015_07_19.csv', 'a') as tsfile:
        ts_writer = csv.DictWriter(tsfile, fieldnames=ts_fieldnames)
        ts_writer.writerow({'date': str(datetime.datetime.now()), 'event': 'occ', 'value': str(int(occ_state))})

def tv_callback(channel):
    global tv_state
    tv_state = not tv_state
    print "tv event " + str(int(tv_state)) + " detected at " + str(datetime.datetime.now())
    with open('TIMESTAMPS_ALL_EVENTS_2015_07_19.csv', 'a') as tsfile:
        ts_writer = csv.DictWriter(tsfile, fieldnames=ts_fieldnames)
        ts_writer.writerow({'date': str(datetime.datetime.now()), 'event': 'tv', 'value': str(int(tv_state))})

print "Make sure you have a button connected so that when pressed"
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"
print "You will also need a second button connected so that when pressed"
print "it will connect GPIO port 24 (pin 18) to 3V3 (pin 1)\n"
print "You will also need a third button connected so that when pressed"
print "it will connect GPIO port 17 (pin 11) to GND (pin 14)"
raw_input("Press Enter when ready\n>")

# when a falling edge is detected on port 17, regardless of whatever 
# else is happening in the program, the function occ_callback will be run
GPIO.add_event_detect(17, GPIO.FALLING, callback=occ_callback, bouncetime=1000)

# when a falling edge is detected on port 23, regardless of whatever 
# else is happening in the program, the function my_callback2 will be run
GPIO.add_event_detect(23, GPIO.FALLING, callback=tv_callback, bouncetime=1000)

try:
    print "Waiting for rising edge on port 24"
    GPIO.wait_for_edge(24, GPIO.RISING)
    print "Rising edge detected on port 24. Here endeth the third lesson."

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
