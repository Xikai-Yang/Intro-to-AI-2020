class Node:
    def __init__(self, _pinyin, _word, _frequency):
        self.pinyin = _pinyin
        self.word = _word
        self.frequency = _frequency
        self.prob = None
        self.viterbi_value = None
        self.nearest_neighbor = None

    def get_prob(self):
        return self.prob

    def get_pinyin(self):
        return self.pinyin
