import os;
import audio
import time
import threading
import random

sampleDuration = 30
fadeDuration = 4
downloadedPath = "../data/downloaded"

def MakeAnnouncement(phrase):
    audio.PlayTextToSpeech(str(phrase[1]) + ", " + phrase[0])

def SpinRecord(file, volume):
    audio.PlayFile(file, volume)

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

        songThread = threading.Thread(target=SpinRecord, args=[os.path.join(downloadedPath, i[0] + ".mp3"), 0.5])
        songThread.start()
        time.sleep(sampleDuration - (fadeDuration * 0.5))