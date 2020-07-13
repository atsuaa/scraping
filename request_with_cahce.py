import requests
from cahcecontrol import CacheControl  # pip install CacheControl[filecache]
from cachecontrol.cahces import FileCache

session = requests.Session()
# sessionをラップしたcached_sessionを作る
# キャッシュはファイルとして .webcache ディレクトリ内に保存する
cached_session = CacheControl(session, cache=FileCache('.webcache'))

# 通常のSessionと同様に使用する
response = cached_session.get('https://docs.python.org/3/')

# response.from_cache属性でキャッシュから取得されたレスポンス可動かを取得できる
# 最初はFalse、２回目以降はTrue
print(f'from_cache: {response.from_cache}')
# ステータスコードを表示
print(f'status_code: {response.status_code}')
# レスポンスボディを表示
print(response.text)
