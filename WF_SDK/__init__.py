"""
    This module realizes communication with Digilent Test & Measurement devices
"""

from . import device
from . import scope
from . import wavegen
from . import supplies
from . import dmm
from . import logic
from . import pattern
from . import static
from .protocol import i2c
from .protocol import spi
from .protocol import uart
