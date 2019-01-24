import requests
from math import trunc
import re
import json
from bs4 import BeautifulSoup
from core import fslogger

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
        rooms = 'Rooms: ' + str(self.num_of_rooms)
        address = 'Address: ' + self.address
        price = 'Price: ' + str(self.total_price)
        area = 'Area: ' + str(self.total_area)
        sqmprice = 'Price \ meter: ' + str(self.sqmeter_price)
        floors = 'Floor: ' + str(self.floor) + ' from ' + str(self.num_of_floors)
        fid = 'Link: ' + self.flat_id
        return rooms + '\n' + address + '\n' + price + '\n' + area + '\n' + sqmprice + '\n' + floors + '\n' + fid

    def __str__(self):
        return self.__pretty_print__()


def http_get(url: str):
    logger.info('HTTP: GET ' + url)
    response = requests.get(url)
    if response.status_code is not 200:
        raise RuntimeError('HTTP Error. Response status code is: ' + response.status_code)
    return response

def http_post(url: str, headers: dict, data: dict):
    logger.info('HTTP: POST ' + url)
    response = requests.post(url, headers=headers, data=data)
    return response



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
        flat.created_date = flat_element['created_at'].split('T')[0]
        flat.updated_date = flat_element['last_time_up'].split('T')[0]
        flat.sqmeter_price = trunc(flat.total_price / flat.total_area)
        flats.append(flat)
    flats = [flat for flat in flats if flat.floor > 2]
    return flats


def __extract_numbers__(input_str: str):
    return re.findall(r'\d*[.,]?\d+|\d+', input_str)


class HttpTransport:

    def __init__(self, base_url):
        self.base_url = base_url

    def http_get(self, url):
        return ''

    def http_post(self):
        pass


class RealtResponseParser:

    def __init__(self, response):
        self.response = response

    def parse(self):
            with open('data/rs.htm', mode='r', encoding='UTF-8') as html:
                soup = BeautifulSoup(html, 'html.parser')
                logger.debug('Web page source:\n' + str(soup.prettify()))
                tags = soup.find_all(attrs={'class': 'bd-table-item-header'})
                for taag in tags:
                    divs = taag.find_all(name='div')
                    href = divs[2].a['href']
                    address = divs[2].a['title']
                    floors = __extract_numbers__(divs[3].span.text)
                    floor = floors[0]
                    from_floors = floors[1]
                    space = __extract_numbers__(divs[4].span.text)
                    total_space = space[0]
                    leaving_space = space[1]
                    kitchen_space = space[2]
                    year = str.strip(divs[5].span.text)
                    prices = divs[7].find_all(name='span')
                    price_total = ''.join([ch for ch in prices[0]['data-0'] if str.isdigit(ch)])
                    price_meter = ''.join([ch for ch in prices[1]['data-0'] if str.isdigit(ch)])
                    print(href)
                    print(price_total)
                    print(price_meter)
                    print(address)
                    print(floor)
                    print(from_floors)
                    print(total_space)
                    print(leaving_space)
                    print(kitchen_space)
                    print(year)
                    print('--------')


class FlatFinderService:

    def __init__(self, base_url):
        self.HttpTransport = HttpTransport(base_url)

    def find_flats(self, flats_search_rq):
        rs1 = self.HttpTransport.http_get(flats_search_rq.params)
        token = rs1.token
        rs2 = self.HttpTransport.http_get(token)
        flist = RealtResponseParser(rs2).parse()
        return list(flist)
