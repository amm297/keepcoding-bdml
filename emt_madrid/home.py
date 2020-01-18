#!/usr/bin/env python
import json
import logging
from functools import partial
from multiprocessing.pool import Pool
from os import cpu_count

from src.domain.apartment import Apartment
from src.exception.login_exception import LoginException
from src.openlabs_emt import login, nearby_stops

file_name_dataset = 'resources/airbnb-listings.json'
file_name_output = 'resources/public-transport.json'


def getApartments(file):
    apartments = []
    logging.info('Reading file {0}'.format(file))
    with open(file, 'r') as f:
        json_apartments = json.load(f)
        aux = json_apartments[0:10]
        for json_apartment in aux:
            fields = json_apartment.get('fields')
            apartments.append(Apartment(fields.get('id'), float(fields.get('latitude')), float(fields.get('longitude'))))
        logging.info('File opened and loaded ({0} items) '.format(len(apartments)))
    return apartments


def write_results(apartments_location):
    logging.info('Open file to write')
    file = open(file_name_output, 'w+')
    file.write(',\n'.join([str(ob.to_json()).replace('\'','\"') for ob in apartments_location]))
    logging.info('File writed')


def process(apartments_location):
    try:
        token = login()
        logging.info('Adapt apartments...')
        pool = Pool(cpu_count())
        func = partial(nearby_stops, token)
        res = pool.map(func, apartments_location)
        logging.info('Apartments adapted')
        write_results(res)
    except LoginException as le:
        logging.error(str(le))


def main():
    apartments_location = getApartments(file_name_dataset)
    if len(apartments_location) == 0:
        logging.warning('No data')
    else:
        process(apartments_location)


if __name__ == '__main__':
    main()
