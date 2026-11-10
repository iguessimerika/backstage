import os, user
from database.artist import dbdata_artist, dbstruct_artist

# Erkennt eine Hörprobe anhand der Link-Adresse
AUDIO_DOMAINS = ("soundcloud.", "spotify.", "bandcamp.", "music.apple.", "deezer.", "audiomack.")
AUDIO_FILES = (".mp3", ".wav", ".ogg", ".m4a", ".flac")


def has_audio_link(artist_data):
    for link in artist_data.get("links") or []:
        values = link.values() if isinstance(link, dict) else link
        for value in values:
            text = str(value).lower()
            if any(domain in text for domain in AUDIO_DOMAINS) or text.endswith(AUDIO_FILES):
                return True
    return False


# Was für den Profilfortschritt zählt – in der Reihenfolge,
# in der es dem Künstler als "nächster Schritt" vorgeschlagen wird.
PROFILE_STEPS = [
    (lambda a: a.get("ARTISTNAME"), "Ergänze deinen Künstlernamen, um dein Profil abzuschließen."),
    (lambda a: a.get("PICTURE"), "Lade ein Profilbild hoch, um dein Profil abzuschließen."),
    (lambda a: a.get("LOCATION"), "Ergänze deinen Standort, um dein Profil abzuschließen."),
    (lambda a: a.get("BIO"), "Schreib ein paar Sätze über dich, um dein Profil abzuschließen."),
    (lambda a: a.get("GENRE_ID"), "Wähle dein Genre, um dein Profil abzuschließen."),
    (has_audio_link, "Ergänze noch eine Hörprobe, um dein Profil abzuschließen."),
]


def create_artist(data, user_id, picture=None):
    # Call the function from dbdata_artist to create the artist in the database
    artist_id = dbdata_artist.create_artist(data, user_id, picture)
    return artist_id


def get_artist_picture(artist_id):
    return dbdata_artist.artist_picture(artist_id)


def get_artist_by_id(artist_id):
    return dbdata_artist.get_artist_by_id(artist_id)


def get_artist_by_userid(user_id):
    return dbdata_artist.get_artist_by_userid(user_id)


""" Calculates how complete the artist profile is.
    Returns the percentage (0-100) and the hint for the next missing field. """
def get_profile_progress(artist_data):
    filled = 0
    next_step = None

    for is_filled, hint in PROFILE_STEPS:
        if is_filled(artist_data):
            filled += 1
        elif next_step is None:
            next_step = hint

    completion = round(filled / len(PROFILE_STEPS) * 100)
    return completion, next_step


def init_artist_db():
    dbstruct_artist.create_artist_table()
