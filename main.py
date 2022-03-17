import sys
import numpy as np

from acoustic_locator import AcousticLocator


def main():
    beacon_positions = []
    if len(sys.argv) > 1:
        b1 = [sys.argv[1], sys.argv[2]]
        b2 = [sys.argv[3], sys.argv[4]]
        b3 = [sys.argv[5], sys.argv[6]]

        beacon_positions = [b1, b2, b3]

    else:
        filename = "beacons/beacons.txt"
        data = []
        with open(filename) as f:
            data.append(f.read().split())
        data = np.array(data)

        b1 = [data[0][0], data[0][1]]
        b2 = [data[0][2], data[0][3]]
        b3 = [data[0][4], data[0][5]]

        beacon_positions = [b1, b2, b3]

    acoustic_localizer = AcousticLocator(beacon_positions)
    input_signal = acoustic_localizer.record_audio()
    outs = acoustic_localizer.compute_convolution(input_signal)
    powers = acoustic_localizer.compute_powers(outs)
    position = acoustic_localizer.compute_position(powers);

    print("POWER: ")
    print(powers)


if __name__ == "__main__":
    main()
