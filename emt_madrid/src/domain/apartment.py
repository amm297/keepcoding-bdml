class Apartment(object):

    def __init__(self, apt_id, latitude, longitude):
        self.apt_id = apt_id
        self.latitude = latitude
        self.longitude = longitude
        self.stops = None

    def to_json(self):
        return {
            'apt_id': self.apt_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'stops': [] if self.stops is None else [stop.to_json() for stop in self.stops]
        }
