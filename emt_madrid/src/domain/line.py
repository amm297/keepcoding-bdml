class Line:

    def __init__(self, code, label, name_from, name_to):
        self.code = code
        self.label = label
        self.name_from = name_from
        self.name_to = name_to

    def to_json(self):
        return {
            'code': self.code,
            'label': self.label,
            'name_from': self.name_from,
            'name_to': self.name_to
        }
