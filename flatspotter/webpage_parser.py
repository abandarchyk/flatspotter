import requests
from math import trunc
import fslogger
import json

logger = fslogger.get_logger(__name__)


class Flat:
    def __init__(self, flat_id=None, address=None, num_of_rooms=None, total_price=None, total_area=None, sqmeter_price=None,
                 floor=None, num_of_floors=None, created_date=None, updated_date=None):
        self.flat_id = flat_id
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
        return 'FLAT ID: ' + str(self.flat_id)

    def __str__(self):
        return self.__pretty_print__()


def http_get(url: str):
    logger.info('HTTP: GET ' + url)
    response = requests.get(url)
    if response.status_code is not 200:
        raise RuntimeError('HTTP Error. Response status code is: ' + response.status_code)
    return response.content


def create_onliner_flats(flats_rs: json):
    flats = []
    for flat_element in flats_rs['apartments']:
        flat = Flat()
        flat.flat_id = flat_element['url']
        flat.address = flat_element['location']['user_address']
        flat.total_price = float(flat_element['price']['converted']['USD']['amount'])
        flat.num_of_rooms = flat_element['number_of_rooms']
        flat.floor = flat_element['floor']
        flat.num_of_floors = flat_element['number_of_floors']
        flat.total_area = flat_element['area']['total']
        flat.created_date = flat_element['created_at']
        flat.updated_date = flat_element['last_time_up']
        flat.sqmeter_price = trunc(flat.total_price / flat.total_area)
        flats.append(flat)
    flats = [flat for flat in flats if flat.floor > 2]
    return flats
