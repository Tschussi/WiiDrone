import cwiid, time, smbus

# Constants
START_TIME = 0
STOP_LOWER_LIMIT = 819
STOP_UPPER_LIMIT = 1638
# Variables
rightStopTime = STOP_LOWER_LIMIT
leftStopTime = STOP_LOWER_LIMIT
button_delay = 0.2
check = 0
# I2C & Servo Hat set up 
bus = smbus.SMBus(1)
addr = 0x40 # sudo i2cdetect -y 1
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)
# PWM start & stop time setup
bus.write_word_data(addr, 0x36, START_TIME) # Ch12
bus.write_word_data(addr, 0x3A, START_TIME) # Ch13
bus.write_word_data(addr, 0x3E, START_TIME) # Ch14
bus.write_word_data(addr, 0x42, START_TIME) # Ch15
bus.write_word_data(addr, 0x38, STOP_LOWER_LIMIT)
bus.write_word_data(addr, 0x3C, STOP_LOWER_LIMIT)
bus.write_word_data(addr, 0x40, STOP_LOWER_LIMIT)
bus.write_word_data(addr, 0x44, STOP_LOWER_LIMIT)
# WiiMote set up

print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
  quit()

print 'Wiimote connection established!\n'
print '********Controls*********'
print 'D-Pad Controls Movement'
print 'Hold A to control movement with motion'
print 'Press PLUS and MINUS together to disconnect and quit.'
print '*************************'

time.sleep(3)

wii.rpt_mode = cwiid.RPT_BTN

while True:

  buttons = wii.state['buttons']

  # Detects whether + and - are held down and if they are it quits the program
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print '\nClosing connection ...'
    # NOTE: This is how you RUMBLE the Wiimote
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)  

  # The following code controls the signals of pwms for flying a drone based on wiimote inputs
  if (buttons & cwiid.BTN_LEFT):
    if (leftStopTime > STOP_LOWER_LIMIT + 10):
      bus.write_word_data(addr, 0x38, leftStopTime-10)
      bus.write_word_data(addr, 0x3C, leftStopTime-10)
    if (rightStopTime > STOP_LOWER_LIMIT + 10):
      bus.write_word_data(addr, 0x40, rightStopTime+10)
      bus.write_word_data(addr, 0x44, rightStopTime+10)
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    if (leftStopTime > STOP_LOWER_LIMIT + 10):
      bus.write_word_data(addr, 0x38, leftStopTime+10)
      bus.write_word_data(addr, 0x3C, leftStopTime+10)
    if (rightStopTime > STOP_LOWER_LIMIT + 10):
      bus.write_word_data(addr, 0x40, rightStopTime-10)
      bus.write_word_data(addr, 0x44, rightStopTime-10)	
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    if (leftStopTime < STOP_UPPER_LIMIT - 10 & rightStopTime < STOP_UPPER_LIMIT - 10):
      leftStopTime = leftStopTime + 10
      rightStopTime = rightStopTime + 10
    bus.write_word_data(addr, 0x38, leftStopTime)
    bus.write_word_data(addr, 0x3C, leftStopTime)
    bus.write_word_data(addr, 0x40, rightStopTime)
    bus.write_word_data(addr, 0x44, rightStopTime)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    if (leftStopTime > STOP_LOWER_LIMIT + 10 & rightStopTime > STOP_LOWER_LIMIT + 10):
      leftStopTime = leftStopTime - 10
      rightStopTime = rightStopTime - 10
    bus.write_word_data(addr, 0x38, leftStopTime)
    bus.write_word_data(addr, 0x3C, leftStopTime)
    bus.write_word_data(addr, 0x40, rightStopTime)
    bus.write_word_data(addr, 0x44, rightStopTime)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    accel = wii.state['acc']
    print(accel)
    if accel[1] < 125:
      print 'Increase Duty Cycle'
    elif accel[1] > 135:
      print 'Decrease Duty Cycle'
    if accel[0] < 125:
      print 'Decrease Left Motors Duty Cycle'
    elif accel[0] > 135:
      print 'Decrease Right Motors Duty Cycle'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_B):	
    bus.write_word_data(addr, 0x38, STOP_LOWER_LIMIT)
    bus.write_word_data(addr, 0x3C, STOP_LOWER_LIMIT)
    bus.write_word_data(addr, 0x40, STOP_LOWER_LIMIT)
    bus.write_word_data(addr, 0x44, STOP_LOWER_LIMIT)
    time.sleep(button_delay)
