# 型ヒントのためにインポート
from typing import Iterater
import requests
import lxml.html

def main():
    """
    クローラーのメインの処理
    """

    response = requests.get('https://gihyo.jp/dp')
    # scrape_list_page()関数を呼び出し、ジェネレーターイテレーターを取得する
    urls = scrape_list_page(response)
    for url in urls:
        print(url)


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


if __name__ == '__main__':
    main()
