# RECEIVER CODE
# Make sure there is a device set up as a SENDER that is connecting to the same
# advertisement.complete_name that you see below. This example has
# advertisement.complete_name = "profg-r" but you should change that to whatever
# you set your receiver_name equal to in the code.py file on your SENDER CPB.
# This code will receive messages from touchpads on the SENDER CPB
# Pressing a CPB touchpad: 1, 2, 3, 4, 5, 6, or TX - will send  a similarly indexed
# ButtonPacket for the first 7 buttons listed in the list named
# bluefruit_buttons, below: ButtonPacket.BUTTON_1 through 4, UP, DOWN, and LEFT).
# Pressing Button_A on the SENDER CPB will send the 8th bluefruit_buttons, ButtonPacket.RIGHT.
# When any of the pads or Button_A are released, a ColorPacket of color (0, 0, 0) is sent
# and the code below will use that packet to turn the lights turn off.
# Pressing Button_B on the SENDER CPB will allow the user to input text in the serial console
# and press return to send it. The text that is sent will print in the serial console of the RECEIVER
# if its code is running in Mu & the serial console is open.

import board, neopixel, digitalio

# ================================
# BLUETOOTH SETUP CODE & FUNCTIONS
# ================================

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket

# Setup BLE connection
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
# Give your CPB a unique name between the quotes below.
# This MUST be the same name - same spelling & capitalization
# as the name in the "receiver_name = " line in the SENDER's code.py file.
# VERY IMPORTANT - the name must also be <= 11 characters!
advertisement.complete_name = "profg-r"
ble.name = advertisement.complete_name

# === END OF BLUETOOTH SETUP CODE & FUNCTIONS ===


# SET UP AUDIO FOR THE CPB
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

# to play a sound, call the play_sound function & pass in a
# filename as a string. Be sure to include the extension, e.g. "splat.wav")
def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass

# set up a list for my drum_sounds
drum_sounds = ["bass_hit_c.wav",
                "bd_tek.wav",
                "bd_zome.wav",
                "drum_cowbell.wav",
                "elec_cymbal.wav",
                "elec_hi_snare.wav",
                "scratch.wav",
                "splat.wav"]


# SET UP THE 10 NEOPIXELS ON THE CPB. NAME THEM PIXELS
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

# SET UP COLORS & A COLORS LIST
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

# CREATE AN ARRAY OF THESE COLORS
colors = [RED, MAGENTA, ORANGE, YELLOW, GREEN, JADE, BLUE, INDIGO, VIOLET, PURPLE, WHITE, BLACK]


# These are the ButtonPacket codes that are the same as the 8 buttons on the Bluefruit App
bluefruit_buttons = [ButtonPacket.BUTTON_1, ButtonPacket.BUTTON_2, ButtonPacket.BUTTON_3,
            ButtonPacket.BUTTON_4, ButtonPacket.UP, ButtonPacket.DOWN,
            ButtonPacket.LEFT, ButtonPacket.RIGHT]

print("Running Receiver Code!") 
while True:
    ble.start_advertising(advertisement)  # Start advertising.
    print(f"Advertising as: {advertisement.complete_name}") # Name prints once each time the board isn't connected
    was_connected = False

    while not was_connected or ble.connected:
        if ble.connected:  # If BLE is connected...
            was_connected = True

            if uart.in_waiting:  # Check to see if any new data has been sent from the SENDER.
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
                elif isinstance(packet, ColorPacket):
                    pixels.fill(packet.color)
                elif isinstance(packet, RawTextPacket):
                    print(f"Message Received: {packet.text.decode().strip()}")

    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
