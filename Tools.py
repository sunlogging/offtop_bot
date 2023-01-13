from settings import STATISTICS_NOTE_USER


def get_note_for_user():
    if STATISTICS_NOTE_USER:
        return '@'
    else:
        return ''