from maestro.model.collection import (
    Song,
    Album,
    MusicCollection,
    ComputationNotReady,
)
from maestro.utils.ressources import DUMMY_NAME, EMPTY_ALBUM_NAME, DUMMY_COVER

from pathlib import Path

import pytest

# SONGS

def test_dummy_song():
    dummy = Song.dummy()
    assert dummy.name == DUMMY_NAME
    assert dummy.is_dummy
    assert dummy.uid is None

def test_init_song():
    path = Path('some/path/to/the_song.ogg')
    album = Album('The best music')
    song = Song(path, album, index_clues=False)
    assert song.name == 'the_song'
    assert song.album is album
    assert song.path == path
    assert not song.is_dummy
    assert song.album_name == 'The best music'
    assert song.cover == DUMMY_COVER.as_posix()

def test_init_song_index_clues():
    path = Path('some/path/to/23 Another One.ogg')
    album = Album('The best music')
    song = Song(path, album)
    assert song.name == 'Another One'
    assert song.album_name == 'The best music'
    assert song.index_clue == 23

def test_real_song_with_uid():
    path = Path(__file__).parent / 'test.mp3'
    album = Album('an album')
    song = Song(path, album)
    uid = '8a05d0036e29777db8f135cda34df2b84c722d45'
    assert song.uid == uid
    assert song.get_cache()[path.as_posix()] == uid


# ALBUMS

def test_empty_album():
    empty = Album.empty()
    assert empty.name == EMPTY_ALBUM_NAME
    assert empty.cover == DUMMY_COVER.as_posix()
    assert len(empty) == 0

def test_init_album():
    cover = Path('some/cover.png')
    album = Album('Hello world', cover)
    assert album.name == 'Hello world'
    assert album.cover == cover.as_posix()
    assert len(album) == 0

def test_album_add_song():
    album = Album('Hello world')
    song = Song.dummy()
    album.append(song)
    assert len(album) == 1

def test_album_add_songs():
    album = Album('Hello world')
    songs = [Song.dummy() for _ in range(12)]
    album.extend(songs)
    assert len(album) == 12

# COLLECTION

def test_empty_collection():
    collection = MusicCollection.dummy()
    assert len(collection) == 0
    assert collection.song_table_ready

def test_collection_add_albums():
    collection = MusicCollection.dummy()
    albums = [Album.empty() for _ in range(12)]
    collection.add_albums(albums)
    assert not collection.song_table_ready
    assert len(collection) == 12
    with pytest.raises(ComputationNotReady):
        collection.get_song_by_uid('auie')

def test_collection_sort():
    cache = {
        'apple.ogg': 1,
        'banana.ogg': 2,
        'lemon.ogg': 3,
        'orange.ogg': 4,
        '3 white.ogg': 5,
        '1 milk.ogg': 6,
        '2 dark.ogg': 7,
    }

    fruits = Album("Fruits")
    apple = Song(Path("apple.ogg"), fruits)
    banana = Song(Path("banana.ogg"), fruits)
    lemon = Song(Path("lemon.ogg"), fruits)
    orange = Song(Path("orange.ogg"), fruits)
    fruits.append(lemon)
    fruits.append(banana)
    fruits.append(apple)
    fruits.append(orange)

    chocolate = Album("Chocolate")
    white = Song(Path("3 white.ogg"), chocolate)
    milk = Song(Path("1 milk.ogg"), chocolate)
    dark = Song(Path("2 dark.ogg"), chocolate)
    chocolate.append(white)
    chocolate.append(milk)
    chocolate.append(dark)

    Song.set_cache(cache)

    collection = MusicCollection()
    collection.add_album(fruits)
    collection.add_album(chocolate)
    collection.sort(recursive=False)
    assert collection[0].name == 'Chocolate'
    assert collection[1].name == 'Fruits'
    assert collection[0][0].name == 'white'
    assert collection[1][0].name == 'lemon'
    collection.sort(recursive=True)
    assert collection[0][0].name == 'milk'
    assert collection[1][0].name == 'apple'

