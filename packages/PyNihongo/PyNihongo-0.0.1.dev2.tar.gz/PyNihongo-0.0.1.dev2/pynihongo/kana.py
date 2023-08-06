"""
@Project: https://github.com/KouShoken/pynihongo
@Time: 西暦2023年6月16日 17:06
@Author: KouShoken

This is an open source project that uses the MIT protocol. 
While I don't make any demands, But　I think respecting copyright 
maybe is a basic morality.
"""


class Kana:
    def __init__(self):
        self.gojyuon_table = self.__gojyuon_table()

        # 仮名（戦前の仮名も含む, 清音のみ）
        self.hiragana_list = self.__kana_list(kana_type="hira")
        self.katagana_list = self.__kana_list(kana_type="kata")
        self.romaji_list = self.__romaji_list()

        # 現代仮名（戦前の仮名は含まない, 清音のみ）
        self.kendai_hiragana_list = []

    @staticmethod
    def __gojyuon_table(only_seion=True) -> list:
        """
            Returns:
                [('', 'た', 'タ'), ('ti', 'ち', 'チ'), ('tu', 'つ', 'ツ'), ('te', 'て', 'テ'), ('to', 'と', 'ト')]
        """
        table = []
        X = "akstnhmyrw"
        Y = "aiueo"

        h = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやいゆえよらりるれろわゐうゑをん"
        k = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤイユエヨラリルレロワヰウヱヲン"

        p = 0
        for index_x, x in enumerate(X):
            row = []
            x = x if x != "a" else ""
            for index_y, y in enumerate(Y):
                row.append((x + y, h[p], k[p]))
                p += 1
            table.append(row)

        return table

    def __kana_list(self, kana_type: str = "hira") -> list:
        gojyuon = self.gojyuon_table

        if kana_type.lower() == "hira":
            flag = 1
        elif kana_type.lower() == "kata":
            flag = 2
        else:
            raise TypeError(
                "Unknown Kana Type: %s. Only `hira` or `kata` can be use　(Case insensitive letters)." % kana_type)

        result = []
        for row in gojyuon:
            for col in row:
                result.append(col[flag])
        return result

    def __romaji_list(self, chi: str = "ti", tsu: str = "tu") -> list:
        """
            ローマ字のListである。「ち」と「つ」の表記が変われる。

            Args:
                chi: 「ち」のローマ表記 `ti` or `chi`。
                tsu: 「つ」のローマ表記 `tu` or `tsu`。

            Returns:
                [
                    [('a', 'あ', 'ア'), ('i', 'い', 'イ'), ...],
                    [('ka', 'か', 'カ'), ('ki', 'き', 'キ'), ...],
                ]
        """
        gojyuon = self.__gojyuon_table()
        gojyuon[3][1] = chi
        gojyuon[3][2] = tsu

        result = []
        for row in gojyuon:
            result.append(row[0])

        return result

    """ Mapping """

    def hira_mapping(self):
        gojyuon = self.__gojyuon_table()
        return {item[1]: (item[0], item[2]) for item in gojyuon}

    def kata_mapping(self):
        gojyuon = self.__gojyuon_table()
        return {item[2]: (item[0], item[1]) for item in gojyuon}

    def roma_mapping(self):
        gojyuon = self.__gojyuon_table()
        return {item[0]: (item[1], item[2]) for item in gojyuon}


if __name__ == '__main__':
    kana = Kana()
    print(kana.gojyuon_table)
    print(kana.hiragana_list)
    print(kana.katagana_list)
