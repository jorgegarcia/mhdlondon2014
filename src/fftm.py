import musicbrainzngs as mbrainz
import download7Dpreview
import py7D
import json

# Musicbrainzngs app setup
mbrainz.set_useragent(
    "fftm",
    "0.1",
    "https://github.com/jorgegarcia/mhdlondon2014/",
)

artistName = "The Gap Band"

def track_previews(artistName):

    response = py7D.request('track', 'search', q=artistName, pageSize=3)
    tracks = response['response']['searchResults']['searchResult']


    for track in tracks:
        print track
        track['preview'] = py7D.preview_url(track['track']['@id'])

    return tracks


if __name__ == "__main__":
    print mbrainz.search_artists(artistName)
    print json.dumps(track_previews(artistName), indent=4)

    # Testing out downloading from 7D
    download7Dpreview.write7DPreview( "../data/downloaded/testdownload.mp3", 33499156 )
