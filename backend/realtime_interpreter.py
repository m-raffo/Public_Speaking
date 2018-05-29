from __future__ import division
import time
import os
import re
import sys
import jellyfish
#import user_interface

# Imports the Google Cloud client library
import pyaudio
from six.moves import queue
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./apicred.json"

transcript_full = ""
transcript_pending = ""
wpm_current = 0
realtime_wpm = 0

start = time.time()

expected_word = ""
current_word_number = 0
current_word_number_temporary_offset = 0
scriptv = []

#Some placeholder data
data_crunched = [50,50,50,50]

# Instantiates a client
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms !!!!THIS IS NOT OUR VARIABLE!!!!
last_time = time.time()
prompt = 'test'#input("write prompt here")
words = prompt.split(",")
#print(words)

class correction:
    expected_index=0
    old_string=""
    new_string=""

transcript_corrections = []
transcript_variations = []
transcript_variations_temporary = []

wordno_store=0

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

def get_wpm():
    global realtime_wpm, data_crunched
    return float(sum(data_crunched[-6:-1]))/len(data_crunched[-6:-1])* 600

wpm_difference_list = [54, 45, 45,45 ,34, 23,42]

def wpm_calc():
    global last_time, realtime_wpm, wpm_difference_list, start
    end = time.time()
    beg = last_time

    wpm_difference_list.append(time.time() - start)

    realtime_wpm = time.time() - start

    counter = -1
    for i in wpm_difference_list:
        counter += 1
        data_crunched.append(i - wpm_difference_list[counter-1])

def get_word_number():
    global wordno_store
    return round(wordno_store)

def get_variations():
    global transcript_variations, transcript_variations_temporary
    return transcript_variations + transcript_variations_temporary



def process_finalised_chunk(chunk_text):
    global wpm_current, current_word_number, current_word_number_temporary_offset, transcript_corrections, transcript_full
    #print ("SCREAMMMMM!MM!M!M!M!M!!M")
    thing = chunk_text

    #athing(chunk_text)
    current_word_number_temporary_offset = 0
    transcript_corrections = []
    gen_corrections(False, chunk_text)
    #print("generation complete")
    transcript_full += apply_corrections(chunk_text, transcript_corrections, current_word_number) + ' '
    #print("applying complete")



    words_temp = chunk_text.split(' ')
    while '' in words_temp:
        words_temp.remove('')
    current_word_number += len(words_temp)
    #current_word_number -= 1

    #print ("Word count: {}".format(current_word_number))
    #wpm_current = word_chunky_thing(thing)




#APPLY FUCKING CORRECTIONS
def apply_corrections(uncorrected_string, corrections, offset):
    words = uncorrected_string.split(' ')
    while '' in words:
        words.remove('')

    i = offset #word index
    j = 0 #correction index

    while (i - offset < len(words) and j < len(corrections)):
        #print ("iteration...")
        if corrections[j].expected_index > i:
            i += 1
        elif corrections[j].expected_index == i:

            if words[i - offset] == corrections[j].old_string:
                #print("correction foumd {} -> {}".format(corrections[j].old_string, corrections[j].new_string))
                words[i - offset]=corrections[j].new_string
            else:
                print("Unexpected change: {} -> {} at index {}".format(corrections[j].old_string, words[i], corrections[j].expected_index))
            j += 1
        else:
            print ("Error in applying corrections: Please yell at Ethan")
    return " ".join(x for x in words)

def gen_corrections(only_last, uncorrected_string):
    global transcript_corrections, expected_word, current_word_number_temporary_offset, transcript_variations, transcript_variations_temporary
    #if not only_last:
        #current_word_number_temporary_offset = -1 #-1?
    words = uncorrected_string.split(' ')
    while '' in words:
        words.remove('')

    print("Gen corrections: {}".format(words))

    words_to_check = []
    if only_last:
        words_to_check = [-1]
    else:
        words_to_check = range(0, len(words))

    for i in words_to_check:
        set_expected_word(current_word_number + i)
        #current_word_number_temporary_offset +=1
        found_correction= False #initial value
        found_variation = False#False #initial value
        #Check if its the same
        if words[i]==expected_word:
            pass
        elif (jellyfish.match_rating_comparison(words[i],expected_word)):
            found_correction=True #if its close indicate the correction to be made
        else:
            found_variation =True

        if found_correction or found_variation:
            o = correction()
            o.expected_index=current_word_number + i# - 1#blechED YOU ARE IT WORKS-ish
            o.old_string=words[i]
            o.new_string=expected_word

            if found_correction:
                transcript_corrections.append(o)

            if found_variation:
                if only_last:
                    transcript_variations_temporary.append(o)
                else:
                    transcript_variations.append(o)

def set_expected_word(index):
    #global current_word_number, current_word_number_temporary_offset, scriptv, expected_word
    #expected_word = scriptv[min(current_word_number+current_word_number_temporary_offset, len(scriptv)-1)]
    global scriptv, expected_word
    expected_word = scriptv[min(index, len(scriptv)-1)]
    if expected_word == None:
        print("Expected: None found!")
        expected_word = "!@#$dummy"
    else:
        #print ("Expected: {}  (index: {})".format(expected_word, min(index, len(scriptv)-1)))
        pass

def flush_unsure():
    global transcript_corrections, transcript_pending, transcript_full
    process_finalised_chunk(transcript_pending)
    #TODO transcript_full += apply_corrections(transcript_pending, transcript_corrections)
    transcript_corrections = []


def athing(inthing): #aadhya's comparision thing. Functionality has been implemented into gen_corrections
    stuff = inthing
    blist = stuff.split()
    #print(blist)

    for d in blist:
        for c in words:
            if c != d:
                #print(d + " this is wrong")
                break

def main():
    try:
        global transcript_full, transcript_pending, transcript_corrections, scriptv
        global current_word_number, current_word_number_temporary_offset, expected_word, wordno_store
        global transcript_variations, transcript_variations_temporary
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
            #print("NO")
            with open("./script.txt", "r") as text_file:
                scriptv = text_file.read().split(' ')
                #print(scriptv)

            #print("daddi")
            expected_word="!@#$initial" #this is a dummy value lol
            for cur_response in responses: #REFPOINT MAIN
                #SET expected_word
                #expected_word = scriptv[min(current_word_number+current_word_number_temporary_offset, len(scriptv)-1)]
                #if expected_word == None:
                #    expected_word = "!@#$" #this is a dummy value too
                #try:
                if len(cur_response.results) != 0:
                    cur_text = str(cur_response.results[0].alternatives[0].transcript)
                    if cur_response.results[0].is_final:
                        #transcript_variations_temporary = []
                        process_finalised_chunk(cur_text)
                        #transcript_corrections = []
                        print (transcript_full)

                        tv_debug = [];
                        for v in transcript_corrections:
                            tv_debug.append(v.expected_index)
                        print (tv_debug)
                        #transcript_full+=str(cur_text)
                    else:
                        #autocorrect based on script
                        #corrections(True, cur_text)
                        wpm_calc()
                        current_word_number_temporary_offset += 1
                        #print (current_word_number_temporary_offset)
                        #transcript_pending = apply_corrections(cur_text, transcript_corrections)

                wordno_store = current_word_number + current_word_number_temporary_offset/3
    except KeyboardInterrupt:
        print ("\n Bye bye!")
    '''except Exception as e:
        print ("timeout quickfix: " + str(e))
        #print ("timeout restart")
        flush_unsure()
        main()'''
if __name__ == '__main__':
    main()
