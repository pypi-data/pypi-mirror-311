from chinus_emotions.src.emotions.emotions import NewEmotions


_inst = NewEmotions()
minds = _inst.minds
feelings = _inst.feelings
senses = _inst.senses

if __name__ == '__main__':
    a = minds(num=2).print()

