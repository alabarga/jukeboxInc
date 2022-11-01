import random
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

song_listened = {    
    "SongId": 1,    
    "DeviceId": 1,    
    "SongCompletedTime": 100,    
    "OccurredAt": "2021-09-01T12:00:00Z"    
}

song_published = {
  "SongId": 1,
  "SongDetails": {
    "ArtistName": "Amy Winehouse",
    "SongName": "Back in Black",
    "AlbumName": "Back in Black",
    "SongLength": "4:15",
    "SongSizeMb": 8.5
  },
  "OccurredAt": "2018-01-01T12:00:00.000Z"
}

class MusicService():
      
    def __init__(self):
      with open('./credentials/spotify.json') as f:
          credentials = json.load(f)


      client_id = credentials['client_id']
      client_secret = credentials['client_secret']

      self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

    def get_tracks(self, playlist_id='78SmfT0PY9vT0Mvsc6GHiV'):
                    
        track_list = []

        results = self.sp.playlist_items(playlist_id)
        
        for t in results['items']: 
            track = t['track'] #self.sp.track(t['id'])
            track_list.append( {
                  'id': track['id'],
                  'artist': track['artists'][0]['name'],
                  'album':  track["album"]["name"],
                  'duration': round(track['duration_ms']/1000),
                  'name': track['name'],
                  'popularity': track['popularity']
                }) 
        while results['next']:
            results = self.sp.next(results)
            for t in results['items']:  
                track = t['track'] # self.sp.track(t['id'])
                track_list.append( {
                      'id': track['id'],
                      'artist': track['artists'][0]['name'],
                      'album':  track["album"]["name"],
                      'duration': round(track['duration_ms']/1000),
                      'name': track['name'],
                      'popularity': track['popularity']
                    }) 

        return track_list

def __main__():
    pass 

# sp.search('Bruce Springsteen', limit=50)


# bob_marley= '2QsynagSdAqZj3U9HgDzjD'


# bruce_sprinsteen = '3eqjTLE0HfPfh78zjh6TqT'

# playlist_africa = '78SmfT0PY9vT0Mvsc6GHiV'

# albums = []
# for artist in [bruce_sprinsteen, bob_marley]:
#     results = sp.artist_albums(artist, album_type='album')
    
#     albums.extend([sp.album(it['id']) for it in results['items']])
#     while results['next']:
#         results = sp.next(results)
#         albums.extend([sp.album(it['id']) for it in results['items']])


# track_list = []
# for album in albums:
#     results = sp.album_tracks(album['id'])
#     for t in results['items']: 
#         track = sp.track(t['id'])
#         track_list.append( {
#               'id': track['id'],
#               'album':  album['id'],
#               'duration': round(track['duration_ms']/1000),
#               'name': track['name'],
#               'popularity': track['popularity']
#             }) 
#     while results['next']:
#         results = sp.next(results)
#         for t in results['items']:  
#             track = sp.track(t['id'])
#             track_list.append( {
#                   'id': track['id'],
#                   'album':  album['id'],
#                   'duration': round(track['duration_ms']/1000),
#                   'name': track['name'],
#                   'popularity': track['popularity']
#                 }) 


# results = sp.playlist_items(id)
# tracks = results['tracks']
# next_pages = 14
# track_list = []

# for i in range(next_pages):
#     tracks = sp.next(tracks)
#     for y in range(0,100):
#         try:
#             track = tracks['items'][y]['track']['name']
#             artist = tracks['items'][y]['track']['artists'][0]['name']
#             track_list.append(artist)
#         except:
#             continue

# print(track_list)

# a = sp.artist(bruce_sprinsteen)

# res = sp.search('Kaya', type='album', limit=50)

# population = list(range(100))
# random.choices(population, weights=None, k=1)

