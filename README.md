# cpb-to-cpb-over-bluefruit
Use two CircuitPlayground Bluefruits, one to send messages over Bluetooth, the other to receive &amp; respond to them. Using CircuitPython

Use two CircuitPlayground Bluefruits. Save sender code to one device as code.py, save receiver code to the other as code.py.
Code currently responds in only a limited way, but shows how you can send button presses & text input from the console from one device to the other. Lotsa of flexibility8 can be created from this basic code.

Now supports cap touch on sender. Each touch sends a button. Receiver interprets the button as a color & lights up NeoPixels.
Button A will turn all neopixels off.
Button B will prompt user to enter text which is sent to Receiver & will be displayed in the console if Receiver code is running in Mu.
