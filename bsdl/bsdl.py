from bsdl.scrape import *

import click
import os
from halo import Halo
import mutagen

red = '\033[91m'
green = '\033[92m'
white = '\033[97m'


def folderCheck(artist):  # from ttdl
    if (not os.path.exists(os.path.join(artist))):
        os.mkdir(os.path.join(artist))


def tagSong(beatPath, title, artist, cover, description, permalink, genre):
    song = mutagen.File(beatPath)

    song["TIT2"] = mutagen.id3.TIT2(encoding=3, text=title)
    song["TPE1"] = mutagen.id3.TPE1(encoding=3, text=artist)

    response = requests.get(cover, headers=headers)
    coverData = response.content
    song["APIC"] = mutagen.id3.APIC(
        encoding=3,
        mime="image/jpeg",
        type=3,
        data=coverData
    )

    song["COMM"] = mutagen.id3.COMM(
        encoding=3, lang="ENG", text=description)

    song["WOAS"] = mutagen.id3.WOAS(url=permalink)
    song["TCON"] = mutagen.id3.TCON(encoding=3, text=genre)

    song.save()


def downloadArtist(artist):
    spinner = Halo(text='Retrieving Data', spinner='dots')
    spinner.start()
    tracksData = getTracksData(artist=artist)
    artistName = getArtist(tracksData)
    streams = getStreams(tracksData)
    titles = getTitles(tracksData)
    covers = getCoverArts(tracksData)
    timestamps = getTimestamps(tracksData)
    descriptions = getDescriptions(tracksData)
    permalinks = getPermalinks(tracksData)
    genres = getGenres(tracksData)
    spinner.stop()

    if streams != None:
        loadFormat = "Downloading tracks..."
        with Halo(text=loadFormat, spinner='dots') as h:
            for (title, link, cover, timestamp, description, permalink, genre) in zip(titles, streams, covers, timestamps, descriptions, permalinks, genres):
                song = requests.get(link, headers=headers)
                if (song.status_code == 200):
                    folderCheck(artistName)
                    songFile = title.replace("/", "_")

                    if song.headers.get('content-type') == 'audio/mpeg':
                        songFile += ".mp3"
                    elif song.headers.get('content-type') == 'audio/wav':
                        songFile += ".wav"
                    else:
                        h.stop_and_persist(
                            symbol=f'{red}✖' + f"{red} Unsupported file type for '{title}'!")
                        continue

                    filePath = os.path.join(os.path.join(artistName), songFile)
                    open(filePath, 'wb').write(song.content)

                    tagSong(filePath, title, artistName,
                            cover, description, permalink, genre)

                    current_atime = os.path.getatime(filePath)
                    os.utime(filePath, (current_atime, timestamp))

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
    timestamp = getTimestamps(trackData)[0]
    description = getDescriptions(trackData)[0]
    permalink = getPermalinks(trackData)[0]
    genre = getGenres(trackData)[0]
    spinner.stop()

    if stream != None:
        loadFormat = "Downloading track..."
        with Halo(text=loadFormat, spinner='dots') as h:
            song = requests.get(stream, headers=headers)
            if (song.status_code == 200):
                songFile = title.replace("/", "_")

                if song.headers.get('content-type') == 'audio/mpeg':
                    songFile += ".mp3"
                elif song.headers.get('content-type') == 'audio/wav':
                    songFile += ".wav"
                else:
                    h.stop_and_persist(
                        symbol=f'{red}✖' + f"{red} Unsupported file type for '{title}'!")

                filePath = songFile
                open(filePath, 'wb').write(song.content)

                tagSong(filePath, title, artistName,
                        cover, description, permalink, genre)

                current_atime = os.path.getatime(filePath)
                os.utime(filePath, (current_atime, timestamp))

                h.stop_and_persist(
                    symbol=f'{green}✔', text=f"{white}Downloaded '{title}' successfully!")
            else:
                h.stop_and_persist(
                    symbol=f'{red}✖' + f"{red} Error Occured")
    else:
        print(f"Invalid link!")


@ click.command(help="bsdl - a CLI tool for downloading BeatStars music.")
@ click.option("-artist", "-a", help='Download all tracks from a artist', metavar="[ARTIST]")
@ click.option("-track", "-t", help='Download a track', metavar="[LINK]")
def main(artist: str, track: str):
    if artist:
        downloadArtist(artist)
    if track:
        downloadTrack(track)


if __name__ == '__main__':
    main()
