import json
import matplotlib.pyplot as plt

from acoustic_locator import AcousticLocator


def getBeaconsPositions():
    f = open('config.json')
    jsonFile = json.load(f)

    data = []
    for i in range(1, 4):
        coordinates = [jsonFile[f'beacon{i}']['coordinates']
                       [0], jsonFile[f'beacon{i}']['coordinates'][1]]
        data.append(coordinates)

    f.close()
    return data


def getBeaconsFrequencies():
    f = open('config.json')
    jsonFile = json.load(f)

    data = []
    for i in range(1, 4):
        frequency = jsonFile[f'beacon{i}']['frequency']
        data.append(frequency)

    f.close()
    return data


def main():
    try:
        beacon_positions = getBeaconsPositions()
        beacon_frequencies = getBeaconsFrequencies()
    except FileNotFoundError:
        exit('\033[91m' + 'Error! Configuration file not found')

    receiver_positions = []
    acoustic_localizer = AcousticLocator(beacon_positions, beacon_frequencies)

    fig, ax = plt.subplots()

    while True:
        input_signal = acoustic_localizer.record_audio()
        outs = acoustic_localizer.compute_convolution(input_signal)
        powers = acoustic_localizer.compute_powers(outs)
        position, r = acoustic_localizer.compute_position(powers)
        receiver_positions.append(position)
        print(position)
        acoustic_localizer.plot_position(receiver_positions, beacon_positions, r, fig, ax)
