import sys
import requests

#第１引数からURLを取得する
url = sys.argv[1]

#URLで指定したWebページを取得する
r = requests.get(url)

#バイト列の特徴から推定したエンキーディングを使用する
r.encoding = r.apparent_encoding

#エンコーディングを標準エラー出力に出力する
print(f'encoding: {r.encoding}', file=sys.stderr)

#デコードしたレスポンスボディを標準出力に出力する
print(r.text)
