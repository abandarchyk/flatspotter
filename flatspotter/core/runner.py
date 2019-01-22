from core import webpage_parser
import json
from core import fslogger
from core import db_module
import time
import telegram.api
from telegram import utils
import sys

logger = fslogger.get_logger(__name__)

# onlnr_base_url = 'https://pk.api.onliner.by/search/apartments?number_of_rooms[]=2&number_of_rooms[]=3' \
#                  '&building_year[min]=1900&building_year[max]=1960&price[min]=4596&price[max]=105000' \
#                  '&currency=usd'

park_chel = '?bounds[lb][lat]=53.9144949346229&bounds[lb][long]=27.581037837905807' \
            '&bounds[rt][lat]=53.934501895658414&bounds[rt][long]=27.616826187994285'

zaharova_pulihova = '?bounds[lb][lat]=53.893009645602724&bounds[lb][long]=27.56793281575766' \
                    '&bounds[rt][lat]=53.911519978530656&bounds[rt][long]=27.59889542491013'

horizont = '?bounds[lb][lat]=53.907822399900596&bounds[lb][long]=27.55463060237178' \
           '&bounds[rt][lat]=53.92632617055908&bounds[rt][long]=27.585593211524245'

centr = '?bounds[lb][lat]=53.89021130416644&bounds[lb][long]=27.539637154032217' \
        '&bounds[rt][lat]=53.90872287666223&bounds[rt][long]=27.570599763184642'

DEFAULT_CONFIG = {'number_of_rooms': '2',
                  'building_year_min': '1900',
                  'building_year_max': '1960',
                  'price_min': '10000',
                  'price_max': '105000'
                  }


def build_onliner_url(config: dict, district: str):
    base_url = 'https://pk.api.onliner.by/search/apartments' + district + \
               '&number_of_rooms[]=' + config['number_of_rooms'] + \
               '&building_year[min]=' + config['building_year_min'] + \
               '&building_year[max]=' + config['building_year_max'] + \
               '&price[min]=' + config['price_min'] + \
               '&price[max]=' + config['price_max'] + \
               '&currency=usd'
    return base_url


def load_flats():
    for dis in [park_chel, zaharova_pulihova, horizont, centr]:
        onliner_base_url = build_onliner_url(DEFAULT_CONFIG, dis)
        rs = webpage_parser.http_get(onliner_base_url)
        json_rs = json.loads(rs, encoding='UTF-8')
        onliner_flats = webpage_parser.create_onliner_flats(json_rs)
        for flat in onliner_flats:
            db_module.save_results(flat)


