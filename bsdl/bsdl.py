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


@click.command()
@click.option("-artist", "-a", help="Downloads all tracks of user")
def main(artist: str):
    spinner = Halo(text='Retrieving Data', spinner='dots')
    spinner.start()
    streams = getArtistData(artist=artist, getTitles=False, getStreams=True,
                            getMetaData=False, headers=headers)
    titles = getArtistData(artist=artist, getTitles=True, getStreams=False,
                           getMetaData=False, headers=headers)
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


if __name__ == '__main__':
    main()
