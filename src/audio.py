import subprocess
import scipy.io.wavfile as wave
import numpy as np

defaultSampleRate = 48000
defaultChannelCount = 2

def ConvertWavFile(inputpath, outputPath):
    subprocess.call(["afconvert", inputpath, outputPath, "-d", "LEI16@" + str(defaultSampleRate)])

def CreateEmptyWavFile(path):
    data = np.zeros((0, defaultChannelCount), dtype=np.int16)
    wave.write(path, defaultSampleRate, data)

def AppendToWavFile(fileA, fileB):
    fsA, dataA = wave.read(fileA)
    fsB, dataB = wave.read(fileB)
    dataC = np.concatenate((dataA, dataB))
    wave.write(fileA, fsA, dataC)

def PlayFile(file, volume=1.0, duration=0.0):
    if(duration > 0.0):
        subprocess.call(["afplay", "-v", str(volume), "-t", str(duration), file])
    else:
        subprocess.call(["afplay", "-v", str(volume), file])

def PlayTextToSpeech(phrase):
    subprocess.call(["say", phrase])


