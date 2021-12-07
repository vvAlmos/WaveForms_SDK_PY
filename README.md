Demo package for the WaveForms SDK Getting Started guide and multiple test scripts for different instruments.

Check: https://digilent.com/reference/test-and-measurement/guides/waveforms-sdk-getting-started for more details.

Available tests:\n
\t- empty test template\n
\t- analog signal generation and recording test\n
\t- digital signal generation and recording test\n
\t- blinking LEDs with the Suplpies and the Static I/O instruments\n
\t- UART in/out test using the Pmod CLS and the Pmod MAXSonar\n
\t- SPI in/out test using the Pmod CLS and the Pmod ALS\n
\t- I2C in/out test using the Pmod CLS and the Pmod TMP2\n

Available instruments and functions:\n
\t- device\n
\t\t- open\n
\t\t- check_error\n
\t\t- close\n
\t- oscilloscope\n
\t\t- open\n
\t\t- measure\n
\t\t- trigger\n
\t\t- record\n
\t\t- close\n
\t- waveform generator\n
\t\t- generate\n
\t\t- close\n
\t- power supplies\n
\t\t- switch\n
\t\t- switch_fixed (for Analog Discovery)\n
\t\t- switch_variable (for Analog Discovery 2 and Studio)\n
\t\t- switch_digital (for Digital Discovery and Analog Discovery Pro 3X50)\n
\t\t- switch_6V (for Analog Discovery Pro 5250)\n
\t\t- switch_25V (for Analog Discovery Pro 5250)\n
\t\t- close\n
\t- digital multimeter\n
\t\t- open\n
\t\t- measure\t   * UNTESTED *\n
\t\t- close\n
\t- logic analyzer\n
\t\t- open\n
\t\t- trigger\n
\t\t- record\n
\t\t- close\n
\t- pattern generator\n
\t\t- generate\n
\t\t- close\n
\t- static I/O\n
\t\t- set_mode\n
\t\t- get_state\n
\t\t- set_state\n
\t\t- set_current   * UNTESTED *\n
\t\t- set_pull\t  * UNTESTED *\n
\t\t- close\n
\t- protocol: UART\n
\t\t- open\n
\t\t- read\n
\t\t- write\n
\t\t- close\n
\t- protocol: SPI\n
\t\t- open\n
\t\t- read\n
\t\t- write\n
\t\t- echange\n
\t\t- spy\t\t   * UNTESTED *\n
\t\t- close\n
\t- protocol: I2C\n
\t\t- open\n
\t\t- read\n
\t\t- write\n
\t\t- echange\n
\t\t- spy\t\t   * UNTESTED *\n
\t\t- close\n
