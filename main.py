import os
import pickle
from urllib import request, response
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from spotify_app import SpotifyApp
from remove_char import Remove
scopes = 'https://www.googleapis.com/auth/youtube.readonly'
credentials = None
# token.pickle stores the user's credentials 

if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)
# Google's Request



# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly'
            ]
        )
        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)

request = youtube.playlistItems().list(part='snippet', playlistId='PlayListID')

response = request.execute()

listofsongs = []
rem =  Remove()
for i in range(len(response['items'])):
    data = response['items'][i]['snippet']['title']
    data = rem.remove(data)
    listofsongs.append(data)
    
print(listofsongs)
app = SpotifyApp()
app.spotify(listofsongs)

