import sys
import logging
from collections import Counter
from pathlib import Path
from typing import List, Iterator, TextIO  # TextIOはstrを取得できるファイルオブジェクトを表す型

import MeCab

tagger = MeCab.Tagger()
tagger.parse('')  # これは、parseToNode()の不具合を回避するためのハック


def main():
    """
    コマンドライン引数で指定したディレクトリ内のファイルを読み込んで、頻出単語を表示する
    """

    # コマンドラインの第１匹数で、WikiExtractorの出力先のディレクトリを指定する
    # Pathオブジェクトはファイルやディレクトリのパス操作を抽象化するオブジェクト
    input_dir = Path(sys.argv[1])

    # 単語の出現回数を格納するCounterオブジェクトを作成する
    # Counterクラスはdictを継承しており、値としてキーの出現回数を保持する

    frequency = Counter()

    # .glob()でワイルドカードにマッチするファイルのリストを取得し、マッチした全てのファイルを処理する
    for path in sorted(input_dir.glob('*/wiki_*')):
        logging.info(f'Processing {path}...')

        with open(path) as file:  # ファイルを開く
            # ファイルに含まれる記事内の単語の出現回数を数え、出現回数をマージする
            frequency += count_words(file)

    # 全処理が完了したら、上位３０件の名刺と出現回数を表示する
    for word, count in frequency.most_common(30):
        print(word, count)


def count_words(file: TextIO) -> Counter:
    """
    WikiExtractorが出力したファイルに含まれる全ての記事から単語の出現回数を数える関数
    """

    # ファイル内の単語の出現頻度を数えるCounterオブジェクト
    frequency = Counter()
    # ログ出力ように、処理した記事数を数えるための変数
    num_docs = 0

    # ファイル内の全記事について反復処理する
    for content in iter_doc_contents(file):
        # 記事に含まれる名刺のリストを取得する
        words = get_words(content)
        # Counterのupdate()メソッドにリストなどの反復可能オブジェクトを指定すると、
        # リストに含まれる値の出現回数を一度に増やせる
        frequency.update(words)
        num_docs += 1

    logging.info(f'Found {len(frequency)} words from {num_docs} documents.')
    return frequency


def iter_doc_contents(file: TextIO) -> Iterator[str]:
    """
    ファイルオブジェクトを読み込んで、記事の中身（開始タグ <doc ...> と終了タグ </doc> の間のテキスト）を
    順に返すジェネレーター関数
    """

    for line in file:
        if line.startswith('<doc '):
            # 開始タグが見つかったらバッファを初期化する
            buffer = []
        elif line.startswith('</doc>'):
            # 終了タグが見つかったらバッファの中身を結合してyieldする
            content = ''.join(buffer)
            yield content
        else:
            # 開始タグ・終了タグ以外の行はバッファに追加する
            buffer.append(line)


def get_words(content: str) -> List[str]:
    """
    文字列内に出現する名刺のリスト（重複含む）を取得する関数
    """

    # 出現した名刺を格納するリスト
    words = []

    node = tagger.parseToNode(content)
    while node:
        # node.featureは間まで区切られた文字列なので、split()で分割して
        # 最初の２項目をposとpos_sub1に代入する。posはPart of Speechの略
        pos, pos_sub1 = node.feature.split(',')[:2]
        # 固有名詞または一般名詞の場合にのみwordsに追加する
        if pos == '名詞' and pos_sub1 in ('固有名詞', '一般'):
            words.append(node.surface)
        node = node.next

    return words


if __name__ == '__main__':
    # INFOレベル以上のログを出力する
    main()

# 実行結果
# 月 245684
# 日本 107683
# 時代 54142
# 駅 46271
# 列車 40740
# 世界 40068
# 昭和 35609
# 作品 35384
# 東京 34624
# 平成 32648
# 一般 32490
# 鉄道 32349
# アメリカ 31932
# 地域 31674
# 中心 29913
# 番組 29027
# 世紀 27427
# ホーム 26819
# 間 25503
# 車両 24794
# バス 24599
# 路線 24500
# 大学 24173
# 主義 24041
# JR 23531
# ドイツ 23411
# 他 23393
# 事業 22604
# 都市 22161
# 形 21955
