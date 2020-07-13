import os
from apiclient.discovery import build  # pip install google-api-python-client

# 環境変数からAPIキーを取得する
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']


youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


search_response = youtube.search().list(
    part='snippet',
    q='pubg',
    type='video',
).execute()


for item in search_response['items']:
    # 動画のタイトルを表示する
    print(item['snippet']['title'])
