import os
import pytest
import datetime

from la_ayudante.eat_app.models.reservation import Reservation
from la_ayudante.eat_app.models.table import Table


def test_get_next_reservations_no_reservation_after(t1_6pm):
    assert len(t1_6pm.get_next_reservations()) == 0

def test_get_next_reservations_one_reservation_after(t1_6pm, t1_7pm):
    result = t1_6pm.get_next_reservations()
    assert len(result) == 1
    assert result[0] is t1_7pm

def test_get_next_reservations_two_reservations_after(t1_6pm, t1_7pm, t1_8pm):
    result = t1_6pm.get_next_reservations()
    assert len(result) == 1
    assert result[0] is t1_7pm
