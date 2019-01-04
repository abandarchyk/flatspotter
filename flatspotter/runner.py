import requests
import json
import fslogger
from math import trunc


logger = fslogger.get_logger(__name__)

horizont_url='https://pk.api.onliner.by/search/apartments?number_of_rooms%5B%5D=2&number_of_rooms%5B%5D=3&price%5Bmin%5D=4583&price%5Bmax%5D=105000&currency=usd&building_year%5Bmin%5D=1900&building_year%5Bmax%5D=1960&bounds%5Blb%5D%5Blat%5D=53.901882598778265&bounds%5Blb%5D%5Blong%5D=27.55170346495189&bounds%5Brt%5D%5Blat%5D=53.91985269894952&bounds%5Brt%5D%5Blong%5D=27.582666074104356'
gorkypark_url='https://pk.api.onliner.by/search/apartments?number_of_rooms%5B%5D=2&number_of_rooms%5B%5D=3&price%5Bmin%5D=4583&price%5Bmax%5D=105000&currency=usd&building_year%5Bmin%5D=1900&building_year%5Bmax%5D=1960&bounds%5Blb%5D%5Blat%5D=53.893431297246714&bounds%5Blb%5D%5Blong%5D=27.56295668214386&bounds%5Brt%5D%5Blat%5D=53.9114050328298&bounds%5Brt%5D%5Blong%5D=27.593919291296324'


class Flat:

    def __init__(self, address=None, num_of_rooms=None, total_price=None, total_area=None, sqmeter_price=None,
                 floor=None, num_of_floors=None, created_date=None, updated_date=None):
        self.address = address
        self.num_of_rooms = num_of_rooms
        self.total_price = total_price
        self.total_area = total_area
        self.sqmeter_price = sqmeter_price
        self.floor = floor
        self.num_of_floors = num_of_floors
        self.created_date = created_date
        self.updated_date = updated_date

    def __pretty_print__(self):
        return 'FLAT: ' + str(trunc(self.sqmeter_price))

    def __str__(self):
        return self.__pretty_print__()


def http_get(url: str):
    logger.info('HTTP: GET ' + url)
    response = requests.get(url)
    if response.status_code is not 200:
        raise RuntimeError('HTTP Error. Response status code is: ' + response.status_code)
    return response.content


def create_onliner_flats(flats_rs: json):
    flats = flats_rs['apartments']
    for flat_element in flats:
        flat = Flat()
        flat.address = flat_element['location']['user_address']
        flat.total_price = float(flat_element['price']['converted']['USD']['amount'])
        flat.num_of_rooms = flat_element['number_of_rooms']
        flat.floor = flat_element['floor']
        flat.num_of_floors = flat_element['number_of_floors']
        flat.total_area = flat_element['area']['total']
        flat.date_created = flat_element['created_at']
        flat.date_updated = flat_element['last_time_up']
        flat.url = flat_element['url']
        flat.sqmeter_price = flat.total_price / flat.total_area
        print(flat)
    print(len(flats))
    print(len([flat for flat in flats if flat['floor'] > 2]))


rs = http_get(horizont_url)
json_rs = json.loads(rs, encoding='UTF-8')
create_onliner_flats(json_rs)


