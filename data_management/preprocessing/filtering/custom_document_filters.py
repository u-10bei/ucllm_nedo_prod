from hojichar import document_filters, Document
from fugashi import Tagger

from os import PathLike
from typing import Any, Union
import re

tagger = Tagger('-Owakati')


class DiscardAdultContentJa(document_filters.NgWordsFilterJa):
    """
    TokenFilter の実装例です.
    日本語の成人向けコンテンツを閾値に応じて排除します.
    """

    def __init__(
        self,
        dict_path: Union[str, PathLike] = document_filters.BASE_PATH / "dict/adult_keywords_ja.txt",
        threshold: float = 0.01,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(dict_path, *args, **kwargs)
        self.threshold = threshold

    def apply(self, doc: Document) -> Document:
        adult_keywords_pattern = self.keyword_pat
        matches = re.findall(adult_keywords_pattern, doc.text)
        adult_content_count = len(matches)
        total_words_count = len(tagger.parse(doc.text).split())

        if total_words_count > 0 and adult_content_count / total_words_count > self.threshold:
            doc.is_rejected = True

        return doc


class DiscardNumericAndChineseContentJa(Filter):
    """
    A custom document filter that rejects documents containing only numeric or Chinese numbers.
    """
    def apply(self, doc: Document) -> Document:
        num_text = self.convert_kanji_to_int(doc.text)
        if self.is_numeric_or_chinese(num_text):
            doc.is_rejected = True
        return doc

    def convert_kanji_to_int(self, text: str) -> str:
      result = text.translate(str.maketrans("零〇一壱二弐三参四五六七八九拾、．", "00112233456789十,.", ""))
      convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000", "億": "00000000", "兆": "000000000000", "京": "0000000000000000"}
      unit_list = "|".join(convert_table.keys())
      while re.search(unit_list, result):
          for unit in convert_table.keys():
              zeros = convert_table[unit]
              for numbers in re.findall(f"(\d+){unit}(\d+)", result):
                  result = result.replace(numbers[0] + unit + numbers[1], numbers[0] + zeros[len(numbers[1]):len(zeros)] + numbers[1])
              for number in re.findall(f"(\d+){unit}", result):
                  result = result.replace(number + unit, number + zeros)
              for number in re.findall(f"{unit}(\d+)", result):
                  result = result.replace(unit + number, "1" + zeros[len(number):len(zeros)] + number)
              result = result.replace(unit, "1" + zeros)
      return result

    def is_numeric_or_chinese(self, text: str) -> bool:
        """
        数字又は漢数字だけで構成されている行をチェック
        """
        pattern = r'^[0-9,]*$'

        return bool(re.match(pattern, text))
