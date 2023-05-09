from bsdl.scrape import *

import click
import os
from halo import Halo

folder = 'beats'

red = '\033[91m'
green = '\033[92m'
white = '\033[97m'


def folderCheck(name):  # from ttdl
    if (not os.path.exists(folder)):
        os.mkdir(folder)
    if (not os.path.exists(os.path.join(folder, name))):
        os.mkdir(os.path.join(folder, name))


def downloadArtist(artist):
    spinner = Halo(text='Retrieving Data', spinner='dots')
    spinner.start()
    streams = getStream(getTrackIDs(getTracksData(artist=artist)))
    titles = getTitle(getTrackIDs(getTracksData(artist=artist)))
    spinner.stop()

    if streams != None:
        loadFormat = "Downloading track..."
        with Halo(text=loadFormat, spinner='dots') as h:
            for (title, link) in zip(titles, streams):
                beat = requests.get(link, headers=headers)
                if (beat.status_code == 200):
                    folderCheck(artist)
                    open(os.path.join(os.path.join(folder, artist), title.replace(
                        "/", "_")) + ".mp3", 'wb').write(beat.content)
                    h.stop_and_persist(
                        symbol=f'{green}✔', text=f"{white}Downloaded '{title}' successfully!")
                else:
                    h.stop_and_persist(
                        symbol=f'{red}✖' + f"{red} Error Occured")
    else:
        print(f"{artist} does not exist or doesn't have any tracks!")


def downloadTrack(link):
    spinner = Halo(text='Retrieving Data', spinner='dots')
    ID = [link.split("-")[-1]]

    stream = getStream(ID)
    title = getTitle(ID)
    spinner.stop()

    if stream != None:
        loadFormat = "Downloading track..."
        with Halo(text=loadFormat, spinner='dots') as h:
            for (title, link) in zip(title, stream):
                beat = requests.get(link, headers=headers)
                if (beat.status_code == 200):
                    open(os.path.join(os.path.join(folder), title.replace(
                        "/", "_")) + ".mp3", 'wb').write(beat.content)
                    h.stop_and_persist(
                        symbol=f'{green}✔', text=f"{white}Downloaded '{title}' successfully!")
                else:
                    h.stop_and_persist(
                        symbol=f'{red}✖' + f"{red} Error Occured")
    else:
        print(f"Invalid link!")


@click.command(help="bsdl - a CLI tool for downloading BeatStars Music.")
@click.option("-artist", "-a", help='Download all tracks from a artist', metavar="[ARTIST]")
@click.option("-track", "-t", help='Download a track', metavar="[LINK]")
def main(artist: str, track: str):
    if artist:
        downloadArtist(artist)
    if track:
        downloadTrack(track)


if __name__ == '__main__':
    main()
