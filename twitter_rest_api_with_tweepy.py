import os
import tweepy  # pip install tweepy

# 環境変数から認証情報を取得する
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET_KEY = os.environ['TWITTER_API_SECRET_KEY']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# 認証情報を設定する
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# APIクライアントを取得する
api = tweepy.API(auth)
# ユーザーのタイムラインを取得する
public_tweets = api.home_timeline()

for status in public_tweets:
    # ユーザー名とツイートを表示する
    print('@' + status.user.screen_name, status.text)
