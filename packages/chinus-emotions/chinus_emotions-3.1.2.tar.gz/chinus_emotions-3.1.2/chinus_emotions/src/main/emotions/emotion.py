import random

from chinus_emotions.src.main.db.db_connect import db_connect


class Emotion:
    def __init__(
            self,
            num: int = 1,
            positive_percent: float = 0.7,
    ):
        self.word: tuple
        self.mean: tuple
        self._set_init_vars(num, positive_percent)

    def _set_init_vars(self, num, positive_percent):
        # positive와 negative 동시 True일 경우 처리
        if positive_percent < 0 or positive_percent > 1:
            raise ValueError('positive_percent must be between 0 and 1')

        # WHERE 절 생성
        where_clause = 'WHERE sentiment != -1' if positive_percent <= random.random() else 'WHERE sentiment = -1'

        # 쿼리
        query = f'''
            SELECT word, mean
            FROM {type(self).__name__.lower()}
            {where_clause}
            ORDER BY RANDOM()
            LIMIT {num}
        '''

        self.word, self.mean = zip(*db_connect(query))


    def print(self):
        for word, mean in zip(self.word, self.mean):
            print(f'{word}: {mean}')
