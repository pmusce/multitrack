import pyaudio
import wave
import time
import numpy
import sys
from module.leitor_cartao import LeitorCartao

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

sound1 = wave.open("pizzica/drums.wav", 'rb')
sound2 = wave.open("pizzica/guitar.wav", 'rb')

volume1 = 0.0


def callback(in_data, frame_count, time_info, status):
    data1 = sound1.readframes(frame_count)
    data2 = sound2.readframes(frame_count)
    decodeddata1 = numpy.fromstring(data1, numpy.int16)
    decodeddata2 = numpy.fromstring(data2, numpy.int16)
    newdata = (decodeddata1 * 0.5 + decodeddata2 * volume1).astype(numpy.int16)
    return (newdata.tostring(), pyaudio.paContinue)


# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(sound1.getsampwidth()),
                channels=sound1.getnchannels(),
                rate=sound1.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

reader_card = LeitorCartao()

try:
    while True:
        if not reader_card.isAlive():
            reader_card.start()
except KeyboardInterrupt:
    print "trl+C received! Sending kill to " + reader_card.getName()
    if reader_card.isAlive():
        reader_card._stopevent.set()

# wait for stream to finish (5)
# while stream.is_active():
#    if volume1 < 0.5:
#        volume1 += 0.005

#    if volume1 > 0.5:
#        volume1 = 0.5

#    time.sleep(0.1)

# stop stream (6)
# stream.stop_stream()
# stream.close()
# sound1.close()
# sound2.close()

# close PyAudio (7)
# p.terminate()
