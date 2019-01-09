import sqlite3
import pickle
import fslogger
from webpage_parser import Flat


logger = fslogger.get_logger(__name__)


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS onliner_results(flat_id TEXT, address TEXT, total_price REAL,'
              'sqmeter_price REAL, num_of_rooms INT, floor INT, num_of_floors INT, total_area REAL, created_date TEXT,'
              'updated_date TEXT)')
    conn.commit()


conn = sqlite3.connect('data/db/scan_results.db')
c = conn.cursor()
create_table()


def close():
    c.close()
    conn.close()


def save_results(flat: Flat):
    logger.info('Saving results to DB for flat: ' + str(flat.flat_id))
    serialized_flat = pickle.dumps(flat)
    c.execute('INSERT INTO onliner_results(flat_id, address, total_price, sqmeter_price, num_of_rooms, floor, num_of_floors,'
              'total_area, created_date, updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (flat.flat_id, flat.address, flat.total_price, flat.sqmeter_price, flat.num_of_rooms, flat.floor,
               flat.num_of_floors, flat.total_area, flat.created_date, flat.updated_date))
    conn.commit()

def show_from_db(site_url):
    logger.info('Fetching results from DB by: ' + site_url)
    c.execute('SELECT site_name, tags FROM scan_results WHERE site_url="' + site_url + '"')
    data = c.fetchall()
    conn.commit()
    logger.debug('DB fetched' + str(data))
    site_name = data[len(data)-1][0]
    tags_pickled = data[len(data)-1][1]
    tags_unpickled = pickle.loads(tags_pickled)