def call_realt():
    rs1 = webpage_parser.http_get('https://realt.by/sale/flats/search/')
    print('RS1: ' + rs1.cookies['fe_typo_user'])
    cookies = {'fe_typo_user': rs1.cookies['fe_typo_user']}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': rs1.cookies['fe_typo_user'],
               'Content-Length': '6260',
               'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary9pjcuj1S2fRAn8y0',
               'Host': 'realt.by',
               'Origin': 'https://realt.by',
               'Referer': 'https://realt.by/sale/flats/search/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    data = {'hash': 'e2ba94e8d0c57a13cbd9a07895f76031',
            'tx_uedbflat_pi2[DATA][state_region_id][e]': '',
            'tx_uedbflat_pi2[DATA][state_district_id][e]': '',
            'tx_uedbflat_pi2[DATA][town_id][e]': '5102',
            'tx_uedbflat_pi2[DATA][town_name][like][0]': '',
            'tx_uedbflat_pi2[DATA][town_name][like][1]': '',
            'tx_uedbflat_pi2[DATA][town_name][like][2]': '',
            'tx_uedbflat_pi2[DATA][town_name][like][3]': '',
            'tx_uedbflat_pi2[DATA][town_name][like][4]': '',
            'tx_uedbflat_pi2[DATA][street_name][like][0]': '',
            'tx_uedbflat_pi2[DATA][house_number][range][0]': '',
            'tx_uedbflat_pi2[DATA][street_name][like][1]': '',
            'tx_uedbflat_pi2[DATA][house_number][range][1]': '',
            'tx_uedbflat_pi2[DATA][street_name][like][2]': '',
            'tx_uedbflat_pi2[DATA][house_number][range][2]': '',
            'tx_uedbflat_pi2[DATA][street_name][like][3]': '',
            'tx_uedbflat_pi2[DATA][house_number][range][3]': '',
            'tx_uedbflat_pi2[DATA][street_name][like][4]': '',
            'tx_uedbflat_pi2[DATA][house_number][range][4]': '',
            'tx_uedbflat_pi2[DATA][rooms][e][1]': '2',
            'tx_uedbflat_pi2[DATA][rooms][e][2]': '3',
            'tx_uedbflat_pi2[DATA][building_year][ge]': '1920',
            'tx_uedbflat_pi2[DATA][building_year][le]': '1960',
            'tx_uedbflat_pi2[DATA][repair_year][ge]': '',
            'tx_uedbflat_pi2[DATA][repair_year][le]': '',
            'tx_uedbflat_pi2[DATA][area_total][ge]': '',
            'tx_uedbflat_pi2[DATA][area_total][le]': '',
            'tx_uedbflat_pi2[DATA][area_living][ge]': '',
            'tx_uedbflat_pi2[DATA][area_living][le]': '',
            'tx_uedbflat_pi2[DATA][area_kitchen][ge]': '',
            'tx_uedbflat_pi2[DATA][area_kitchen][le]': '',
            'tx_uedbflat_pi2[DATA][storeys][ge]': '',
            'tx_uedbflat_pi2[DATA][storeys][le]': '',
            'tx_uedbflat_pi2[DATA][storey][ge]': '3',
            'tx_uedbflat_pi2[DATA][storey][le]': '9',
            'tx_uedbflat_pi2[DATA][price_m2][ge]': '',
            'tx_uedbflat_pi2[DATA][price_m2][le]': '',
            'tx_uedbflat_pi2[DATA][ceiling_height][ge]': '',
            'tx_uedbflat_pi2[DATA][ceiling_height][le]': '',
            'tx_uedbflat_pi2[DATA][price][ge]': '',
            'tx_uedbflat_pi2[DATA][price][le]': '105',
            'tx_uedbflat_pi2[DATA][terms][e]': '',
            'tx_uedbflat_pi2[DATA][x_days_old][e]': '',
            'tx_uedbflat_pi2[DATA][agency_id][e]': '',
            'tx_uedbflat_pi2[rec_per_page]': '30',
            'tx_uedbflat_pi2[sort_by][0]': '',
            'tx_uedbflat_pi2[asc_desc][0]': '0',
            'tx_uedbflat_pi2[sort_by][1]': '',
            'tx_uedbflat_pi2[asc_desc][1]': '0'
            }

    rs2 = webpage_parser.http_post('https://realt.by/sale/flats/', headers, data)
    print(rs2.status_code)
    print(rs2.text)
    sys.exit()

call_realt()

offset = 263178230

while False:
    #   print("you: ")
    #   user_input = input()

    time.sleep(0.5)
    res = telegram.api.get_updates(offset)
    asJson = res.json()

    updates = utils.decode_updates(asJson)

    if len(updates) > 0:
        for update in updates:
            user_chat = update.Message.Chat.id
            user_input = update.Message.text

            results = []

            if user_input == 'stop':
                sys.exit('Code word is given')
            elif user_input == 'today':
                results = db_module.show_new()
            elif user_input == 'updated':
                print('CATCH: ' + user_input)
                results = db_module.show_updated()

            print('LOG: flats count:' + str(len(results)))

            print(results)

            for result in results:
                telegram.api.send_message(user_chat, result)
            offset = update.update_id + 1
    else:
        continue
