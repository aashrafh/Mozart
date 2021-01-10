from box import Box

note_step = 0.0625

note_defs = {
    -4: ("g5", 79),
    -3: ("f5", 77),
    -2: ("e5", 76),
    -1: ("d5", 74),
    0: ("c5", 72),
    1: ("b4", 71),
    2: ("a4", 69),
    3: ("g4", 67),
    4: ("f4", 65),
    5: ("e4", 64),
    6: ("d4", 62),
    7: ("c4", 60),
    8: ("b3", 59),
    9: ("a3", 57),
    10: ("g3", 55),
    11: ("f3", 53),
    12: ("e3", 52),
    13: ("d3", 50),
    14: ("c3", 48),
    15: ("b2", 47),
    16: ("a2", 45),
    17: ("f2", 53),
}

pitches = {
    -4: ("g5", 79),
    -3: ("f5", 77),
    -2: ("e5", 76),
    -1: ("d5", 74),
    0: ("c5", 72),
    1: ("b4", 71),
    2: ("a4", 69),
    3: ("g4", 67),
    4: ("f4", 65),
    5: ("e4", 64),
    6: ("d4", 62),
    7: ("c4", 60),
    8: ("b3", 59),
    9: ("a3", 57),
    10: ("g3", 55),
    11: ("f3", 53),
    12: ("e3", 52),
    13: ("d3", 50),
    14: ("c3", 48),
    15: ("b2", 47),
    16: ("a2", 45),
    17: ("f2", 53),
}
p = ['c', 'd', 'e', 'f', 'g', 'a', 'b']


class Note(object):
    def __init__(self, rec, sym, staff_rec, sharp_notes=[], flat_notes=[]):
        self.rec = rec
        self.sym = sym

        middle = rec.y + (rec.h / 2.0)
        height = (middle - staff_rec.y) / staff_rec.h

        # print(p[int(height/note_step + 0.5)%7])
        note_def = pitches[int(height/note_step + 0.5)]
        self.note = note_def[0]
        self.pitch = note_def[1]
        if any(n for n in sharp_notes if n.note[0] == self.note[0]):
            self.note += "#"
            self.pitch += 1
        if any(n for n in flat_notes if n.note[0] == self.note[0]):
            self.note += "b"
            self.pitch -= 1
