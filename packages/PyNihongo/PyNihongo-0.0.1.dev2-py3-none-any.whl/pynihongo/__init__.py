"""
@Project: PyCharm　https://github.com/KouShoken/pynihongo
@Time: 西暦2023年6月16日 14:49
@Author: KouShoken

This is an open source project that uses the MIT protocol. 
While I don't make any demands, But　I think respecting copyright 
maybe is a basic morality.
"""
from .kana import Kana
from .method import Method


class Get:
    __kana = Kana()
    gojyuon_table = __kana.gojyuon_table

    # 仮名（戦前の仮名も含む, 清音のみ）
    hiragana_list = __kana.hiragana_list
    katagana_list = __kana.katagana_list
    romaji_list = __kana.romaji_list

    # 現代仮名（戦前の仮名はない, 清音のみ）
    kendai_hiragana_list = []
