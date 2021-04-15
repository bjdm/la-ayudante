from datetime import datetime
from datetime import timedelta

from la_ayudante.eat_app.models.note import Note
from la_ayudante.eat_app.models.table import Table

class Reservation:
    def __init__(self, id, start_time, notes, table_ids, json):
        self.id = id
        self.start_time = start_time
        self.notes = Note(notes)
        self.json = json
        self.tables = []
        for table_id in table_ids:
            t = Table.get_table_by_id(table_id)
            self.tables.append(t)
            t.add_reservation(self)

    def update_time_notes(self, setup_minutes=5):
        """ Add notes
        Sort out different cases
        """
        # TODO: change this. I want to calculate out_time by getting the
        # generate out string and next string
        #out_time = datetime.DateTime
        next_reservations = self.get_next_reservations()
        if len(next_reservations) < 1:
            # There are no reservations after -> remove the note header if it 
            # exists and exit early
            self.notes.remove_header()
            return
        elif len(next_reservations) == 1:
            if len(self.tables) > 1:
                # the current reservation uses more than one table. allow
                # setup_minutes minutes for setup
                out_time = next_reservations[0].start_time - timedelta(minutes=setup_minutes)
            else:
                out_time = next_reservations[0].start_time
        elif len(next_reservations) > 1:
            if len(self.tables) > 1:
                # more than one of the tables being used by this reservation is
                # required for a proceeding reservation. allow setup_minutes
                # minutes for setup from the EARLIEST next_reservation
                out_time = min(
                    next_reservations,
                    key=lambda r: r.start_time
                ).start_time - timedelta(minutes=setup_minutes)
            else:
                # the current table is part of a reservation using multiple
                # tables. allow setup_minutes minutes for setup
                out_time = next_reservations[0].start_time - timedelta(minutes=setup_minutes)
        else:
            out_time = next_reservations[0].start_time

        self.notes.generate_note(
            out_time,
            (([table.number for table in res.tables], res.start_time) for res in next_reservations)
        )


    def get_next_reservations(self):
        # TODO: only returns 1 reservation if the start_time's are the same. is
        # this the best way to handle this?
        return [table.get_reservation_after(self.start_time)
                for table in self.tables
                if table.get_reservation_after(self.start_time)]


def reservation_from_dict(rd):
    reservation = Reservation(
        rd['id'],
        rd['attributes']['start_time'],
        rd['attributes']['notes'],
        [table['id'] for table in rd['relationships']['tables']['data']],
        rd
    )
    return reservation
