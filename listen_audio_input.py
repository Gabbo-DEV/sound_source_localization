import time as Time
import sounddevice as SoundDevice
from scipy.io.wavfile import write as SaveFile
from os.path import exists

def listen_audio_input(RECORD_SECONDS=5, RATE=44100, WAVE_OUTPUT_FILENAME="noname", OVERWRITE=False, CHANNELS=1):
    PATH = "media/"
    EXTENSION = ".wav"
    if OVERWRITE:
        FULL_PATH = PATH + WAVE_OUTPUT_FILENAME + EXTENSION
    else:
        FULL_PATH = find_right_rename_on_overwriting(PATH + WAVE_OUTPUT_FILENAME + EXTENSION)

    print("----------------------------------")
    print("Start recording with this values:")
    print("\trecord seconds: {0}".format(RECORD_SECONDS))
    print("\trecord rate: {0}".format(RATE))
    print("\trecord channels: {0}".format(CHANNELS))
    print("\tpath and filename: {0}".format(FULL_PATH))
    print()

    recording = SoundDevice.rec(int(RECORD_SECONDS * RATE), samplerate = RATE, channels = CHANNELS)
    for index_range in range(round(RECORD_SECONDS, 0)):
        second = index_range + 1
        percent = "{0}".format((second*100)/RECORD_SECONDS)
        print("{0}s/{1}s - {0:3.1f}%".format(second, RECORD_SECONDS, percent))
        Time.sleep(1)
    
    print()
    SoundDevice.wait()
    print("record done")
    SaveFile(FULL_PATH, RATE, recording)
    print("file saved in \"{0}\"".format(FULL_PATH))
    print("----------------------------------")

def find_right_rename_on_overwriting(FILE_PATHNAME, FORMAT_STRING_OFNUM="({})", FORMAT_STARTING_NUM=0):
    extension = FILE_PATHNAME[FILE_PATHNAME.rfind('.'):len(FILE_PATHNAME)]
    file_pathname_nonextended = FILE_PATHNAME[0:FILE_PATHNAME.rfind('.')]
    temp_file_pathname = FILE_PATHNAME
    if (exists(temp_file_pathname)):
        while True:
            if exists(temp_file_pathname):
                temp_file_pathname = file_pathname_nonextended + (FORMAT_STRING_OFNUM.format(FORMAT_STARTING_NUM)) + extension
                FORMAT_STARTING_NUM += 1
            else:
                return temp_file_pathname
    else: 
        return FILE_PATHNAME

def main():
    listen_audio_input()

# start line
if __name__ == "__main__":
    main()