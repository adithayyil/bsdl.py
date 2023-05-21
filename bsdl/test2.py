import requests
from mutagen.id3 import ID3, APIC, TIT2, TDRC, TPE1


headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.beatstars.com',
    'Referer': 'https://www.beatstars.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'x-algolia-api-key': 'b3513eb709fe8f444b4d5c191b63ea47',
    'x-algolia-application-id': 'NMMGZJQ6QI',
}


def tag_mp3(file_path, title, artist, cover_art_url, date):
    # Load the MP3 file
    audio = ID3(file_path)

    # Clear existing tags
    audio.delete()

    # Set the title
    audio["TIT2"] = TIT2(encoding=3, text=title)

    # Set the artist
    audio["TPE1"] = TPE1(encoding=3, text=artist)

    # Download the cover art image from the URL
    response = requests.get(cover_art_url, headers=headers)
    cover_art_data = response.content

    # Set the cover art
    audio["APIC"] = APIC(
        encoding=3,
        mime="image/jpeg",
        type=3,
        data=cover_art_data
    )

    # Set the date
    audio["TDRC"] = TDRC(encoding=3, text=date)

    # Save the changes
    audio.save(v2_version=3)


# Usage example
file_path = 'beats/kiryano/service 150.mp3'
title = 'gtfo'
artist = 'kiryano'
cover_art_url = 'https://main.v2.beatstars.com/fit-in/1000x1000/filters:format(.jpeg):quality(80):fill(000000)//users/prod/822818/image/1665341788/ivvy.jpg'
hashtags = 'music, song, artist'
date = '2023-05-19'

tag_mp3(file_path, title, artist, cover_art_url, date)
