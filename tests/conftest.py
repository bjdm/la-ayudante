import pytest
from datetime import datetime

from la_ayudante.eat_app.models.table import Table
from la_ayudante.eat_app.models.reservation import Reservation
from la_ayudante.eat_app.models.note import Note

@pytest.fixture
def t1():
    table = Table('t1_uuid', 1, {})
    return table

@pytest.fixture
def t2():
    table = Table('t2_uuid', 2, {})
    return table

@pytest.fixture
def t1_6pm(t1):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 6:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t1.id],
        {}
    )
    return reservation

@pytest.fixture
def t1_7pm(t1):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 7:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t1.id],
        {}
    )
    return reservation

@pytest.fixture
def t1_8pm(t1):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 8:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t1.id],
        {}
    )
    return reservation

@pytest.fixture
def t2_6pm(t2):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 6:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t2.id],
        {}
    )
    return reservation

@pytest.fixture
def t2_7pm(t2):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 7:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t2.id],
        {}
    )
    return reservation

@pytest.fixture
def t2_8pm(t2):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 8:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t2.id],
        {}
    )
    return reservation

@pytest.fixture
def t1t2_6pm(t1, t2):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 6:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t1.id, t2.id],
        {}
    )
    return reservation

@pytest.fixture
def t1t2_7pm(t1, t2):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 7:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t1.id, t2.id],
        {}
    )
    return reservation

@pytest.fixture
def t1t2_8pm(t1, t2):
    reservation = Reservation(
        'reservation_uuid',
        datetime.strptime('Apr 1 2020 8:00PM', '%b %d %Y %I:%M%p'),
        6300,
        '',
        [t1.id, t2.id],
        {}
    )
    return reservation


@pytest.fixture
def empty_note():
    return Note(None)
