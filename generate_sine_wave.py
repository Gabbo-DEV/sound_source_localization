import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plot


def writeWavFile(sampleRate, y):
    wavfile.write('media/Sine.wav', sampleRate, y)  # Produces a 5 second Audio-File

def buildGraph(time):
    amplitude = np.sin(time)
    # Plot a sine wave using time and amplitude obtained for the sine wave

    plot.plot(time, amplitude)

    # Give a title for the sine wave plot

    plot.title('Sine wave')

    # Give x axis label for the sine wave plot

    plot.xlabel('Time')

    # Give y axis label for the sine wave plot

    plot.ylabel('Amplitude = sin(time)')

    plot.grid(True, which='both')

    plot.axhline(y=0, color='k')

    plot.show()

    # Display the sine wave

    plot.show()

def writeTxtFile(freq):
    with open('beacons/frequencies.txt', 'a') as f:
        f.write(str(freq) + " ")

def main():
    sampleRate = 44100

    frequency = int(input("Enter the frequency: (17500, 18500, 19500..) "))  # 17.5 kHz
    length = 5
    t = np.linspace(0, length, sampleRate * length)  # --> x (t)= A o⋅sin (2 π f o t + ϕ )
    y = np.sin(frequency * 2 * np.pi * t)

    try:   
        writeWavFile(sampleRate, y)
        writeTxtFile(frequency)
        # buildGraph(t)
        print("File successfully created")
    except KeyboardInterrupt:
        print("\nGoodbye")


if __name__ == "__main__":
    main()
