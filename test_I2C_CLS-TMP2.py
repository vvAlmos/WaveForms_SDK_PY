from WF_SDK import device, supplies     # import instruments
from WF_SDK.protocol import i2c         # import protocol instrument

from time import sleep          # needed for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_handle, device_name = device.open()

# check for connection errors
device.check_error(device_handle)

"""-----------------------------------"""

# define i2c addresses
CLS_address = 0x48
TMP2_address = 0x4B

# start the power supplies
supplies.switch(device_handle, device_name, True, True, False, 3.3, 0)

# initialize the i2c interface on DIO0 and DIO1
i2c.open(device_handle, sda=0, scl=1)

# initialize the PMOD TMP2 (set output size to 16-bit)
i2c.write(device_handle, [0x03, 0x80], TMP2_address)

try:
    # repeat
    while True:
        # clear the screen and home cursor
        i2c.write(device_handle, "\x1b[j", CLS_address)

        # display a message
        i2c.write(device_handle, "Temp: ", CLS_address)

        # read the temperature
        i2c.write(device_handle, "", TMP2_address)  # address the device
        message, error = i2c.read(device_handle, 2, TMP2_address)   # read 2 bytes
        value = (int(message[0]) << 8) | int(message[1])    # create integer from received bytes
        if ((value >> 15) & 1) == 0:
            value /= 128    # decode positive numbers
        else:
            value = (value - 65535) / 128   # decode negative numbers

        # display the temperature
        i2c.write(device_handle, str(round(value, 2)), CLS_address)

        # display a message
        i2c.write(device_handle, [223, 67], CLS_address)

        # delay 1s
        sleep(1)

except KeyboardInterrupt:
    # exit on Ctrl+C
    pass

# reset the interface
i2c.close(device_handle)

# stop and reset the power supplies
supplies.switch(device_handle, device_name, False, False, False, 0, 0)
supplies.close(device_handle)

"""-----------------------------------"""

# close the connection
device.close(device_handle)