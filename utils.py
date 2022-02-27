from random import random
from merger import merge
import requests, logging, os 
#from merger import merge

API_URL = "https://api.stemplayer.com/"
BASE_FOLDER = "Dump"
MERGE_SONGS = True
FORMAT = "wav" #or WAV

# https://github.com/krystalgamer/stem-player-emulator/blob/master/stem_emulator.user.js#L310
# broken
def random_serial() -> str:
    res = 0
    i = 0
    
    while (i < 24):
        res += int(random() * 10)
        i += 1
    
    return str(res)

def save_file(url, path):
    r = requests.get(url).content
    with open(path, 'wb') as f:
        f.write(r)
        
def download_stems(data, album, track):
    logging.debug("      download_stems: initialized")
    
    try:
        os.makedirs(f'{os.getcwd()}/{BASE_FOLDER}/{album}/{track}')
    except:
        pass
    
    for url in data:
        match (url):
            case "1":
                save_file(data[url], f'{BASE_FOLDER}/{album}/{track}/instrumental.{FORMAT}')
            case "2":
                save_file(data[url], f'{BASE_FOLDER}/{album}/{track}/vocals.{FORMAT}')
            case "3":
                save_file(data[url], f'{BASE_FOLDER}/{album}/{track}/drums.{FORMAT}')
            case "4":
                save_file(data[url], f'{BASE_FOLDER}/{album}/{track}/bass.{FORMAT}')
            case _:
                logging.info("      download_stems: Unsupported stem?")
    
        if (MERGE_SONGS):
            logging.info(f"      download_stems: merging tracks {track}")
            merge(album, track, FORMAT)
            
    logging.debug("      download_stems: finished")
    
    
def get_albums():
    logging.info('request: Getting list of albums from the Kano API')
    
    r = requests.get(API_URL + "content/albums").json()['data']
    return r

def get_track(track_id, version=1):
    logging.debug('      request: Getting track by id {} with codec {}'.format(track_id, FORMAT))
    
    url = API_URL + f'content/stems?track_id={track_id}&version={version}&codec={FORMAT}&device_id=002800273330510139323636'
    r = requests.get(url).json()['data']
    
    return r