from bsdl.scrape import *

import click
import os
from halo import Halo

folder = 'beats'

red = '\033[91m'
white = '\033[97m'
purple = '\033[95m'
green = '\033[92m'
blue = '\033[94m'
grey = '\033[90m'
yellow = '\033[93m'


def folderCheck(name):
    if (not os.path.exists(folder)):
        os.mkdir(folder)
    if (not os.path.exists(os.path.join(folder, name))):
        os.mkdir(os.path.join(folder, name))


@click.command()
@click.option("-artist", "-a", help="Downloads all tracks of user")
def main(artist: str):
    streams = getArtistData(artist=artist, getStreams=True,
                            getMetaData=False, headers=headers,)
    if streams != None:
        loadFormat = f"Downloading beat from {artist}"
        with Halo(text=loadFormat, spinner='dots', color='red') as h:
            for link in streams:
                beat = requests.get(link, headers=headers)
                if (beat.status_code == 200):
                    folderCheck(artist)
                    open(os.path.join(os.path.join(folder, artist), link.replace(
                        "/", "_")), 'wb').write(beat.content)
                    h.stop_and_persist(
                        symbol=f'{green}✔', text=loadFormat + f"{blue}, Downloaded Successfully!")
                else:
                    h.stop_and_persist(
                        symbol=f'{red}✖' + f"{red} Error Occured")
    else:
        print(f"{artist} does not exist or doesn't have any tracks!")


if __name__ == '__main__':
    main()
