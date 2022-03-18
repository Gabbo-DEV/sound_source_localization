import json

import numpy as np

from sender import Sender

def runSetup():
    data = {}
    for i in range(1, 4):
        print(f"-- Setup beacon {i} --")
        coordinates = input("Enter the coordinates: ").split(', ') # le coordinate devono necessariamente essere inserite in forma 'x, y' 
        coordinates[0] = float(coordinates[0])
        coordinates[1] = float(coordinates[1])
        frequency = int(input("Enter the frequency (Hz): "))
        dictionary = {
            "coordinates": coordinates,
            "frequency": frequency
        }

        beacon = Sender(f'f{i}')
        beacon.run(frequency)
        data.update({f'beacon{i}': dictionary})


    json_object = json.dumps(data, indent = 4)
  
    with open("config.json", "w") as outfile:
        outfile.write(json_object)

    print("\033[92m" + "All done.")


if __name__ == '__main__':
    runSetup()
