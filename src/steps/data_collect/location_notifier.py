import requests
import pandas as pd

from typing import Tuple, List

from utils.util_path import PathUtils


class LocationNotifier:
    def __init__(self):
        self.api_key = 'AIzaSyC8rKLy2tGkM7qgLAKZiPtsqpWuvhDjNdw'

    def _get_location(self) -> Tuple[float, float]:
        """
        2022.02.18.hsk : send request to google geolocation api
        :return: lat, lng
        """
        params = {
            'considerIP': True
        }
        url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={self.api_key}'
        response = requests.post(url, params)
        loc = response.json()['location']
        return loc['lat'], loc['lng']

    def _get_addresses(self, lat, lng) -> List[str]:
        """
        2022.02.18.hsk : send requests to google geocoding api
        :return:
        """
        # language support
        # https://developers.google.com/maps/faq#languagesupport
        language = 'ko'
        latlng = f'{lat},{lng}'
        url = f'https://maps.googleapis.com/maps/api/geocode/json?language={language}&latlng={latlng}&key={self.api_key}'
        response = requests.post(url)
        results = response.json().get('results')
        key = 'formatted_address'
        results = list(filter(lambda result: key in result.keys(), results))
        results = list(map(lambda result: result.get(key), results))
        results = list(filter(lambda result: '동' in result, results))
        return results

    def _parse_village(self, address: str) -> str:
        """
        2022.03.04.hsh : parse village name from address
        :param address:
        :return:
        """
        words = address.split(sep=' ')
        for word in words:
            if word.endswith('동'):
                return word
            
    def get_near_addresses(self) -> List[str]:
        """
        2022.02.18.hsk : send requests to google geocoding api
        :return:
        """
        lat, lng = self._get_location()
        addresses = self._get_addresses(lat, lng)
        return list(set([self._parse_village(address) for address in addresses]))

    def get_all_address(self) -> List[str]:
        """
        2022.02.20.hsk : parse village names from region.xlsx
        :return:
        """
        df: pd.DataFrame = pd.read_excel(PathUtils.resources_folder_path() + '\\region.xlsx', engine='openpyxl')
        last_col = df.keys().values[-1]
        df_filtered = df[df[last_col].str.contains('동').fillna(False)]
        val_filtered = df_filtered[last_col].values
        val_filtered = list(filter(lambda v: v.endswith('동'), val_filtered))
        val_filtered = list(set(val_filtered))
        return val_filtered
