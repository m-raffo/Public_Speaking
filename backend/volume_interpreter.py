import pyaudio
import wave
import audioop
import time

CHUNK = int(1024 / 2)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


def get_volume():
    t1 = time.time()
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    t2 = time.time()
    print("Time: " + str(t2-t1))
    print(rms)

def end_volume():
    stream.stop_stream()
    stream.close()
    p.terminate()
