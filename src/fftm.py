import musicbrainzngs as m
import download7Dpreview

# Musicbrainzngs app setup
m.set_useragent(
    "fftm",
    "0.1",
    "https://github.com/jorgegarcia/mhdlondon2014/",
)

print m.search_artists( 'The Gap Band' )

# Testing out downloading from 7D
download7Dpreview.write7DPreview( "../data/downloaded/testdownload.mp3", 1234 )
