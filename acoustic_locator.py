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

        print(powers)
        return powers

    def compute_power(self):
        pass  # calcolare la potenza del segnale generato con lo stesso metodo con cui la si calcola sul segnale ricevuto

    def compute_radiuses(self, P, powers):
        
        P = [196, 9.8, 140] 

        r1 = self.K * np.sqrt(P[0] / powers[0])
        r2 = self.K * np.sqrt(P[1] / powers[1])
        r3 = self.K * np.sqrt(P[2] / powers[2])

        print(f'R1: {r1}')
        print(f'R2: {r2}')
        print(f'R3: {r3}')
        return r1, r2, r3

    def compute_position(self, powers):
        r1, r2, r3 = self.compute_radiuses(self.compute_power(), powers)

        x1 = self.b1[0]
        y1 = self.b1[1]
        x2 = self.b2[0]
        y2 = self.b2[1]
        x3 = self.b3[0]
        y3 = self.b3[1]

        b1 = r1**2-r2**2-(x1**2+y1**2)+(x2**2+y2**2)
        b2 = r1**2-r3**2-(x1**2+y1**2)+(x3**2+y3**2)
        
        A = np.array([[-2*(x1-x2), -2*(y1-y2)], [-2*(x1-x3), -2*(y1-y3)]])
        B = np.array([[b1],[b2]])

        solution = 0
        try:
            solution = np.linalg.solve(A, B)
        except Exception as e:
            print(e)

        return [solution, [r1, r2, r3]]


    def plot_position(self, receiver_position, r, ax):
        cir1 = plt.Circle((self.b1[0], self.b1[1]), r[0], color='r', fill=False)
        cir2 = plt.Circle((self.b2[0], self.b2[1]), r[1], color='b', fill=False)
        cir3 = plt.Circle((self.b3[0], self.b3[1]), r[2], color='y', fill=False)
        
        ax.set_aspect('equal', adjustable='datalim')
        ax.clear()
        
        ax.add_patch(cir1)
        ax.add_patch(cir2)
        ax.add_patch(cir3)
       
        
        
        

    
