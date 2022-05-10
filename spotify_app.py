import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyApp:
    def __init__(self):
        self.song_uris = []
        
    def spotify(self, song_names):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",redirect_uri="http://localhost:8888/callback",client_id="ClientId",client_secret="ClientSecret",show_dialog=True,
        cache_path="token.txt"))
        user_id = sp.current_user()["id"]
        
        for song in song_names:
            track = song.split('-')[1]
            artist = song.split('-')[0]
            result = sp.search(q=f"track:{track} {artist}", type="track")
        
            try:
                uri = result["tracks"]["items"][0]["uri"]
                self.song_uris.append(uri)
            except IndexError:
                print(f"{song} doesn't exist, skipped.")

        playlist = sp.user_playlist_create(user=user_id, name="Youtube_playlist", public=False)
         
        sp.playlist_add_items(playlist_id=playlist["id"], items=self.song_uris)
        
        print('Done!')

