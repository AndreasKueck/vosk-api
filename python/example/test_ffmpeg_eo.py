#!/usr/bin/env python3

import subprocess
import sys
import json
import re

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

SetLogLevel(0)

dosiero = open('rezulto.txt','w')

rez = "KOMENCO "
pattern = re.compile(r'KOMENCO .+? FINO')
patternfinrez = re.compile(r'\"text\" \: \".+?\"')
tekstofina = ""

model = Model(lang="eo")
rec = KaldiRecognizer(model, SAMPLE_RATE)

with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                            sys.argv[1],
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            vc = json.loads(rec.Result())
            print(rec.Result())
            rez = rez + str(vc['text'])
        else:
            print(rec.PartialResult())

    recfinrez = str(rec.FinalResult())
    print(recfinrez)
    

    for match in re.findall(patternfinrez, recfinrez):
        tekstofina = "" if tekstofina is None else match

    rez = rez + tekstofina + " FINO"


    for match in re.findall(pattern, rez):
        dosiero.write(match)