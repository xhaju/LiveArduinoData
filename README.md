# LiveArduinoData: a package to acquire a plot live data from an arduino (Due)

The data, obtained by arduino, is sent to the computer via a COM port (the USB native port) and python receives it.

* The 'LivePlotter' folder contains the arduino sketch that takes care of the data taking.
* 'SerialDataFetcher.py' has the code that receives the data from the serial port.
* 'animate_live.py' assists in plotting live data obtained from arduino.

This project is a fork from [James Keaveney's equally named project](https://github.com/jameskeaveney/LiveArduinoData "LiveArduinoData"), with some modifications to accept several channels and to plot live.

His License can be found in LICENSE.Keaveney, and pretty much the same LICENSE applies to my changes.