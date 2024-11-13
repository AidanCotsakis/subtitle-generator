print("Importing Modules...")

import wave
import json
import string

from vosk import Model, KaldiRecognizer, SetLogLevel

import time

print("Loading Model...")
# https://alphacephei.com/vosk/models
model_path = "models/vosk-model-en-us-0.42-gigaspeech"
audio_filename = "output/audio.wav"
fps = 30
frameCutoff = 30

model = Model(model_path)

wf = wave.open(audio_filename, "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

print("Finding Words...")

class Word:
	''' A class representing a word from the JSON format for vosk speech recognition API '''
	def __init__(self, dict):

		self.conf = dict["conf"]
		self.end = dict["end"]
		self.start = dict["start"]
		self.word = dict["word"]

	def to_string(self):
		return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
			self.word, self.start, self.end, self.conf*100)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
	data = wf.readframes(4000)
	if len(data) == 0:
		break
	if rec.AcceptWaveform(data):
		part_result = json.loads(rec.Result())
		results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

print("Generating Word List...")

# convert list of JSON dictionaries to list of 'Word' objects
list_of_Words = []
for sentence in results:
	if len(sentence) == 1:
		# sometimes there are bugs in recognition 
		# and it returns an empty dictionary
		# {'text': ''}
		continue
	for obj in sentence['result']:
		w = Word(obj)  # create custom Word object
		list_of_Words.append(w)  # and add it to list

wf.close()  # close audiofile

words = []

for word in list_of_Words:
	words.append([string.capwords(word.word), int(word.start*fps), int(word.end*fps)])

for i in range(len(words)-1):
	if words[i+1][1] - words[i][2] < frameCutoff:
		words[i][2] = words[i+1][1]

fileString = ""
for word in words:
	fileString += f"{word[1]} {word[2]} {word[0]}\n"

with open("temp/words.txt", "w") as f:
	f.write(fileString)
