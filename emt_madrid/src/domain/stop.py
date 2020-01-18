from src.domain.stop_type import StopType


class Stop:

    def __init__(self, stop_id, latitude, longitude, name, meters, lines):
        self.stop_id = stop_id
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.meters = meters
        self.lines = lines
        self.type = (StopType.BUS, StopType.METRO)['metro' in name.lower()]

    def to_json(self):
        return {
            'stop_id': self.stop_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'name': self.name,
            'meters': self.meters,
            'lines': [] if self.lines is None else [line.to_json() for line in self.lines],
            'type': ('', self.type.name)[self.type is not None],
        }
