#!/usr/bin/env python3

import wave
import sys
import json
import re

from vosk import Model, KaldiRecognizer, SetLogLevel

# You can set log level to -1 to disable debug messages
SetLogLevel(0)

dosiero = open('rezulto.txt','w')

rez = "KOMENCO "
pattern = re.compile(r'KOMENCO .+? FINO')
patternfinrez = re.compile(r'\"text\" \: \".+?\"')
tekstofina = ""

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

model = Model(lang="de")

# You can also init model by name or with a folder path
# model = Model(model_name="vosk-model-en-us-0.21")
# model = Model("models/en")

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
rec.SetPartialWords(True)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        vc = json.loads(rec.Result())
        print(rec.Result())
        rez = rez + str(vc['text'])
    else:
        print(rec.PartialResult())
                        
recfinrez = str(rec.FinalResult())

for match in re.findall(patternfinrez, recfinrez):
    tekstofina = "" if tekstofina is None else match

rez = rez + tekstofina + " FINO"

for match in re.findall(pattern, rez):
    dosiero.write(match)
