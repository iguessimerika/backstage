import db
from urllib.parse import urlsplit


ARTIST_RELATION_TYPE = '1'
ORGANIZER_RELATION_TYPE = '2'

LINK_LABELS = {
    1: "Instagram",
    2: "YouTube-Kanal",
    3: "Spotify-Hörprobe",
    4: "SoundCloud-Hörprobe",
    5: "YouTube-Vorschauvideo",
    6: "Facebook-Profil",
    7: "Veranstaler-Website",
    90: "Weitere Plattform",
}

LINK_TYPES = {
    "instagram": 1,     # Instagram
    "youtube": 2,  # YouTube-Profil
    "audio-2": 3,       # Spotify-Hörprobe
    "audio-1": 4,       # SoundCloud-Hörprobe
    "video-1": 5,       # YouTube-Vorschauvideo
    "organizer-fb": 6,  # Facebook Profil
    "organizer-www": 7, # Website der Veranstalter
    "other-sc": 90,    # Weitere Plattform
}


from werkzeug.datastructures import MultiDict


def map_links(data):
    links = []
    fields = data.items(multi=True) if isinstance(data, MultiDict) else data.items()

    for field, value in fields:
        link_type = LINK_TYPES.get(field)

        if field == "additional_links" or field.startswith("additional_links_"):
            link_type = 90

        if link_type is None or not isinstance(value, str):
            continue

        url = value.strip()
        if url:
            links.append((link_type, url))

    return links


def insert_links(cursor, data, relation_id, relation_type):
    rows = [
        (link_type, url, relation_type, relation_id)
        for link_type, url in map_links(data)
    ]

    if rows:
        cursor.executemany(
            """
            INSERT INTO LINKS (`TYPE`, `VALUE`, RELATION_TYPE, RELATION_ID)
            VALUES (%s, %s, %s, %s)
            """,
            rows,
        )






def get_links_byRelationType(relation_id, cursor, relation_type):
    cursor.execute(
        """
        SELECT `TYPE`, `VALUE`
        FROM LINKS
        WHERE RELATION_TYPE = %s AND RELATION_ID = %s
        ORDER BY `TYPE`, LINKID
        """,
        (relation_type, relation_id),
    )

    result = []

    for row in cursor.fetchall():
        url = row["VALUE"].strip()

        try:
            parsed = urlsplit(url)
            hostname = parsed.hostname
        except ValueError:
            continue

        if parsed.scheme not in ("http", "https") or not hostname:
            continue

        result.append({
            "label": LINK_LABELS.get(row["TYPE"], "Weiterer Link"),
            "url": url,
            "domain": hostname.removeprefix("www."),
        })
    return result