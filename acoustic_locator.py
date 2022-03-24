import sounddevice
import numpy as np
import matplotlib.pyplot as plt

class AcousticLocator:
    
    filtersPathName = 'beacons/filters.npz'

    def __init__(self, beacon_positions, f):
        self.record_time = 1
        self.sample_rate = 44100
        self.record_channels = 1
        self.initialize_params(beacon_positions, f)

    def initialize_params(self, beacon_positions, freqs):
        filters_file = np.load(self.filtersPathName)

        self.h1 = filters_file["h1"][0][0]
        self.h2 = filters_file["h2"][0][0]
        self.h3 = filters_file["h3"][0][0]

        self.f1 = freqs[0]
        self.f2 = freqs[1]
        self.f3 = freqs[2]

        self.b1 = beacon_positions[0]  # b1 = [x , y]
        self.b2 = beacon_positions[1]
        self.b3 = beacon_positions[2]

        self.K = 1

    def record_audio(self):
        audio = sounddevice.rec(int(self.record_time * self.sample_rate),
                                samplerate=self.sample_rate, channels=self.record_channels)
        # audio is partially empty
        sounddevice.wait()
        # audio is full

        return audio

    def compute_convolution(self, input_signal):

        outs = []
        out1 = self.convolve(input_signal, self.h1)
        out2 = self.convolve(input_signal, self.h2)
        out3 = self.convolve(input_signal, self.h3)

        outs.append(out1)
        outs.append(out2)
        outs.append(out3)

        return outs

    def convolve(self, array_one, array_two):
        array_input = []
        for el in array_one:
            array_input.append(float(el[0]))

        array_filter = []
        for el in array_two:
            array_filter.append(float(el))

        array_one = array_one[0:len(array_two)-1]
        return np.convolve(array_input, array_filter, 'valid')

    def my_fix_array(array, nested=0):
        # type = 0 means that
        return_array = []

        for element in array:
            return_array.append(float(element[0]))

        return return_array

    def compute_powers(self, outs):
        '''
        ComputePowers(outs) 
        powers = []
        for el in out: 
            Compute power of el 
            powers.append(power)
        return powers
        '''
        powers = []
        for signal in outs:
            power = sum(np.abs(signal)**2)
            powers.append(power)

        return powers

    def compute_power(self):
        pass # calcolare la potenza del segnale generato con lo stesso metodo con cui la si calcola sul segnale ricevuto

    def compute_radiuses(self, P, powers):
        radiuses = []
        for power in powers:
            radiuses.append(self.K * np.sqrt(P/power))
        
        return radiuses

    def compute_position(self, powers):
        # r1, r2, r3 = self.compute_radius(self.compute_power(), powers)
        r1 = 1
        r2 = 1
        r3 = 1
        
        A = np.array([
            [-2*(self.b1[0]-self.b2[0]), -2*(self.b1[1]-self.b2[1])],
            [-2*(self.b1[0]-self.b3[0]), -2*(self.b1[1]-self.b3[1])]
        ])

        B = np.array([
            [r1-r2-(self.b1[0]**2+self.b1[1]**2)+(self.b2[0]**2+self.b2[1]**2)],
            [r1-r3-(self.b1[0]**2+self.b3[1]**2)+(self.b1[0]**2+self.b3[1]**2)]
        ])

        solution = 0
        try:
            solution = np.linalg.solve(A, B)
        except Exception as e:
            print(e)
        
        return solution

    def plot_position(self, receiver_positions):

        plt.scatter(receiver_positions[-1][0], receiver_positions[-1][1])
        plt.show()
