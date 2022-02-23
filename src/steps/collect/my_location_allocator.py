import requests
import pandas as pd

from typing import Tuple, List


class MyLocationAllocator:
    def __init__(self):
        self.api_key = 'AIzaSyC8rKLy2tGkM7qgLAKZiPtsqpWuvhDjNdw'

    def get_location(self) -> Tuple[float, float]:
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

    def get_addresses(self, lat, lng) -> List[str]:
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

    def get_near_addresses(self) -> List[str]:
        """
        2022.02.18.hsk : send requests to google geocoding api
        :return:
        """
        lat, lng = self.get_location()
        return self.get_addresses(lat, lng)

    def get_all_address(self) -> List[str]:
        """
        2022.02.20.hsk : parse village names from region.xlsx
        :return:
        """
        df: pd.DataFrame = pd.read_excel("../../../resources/region.xlsx")
        last_col = df.keys().values[-1]
        df_filtered = df[df[last_col].str.contains('동').fillna(False)]
        val_filtered = df_filtered[last_col].values
        val_filtered = list(filter(lambda v: v.endswith('동'), val_filtered))
        val_filtered = list(set(val_filtered))
        return val_filtered


# addresses = MyLocationAllocator().get_all_address()
# print(addresses)
