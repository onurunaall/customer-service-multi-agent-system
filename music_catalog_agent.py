from langchain_core.tools import tool
import ast

def query(request_query: str):
    """Execute SQL with column headers."""
    return db.run(request_query, include_columns=True)


@tool
def get_albums_by_artist(artist: str):
    """Get all albums by a given artist name."""
    request_query = f"""
        SELECT Album.Title, Artist.Name
        FROM Album
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Artist.Name LIKE '%{artist}%';
    """
    result = query(request_query)
    return result


@tool
def get_tracks_by_artist(artist: str):
    """Get all track names for a given artist."""
    request_query = f"""
        SELECT Track.Name AS SongName, Artist.Name AS ArtistName
        FROM Track
        JOIN Album ON Track.AlbumId = Album.AlbumId
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Artist.Name LIKE '%{artist}%';
    """
    result = query(request_query)
    return result


@tool
def get_songs_by_genre(genre: str):
    """Return up to 8 songs for a genre, grouped by artist."""

    # Get matching genre IDs
    genre_id_query = f"SELECT GenreId FROM Genre WHERE Name LIKE '%{genre}%'"
    raw_ids = db.run(genre_id_query)

    if not raw_ids:
        return f"No songs found for genre: {genre}"

    genre_ids = ast.literal_eval(raw_ids)
    id_list = ", ".join(str(row[0]) for row in genre_ids)

    # Query songs with those genre IDs
    request_query = f"""
        SELECT Track.Name AS Song, Artist.Name AS Artist
        FROM Track
        JOIN Album ON Track.AlbumId = Album.AlbumId
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Track.GenreId IN ({id_list})
        GROUP BY Artist.Name
        LIMIT 8;
    """
    result = query(request_query)

    if not result:
        return f"No songs found for genre: {genre}"

    formatted = []
    parsed = ast.literal_eval(result)
    for row in parsed:
        formatted.append({"Song": row["Song"], "Artist": row["Artist"]})

    return formatted


@tool
def check_for_songs(song_title: str):
    """Check if any songs match the given title."""
    request_query = f"""
        SELECT * FROM Track
        WHERE Name LIKE '%{song_title}%';
    """
    result = query(request_query)
    return result
