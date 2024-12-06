from chinus_emotions.src.main.emotions.emotion import Emotion


class Minds(Emotion):
    """
    emotions.db의 minds 테이블의 랜덤 row

    생성자 매개변수:
        - num: 갯수
        - positive_percent: 긍적적인 row일 확률

    :ivar word: 단어 리스트
    :ivar mean: 단어의 뜻 리스트
    """


class Feelings(Emotion):
    """
    emotions.db의 feelings 테이블의 랜덤 row

    생성자 매개변수:
        - num: 갯수
        - positive_percent: 긍적적인 row일 확률

    :ivar word: 단어 리스트
    :ivar mean: 단어의 뜻 리스트
    """


class Senses(Emotion):
    """
    emotions.db의 senses 테이블의 랜덤 row

    생성자 매개변수:
        - num: 갯수
        - positive_percent: 긍적적인 row일 확률

    :ivar word: 단어 리스트
    :ivar mean: 단어의 뜻 리스트
    """


if __name__ == '__main__':
    Minds(num=2).print()
