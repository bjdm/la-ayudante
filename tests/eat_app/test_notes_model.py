import pytest
from datetime import datetime

from la_ayudante.eat_app.models.note import Note

# TODO: add fixtures. this is super hacky and gross

def test_next_string_one_reservation_single_table_after(empty_note):
    table_numbers = [1]
    time = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    assert empty_note._next_string([(table_numbers, time)]) == "# Next: T1@7:30PM"

def test_next_string_one_reservation_single_table_after(empty_note):
    table_numbers = [1]
    time = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    assert empty_note._next_string([(table_numbers, time)]) == "# Next: T1@7:30PM"


def test_next_string_one_reservation_multiple_tables_after(empty_note):
    table_numbers = [1, 2]
    time = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    assert empty_note._next_string([(table_numbers, time)]) == "# Next: T1T2@7:30PM"

def test_next_string_multiple_reservations_single_table_after(empty_note):
    table1 = [1]
    table2 = [2]
    time1 = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    time2 = datetime.strptime('Apr 1 2020 7:45PM', '%b %d %Y %I:%M%p')
    res1 = (table1, time1)
    res2 = (table2, time2)
    assert empty_note._next_string([res1, res2]) == "# Next: T1@7:30PM, T2@7:45PM"

def test_next_string_multiple_reservations_single_table_after():
    test_note = Note(None)
    table1 = [1, 2]
    table2 = [3, 4]
    time1 = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    time2 = datetime.strptime('Apr 1 2020 7:45PM', '%b %d %Y %I:%M%p')
    res1 = (table1, time1)
    res2 = (table2, time2)
    assert test_note._next_string([res1, res2]) == "# Next: T1T2@7:30PM, T3T4@7:45PM"

def test_notes_has_header_returns_false_on_none_note():
    test_note = Note(None)
    assert test_note.has_header() == False

def test_has_header_returns_true_only_outstring():
    test_note = Note("# Out @ 7:45PM")
    assert test_note.has_header() == True

def test_has_header_returns_true_only_nextstring():
    test_note = Note("# Next: T1@7:45PM")
    assert test_note.has_header() == True

def test_has_header_returns_true_only_header():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM")
    assert test_note.has_header() == True

def test_has_header_returns_true_header_with_notes():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM\nSome notes.")
    assert test_note.has_header() == True

def test_remove_header_no_current_note():
    test_note = Note(None)
    assert test_note.remove_header() == None
    #assert test_note.note is None

def test_remove_header_only_out_string():
    test_note = Note("# Out @ 7:45PM")
    assert test_note.remove_header() == None

def test_remove_header_only_next_string():
    test_note = Note("# Next: T1@7:45PM")
    assert test_note.remove_header() == None

def test_remove_header_with_note():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM\nSome notes.")
    assert test_note.remove_header() == 'Some notes.'

def test_remove_header_with_multiple_line_note():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM\nSome notes.\nSome other notes.")
    assert test_note.remove_header() == "Some notes.\nSome other notes."

def test_set_header_no_current_note():
    test_note = Note(None)
    assert test_note.set_header("# Out @ 6:45PM", "# Next: T1@7:00PM") == "# Out @ 6:45PM\n# Next: T1@7:00PM"

def test_set_header_only_out_string():
    test_note = Note("# Out @ 7:45PM")
    assert test_note.set_header("# Out @ 6:45PM", "# Next: T1@7:00PM") == "# Out @ 6:45PM\n# Next: T1@7:00PM"

def test_set_header_only_next_string():
    test_note = Note("# Next: T1@7:45PM")
    assert test_note.set_header("# Out @ 6:45PM", "# Next: T1@7:00PM") == "# Out @ 6:45PM\n# Next: T1@7:00PM"

def test_set_header_with_note():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM\nSome notes.")
    assert test_note.set_header("# Out @ 6:45PM", "# Next: T1@7:00PM") == \
    "# Out @ 6:45PM\n# Next: T1@7:00PM\nSome notes."

def test_set_header_with_multiple_line_note():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM\nSome notes.\nSome other notes.")
    assert test_note.set_header("# Out @ 6:45PM", "# Next: T1@7:00PM") == \
    "# Out @ 6:45PM\n# Next: T1@7:00PM\nSome notes.\nSome other notes."

def test_set_header_only_out_time():
    test_note = Note("# Out @ 7:45PM\n# Next: T1@7:45PM\nSome notes.\nSome other notes.")
    assert test_note.set_header("# Out @ 6:45PM") == \
    "# Out @ 6:45PM\nSome notes.\nSome other notes."

def test_generate_note_no_reservation_after():
    test_note = Note(None)
    time = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    test_note.generate_note(time)
    assert test_note.temp_note == "# Out @ 7:30PM"

def test_generate_note_one_reservation_after():
    test_note = Note(None)
    time = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    table = [1]
    res1 = (table, time)
    test_note.generate_note(time, [res1])
    assert test_note.temp_note == "# Out @ 7:30PM\n# Next: T1@7:30PM"

def test_generate_note_one_reservation_after_two_tables():
    test_note = Note(None)
    time = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    table = [1, 2]
    res1 = (table, time)
    test_note.generate_note(time, [res1])
    assert test_note.temp_note == "# Out @ 7:30PM\n# Next: T1T2@7:30PM"

def test_generate_note_two_reservations_after_one_table():
    test_note = Note(None)
    time1 = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    time2 = datetime.strptime('Apr 1 2020 7:45PM', '%b %d %Y %I:%M%p')
    table1 = [1]
    res1 = (table1, time1)
    table2 = [2]
    res2 = (table2, time2)
    test_note.generate_note(time1, [res1, res2])
    assert test_note.temp_note == "# Out @ 7:30PM\n# Next: T1@7:30PM, T2@7:45PM"

def test_generate_note_two_reservations_after_two_tables():
    test_note = Note(None)
    time1 = datetime.strptime('Apr 1 2020 7:30PM', '%b %d %Y %I:%M%p')
    time2 = datetime.strptime('Apr 1 2020 7:45PM', '%b %d %Y %I:%M%p')
    table1 = [1,2]
    res1 = (table1, time1)
    table2 = [3,4]
    res2 = (table2, time2)
    test_note.generate_note(time1, [res1, res2])
    assert test_note.temp_note == "# Out @ 7:30PM\n# Next: T1T2@7:30PM, T3T4@7:45PM"
