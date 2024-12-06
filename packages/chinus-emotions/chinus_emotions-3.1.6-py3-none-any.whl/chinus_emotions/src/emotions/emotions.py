import random
from chinus_emotions.src.db.db_connect import db_connect
import inspect


class Emotions:
    """
    랜덤한 감정 가져오는 클래스

    :ivar words: 단어 리스트
    :ivar means: 단어의 뜻 리스트
    """
    def __init__(self, words, means):
        self.words = words
        self.means = means

    def print(self):
        for word, mean in zip(self.words, self.means):
            print(f'{word}: {mean}')
        return self


class NewEmotions:
    _NUM = 1
    _POSITIVE_PERCENTAGE = 0.7

    def __init__(self):
        self.words: tuple
        self.means: tuple

    def _set_ivars(self, table_name, num, positive_percent):
        """
        :param table_name: db에서 선택할 테이블 이름
        :param num: db에서 가져올 감정 갯수
        :param positive_percent: 긍적적인 감정일 확률 default 70%
        :return:
        """

        if positive_percent < 0 or positive_percent > 1:
            raise ValueError('positive_percent must be between 0 and 1')

        # WHERE 절 생성
        where_clause = 'WHERE sentiment != -1' if positive_percent <= random.random() else 'WHERE sentiment = -1'

        # 쿼리
        query = f'''
            SELECT word, mean
            FROM {table_name}
            {where_clause}
            ORDER BY RANDOM()
            LIMIT {num}
        '''

        self.words, self.means = zip(*db_connect(query))

    def _process(self, num, positive_percent):
        table_name = inspect.currentframe().f_back.f_code.co_name
        self._set_ivars(table_name, num, positive_percent)

    def minds(self, num: int = _NUM, positive_percent: float = _POSITIVE_PERCENTAGE) -> Emotions:
        self._process(num, positive_percent)
        return Emotions(self.words, self.means)

    def feelings(self, num: int = _NUM, positive_percent: float = _POSITIVE_PERCENTAGE) -> Emotions:
        self._process(num, positive_percent)
        return Emotions(self.words, self.means)

    def senses(self, num: int = _NUM, positive_percent: float = _POSITIVE_PERCENTAGE) -> Emotions:
        self._process(num, positive_percent)
        return Emotions(self.words, self.means)