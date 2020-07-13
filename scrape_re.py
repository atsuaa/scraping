import re
from html import unescape
from urllib.parse import urljoin

#ダウンロードしたファイルを開き、中身を変数htmlに格納する
with open('dp.html') as f:
    html = f.read()

#re.findall()を使って、書籍１冊に相当する部分のhtmlを取得する
#*?は*と同様だが、なるべく短い文字列にマッチする（non-greetyである）ことを表すメタ文字
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    #書籍のURLは itemprop="url" という属性を持つa要素のhref属性から取得する
    url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
    url = urljoin('https://gihyo.jp/', url)

    #書籍のタイトルは itemprop="name" という属性を持つp要素から取得する
    #まずはp要素全体を取得する
    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
    #brタグをスペースに置き換える。str_replace()は文字列を置換する
    title = title.replace('<br/>', ' ')
    #タグを取り除く
    title = re.sub(r'<.*?>', '', title)
    #文字参照（後のコラムを参照）が含まれている場合は元に戻す
    title = unescape(title)

    print(url, title)
