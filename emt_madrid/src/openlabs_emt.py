import logging
import os

import requests

from src.domain.line import Line
from src.domain.stop import Stop
from src.exception.login_exception import LoginException

LOGIN = 'https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/'
NEARBY_STOPS = 'https://openapi.emtmadrid.es/v2/transport/busemtmad/stops/arroundxy/{0}/{1}/{2}/'


def login_secrets():
    return {
        'email': os.getenv('EMAIL'),
        'password': os.getenv('PASSWORD'),
        'X-ApiKey': os.getenv('X-API-KEY'),
        'X-ClientId': os.getenv('X-CLIENT-ID')
    }


def login():
    logging.info('Login to openlabs')
    response = requests.get(LOGIN, headers=login_secrets())
    if response.status_code == 200:
        logging.info('Logged OK')
        return response.json().get('data')[0].get('accessToken')
    else:
        raise LoginException('Failed to login')


def nearby_stops_secrets(token):
    return {
        'accessToken': token
    }


# GET AND ADAPT STOP DATA

def adapt_line(json_line):
    name_from = (json_line.get('nameA'), json_line.get('nameB'))[json_line.get('to') == 'A']
    name_to = (json_line.get('nameB'), json_line.get('nameA'))[json_line.get('to') == 'A']
    return Line(json_line.get('line'), json_line.get('label'), name_from, name_to)


def adapt_stop(json_stop):
    return Stop(json_stop.get('stopId'),
                json_stop.get('geometry').get('coordinates')[1],
                json_stop.get('geometry').get('coordinates')[0],
                json_stop.get('stopName'),
                json_stop.get('metersToPoint'),
                [adapt_line(json_line) for json_line in json_stop.get('lines')])


def nearby_stops(token, apartment):
    path = NEARBY_STOPS.format(apartment.longitude, apartment.latitude, 500)
    response = requests.get(path, headers=nearby_stops_secrets(token))
    json_stops = response.json().get('data')
    apartment.stops = [adapt_stop(json_stop) for json_stop in json_stops]
    return apartment
