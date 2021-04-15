from datetime import timedelta, datetime
import re

class Note:
    out_re = re.compile(r"^#\sOut\s@\s[0-1]?[0-9]:[0-5][0-9][A|P]M$")
    next_re = re.compile(r"^#\sNext:\s(((T\d+)*@[0-1]?[0-9]:[0-5][0-9][A|P]M)(,\s?)?)*$")


    def __init__(self, note):
        self.note = note
        self.temp_note = None
        self.requires_update = False 

    def _out_string(self, out_time, prefix="# Out @ "):
        return "{}{}".format(
            prefix,
            datetime.strftime(out_time, "%I:%M%p").lstrip('0').rstrip('\n')
        )

    def _next_string(self, reservations, prefix="# Next: "):
        """ Next reservations should be a list of tuples where the tuples are
        Tuple(List[table_number: Int], Datetime: start_time) 
        Note: sanity checking for whether or not there is a reservation after
        should happen before this function is called.
        """
        string = prefix
        for reservation_tuple in reservations:
            for table in reservation_tuple[0]:
                string += 'T' + str(table)
            string += '@' + datetime.strftime(reservation_tuple[1], "%I:%M%p").lstrip('0') + ', '
        return string.rstrip(', ')

    def has_header(self):
        if self.note is not None:
            lines = self.note.splitlines()
            for line in lines:
                if re.match(self.out_re, line) or re.match(self.next_re, line):
                    return True
                else:
                    return False
        else:
            return False

    def remove_header(self):
        if self.note is None:
            return
        new_note = []
        for line in self.note.splitlines():
            if re.match(self.out_re, line) or re.match(self.next_re, line):
                pass
            else:
                new_note.append(line) 
        return '\n'.join(new_note) or None


    def set_header(self, out_string, next_string):
        if self.remove_header():
            note = self.remove_header().splitlines()
        else:
            note = []
        note.insert(0, next_string)
        note.insert(0, out_string)
        return '\n'.join(note)


    def generate_note(self, out_time, next_tables):
        if next_tables is None:
            self.temp_note = self.note.remove_header()
        else:
            out_string = self._out_string(out_time)
            next_string = self._next_string(next_tables)
            self.temp_note = self.set_header(out_string, next_string)
        if self.temp_note == self.note:
            self.requires_update = False
            self.temp_note = None
        else:
            self.requires_update = True
