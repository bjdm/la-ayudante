class Table:
    _tables = {}

    def __init__(self, id, number, json):
        self.id = id
        self.number = number
        self.json = json
        self.reservations = []
        Table._tables[str(self.id)] = self

    def add_reservation(self, reservation):
        """ Add the given `reservation` to the current tables list of 
        reservations."""
        self.reservations.append(reservation)

    def get_reservation_after(self, start_time):
        """ Returns the reservation after `start_time` on the given table."""
        return( 
            min(
                (reservation for reservation in self.reservations
                if start_time < reservation.start_time),
                key=lambda k: k.start_time,
                default=None
            )
        )

    @classmethod
    def add_reservation_by_id(cls, id, reservation):
        cls._tables[id].add_reservation(reservation)

    @classmethod
    def get_table_by_id(cls, id):
        return cls._tables[id]


def table_from_dict(td):
    table = Table(
        td['id'],
        td['attributes']['number'],
        td
    )
    return table
