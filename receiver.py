from gettext import npgettext

import numpy as np


class Receiver:
    def __init__(self):
        pass

    def calculate_receiver_position():
        pass

    def ComputeConvolution(array_one, array_two):
        np.convolve(array_one, array_two, 'valid')

    def ComputePower(input_signal):
        # The power of a signal is the sum of the absolute squares of its time-domain samples divided
        # by the signal length, or, equivalently, the square of its RMS level.

        n_sample = input_signal.shape[0]
        n_time = input_signal.shape[1]

        results_array = npgettext.empty((n_sample, 1))

        for i in range(n_sample):
            sum_sample = 0
            for j in range(n_time):
                sum_sample += input_signal[i, j]*input_signal[i, j]
            sum_sample = sum_sample/n_time
            results_array[i] = sum_sample

        return results_array


def main():
    receiver = Receiver()
    # InitializeParams()
    outs = receiver.ComputeConvolution(input)
    powers = receiver.ComputePowers(outs)
    positions = receiver.ComputePosition(powers)
    print(f"outs= ${outs}")
    print(f"powers= ${powers}")
    print(f"positions= ${positions}")


if __name__ == "__main__":
    main()
