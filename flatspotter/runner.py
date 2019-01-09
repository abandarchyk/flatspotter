from webpage_parser import http_get
from webpage_parser import create_onliner_flats
import json
import fslogger
import db_module


logger = fslogger.get_logger(__name__)

onlnr_base_url = 'https://pk.api.onliner.by/search/apartments?number_of_rooms[]=2&number_of_rooms[]=3' \
                 '&building_year[min]=1900&building_year[max]=1960&price[min]=4596&price[max]=105000' \
                 '&currency=usd'

park_chel='#bounds[lb][lat]=53.9144949346229&bounds[lb][long]=27.581037837905807' \
          '&bounds[rt][lat]=53.934501895658414&bounds[rt][long]=27.616826187994285'

horizont_url='https://pk.api.onliner.by/search/apartments?number_of_rooms%5B%5D=2&number_of_rooms%5B%5D=3&price%5Bmin%5D=4583&price%5Bmax%5D=105000&currency=usd&building_year%5Bmin%5D=1900&building_year%5Bmax%5D=1960&bounds%5Blb%5D%5Blat%5D=53.901882598778265&bounds%5Blb%5D%5Blong%5D=27.55170346495189&bounds%5Brt%5D%5Blat%5D=53.91985269894952&bounds%5Brt%5D%5Blong%5D=27.582666074104356'
gorkypark_url='https://pk.api.onliner.by/search/apartments?number_of_rooms%5B%5D=2&number_of_rooms%5B%5D=3&price%5Bmin%5D=4583&price%5Bmax%5D=105000&currency=usd&building_year%5Bmin%5D=1900&building_year%5Bmax%5D=1960&bounds%5Blb%5D%5Blat%5D=53.893431297246714&bounds%5Blb%5D%5Blong%5D=27.56295668214386&bounds%5Brt%5D%5Blat%5D=53.9114050328298&bounds%5Brt%5D%5Blong%5D=27.593919291296324'


rs = http_get(onlnr_base_url + park_chel)
json_rs = json.loads(rs, encoding='UTF-8')
onliner_flats = create_onliner_flats(json_rs)
for flat in onliner_flats:
    db_module.save_results(flat)


