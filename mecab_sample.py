import MeCab

tagger = MeCab.Tagger()
tagger.parse('')  # これは、parseToNode()の不具合を回避するためのハック

# .parseToNode() で最初の形態素を表すNodeオジェクトを取得する
node = tagger.parseToNode('すもももももももものうち')

while node:
    # .surfaceは形態素の文字列、 .featureは品詞などを含む文字列をそれぞれ表す
    print(node.surface, node.feature)
    node = node.next  # .nextで次のNodeを取得する



"""
実行結果

 BOS/EOS,*,*,*,*,*,*,*,*
すもも 名詞,一般,*,*,*,*,すもも,スモモ,スモモ
も 助詞,係助詞,*,*,*,*,も,モ,モ
もも 名詞,一般,*,*,*,*,もも,モモ,モモ
も 助詞,係助詞,*,*,*,*,も,モ,モ
もも 名詞,一般,*,*,*,*,もも,モモ,モモ
の 助詞,連体化,*,*,*,*,の,ノ,ノ
うち 名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
 BOS/EOS,*,*,*,*,*,*,*,*
"""
