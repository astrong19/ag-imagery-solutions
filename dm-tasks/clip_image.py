#https://developers.planet.com/tutorials/clip-images-to-aoi/
#https://github.com/planetlabs/notebooks/blob/16d8f52d45c89f80b610e657b6e9d9e7b2501b4a/jupyter-notebooks/data-api-tutorials/clip_and_ship_introduction.ipynb
import sys
import json
import requests
import time
import zipfile
import os
from tqdm import tqdm
sys.path.append("..")
from utilities import util

def define_payload(geojson, scene_id, item_type, asset_type):

    with open(geojson) as f:
        data = json.load(f)
        print(f"aoi: {data}")

    clip_payload = {
        'aoi': data,
        'targets': [
          {
            'item_id': scene_id,
            'item_type': item_type,
            'asset_type': asset_type
          }
        ]
    }

    return clip_payload

def clip_request(api_key, clip_payload):

    # Request clip of scene (This will take some time to complete)
    request = requests.post('https://api.planet.com/compute/ops/clips/v1', auth=(api_key, ''), json=clip_payload)
    print(request.json())
    clip_url = request.json()['_links']['_self']

    # Poll API to monitor clip status. Once finished, download and upzip the scene
    clip_succeeded = False
    while not clip_succeeded:

        # Poll API
        check_state_request = requests.get(clip_url, auth=(api_key, ''))

        # If clipping process succeeded , we are done
        if check_state_request.json()['state'] == 'succeeded':
            clip_download_url = check_state_request.json()['_links']['results'][0]
            clip_succeeded = True
            print("Clip of scene succeeded and is ready to download")

        # Still activating. Wait 1 second and check again.
        else:
            print("...Still waiting for clipping to complete...")
            time.sleep(1)

    return clip_download_url

def download_image(scene_id, clip_download_url):

    # Download clip
    response = requests.get(clip_download_url, stream=True)
    with open('output/' + scene_id + '.zip', "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    # Unzip file
    ziped_item = zipfile.ZipFile('output/' + scene_id + '.zip')
    ziped_item.extractall('output/' + scene_id)

    # Delete zip file
    os.remove('output/' + scene_id + '.zip')
    print('Downloaded clips located in: output/')


if __name__ == '__main__':

    #Specify API Key
    api_key = util.get_token('planet_api.json')['planet-api-key']

    endpoint = "https://api.planet.com/compute/ops/clips/v1/"

    #set image ID
    scene_id = '20180716_175654_1006'

    # Set Item Type
    item_type = 'PSScene4Band'

    # Set Asset Type
    asset_type = 'analytic'

    #path to geojson defining aoi
    aoi = r'data\clip_aoi.geojson'

    clip_payload = define_payload(aoi, scene_id, item_type, asset_type)

    clip_download_url = clip_request(api_key, clip_payload)

    download_image(scene_id, clip_download_url)
