class Resource:

    def __init__(self, id, totUnits):
        self.id = id

        self.totUnits = totUnits
        self.available = totUnits
        self.busy = 0

    def __repr__(self):
        return str(self.__dict__)
