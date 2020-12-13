from corpusParser import CorpusParser
import numpy as np
from Layer import Layer
from Node import Node


class Network:
    def __init__(self, sentence, parser: CorpusParser, pinyin_lib, n_gram=3):
        self.sentence = sentence
        self.parser = parser
        self.network = []
        self.pinyin_lib = pinyin_lib
        self.n_gram = n_gram
        self.lamb = 0.95
        self.alpha = 0.88
        self.beta = 0.1
        self.build_network()


    def cond_prob1(self, cur_node):
        return cur_node.frequency / self.parser.single_word_count

    def cond_prob2(self, cur_node, prev_node):
        pair_pinyin = prev_node.pinyin + " " + cur_node.pinyin
        pair_word = prev_node.word + cur_node.word
        pair_count = self.parser.double_word_db[pair_pinyin].get(pair_word, 0)
        word_count = self.parser.single_word_db[prev_node.pinyin].get(prev_node.word, 0)

        return pair_count / word_count

    def cond_prob3(self, cur_node, prev_node, prev_prev_node):
        triple_pinyin = prev_prev_node.pinyin + " " + prev_node.pinyin + " " + cur_node.pinyin
        triple_word = prev_prev_node.word + prev_node.word + cur_node.word
        if triple_pinyin not in self.parser.triple_word_db:
            return 0
        triple_count = self.parser.triple_word_db[triple_pinyin].get(triple_word, 0)

        pair_pinyin = prev_prev_node.pinyin + " " + prev_node.pinyin
        pair_word = prev_prev_node.word + prev_node.word
        pair_count = self.parser.double_word_db[pair_pinyin].get(pair_word, 0)
        if pair_count == 0:
            return 0
        return triple_count / pair_count

    def cal_prob2(self, cur_node, cur_k):
        lamb = self.lamb
        prob_dict = {}
        prev_node_list = self.network[cur_k - 1].node_list
        for node in prev_node_list:
            pair_pinyin = node.pinyin + " " + cur_node.pinyin
            pair_word = node.word + cur_node.word
            pair_count = self.parser.double_word_db[pair_pinyin].get(pair_word, 0)
            word_count = self.parser.single_word_db[node.pinyin].get(node.word, 0)
            prob = np.log2((pair_count / word_count) * lamb + (1 - lamb) * self.cond_prob1(cur_node))
            prob_dict[pair_word] = prob
        return prob_dict

    def cal_prob3(self, cur_node, cur_k):
        prob_dict = {}
        prev_node_list = self.network[cur_k - 1].node_list
        if cur_k == 1:
            lamb = self.lamb
            for node in prev_node_list:
                pair_word = node.word + cur_node.word
                prob = np.log2(self.cond_prob2(cur_node, node) * lamb + (1 - lamb) * self.cond_prob1(cur_node))
                prob_dict[pair_word] = prob
            return prob_dict
        if cur_k > 1:
            prev_prev_node_list = self.network[cur_k - 2].node_list
            alpha = self.alpha
            beta = self.beta
            gamma = 1 - alpha - beta
            for prev_node in prev_node_list:
                for prev_prev_node in prev_prev_node_list:
                    triple_word = prev_prev_node.word + prev_node.word + cur_node.word
                    prob = alpha * self.cond_prob3(cur_node, prev_node, prev_prev_node) + beta * self.cond_prob2(cur_node,
                            prev_node) + gamma * self.cond_prob1(cur_node)
                    prob = np.log2(prob)
                    prob_dict[triple_word] = prob
            return prob_dict

    def cal_prob(self, cur_node, cur_k):
        if self.n_gram == 2:
            return self.cal_prob2(cur_node, cur_k)
        if self.n_gram == 3:
            return self.cal_prob3(cur_node, cur_k)

    def build_network(self):
        layer = Layer()
        layer.append(Node('B', 'B', self.parser.single_word_db['B']['B']))
        self.network.append(layer)
        for i in range(len(self.sentence)):
            pinyin = self.sentence[i]
            word_list = self.parser.single_word_db[pinyin]
            new_layer = Layer()
            for word, frequency in word_list.items():
                if word not in self.pinyin_lib:
                    continue
                node = Node(pinyin, word, frequency)
                node.prob = self.cal_prob(node, i + 1)
                new_layer.append(node)
            self.network.append(new_layer)

        i = len(self.sentence)
        pinyin = 'E'
        word_list = self.parser.single_word_db[pinyin]
        new_layer = Layer()
        for word, frequency in word_list.items():
            node = Node(pinyin, word, frequency)
            node.prob = self.cal_prob(node, i + 1)
            new_layer.append(node)
        self.network.append(new_layer)

    def viterbi(self):
        if self.n_gram == 2:
            return self.viterbi_2gram()
        if self.n_gram == 3:
            return self.viterbi_3gram()

    def viterbi_2gram(self):
        layer_count = len(self.network)
        for layer_num in range(1, layer_count):
            cur_layer = self.network[layer_num]
            prev_layer = self.network[layer_num - 1]
            if layer_num == 1:
                for cur_node in cur_layer.node_list:
                    word_pair = 'B' + cur_node.word
                    word_pair_prob = cur_node.prob[word_pair]
                    cur_node.viterbi_value = word_pair_prob
            else:
                for cur_node in cur_layer.node_list:
                    for prev_node in prev_layer.node_list:
                        word_pair = prev_node.word + cur_node.word
                        word_pair_prob = cur_node.prob[word_pair]
                        prob = prev_node.viterbi_value + word_pair_prob
                        if cur_node.viterbi_value is None:
                            cur_node.viterbi_value = prob
                            cur_node.nearest_neighbor = prev_node.word
                        else:
                            if prob > cur_node.viterbi_value:
                                cur_node.viterbi_value = prob
                                cur_node.nearest_neighbor = prev_node.word
        answer_hanzi = []
        final_layer = self.network[-1]
        cur_k = layer_count - 2
        last_word = final_layer.node_list[0].nearest_neighbor
        answer_hanzi.append(last_word)
        while True:
            cur_layer = self.network[cur_k]
            if cur_k == 1:
                break
            cur_k -= 1
            for node in cur_layer.node_list:
                if node.word == last_word:
                    answer_hanzi.append(node.nearest_neighbor)
                    last_word = node.nearest_neighbor
                    break
        return answer_hanzi[::-1]

    def viterbi_3gram(self):
        layer_count = len(self.network)
        for layer_num in range(1, layer_count):
            cur_layer = self.network[layer_num]
            prev_layer = self.network[layer_num - 1]
            if layer_num == 1:
                for cur_node in cur_layer.node_list:
                    cur_node.viterbi_value = {}
                    word_pair = 'B' + cur_node.word
                    word_pair_prob = cur_node.prob[word_pair]
                    cur_node.viterbi_value[word_pair] = word_pair_prob

            if layer_num >= 2:
                prev_prev_layer = self.network[layer_num - 2]
                for cur_node in cur_layer.node_list:
                    cur_node.viterbi_value = {}
                    for prev_node in prev_layer.node_list:
                        cur_node.viterbi_value[prev_node.word + cur_node.word] = None
                        for prev_prev_node in prev_prev_layer.node_list:
                            word_triple = prev_prev_node.word + prev_node.word + cur_node.word
                            word_triple_prob = cur_node.prob[word_triple]
                            prob = prev_node.viterbi_value[prev_prev_node.word + prev_node.word] + word_triple_prob

                            if cur_node.viterbi_value[prev_node.word + cur_node.word] is None:
                                cur_node.viterbi_value[prev_node.word + cur_node.word] = prob
                            else:
                                if prob > cur_node.viterbi_value[prev_node.word + cur_node.word]:
                                    cur_node.viterbi_value[prev_node.word + cur_node.word] = prob
        answer_hanzi = []
        cur_k = layer_count - 1
        max_word = None
        max_prob = None
        for node in self.network[cur_k].node_list:
            for key, prob in node.viterbi_value.items():
                if max_word is None:
                    max_word = key[0]
                    max_prob = prob
                if prob > max_prob:
                    max_word = key[0]
                    max_prob = prob
        answer_hanzi.append(max_word)

        while cur_k >= 3:
            cur_k -= 1
            for node in self.network[cur_k].node_list:
                if node.word == max_word:
                    max_word = None
                    max_prob = None
                    for key, prob in node.viterbi_value.items():
                        if max_word is None:
                            max_word = key[0]
                            max_prob = prob
                        if prob > max_prob:
                            max_word = key[0]
                            max_prob = prob
            answer_hanzi.append(max_word)

        return answer_hanzi[::-1]
