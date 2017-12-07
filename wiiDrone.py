import cwiid, time, smbus

# Constants
START_TIME = 0
STOP_LOWER_LIMIT = 819
STOP_UPPER_LIMIT = 1638
MTR1 = 0x44 # Ch15 end address 
MTR2 = 0x34 # Ch11 ..
MTR3 = 0x14 # Ch3 ..
MTR4 = 0x24 # Ch7 ..
INCREMENT = 3
BUTTON_DELAY = 0.2
HOVER = 1000
ADDR = 0x40 # I2C address: sudo i2cdetect -y 1

# Variables
rightStopTime = STOP_LOWER_LIMIT
leftStopTime = STOP_LOWER_LIMIT

# I2C & Servo Hat set up 
bus = smbus.SMBus(1)
bus.write_byte_data(ADDR, 0, 0x20)
bus.write_byte_data(ADDR, 0xfe, 0x1e)

# PWM start & stop time setup
bus.write_word_data(ADDR, 0x42, START_TIME) # Ch15 Start 
bus.write_word_data(ADDR, 0x32, START_TIME) # Ch11 ..
bus.write_word_data(ADDR, 0x12, START_TIME) # Ch3 ..
bus.write_word_data(ADDR, 0x22, START_TIME) # Ch7 ..
bus.write_word_data(ADDR, MTR1, STOP_LOWER_LIMIT)
bus.write_word_data(ADDR, MTR2, STOP_LOWER_LIMIT)
bus.write_word_data(ADDR, MTR3, STOP_LOWER_LIMIT)
bus.write_word_data(ADDR, MTR4, STOP_LOWER_LIMIT)

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
print 'Press B to kill motors'
print 'Press 1 to set motors to max power' 
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
  if (buttons & cwiid.BTN_LEFT): # Tilt Left
    if (leftStopTime > STOP_LOWER_LIMIT + INCREMENT):
      leftStopTime = leftStopTime - INCREMENT
      bus.write_word_data(ADDR, MTR1, leftStopTime)
      bus.write_word_data(ADDR, MTR2, leftStopTime)
    if (rightStopTime < STOP_UPPER_LIMIT - INCREMENT):
      rightStopTime = rightStopTime + INCREMENT
      bus.write_word_data(ADDR, MTR3, rightStopTime)
      bus.write_word_data(ADDR, MTR4, rightStopTime)
    time.sleep(BUTTON_DELAY)

  if(buttons & cwiid.BTN_RIGHT): # Tilt Right
    if (leftStopTime < STOP_UPPER_LIMIT - INCREMENT):
      leftStopTime = leftStopTime + INCREMENT
      bus.write_word_data(ADDR, MTR1, leftStopTime)
      bus.write_word_data(ADDR, MTR2, leftStopTime)
    if (rightStopTime > STOP_LOWER_LIMIT + INCREMENT):
      rightStopTime = rightStopTime - INCREMENT
      bus.write_word_data(ADDR, MTR3, rightStopTime)
      bus.write_word_data(ADDR, MTR4, rightStopTime)	
    time.sleep(BUTTON_DELAY)

  if (buttons & cwiid.BTN_UP): # Increase Vertical speed
    if (leftStopTime < STOP_UPPER_LIMIT - INCREMENT and rightStopTime < STOP_UPPER_LIMIT - INCREMENT):
      leftStopTime = leftStopTime + INCREMENT
      rightStopTime = rightStopTime + INCREMENT
    bus.write_word_data(ADDR, MTR3, rightStopTime+15)
    bus.write_word_data(ADDR, MTR4, rightStopTime)
    bus.write_word_data(ADDR, MTR2, leftStopTime)
    bus.write_word_data(ADDR, MTR1, leftStopTime)
    print leftStopTime, rightStopTime
    time.sleep(BUTTON_DELAY)

  if (buttons & cwiid.BTN_DOWN): # Decrease Vertical speed
    if (leftStopTime > STOP_LOWER_LIMIT + INCREMENT and rightStopTime > STOP_LOWER_LIMIT + INCREMENT):
      leftStopTime = leftStopTime - INCREMENT
      rightStopTime = rightStopTime - INCREMENT
    bus.write_word_data(ADDR, MTR1, leftStopTime)
    bus.write_word_data(ADDR, MTR2, leftStopTime)
    bus.write_word_data(ADDR, MTR3, rightStopTime)
    bus.write_word_data(ADDR, MTR4, rightStopTime)
    print leftStopTime, rightStopTime
    time.sleep(BUTTON_DELAY)

  if (buttons & cwiid.BTN_A): # Drone Movement with accelerometer readings
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    accel = wii.state['acc']
    print(accel)
    
    if accel[1] > 135: # Vertical movement 3 speeds for both up and down
      if accel[1] > 142:
        if accel[1] > 149:
          print 'Down Level 3'
          rightStopTime = HOVER - 3 * INCREMENT
          leftStopTime = HOVER - 3 * INCREMENT
        else:
          print 'Down Level 2'
          rightStopTime = HOVER - 2 * INCREMENT
          leftStopTime = HOVER - 2 * INCREMENT
      else:
        print 'Down Level 1'
        rightStopTime = HOVER - INCREMENT
        leftStopTime = HOVER - INCREMENT 
    elif accel[1] < 125:
      if accel[1] < 118:
        if accel[1] < 111:
          print 'Up Level 3'
          rightStopTime = HOVER + 3 * INCREMENT
          leftStopTime = HOVER + 3 * INCREMENT
        else:
          print 'Up Level 2'
          rightStopTime = HOVER + 2 * INCREMENT
          leftStopTime = HOVER + 2 * INCREMENT
      else:
        print 'Up Level 3'
        rightStopTime = HOVER + INCREMENT
        leftStopTime = HOVER + INCREMENT 
    else:
      print 'Hover'
      rightStopTime = HOVER
      leftStopTime = HOVER
    
    if accel[0] < 125: # Horizontal Movement 3 speeds for both left and right
      if accel[0] < 118:
        if accel[0] < 111:
          print 'Left Level 3'
          rightStopTime = rightStopTime + 3 * INCREMENT
          leftStopTime = leftStopTime - 3 * INCREMENT
        else:
          print 'Left Level 2'
          rightStopTime = rightStopTime + 2 * INCREMENT
          leftStopTime = leftStopTime + 2 * INCREMENT
      else:
        print 'Left Level 1'
        rightStopTime = rightStopTime + INCREMENT
        leftSTOPTIME = leftStopTime + INCREMENT
    elif accel[0] > 135:
      if accel[0] > 142:
        if accel[0] > 149:
          print 'Right Level 3'
          rightStopTime = rightStopTime - 3 * INCREMENT
          leftStopTime = leftStopTime + 3 * INCREMENT
        else:
          print 'Right Level 2'
          rightStopTime = rightStopTime - 2 * INCREMENT
          leftStopTime = leftStopTime + 2 * INCREMENT
      else:
        print 'Right Level 1'
        rightStopTime = rightStopTime - INCREMENT
        leftSTOPTIME = leftStopTime + INCREMENT
    
    bus.write_word_data(ADDR, MTR1, leftStopTime)
    bus.write_word_data(ADDR, MTR2, leftStopTime)
    bus.write_word_data(ADDR, MTR3, rightStopTime)
    bus.write_word_data(ADDR, MTR4, rightStopTime)    
    time.sleep(BUTTON_DELAY)

  if (buttons & cwiid.BTN_B): # Kill Motors
    bus.write_word_data(ADDR, MTR1, STOP_LOWER_LIMIT)
    bus.write_word_data(ADDR, MTR2, STOP_LOWER_LIMIT)
    bus.write_word_data(ADDR, MTR3, STOP_LOWER_LIMIT)
    bus.write_word_data(ADDR, MTR4, STOP_LOWER_LIMIT)
    leftStopTime = STOP_LOWER_LIMIT
    rightStopTime = STOP_LOWER_LIMIT
    time.sleep(BUTTON_DELAY)
   
  if (buttons & cwiid.BTN_1): # Set Motors to max
    leftStopTime = leftStopTime + 50
    rightStopTime = rightStopTime + 50
    bus.write_word_data(ADDR, MTR1, leftStopTime)
    bus.write_word_data(ADDR, MTR3, rightStopTime+5)
    bus.write_word_data(ADDR, MTR2, leftStopTime)
    bus.write_word_data(ADDR, MTR4, rightStopTime)
    #bus.write_word_data(ADDR, MTR1, STOP_UPPER_LIMIT - INCREMENT)
    #bus.write_word_data(ADDR, MTR2, STOP_UPPER_LIMIT - INCREMENT)
    #bus.write_word_data(ADDR, MTR3, STOP_UPPER_LIMIT - INCREMENT)
    #bus.write_word_data(ADDR, MTR4, STOP_UPPER_LIMIT - INCREMENT)
    #leftStopTime = STOP_UPPER_LIMIT - INCREMENT
    #rightStopTime = STOP_UPPER_LIMIT - INCREMENT
    time.sleep(BUTTON_DELAY)
