# RECEIVER CODE
# e.g. code on CPB wired to the sign

import board
import neopixel

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket


RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

# Setup BLE connection
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
# Give your CPB a unique name between the quotes below
# VERY IMPORTANT - must be < 11 characters!
advertisement.complete_name = "profg-r"

while True:
    ble.start_advertising(advertisement)  # Start advertising.
    print(f"Adveriting name as: {advertisement.complete_name}")
    was_connected = False
    while not was_connected or ble.connected:
        #if not blanked:  # If LED-off signal is not being sent...
            #pass
            #animations.animate()  # Run the animations.
        if ble.connected:  # If BLE is connected...
            was_connected = True
            if uart.in_waiting:  # Check to see if any data is available from the Remote Control.
                try:
                    packet = Packet.from_stream(uart)  # Create the packet object.
                except ValueError:
                    continue
                if isinstance(packet, ButtonPacket):  # If the packet is a button packet...
                    # Check to see if it's BUTTON_1 (which is being sent by the slide switch)
                    if packet.pressed:  # If the buttons on the Remote Control are pressed...
                        if packet.button == ButtonPacket.BUTTON_1:  # If button A is pressed...
                            print("BUTTON_1 was pressed")
                            print("This should be BUTTON_A")
                            pixels.fill(RED)
                        if packet.button == ButtonPacket.BUTTON_2:  # If Button B is pressed...
                            print("BUTTON_2 Pressed")
                            print("This should be BUTTON_B")
                            pixels.fill(BLUE)
                        if packet.button == ButtonPacket.BUTTON_3:
                            print("BUTTON_3 Pressed")
                        if packet.button == ButtonPacket.BUTTON_4:
                            print("BUTTON_4 Pressed")
                        if packet.button == ButtonPacket.UP:
                            print("UP was pressed")
                        if packet.button == ButtonPacket.DOWN:
                            pixels.fill(BLACK)
                elif isinstance(packet, RawTextPacket):
                    print(f"Message Received: {packet.text.decode().strip()}")
    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
