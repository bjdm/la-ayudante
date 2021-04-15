import os
import logging
from la_ayudante.eat_app.api_client import ApiClient
from la_ayudante.eat_app.models.table import table_from_dict
from la_ayudante.eat_app.models.reservation import reservation_from_dict

log = logging.getLogger(__name__)

URL = 'https://api.eatapp.co/restaurant/v2/'

class EatAppWorker:
    """
    Object to be imported into la_ayudante's main module. Should abstract any 
    jobs that may need to be performed with the EatApp API.
    """
    def __init__(self, username=None, password=None):
        self.client = ApiClient(
            URL,
            username=username,
            password=password,
        )

    def process_reservation_finish_times(self):
        _tables = self.client.get_tables_from_api()
        _reservations = self.client.get_reservations_from_api()
        
        tbl = []
        for table in _tables:
            tbl.append(table_from_dict(table))
        rsv = []
        for reservation in _reservations:
            if reservation['attributes']['status'] != 'canceled':
                rsv.append(reservation_from_dict(reservation))

        updated_reservations = []
        for reservation in rsv:
            reservation.update_time_notes()
            if reservation.notes.requires_update:
                updated_reservations.append(reservation)
        
        for reservation in updated_reservations:
            #client.update_note(reservation.id, reservation.notes.note)
            log.debug(reservation.notes.note)
            log.debug(reservation.notes.temp_note)
            self.client.update_note(reservation.id, reservation.notes.temp_note)
