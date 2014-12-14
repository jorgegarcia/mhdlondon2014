import musicbrainzngs as mbrainz
import download7Dpreview
import py7D
import discJockey
import sys
import audio
import threading
import string

# Musicbrainzngs app setup
mbrainz.set_useragent(
    "fftm",
    "0.1",
    "https://github.com/jorgegarcia/mhdlondon2014/",
)

artistName = ""
downloadFolder = "../data/downloaded/"

class TrackDataEntry:

    _trackTitle = ""
    _trackReleaseDate = 1900
    _track7DId = 0

def TrackPreviews(artistName):

    response = py7D.request('track', 'search', q=artistName, pageSize=100)
    tracks = response['response']['searchResults']['searchResult']

    trackData = []

    for track in tracks:
        trackDataEntry = TrackDataEntry()
        trackDataEntry._trackTitle          = track['track']['title']

        trackDataEntry._trackTitle = trackDataEntry._trackTitle.replace('/', '')
        trackDataEntry._trackTitle = filter(lambda x: x in string.printable, trackDataEntry._trackTitle)

        trackDataEntry._trackReleaseDate    = track['track']['release']['releaseDate'][0:4]
        trackDataEntry._track7DId           = track['track']['@id']

        trackData.append(trackDataEntry)

    return trackData

def ApplyAnnualCap(trackList, cap=999):
    yearHitTable = {}
    newTrackList = []
    for track in trackList:
        if track._trackReleaseDate not in yearHitTable:
            yearHitTable[track._trackReleaseDate] = 1
        else:
            yearHitTable[track._trackReleaseDate] += 1
        if yearHitTable[track._trackReleaseDate] <= cap:
            newTrackList.append(track)

    return newTrackList

def DownloadTracks(tracksFound):

    downloadedTracks = []

    for track in tracksFound:
        downloadedTrackEntry = []

        file = downloadFolder + str(track._trackTitle) + ".mp3"

        if(len(downloadedTracks) == 0): #initialise
            downloadedTrackEntry.append(track._trackTitle)
            downloadedTrackEntry.append(track._trackReleaseDate)

            downloadedTracks.append(downloadedTrackEntry)

            print "Downloading preview to " + file
            download7Dpreview.write7DPreview(file, track._track7DId)
        else:
            wasDownloaded = False
            for downloadedTrack in downloadedTracks:
                if(downloadedTrack[0].lower() == track._trackTitle.lower()):
                    wasDownloaded = True

            if not wasDownloaded:
                downloadedTrackEntry.append(track._trackTitle)
                downloadedTrackEntry.append(track._trackReleaseDate)

                downloadedTracks.append(downloadedTrackEntry)

                print "Downloading preview to " + file
                download7Dpreview.write7DPreview(file, track._track7DId)

    return downloadedTracks


if __name__ == "__main__":
    inputArgs = sys.argv[1:]
    if(len(inputArgs) == 0):
        artistName = "Bob Marley"
    else:
        artistName = inputArgs[0]

    artistData = mbrainz.search_artists(artistName)
    artistLifeSpan = artistData['artist-list'][0]['life-span']
    artistStartYear = "1900"
    artistEndYear = "2015"

    if artistLifeSpan['ended'] == 'true':
        artistStartYear = artistLifeSpan['begin'][0:4]
        artistEndYear = artistLifeSpan['end'][0:4]
        print artistName + " " + "from " + artistStartYear + " to " + artistEndYear
    else:
        print artistName + " is still active!"

    alltrackPreviewsFound = TrackPreviews(artistName)
    alltrackPreviewsFound = ApplyAnnualCap(alltrackPreviewsFound, 3)
    downloadedTracks = DownloadTracks(alltrackPreviewsFound)

    sortedDownloadedTracksByYear = sorted(downloadedTracks, key=lambda track: track[1])

    announcerThread = threading.Thread(target=discJockey.AnnounceSetlist, args=[artistName, int(artistStartYear), int(artistEndYear)])
    announcerThread.start()

    audio.PlayFile("../data/backtothefuture.mp3", 0.5, 8.0)

    discJockey.PlaySetlist(sortedDownloadedTracksByYear)
