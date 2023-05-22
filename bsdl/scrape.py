import json
import requests
from datetime import datetime

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


def getTrackData(ID):
    trackData = [requests.get(
        f'https://main.v2.beatstars.com/beat?id={ID}&fields=details,stats,licenses', headers=headers).json()]

    return trackData


def getTracksData(artist: str):

    artistPageResponse = requests.get(
        f'https://main.v2.beatstars.com/musician?permalink={artist}&fields=profile,user_contents,stats,bulk_deals,social_networks', headers=headers)

    if artistPageResponse.status_code == 404:
        return None

    userID = artistPageResponse.json()[
        'response']['data']['profile']['user_id']
    memberId = f'MR{userID}'

    page = 0
    dataBundle = []

    while True:

        data = '{{"query":"","page":{0},"hitsPerPage":1000,"facets":["*"],"analytics":true,"clickAnalytics":true,"tagFilters":[],"facetFilters":[["profile.memberId:{1}"]],"maxValuesPerFacet":1000,"maxFacetHits":100,"enableABTest":false,"userToken":null,"filters":"","ruleContexts":[]}}'.format(
            page, memberId)

        profileDataResponse = requests.post(
            'https://nmmgzjq6qi-dsn.algolia.net/1/indexes/public_prod_inventory_track_index_bycustom/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.12.0)%3B%20Browser',
            headers=headers,
            data=data,
        )

        # No tracks in artist/server error
        if profileDataResponse.status_code == 404:
            return

        if profileDataResponse.status_code == 200:
            profileData = profileDataResponse.json()

            hits = profileData['hits']
            dataBundle.extend(hits)

            if profileData.get('nbPages', 0) <= page:
                break
            page += 1

    with open('data.json', "w") as file:
        json.dump(dataBundle, file)

    trackIDs = [v2Id['v2Id'] for v2Id in dataBundle]
    tracksData = [getTrackData(ID=ID)[0] for ID in trackIDs]

    return tracksData


def getTitles(tracksData):
    titles = [data['response']['data']['details']['title']
              for data in tracksData]

    return titles


def getArtist(tracksData):
    artist = [data['response']['data']['details']
              ['musician']['display_name'] for data in tracksData][0]

    return artist


def getStreams(tracksData):
    streamLinks = [data['response']['data']['details']['stream_ssl_url']
                   for data in tracksData]

    return streamLinks


def getCoverArts(tracksData):
    coverLinks = [data['response']['data']['details']['artwork']['original']
                  for data in tracksData]

    return coverLinks


def getTimestamps(tracksData):
    timestamps = [data['response']['data']['details']['release_date_time']
                  for data in tracksData]

    return timestamps


def getDescriptions(tracksData):
    descriptions = [data['response']['data']['details']['description']
                    for data in tracksData]

    return descriptions


def getPermalinks(tracksData):
    permalinks = [data['response']['data']['details']['beatstars_uri']
                  for data in tracksData]

    return permalinks


def getGenres(tracksData):
    genres = [data['response']['data']['details']['genre'][0]['name']
              for data in tracksData]

    return genres
