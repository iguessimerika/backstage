import db

ARTIST_RELATION_TYPE = '1'

LINK_LABELS = {
    1: "Instagram",
    2: "YouTube-Kanal",
    3: "Spotify-Hörprobe",
    4: "SoundCloud-Hörprobe",
    5: "YouTube-Vorschauvideo",
    6: "Weitere Plattform",
}

LINK_TYPES = {
    "artist-ig": 1,     # Instagram
    "artist-other": 2,  # YouTube-Profil
    "audio-2": 3,       # Spotify-Hörprobe
    "audio-1": 4,       # SoundCloud-Hörprobe
    "video-1": 5,       # YouTube-Vorschauvideo
    "artist-sc": 6,     # Weitere Plattform
}


def map_artist_links(data):
    links = []

    for field, value in data.items():
        link_type = LINK_TYPES.get(field)

        if field == "additional_links" or field.startswith("additional_links_"):
            link_type = 6

        if link_type is None or not isinstance(value, str):
            continue

        url = value.strip()
        if url:
            links.append((link_type, url))

    return links


def insert_artist_links(cursor, data, artist_id, relation_type):
    rows = [
        (link_type, url, relation_type, artist_id)
        for link_type, url in map_artist_links(data)
    ]

    if rows:
        cursor.executemany(
            """
            INSERT INTO LINKS (`TYPE`, `VALUE`, RELATION_TYPE, RELATION_ID)
            VALUES (%s, %s, %s, %s)
            """,
            rows,
        )

from urllib.parse import urlsplit




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