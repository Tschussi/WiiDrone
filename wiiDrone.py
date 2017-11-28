import cwiid, time

button_delay = 0.1

print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
  quit()

print 'Wiimote connection established!\n'
print '********Controls*********\n'
print 'D-Pad Controls Movement\n'
print 'Hold A to control movement with motion\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'
print '*************************

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
    print 'Move Left'
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    print 'Move Right'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    print 'Move Up'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    print 'Move Down'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
	wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    check = 0
    while check == 0:
      accel = wii.state['acc']
	  print(accel)
	  if accel[1] < 125:
		print 'Increase Duty Cycle'
	  else if accel[1] > 135:
		print 'Decrease Duty Cycle'
	  if accel[0] < 125:
		print 'Decrease Left Moters Duty Cycle'
	  else if accel[0] > 135:
		print 'Decrease Right Motors Duty Cycle'
      time.sleep(0.1)
      check = (buttons & cwiid.BTN_A)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_B):
    print 'Button B pressed'
    time.sleep(button_delay)
