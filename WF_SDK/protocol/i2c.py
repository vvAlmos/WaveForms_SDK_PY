""" PROTOCOL: I2C CONTROL FUNCTIONS: generate, close """

import ctypes                            # import the C compatible data types
import WF_SDK.dwfconstants as constants  # import every constant
from sys import platform                 # this is needed to check the OS type

# load the dynamic library (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
elif platform.startswith("darwin"):
    # on macOS
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""-----------------------------------------------------------------------"""

def open(device_handle, sda, scl, clk_rate=100e03, stretching=True):
    """
        initializes I2C communication

        parameters: - device handle
                    - sda (DIO line used for data)
                    - scl (DIO line used for clock)
                    - rate (clock frequency in Hz, default is 100KHz)
                    - stretching (enables/disables clock stretching)

        returns:    - error message or empty string
    """
    # reset the interface
    dwf.FDwfDigitalI2cReset(device_handle)

    # clock stretching
    if stretching:
        dwf.FDwfDigitalI2cStretchSet(device_handle, ctypes.c_int(1))
    else:
        dwf.FDwfDigitalI2cStretchSet(device_handle, ctypes.c_int(0))

    # set clock frequency
    dwf.FDwfDigitalI2cRateSet(device_handle, ctypes.c_double(clk_rate))

    #  set communication lines
    dwf.FDwfDigitalI2cSclSet(device_handle, ctypes.c_int(scl))
    dwf.FDwfDigitalI2cSdaSet(device_handle, ctypes.c_int(sda))

    # check bus
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cClear(device_handle, ctypes.byref(nak))
    if nak.value == 0:
        return "Error: I2C bus lockup"


    # write 0 bytes
    dwf.FDwfDigitalI2cWrite(device_handle, ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(0), ctypes.byref(nak))
    if nak.value != 0:
        return "NAK: index " + str(nak.value)
    
    return ""

"""-----------------------------------------------------------------------"""

def write(device_handle, data, address):
    """
        send data through I2C
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - address (8-bit address of the slave device)
                    
        returns:    - error message or empty string
    """
    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = ctypes.create_string_buffer(data.encode("UTF-8"))

    # send
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWrite(device_handle, ctypes.c_int(address), data, ctypes.c_int(ctypes.sizeof(data)-1), ctypes.byref(nak))

    # check for not acknowledged
    if nak.value != 0:
        return "NAK: index " + str(nak.value)
    
    return ""

"""-----------------------------------------------------------------------"""

def read(device_handle, count, address):
    """
        receives data from I2C
        
        parameters: - device handle
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - string containing the received bytes
                    - error message or empty string
    """
    # create buffer to store data
    buffer = (ctypes.c_ubyte * count)()

    # receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cRead(device_handle, ctypes.c_int(address), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    data = list(buffer.value)
    data = "".join(chr(element) for element in data)

    # check for not acknowledged
    if nak.value != 0:
        return data, "NAK: index " + str(nak.value)
    
    return data, ""

"""-----------------------------------------------------------------------"""

def exchange(device_handle, data, count, address):
    """
        sends and receives data using the I2C interface
        
        parameters: - device handle
                    - data of type string, int, or list of characters/integers
                    - count (number of bytes to receive)
                    - address (8-bit address of the slave device)
        
        return:     - string containing the received bytes
                    - error message or empty string
    """
    # create buffer to store data
    buffer = (ctypes.c_ubyte * count)()

    # cast data
    if type(data) == int:
        data = "".join(chr(data))
    elif type(data) == list:
        data = "".join(chr(element) for element in data)

    # encode the string into a string buffer
    data = ctypes.create_string_buffer(data.encode("UTF-8"))

    # send and receive
    nak = ctypes.c_int()
    dwf.FDwfDigitalI2cWriteRead(device_handle, ctypes.c_int(address), data, ctypes.c_int(ctypes.sizeof(data)-1), buffer, ctypes.c_int(count), ctypes.byref(nak))

    # decode data
    rec_data = list(buffer.value)
    rec_data = "".join(chr(element) for element in rec_data)

    # check for not acknowledged
    if nak.value != 0:
        return rec_data, "NAK: index " + str(nak.value)
    
    return rec_data, ""

"""-----------------------------------------------------------------------"""

def spy(device_handle, count = 16):
    """
        receives data from I2C
        
        parameters: - device handle
                    - count (number of bytes to receive), default is 16
        
        return:     - class containing the received data: start, address, direction, message, stop
                    - error message or empty string
    """
    # variable to store the errors
    error = ""

    # variable to store the data
    class message:
        start = ""
        address = 0
        direction = ""
        data = ""
        stop = ""

    # start the interfcae
    dwf.FDwfDigitalI2cSpyStart(device_handle)

    # read data
    start = ctypes.c_int()
    stop = ctypes.c_int()
    data = (ctypes.c_ubyte * count)()
    count = ctypes.c_int(count)
    nak = ctypes.c_int()
    if dwf.FDwfDigitalI2cSpyStatus(device_handle, ctypes.byref(start), ctypes.byref(stop), ctypes.byref(data), ctypes.byref(count), ctypes.byref(nak)) == 0:
        error = "Communication with the device failed."
    
    # decode data
    if start.value != 0:

        # start condition
        if start.value == 1:
            message.start = "Start"
        elif start.value == 2:
            message.start = "Restart"

        # get address
        message.address = hex(data[0] >> 1)

        # decide message direction
        if data[0] & 1 == 0:
            message.direction = "Write"
        else:
            message.direction = "Read"
        
        # get message
        message.data = list(data.value)
        message.data = "".join(chr(element) for element in message.data)

        if stop.value != 0:
            message.stop = "Stop"

    # check for not acknowledged
    if nak.value != 0 and error == "":
        error = "NAK: index " + str(nak.value)
    
    return message, error

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        reset the i2c interface
    """
    dwf.FDwfDigitalI2cReset(device_handle)
    return
