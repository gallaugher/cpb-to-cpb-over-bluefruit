# RECEIVER CODE
# Make sure there is a device set up as a SENDER that is connecting to the same
# advertisement.complete_name = "profg-r" name that you see below.
# This code will receive messages from touchpads on the SENDER CPB
# The pad order 1, 2, 3, 4, 5, 6, TX - send the first 7 buttons listed
# in the button list below: bluefruit_buttons
# Button_A on the SENDER CPB will send the 8th button ButtonPacket.RIGHT
# When any of the pads or Button_A are released, the lights turn off.
# Pressing Button_B on the SENDER CPB will allow the user to input text in the serial console
# and press return to send it. The text sent will print in the serial console of the RECEIVER
# if it is running in Mu & the serial console is open.

import board, neopixel, digitalio

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket

# import lines needed to play sound files
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

# set up the speaker
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True
audio = AudioOut(board.SPEAKER)

# set path where sound files can be found
path = "drumSounds/"

# set up a list for my drum_sounds
drum_sounds = ["bass_hit_c.wav",
                "bd_tek.wav",
                "bd_zome.wav",
                "drum_cowbell.wav",
                "elec_cymbal.wav",
                "elec_hi_snare.wav",
                "scratch.wav",
                "splat.wav"]

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

ble_radio = BLERadio()
ble_radio.name = advertisement.complete_name

def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass

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
                                play_sound(drum_sounds[i])
                elif isinstance(packet, RawTextPacket):
                    print(f"Message Received: {packet.text.decode().strip()}")
                elif isinstance(packet, ColorPacket):
                    pixels.fill(packet.color)
    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
