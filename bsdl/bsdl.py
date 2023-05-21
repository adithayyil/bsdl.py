from bsdl.scrape import *

import click
import os
from halo import Halo
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TDRC, TPE1, WXXX, TCON, ID3NoHeaderError


red = '\033[91m'
green = '\033[92m'
white = '\033[97m'


def folderCheck(artist):  # from ttdl
    if (not os.path.exists(os.path.join(artist))):
        os.mkdir(os.path.join(artist))


def tagSong(beatPath, title, artist, cover, date, permalink, genre):
    try:
        song = ID3(beatPath)
    except ID3NoHeaderError:
        # TODO: handle with wavs (mutagen.mp3.HeaderNotFoundError: can't sync to MPEG frame)
        song = MP3(beatPath, ID3=ID3)
        song.add_tags()

    song["TIT2"] = TIT2(encoding=3, text=title)
    song["TPE1"] = TPE1(encoding=3, text=artist)

    response = requests.get(cover, headers=headers)
    coverData = response.content

    song["APIC"] = APIC(
        encoding=3,
        mime="image/jpeg",
        type=3,
        data=coverData
    )

    song["TDRC"] = TDRC(encoding=3, text=date)
    song["WXXX"] = WXXX(encoding=3, url=permalink)
    song["TCON"] = TCON(encoding=3, text=genre)

    song.save(v2_version=3)


def downloadArtist(artist):
    spinner = Halo(text='Retrieving Data', spinner='dots')
    spinner.start()
    tracksData = getTracksData(artist=artist)
    artistName = getArtist(tracksData)
    streams = getStreams(tracksData)
    titles = getTitles(tracksData)
    covers = getCoverArts(tracksData)
    dates = getDates(tracksData)
    permalinks = getPermalinks(tracksData)
    genres = getGenres(tracksData)
    spinner.stop()

    if streams != None:
        loadFormat = "Downloading track..."
        with Halo(text=loadFormat, spinner='dots') as h:
            for (title, link, cover, date, permalink, genre) in zip(titles, streams, covers, dates, permalinks, genres):
                song = requests.get(link, headers=headers)
                if (song.status_code == 200):
                    folderCheck(artistName)
                    songFile = title.replace("/", "_") + ".mp3"
                    filePath = os.path.join(os.path.join(
                        artistName), songFile)
                    open(filePath, 'wb').write(song.content)

                    tagSong(filePath, title, artistName,
                            cover, date, permalink, genre)

                    h.stop_and_persist(
                        symbol=f'{green}✔', text=f"{white}Downloaded '{title}' successfully!")
                else:
                    h.stop_and_persist(
                        symbol=f'{red}✖' + f"{red} Error Occured")
    else:
        print(f"{artistName} does not exist or doesn't have any tracks!")


def downloadTrack(link):
    spinner = Halo(text='Retrieving Data', spinner='dots')
    ID = link.split("-")[-1]

    trackData = getTrackData(ID)
    artistName = getArtist(trackData)
    stream = getStreams(trackData)[0]
    title = getTitles(trackData)[0]
    cover = getCoverArts(trackData)[0]
    date = getDates(trackData)[0]
    permalink = getPermalinks(trackData)[0]
    genre = getGenres(trackData)[0]
    spinner.stop()

    if stream != None:
        loadFormat = "Downloading track..."
        with Halo(text=loadFormat, spinner='dots') as h:
            beat = requests.get(stream, headers=headers)
            if (beat.status_code == 200):
                open(os.path.join(title.replace(
                    "/", "_")) + ".mp3", 'wb').write(beat.content)
                filePath = f'{title}.mp3'

                tagSong(filePath, title, artistName,
                        cover, date, permalink, genre)

                h.stop_and_persist(
                    symbol=f'{green}✔', text=f"{white}Downloaded '{title}' successfully!")
            else:
                h.stop_and_persist(
                    symbol=f'{red}✖' + f"{red} Error Occured")
    else:
        print(f"Invalid link!")


@click.command(help="bsdl - a CLI tool for downloading BeatStars music.")
@click.option("-artist", "-a", help='Download all tracks from a artist', metavar="[ARTIST]")
@click.option("-track", "-t", help='Download a track', metavar="[LINK]")
def main(artist: str, track: str):
    if artist:
        downloadArtist(artist)
    if track:
        downloadTrack(track)


if __name__ == '__main__':
    main()
