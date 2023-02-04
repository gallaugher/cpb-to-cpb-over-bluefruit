# Bluetooth to Bluetooth Sender Code (requires a BLE device running Receiver Code)
# Also note sender & receiver must also send / look for the same receiver_name,
# which you'll find in the line below named.
# Be sure to change to something unique & <11 chars in BOTH the sender & receiver code.py files.
# receiver_name = "profg-r"

import board, time, touchio, digitalio, neopixel
from adafruit_debouncer import Button

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket

from adafruit_bluefruit_connect.raw_text_packet import Packet

# Set up CPB built-in Buttons A & B
button_A_input = digitalio.DigitalInOut(board.BUTTON_A)
button_A_input.switch_to_input(digitalio.Pull.DOWN) # Note: Pull.UP for external buttons
button_A = Button(button_A_input, value_when_pressed = True) # NOTE: value_when_pressed = default False for external buttons

button_B_input = digitalio.DigitalInOut(board.BUTTON_B)
button_B_input.switch_to_input(digitalio.Pull.DOWN)
button_B = Button(button_B_input, value_when_pressed = True)

# name of device this remote is seeking:
receiver_name = "profg-r"

# Empty out button selection
button_selection = ""

def send_packet(uart_connection_name, packet):
    """Returns False if no longer connected."""
    print(f"The packet is: {packet}")
    try:
        uart_connection_name[UARTService].write(packet.to_bytes())
    except:  # pylint: disable=bare-except
        try:
            uart_connection_name.disconnect()
        except:  # pylint: disable=bare-except
            pass
        print("No longer connected")
        return False
    return True

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
# Give your CPB a unique name between the quotes below
advertisement.complete_name = "profg-sender"

uart_connection = None
# See if any existing connections are providing UARTService.
if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

while True:
    if not uart_connection or not uart_connection.connected:  # If not connected...
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):  # Scan...
            if UARTService in adv.services:  # If UARTService found...
                if adv.complete_name == receiver_name:
                    uart_connection = ble.connect(adv)  # Create a UART connection...
                    break # MUST include this here or code will never continue after connection.
        # Stop scanning whether or not we are connected.
        ble.stop_scan()  # And stop scanning.
    while uart_connection and uart_connection.connected:  # If connected...
        button_A.update()
        button_B.update() # VERY important to call .update() on EACH button before checking state
        if button_A.pressed: # if button is pressed
            print("button A pressed")
            button_selection = ButtonPacket.BUTTON_1
            if not send_packet(uart_connection,
                                   ButtonPacket(button_selection, pressed=True)):
                print(f"Just sent button {button_selection}")
        elif button_B.pressed:
            print("button B pressed")
            user_input = input("Enter text to send: ")+"\r\n"
            uart_connection[UARTService].write(user_input.encode())
            print(f"Just sent message {user_input}")
#                 print(f"Just sent button {button_selection}")
        elif button_A.released:
            print(f"button_A was released!")
            button_selection = ButtonPacket.DOWN # turns off pixels
            if not send_packet(uart_connection,
                ButtonPacket(button_selection, pressed=True)):
                print(f"Just sent button {button_selection}")
        elif button_B.released:
            print(f"button_B was released!")
            button_selection = ButtonPacket.DOWN # turns off pixels
            if not send_packet(uart_connection,
                ButtonPacket(button_selection, pressed=True)):
                print(f"Just sent button {button_selection}")
