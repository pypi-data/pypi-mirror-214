import requests

from .videos import VideosApi
from .collections import CollectionsApi
from .storage import StorageApi

__version__ = '0.1.4'

def purge(access_key: str, url: str) -> dict:
    """
    Purge URL from cache.

    Parameters:
    access_key (str): Your private api key
    url (str): The URL to be purged 
    """
    r = requests.post(f'https://api.bunny.net/purge?url={url}&async=false')
    r.raise_for_status()
    return r.json()
