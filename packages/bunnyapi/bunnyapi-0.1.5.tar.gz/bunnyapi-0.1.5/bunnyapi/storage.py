import requests

from typing import BinaryIO

class StorageApi:
    
    def __init__(self, api_key: str, storage_zone_name):
        """
        Initialize API for edge storage.

        Parameters:
        api_key (str): Your private API key
        storage_zone_name (str): The ID of the video library you want to operate on
        """
        self._api_key = api_key
        self._storage_zone_name = storage_zone_name
        self._base_url = f'https://storage.bunnycdn.com/{self._storage_zone_name}'
        self._headers = { 'AccessKey' : self._api_key }
    
    def list(self, path: str) -> dict:
        """
        Retrieve a list of files and directories located in the given directory.
        """
        url = f'{self._base_url}/{path}'
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()
        return r.json()
    
    def download(self, path: str, name: str) -> BinaryIO:
        """
        Returns the stored file at the given path. If the file does not exist, a 404 response will be returned.
        """
        url = f'{self._base_url}/{path}/{name}'
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()
        return r.content

    def upload(self, name: str, file: BinaryIO) -> dict:
        """
        Upload a file to a storage zone based on the URL path. If the directory tree does not exist,
        it will be created automatically. The file content should be sent as the body of the request without any type of encoding.
        """
        url = f'{self._base_url}/{name}'
        r = requests.put(url, headers=self._headers, data=file)
        r.raise_for_status()
        return r.json()

    def delete(self, path: str, name: str) -> dict:
        """
        Delete an object from the storage zone. In case the object is a directory all the data in it will be recursively deleted as well.
        """
        url = f'{self._base_url}/{path}/{name}'
        r = requests.delete(url, headers=self._headers)
        r.raise_for_status()
        return r.json()
