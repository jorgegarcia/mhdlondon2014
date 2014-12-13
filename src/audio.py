import subprocess

def CreateWavFile(inputpath, outputPath):
    subprocess.call(["afconvert", inputpath, outputPath, "-d", "LEI16@48000"])



