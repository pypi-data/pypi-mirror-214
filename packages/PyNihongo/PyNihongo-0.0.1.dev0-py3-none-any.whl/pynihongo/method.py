"""
@Project: https://github.com/KouShoken/pynihongo
@Time: 西暦2023年6月16日 22:00
@Author: KouShoken

This is an open source project that uses the MIT protocol. 
While I don't make any demands, But　I think respecting copyright 
maybe is a basic morality.
"""


class Method:
    def __init__(self):
        pass

    @staticmethod
    def to_seion(text: str) -> str:
        trans = str.maketrans({
            'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
            'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
            'だ': 'た', 'ぢ': 'ち', 'づ': 'つ', 'で': 'て', 'ど': 'と',
            'ば': 'は', 'び': 'ひ', 'ぶ': 'ふ', 'べ': 'へ', 'ぼ': 'ほ',
            'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ',
        })
        return text.translate(trans)
