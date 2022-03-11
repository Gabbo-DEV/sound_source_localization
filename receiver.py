import numpy

def calculate_receiver_position():
    print("work_in_progress")

def ComputeConvolution(array_one, array_two):
    numpy.convolve(array_one, array_two)

def ComputePower(input_signal):
    #The power of a signal is the sum of the absolute squares of its time-domain samples divided 
    #by the signal length, or, equivalently, the square of its RMS level.
    
    n_sample = input_signal.shape[0]
    n_time = input_signal.shape[1]
    
    results_array = np.empty((n_sample, 1))
    
    for i in range(n_sample):
        sum_sample = 0
        for j in range(n_time):
            sum_sample += input_signal[i, j]*input_signal[i, j]
        sum_sample = sum_sample/n_time
        results_array[i] = sum_sample
    
    return results_array

def main():
    InitializeParams()
    outs = ComputeConvolution(input)
    powers = ComputePowers(outs)
    positions = ComputePosition(powers)
    print("outs='" + outs + "'")
    print("powers='" + powers + "'")
    print("positions='" + positions + "'")


if __name__ == "__main__":
    main()
