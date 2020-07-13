# 型ヒントのためにインポート
from typing import Iterater
import requests
import lxml.html

def main():
    """
    クローラーのメインの処理
    """

    #複数のページをクロールするのでSessionを使う
    session = requests.Session()


    response = requests.get('https://gihyo.jp/dp')
    # scrape_list_page()関数を呼び出し、ジェネレーターイテレーターを取得する
    urls = scrape_list_page(response)
    for url in urls:
        # Sessionを使って詳細ページを取得する
        response = session.get(url)
        # 詳細ページからスクレイピングして電子書籍の情報を得る
        ebook = scrape_detail_page(response)
        print(ebook)
        # まず１ページだけで試すため、break文で抜ける
        break


def scrape_list_page():
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数
    """
    html = lxml.html.fromstring(response.text)
    # 絶対URLに変換する
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        # yield文でジェネレーターイテレーターの要素を返す
        yield url

def scrape_detail_page(response: requests.Response) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する
    """
    html = lxml.html.fromstring(response.text)
    ebook = {
        # url
        'url': response.url,
        # タイトル
        'title': html.cssselect('#bookTitle')[0].text_content(),
        # 価格（.textで直接の子である文字列のみを取得）, strip()で前後の空白を削除
        'price': html.cssselect('.buy')[0].text.strip(),
        # 目次
        'content': [h3.text_content() for h3 in html.cssselect('#content > h3')]
    }
    # dictを返す
    return ebook

if __name__ == '__main__':
    main()
