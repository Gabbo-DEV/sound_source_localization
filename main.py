import json

from acoustic_locator import AcousticLocator
from setup import runSetup

def getBeaconsPositions():
    f = open('config.json')
    jsonFile = json.load(f)
    
    data = []
    for i in range(1, 4):
        coordinates = [jsonFile[f'beacon{i}']['coordinates'][0], jsonFile[f'beacon{i}']['coordinates'][1]]
        data.append(coordinates)

    return data

def getBeaconsFrequencies():
    f = open('config.json')
    jsonFile = json.load(f)
    
    data = []
    for i in range(1, 4):
        frequency = jsonFile[f'beacon{i}']['frequency']
        data.append(frequency)

    return data

def main():
    try:
        beacon_positions = getBeaconsPositions()
        beacon_positions = getBeaconsFrequencies()
    except FileNotFoundError:
        exit('\033[91m' + 'Error! Configuration file not found')
       

    receiver_positions = []
    acoustic_localizer = AcousticLocator(beacon_positions, beacon_positions)
    # start loop
    input_signal = acoustic_localizer.record_audio()
    outs = acoustic_localizer.compute_convolution(input_signal)
    powers = acoustic_localizer.compute_powers(outs)
    position = acoustic_localizer.compute_position(powers)
    print(position)
    receiver_positions.append(position)
    # end loop


if __name__ == "__main__":
    main()
