from webpage_parser import http_get
from webpage_parser import create_onliner_flats
import json
import fslogger
import db_module


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
    base_url = 'https://pk.api.onliner.by/search/apartments' + district +\
               '&number_of_rooms[]=' + config['number_of_rooms'] + \
               '&building_year[min]=' + config['building_year_min'] +\
               '&building_year[max]=' + config['building_year_max'] +\
               '&price[min]=' + config['price_min'] + \
               '&price[max]=' + config['price_max'] + \
               '&currency=usd'
    return base_url


onliner_base_url = build_onliner_url(DEFAULT_CONFIG, park_chel)
rs = http_get(onliner_base_url)
json_rs = json.loads(rs, encoding='UTF-8')
onliner_flats = create_onliner_flats(json_rs)
for flat in onliner_flats:
    db_module.save_results(flat)


