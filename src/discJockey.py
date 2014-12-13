import os;
import audio
import time
import threading
import random

sampleDuration = 10
fadeDuration = 1
downloadedPath = "../data/downloaded"

included_extenstions = ['mp3']
downloadedFiles = [fn for fn in os.listdir(downloadedPath) if any([fn.endswith(ext) for ext in included_extenstions])]

def MakeAnnouncement(phrase):
    audio.PlayTextToSpeech(phrase)

def SpinRecord(file, volume):
    audio.PlayFile(file, volume)

def AnnounceSetlist(category, yearStart, yearEnd):
    intro = ("Welcome", "Greetings", "Wazzzzzzz-up")
    audience = ("party people", "fans")
    body = ("let's listen to some " + category + " tracks between " + str(yearStart) + " and " + str(yearEnd),
            "here are the " + category + " tunes from " + str(yearStart) + " and the following " + str(yearEnd - yearStart) + " years")

    finalMessage = intro[random.randint(0, len(intro)-1)]
    finalMessage += " "
    finalMessage += audience[random.randint(0, len(audience)-1)]
    finalMessage += ","
    finalMessage += body[random.randint(0, len(body)-1)]
    finalMessage += "."
    print finalMessage

    audio.PlayTextToSpeech(finalMessage)

def PlaySetlist():
    for f in downloadedFiles:
        announcementThread = threading.Thread(target=MakeAnnouncement, args=[f])
        announcementThread.start()

        songThread = threading.Thread(target=SpinRecord, args=[os.path.join(downloadedPath, f), 0.5])
        songThread.start()
        time.sleep(sampleDuration - (fadeDuration * 0.5))

# PlaySetlist()