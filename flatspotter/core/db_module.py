import sqlite3

from core import fslogger
from core import webpage_parser
import datetime

logger = fslogger.get_logger(__name__)


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS onliner_results(flat_id TEXT, address TEXT, total_price REAL,'
              'sqmeter_price REAL, num_of_rooms INT, floor INT, num_of_floors INT, total_area REAL, created_date TEXT,'
              'updated_date TEXT);')

    c.execute('CREATE TABLE IF NOT EXISTS history(flat_id TEXT, updated_date TEXT, total_price REAL);')

    conn.commit()


conn = sqlite3.connect('data/db/scan_results.db')
c = conn.cursor()
create_table()


def close():
    c.close()
    conn.close()


def save_results(flat: webpage_parser.Flat):
    logger.info('Saving results to DB for flat: ' + str(flat.flat_id))
    c.execute('SELECT * FROM onliner_results WHERE flat_id="' + flat.flat_id +
              '" AND updated_date = "' + flat.updated_date + '";')
    data = c.fetchall()
    conn.commit()
    if len(data) is not 0:
        return

    elif len(data) is 0:
        c.execute('SELECT * FROM onliner_results WHERE flat_id="' + flat.flat_id +
                  '" AND updated_date < "' + flat.updated_date + '";')
        data = c.fetchall()
        conn.commit()

        if len(data) is not 0:
            c.execute('INSERT INTO history(flat_id, updated_date, total_price) SELECT flat_id, updated_date, total_price FROM onliner_results'
                      ' WHERE flat_id="' + flat.flat_id + '" AND updated_date < "' + flat.updated_date + '";')
            conn.commit()

            c.execute('UPDATE onliner_results SET flat_id=' + flat.flat_id + ', address=' + flat.address +
                      ', total_price=' + flat.total_price + ', sqmeter_price=' + flat.sqmeter_price +
                      ', num_of_rooms=' + flat.num_of_rooms + ', floor=' + flat.floor +
                      ', num_of_floors=' + flat.num_of_floors + ', total_area=' + flat.total_area +
                      ', created_date=' + flat.created_date + ', updated_date=' + flat.updated_date +
                      ' WHERE flat_id = "' + flat.flat_id + '";')
            conn.commit()

        elif len(data) is 0:
            c.execute('INSERT INTO onliner_results(flat_id, address, total_price, sqmeter_price, num_of_rooms,'
                      ' floor, num_of_floors, total_area, created_date, updated_date)'
                      ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                      (flat.flat_id, flat.address, flat.total_price, flat.sqmeter_price, flat.num_of_rooms, flat.floor,
                       flat.num_of_floors, flat.total_area, flat.created_date, flat.updated_date))
            conn.commit()


def show_new():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    logger.info('Fetching results from DB for new flats for date: ' + current_date)
    c.execute('SELECT * FROM onliner_results WHERE created_date="' + current_date + '"')
    data = c.fetchall()
    conn.commit()
    logger.debug('DB fetched:\n' + str(data))
    flats = []
    for flat_item in data:
        flat = webpage_parser.Flat()
        flat.flat_id = flat_item[0]
        flat.address = flat_item[1]
        flat.total_price = flat_item[2]
        flat.num_of_rooms = flat_item[4]
        flat.floor = flat_item[5]
        flat.num_of_floors = flat_item[6]
        flat.total_area = flat_item[7]
        flat.created_date = flat_item[8]
        flat.updated_date = flat_item[9]
        flat.sqmeter_price = flat_item[3]
        flats.append(flat)
    return flats


def show_updated():
    current_date = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    updated_date = (current_date - delta).strftime('%Y-%m-%d')
    c.execute('SELECT * FROM onliner_results WHERE updated_date > "' + updated_date + '"')
    data = c.fetchall()
    conn.commit()
    logger.debug('DB fetched:\n' + str(data))
    flats = []
    for flat_item in data:
        flat = webpage_parser.Flat()
        flat.flat_id = flat_item[0]
        flat.address = flat_item[1]
        flat.total_price = flat_item[2]
        flat.num_of_rooms = flat_item[4]
        flat.floor = flat_item[5]
        flat.num_of_floors = flat_item[6]
        flat.total_area = flat_item[7]
        flat.created_date = flat_item[8]
        flat.updated_date = flat_item[9]
        flat.sqmeter_price = flat_item[3]
        flats.append(flat)
    return flats