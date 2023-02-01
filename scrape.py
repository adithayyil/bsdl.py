import json
import requests


"""
    For Reference
    
    # trackIds = []
    # for elements in trackData['hits']:
    #     trackIds.append(elements['id'])

    # metaData = []
    # for elements in trackData['hits']:
    #     metaData.append(elements['metadata'])

"""

artist = 'shinjin'


def getStreams(artist):

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

    artistData = requests.get(
        f'https://main.v2.beatstars.com/musician?permalink={artist}&fields=profile,user_contents,stats,bulk_deals,social_networks', headers=headers)

    userID = artistData.json()[
        'response']['data']['profile']['user_id']
    memberId = f'MR{userID}'

    data = '{{"query":"","page":0,"hitsPerPage":1000,"facets":["*"],"analytics":true,"clickAnalytics":true,"tagFilters":[],"facetFilters":[["profile.memberId:{0}"]],"maxValuesPerFacet":1000,"enableABTest":false,"userToken":null,"filters":"","ruleContexts":[]}}'.format(
        memberId)

    reponseTrackData = requests.post(
        'https://nmmgzjq6qi-dsn.algolia.net/1/indexes/public_prod_inventory_track_index_bycustom/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.12.0)%3B%20Browser',
        headers=headers,
        data=data,
    )

    trackData = reponseTrackData.json()
    trackStreamLinks = trackData['facets']['bundle.stream.url'].keys()

    return trackStreamLinks


def downloadTracks(streams):
    # TODO: Add dl funcs
    print(streams)


downloadTracks(getStreams(artist))
