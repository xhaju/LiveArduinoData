""" 
Interface between python and arduino for live data logger 

Author: James Keaveney
19/05/2015
"""

import time
import serial
import numpy as np

nchannels = 9 # number of total channels (time axis + ADC channels 0-7)
datalen = 1 # numbers in each array that serial.print does in arduino


class SerialDataFetcher:
    """
    class for interfacing with the Arduino Data Logger

    The data logger runs on an Arduino DUE; the sketch is "SixChannelLogger.ino"
    and should also be in this directory

    """
    def __init__(self,recording_time=1,verbose=True):
        self.recording_time = recording_time
        self.verbose = verbose
        self.time_axis = None

    def get_data(self):
        """
    	Initialise serial port and listen for data until timeout.
    	Convert the bytestream into numpy arrays for each channel

    	Returns:

    		7 numpy arrays (1D) representing time and ADC channels 0-5

	    """
		
        # setup serial port - it's the native USB port so baudrate is irrelevant,
        # the data is always transferred at full USB speed   -COM4!
        ser = serial.Serial(
            port='COM4',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=self.recording_time # seconds - should be the same amount of time as the arduino will send data for + 1
        )

        #testing - repeat serial read to confirm data arrays are always predictable
        #n_reps = 2
        #for i in range(n_reps):
        st = time.clock()
		
        #sync
        self._handshake(ser)

        #get data
        data = ser.readline()# this number should be larger than the number of
                                # bytes that will actually be sent
        ser.close()				# close serial port
        et = time.clock() - st
        if self.verbose:
            print 'Elapsed time reading data (s): ', et

        #make string into list of strings, comma separated
        data_list = data.split(',')
        # remove new line characters (are any present?)
        # data_list = filter(lambda a: a != '\n', data_list)

        # make list of strings into 1D numpy array of floats (ignore last point as it's an empty string)
        data_array = np.array([float(i) for i in data_list[:-1]])
        if self.verbose:
            print 'Length of array:', len(data_array)
        # reshape array into 3D array
        data_array_3d = data_array.reshape(-1,nchannels,datalen)
        # then separate 1d arrays
        self.time_axis = data_array_3d[0][0]
        #for i in range(1,len(data_array_3d)):
        #    self.time_axis = np.append(self.time_axis, data_array_3d[i][0])
        # convert time axis into ms, and zero the axis
        self.time_axis = self.time_axis*1e-3#(self.time_axis - self.time_axis[0])/1e3
        self.channel0 = data_array_3d[0][1]
        self.channel1 = data_array_3d[0][2]
        self.channel2 = data_array_3d[0][3]
        self.channel3 = data_array_3d[0][4]
        self.channel4 = data_array_3d[0][5]
        self.channel5 = data_array_3d[0][6]
        self.channel6 = data_array_3d[0][7]
        self.channel7 = data_array_3d[0][8]


        for i in range(1,len(data_array_3d)):
            self.channel0 = np.append(self.channel0, data_array_3d[i][1])
            self.channel1 = np.append(self.channel1, data_array_3d[i][2])
            self.channel2 = np.append(self.channel2, data_array_3d[i][3])
            self.channel3 = np.append(self.channel3, data_array_3d[i][4])
            self.channel4 = np.append(self.channel4, data_array_3d[i][5])
            self.channel5 = np.append(self.channel5, data_array_3d[i][6])
            self.channel6 = np.append(self.channel6, data_array_3d[i][7])
            self.channel7 = np.append(self.channel7, data_array_3d[i][8])

        if self.verbose:
            print 'Data acquisition complete. Time spent {}'.format( time.clock() - st)
        return self.time_axis,self.channel0,self.channel1,self.channel2,self.channel3,self.channel4,self.channel5,self.channel6,self.channel7


    def _handshake(self,serialinst):
        """ Send/receive pair of bytes to synchronize data gathering """
        nbytes = serialinst.write('A') # can write anything here, just a single byte (any ASCII char)
        if self.verbose:
            print 'Wrote bytes to serial port: ', nbytes
        #wait for byte to be received before returning
        st = time.clock()
        byte_back = serialinst.readline()
        et = time.clock()
        if self.verbose:
            print 'Received handshake data from serial port: ',byte_back
            print 'Time between send and receive: ',et-st


    def cleanup(self):
        # delete serial port instance?
        pass

def main():
    """ Grab data once and save it to file, with current timestamp """

    SR = SerialDataLogger(recording_time=6)

    filename = "TestData"
    t, C1, C2, C3, C4, C5, C6 = SR.get_data()
    SR.save_data(filename)
	
if __name__ == '__main__':
    main()