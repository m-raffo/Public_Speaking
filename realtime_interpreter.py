
from __future__ import division
import os
import re
import sys
import jellyfish


# Imports the Google Cloud client library
import pyaudio
from six.moves import queue
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./apicred.json"
transcript_full = ""
transcript_pending = ""

# Instantiates a client
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms !!!!THIS IS NOT OUR VARIABLE!!!!

class correction:
    expected_index=0
    old_string=""
    new_string=""
transcript_corrections = []

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]


def listen_print_loop(responses): #unused
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if False:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break
            num_chars_printed = 0

def process_chunk(chunk_text):
    print (chunk_text)

#APPLY FUCKING CORRECTIONS
def apply_corrections(uncorrected_string, corrections):
    words = uncorrected_string.split(' ')

    i = 0 #word index
    j = 0 #correction index

    while (i < len(words) and j < len(corrections)):
        if corrections[j].expected_index == i:
            if words[i] == corrections[j].old_string:
                print("correction foumd")
                words[i]=corrections[j].new_string

            else:
                print("Minor error: it seems the string has unexpectedly changed")
            j += 1
        else:
            i += 1
    return ' '.join(x for x in words)

def gen_corrections(only_last, uncorrected_string):
    global transcript_corrections
    words = uncorrected_string.split(' ')
    if only_last:
        words_to_check = len(words)-1
    else:
        words_to_check = range(0, len(words)-1)

    for i in words_to_check:
        found_correction=False #initial value
        #Perform a phonetic comparision
        if (jellyfish.match_rating_comparison(words[i],expected_word)):
            found_correction=True #if its close indicate the correction to be made

        if found_correction:
            #Replace the actual word in the list, and store to intrim
            #words[-1] = expected_word
            #Create correction object
            o = correction
            o.expected_index=i #blechED YOU ARE IT WORKS-ish
            o.old_string=words[i]
            o.new_string=expected_word
            #Add it to the list...
            transcript_corrections.append(o)
        transcript_pending = cur_text



def main():
    global transcript_full, transcript_pending, transcript_corrections
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        print ("Init.")
        expected_word = "emeel"
        for cur_response in responses:
            try:
                cur_text = str(cur_response.results[0].alternatives[0].transcript)
                if cur_response.results[0].is_final:
                    transcript_corrections = []
                    process_chunk(cur_text)
                    transcript_full += apply_corrections(cur_text, transcript_corrections)
                    transcript_corrections = []
                    #transcript_full+=str(cur_text)
                else:
                    #autocorrect based on script

                    transcript_pending = cur_text

            except:
                print ("error: likely recieved and empty input")

            print("\n")
            transcript_pending = apply_corrections(transcript_pending, transcript_corrections)
            #print(transcript_full+transcript_pending)
if __name__ == '__main__':
    main()

# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
