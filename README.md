# cpb-to-cpb-over-bluefruit
Use two CircuitPlayground Bluefruits, one to send messages over Bluetooth, the other to receive &amp; respond to them. Using CircuitPython

Use two CircuitPlayground Bluefruits. Save sender code to one device as code.py, save receiver code to the other as code.py.
Code currently responds by pressing touchpads on the CPB (debounced), as well as the two buttons built into the CPB.

Each pad sends a ButtonPacket with a name identical to what would be sent by the Adafruit Bluefruit Connect app (e.g. BUTTON_1 through BUTTON_4, and UP, DOWN, LEFT.
Button_A sends the RIGHT button press.
Releasing a pad or Button_A will send a ColorPacket of (0, 0, 0) to turn all pixels on Receiver off.
Receiver is coded so that when ButtonPackets are received, they plan a sound & color.

Button B will prompt user to enter text which is sent to Receiver & will be displayed in the console if Receiver code is running in Mu.

Be sure to drag the drumSounds folder onto the RECEIVER CPB.

Want to send a potentiomter value as a color? The file "Send Potentiometer As Color" shows how you can do this by hooking a potentiometer to board.A1 on a CPB. Nothing in the Reciever Code file would need to be changed. More information in the comments of the "Send Potentiometer As Color" file.
