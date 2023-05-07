import json
import requests

"""
    For Reference

    # trackIds = []
    # for elements in trackData['hits']:
    #     trackIds.append(elements['id'])

"""


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


def getArtistData(artist: str, getTitles: bool, getStreams: bool, getMetaData: bool, headers: dict):
    artistDoesNotExist = True

    artistPageResponse = requests.get(
        f'https://main.v2.beatstars.com/musician?permalink={artist}&fields=profile,user_contents,stats,bulk_deals,social_networks', headers=headers)

    if artistPageResponse.status_code == 404:
        return None

    userID = artistPageResponse.json()[
        'response']['data']['profile']['user_id']
    memberId = f'MR{userID}'

    data = '{{"query":"","page":0,"hitsPerPage":1000,"facets":["*"],"analytics":true,"clickAnalytics":true,"tagFilters":[],"facetFilters":[["profile.memberId:{0}"]],"maxValuesPerFacet":1000,"maxFacetHits":100,"enableABTest":false,"userToken":null,"filters":"","ruleContexts":[]}}'.format(
        memberId)

    responseTracksData = requests.post(
        'https://nmmgzjq6qi-dsn.algolia.net/1/indexes/public_prod_inventory_track_index_bycustom/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.12.0)%3B%20Browser',
        headers=headers,
        data=data,
    )

    # No tracks in artist/server error
    if responseTracksData.status_code == 404:
        return

    tracksData = responseTracksData.json()

    # Gets all track titles on page 0 (100 tracks)
    if getTitles:
        trackTitles = []
        for track in tracksData['hits']:
            trackTitles.append(
                track['title'])

        return trackTitles

    # Gets all stream links on page 0 (100 tracks)
    if getStreams:
        ''' # OLD VERSION OF GETTING STREAM LINKS
        if "bundle.stream.url" in tracksData['facets']:
            tracksStreamLinks = tracksData['facets']['bundle.stream.url'].keys(
            )
            return tracksStreamLinks
        '''
        if tracksData['hits'] != None:
            tracksStreamLinks = []
            for track in tracksData['hits']:
                try:
                    tracksStreamLinks.append(
                        track['bundle']['stream']['url'])
                except KeyError:
                    tracksStreamLinks.append(
                        track['bundle']['mp3']['url'].replace('download', 'stream'))

            return tracksStreamLinks

        else:
            return None

    # Gets all track metadata (not really...)
    elif getMetaData:
        metaData = []
        for elements in tracksData['hits']:
            metaData.append(elements['metadata'])

        return metaData

    return "Error Occured: Missed Paramaters"
