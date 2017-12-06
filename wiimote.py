# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following lines of code demonstrate many of the features realted to wiimotes, such as capturing button presses and rumbling the controller.
# I have managed to map the home button to the accelerometer - simply hold it and values will appear!

# Original Code by The Raspberry Pi Guy (IR code not included). Work based on some of Matt Hawkins's! 

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
print 'Go ahead and press some buttons\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

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

  # The following code detects whether any of the Wiimotes buttons have been pressed and then prints a statement to the screen!
  if (buttons & cwiid.BTN_LEFT):
    print 'Left pressed'
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    print 'Up pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    print 'Button A pressed'
    wii.rpt_mode = cwiid.RPT_IR
    time.sleep(1)
    ir_sensor = wii.state['ir_src']
        
    if ir_sensor[0] is None:
      x0 = -1
      y0 = -1
    else:    
      ir0 = ir_sensor[0]
      x0,y0 = ir0['pos']
        
    if ir_sensor[1] is None:
      x1 = -1
      y1 = -1
    else:  
      ir1 = ir_sensor[1]
      x1,y1 = ir1['pos']
        
    if ir_sensor[2] is None:
      x2 = -1
      y2 = -1
    else:  
      ir2 = ir_sensor[2]
      x2,y2 = ir2['pos']
        
    if ir_sensor[3] is None:
      x3 = -1
      y3 = -1
    else:  
      ir3 = ir_sensor[3]
      x3,y3 = ir3['pos']
        
    x = [x0,x1,x2,x3]
    y = [y0,y1,y2,y3]
    count = 0
    avgx = 0
    avgy = 0
    for i in range (0,4):
      print x[i],y[i]
      if x[i] != -1:
        avgx = avgx + x[i]
        avgy = avgy + y[i]
        count = count + 1
    if count > 0:
      avgx = avgx / count
      avgy = avgy / count
      print 'Average Level {0}, {1}'.format(avgx,avgy)
    else:
      print 'No IR LEDs detected'
        
    wii.rpt_mode = cwiid.RPT_BTN
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_B):
    print 'Button B pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_HOME):
    print 'Home button pressed'
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    check = 0
    while check == 0:
      print(wii.state['acc'])
      time.sleep(0.01)
      check = (buttons & cwiid.BTN_HOME)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    print 'Minus Button pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    print 'Plus Button pressed'
    time.sleep(button_delay)
