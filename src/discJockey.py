import os
import audio
import time
import threading
import random

sampleDuration = 15
fadeDuration = 1
downloadedPath = "../data/downloaded"
effectsPath = "../data/effects/"
effectsFiles = os.listdir(effectsPath)

def MakeAnnouncement(phrase):
    audio.PlayTextToSpeech(str(phrase[1]) + ", " + phrase[0])

def SpinRecord(file, volume, sampleDuration):
    audio.PlayFile(file, volume, sampleDuration)

def PlayRandomFX():
    audio.PlayFile(effectsPath + effectsFiles[random.randint(0, len(effectsFiles)-1)], 0.5)

def AnnounceSetlist(category, yearStart, yearEnd):
    intro = ("Welcome", "Greetings", "Wazzzzzzz-up")
    audience = ("party people", "fans", "music lovers")
    body = ("let's listen to some " + category + " tracks between " + str(yearStart) + " and " + str(yearEnd),
            "here are the " + category + " tunes from " + str(yearStart) + " and the following " + str(yearEnd - yearStart) + " years",
            "it is time for some " + category)

    finalMessage = intro[random.randint(0, len(intro)-1)]
    finalMessage += " "
    finalMessage += audience[random.randint(0, len(audience)-1)]
    finalMessage += ", "
    finalMessage += body[random.randint(0, len(body)-1)]
    finalMessage += "."

    audio.PlayTextToSpeech(finalMessage)

def PlaySetlist(downloadedFiles):
    for i in downloadedFiles:
        announcementThread = threading.Thread(target=MakeAnnouncement, args=[i])
        announcementThread.start()

        playFXThread = threading.Thread(target=PlayRandomFX)
        playFXThread.start()

        songThread = threading.Thread(target=SpinRecord, args=[os.path.join(downloadedPath, i[0] + ".mp3"), 0.5, sampleDuration])
        songThread.start()
        time.sleep(sampleDuration - (fadeDuration))