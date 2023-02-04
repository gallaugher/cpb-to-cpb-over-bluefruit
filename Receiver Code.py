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
MAGENTA = (255, 0, 20)
ORANGE = (255, 40, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
JADE = (0, 255, 40)
BLUE = (0, 0, 255)
INDIGO = (63, 0, 255)
VIOLET = (127, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [RED, MAGENTA, ORANGE, YELLOW, GREEN, JADE, BLUE, INDIGO, VIOLET, PURPLE, BLACK]
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

bluefruit_buttons = [ButtonPacket.BUTTON_1, ButtonPacket.BUTTON_2, ButtonPacket.BUTTON_3,
            ButtonPacket.BUTTON_4, ButtonPacket.UP, ButtonPacket.DOWN,
            ButtonPacket.LEFT, ButtonPacket.RIGHT]

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
        if ble.connected:  # If BLE is connected...
            was_connected = True
            if uart.in_waiting:  # Check to see if any data is available from the Remote Control.
                try:
                    packet = Packet.from_stream(uart)  # Create the packet object.
                except ValueError:
                    continue
                # Note: I could have sennt ColorPackets that would have had colors, but I wanted
                # to show ButtonPackets because you could do non-color things here, too. For example,
                # if Button_1, then move a servo, if Button_2, then play a certain sound, etc.
                if isinstance(packet, ButtonPacket):  # If the packet is a button packet...
                    if packet.pressed:  # If the buttons on the Remote Control are pressed...
                        for i in range(len(bluefruit_buttons)):
                            if packet.button == bluefruit_buttons[i]:
                                print(f"Button Pressed: {i}")
                                pixels.fill(colors[i])
                elif isinstance(packet, RawTextPacket):
                    print(f"Message Received: {packet.text.decode().strip()}")
                elif isinstance(packet, ColorPacket):
                    pixels.fill(packet.color)
    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
