import re

def validate_price(value: str):
    """
    valueが価格として正しい文字列（数字とカンマのみを含む文字列）であるかどうかを判断し、
    正しくない値の場合は例外ValueErrorを発生させる
    """
    # 数字とカンマのみを含む正規表現にマッチするかチェックする
    if not re.search(r'^[0-9,]+$', value):
        #マッチしない場合は例外を発生させる
        raise ValueError(f'Invalid price: {value}')

validate_price('3,000')  # 例外は発生しない
validate_price('無料')  # 例外は発生する
