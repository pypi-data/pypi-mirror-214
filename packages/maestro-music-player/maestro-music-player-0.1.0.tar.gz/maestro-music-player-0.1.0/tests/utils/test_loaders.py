from maestro.utils.ressources import FALLBACK_COVER

from maestro.utils.loaders import (
    load_config_file,
    load_playlist_file,
    save_playlist_file,
    scan_music_collection,
)

def test_load_config_file(tmp_path):
    config_text = '''
# This is some comment
a:
    b: this is nice # should work
    c: 34
    d: True

# blablabla

other: ['int', 'str']
'''
    expected = {
        'a': {
            'b': 'this is nice',
            'c': 34,
            'd': True,
        },
        'other': ['int', 'str']
    }
    config_path = tmp_path / 'config.yaml'
    with open(config_path, 'w') as file:
        file.write(config_text)
    assert load_config_file(config_path) == expected

def test_load_playlist_file(tmp_path):
    playlist_data = '''
1234
4567

8900
'''
    playlist_path = tmp_path / 'playlist.list'
    with open(playlist_path, 'w') as file:
        file.write(playlist_data)
    db = {
        '4567': 'apple',
        '1234': 'banana',
        '2345': 'lemon',
        '8900': 'orange',
    }
    getter = lambda key: db[key]
    result = list(load_playlist_file(playlist_path, getter))
    assert result == ['banana', 'apple', 'orange']

def test_save_playlist_file(tmp_path):
    playlist_path = tmp_path / 'playlist.list'
    playlist = ['banana', 'apple', 'orange']
    playlist_data = ['1234', '4567', '8900']
    db = {
        '4567': 'apple',
        '1234': 'banana',
        '2345': 'lemon',
        '8900': 'orange',
    }
    getter = lambda key: db[key]
    save_playlist_file(playlist_path, playlist_data)
    assert list(load_playlist_file(playlist_path, getter)) == playlist


def collection_scan_matches_expectations(iter_collection, expectations):
    count = 0
    for album in iter_collection:
        cover, songs = expectations[album.name]
        assert len(album) == len(songs)
        assert cover == album.cover
        album_songs = set(song.name for song in album)
        exp_songs = set(songs)
        assert album_songs == exp_songs
        count += 1
    assert count == len(expectations)

def test_scan_music_collection(tmp_path):
    # prepare directory
    soup_album = tmp_path / 'The big soup'
    soup_album.mkdir()
    for song in ['Carrot.ogg', 'Pumpkin.ogg', 'Salty water.mp3']:
        song_path = soup_album / song
        song_path.touch()
    picture = soup_album / 'big_soup.png'
    picture.touch()
    cover = soup_album / 'cover.png'
    cover.touch()

    cake_album = tmp_path / 'Cakes'
    cake_album.mkdir()
    for song in ['Cupcakes.ogg', 'Pie.ogg']:
        song_path = cake_album / song
        song_path.touch()
    junk = cake_album / 'junk.txt'
    junk.touch()
    cake_cover = cake_album / 'big_soup.png'
    cake_cover.touch()

    empty_album = tmp_path / 'Empty'
    empty_album.mkdir()

    fallback_cover = FALLBACK_COVER.as_posix()

    # not recursive mode
    expectations = {
        'The big soup': (cover.as_posix(), ['Carrot', 'Pumpkin', 'Salty water']),
        'Cakes': (cake_cover.as_posix(), ['Cupcakes', 'Pie']),
    }
    iter_collection = scan_music_collection(tmp_path, recurse=False)
    collection_scan_matches_expectations(iter_collection, expectations)

    # recursive mode
    expectations = {
        tmp_path.stem: (fallback_cover, ['Carrot', 'Pumpkin', 'Salty water',
                                         'Cupcakes', 'Pie']),
        'The big soup': (cover.as_posix(), ['Carrot', 'Pumpkin', 'Salty water']),
        'Cakes': (cake_cover.as_posix(), ['Cupcakes', 'Pie']),
    }
    iter_collection = scan_music_collection(tmp_path, recurse=True)
    collection_scan_matches_expectations(iter_collection, expectations)



