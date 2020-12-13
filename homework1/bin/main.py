import sys
from corpusParser import CorpusParser
from path import *
import os
from Network import Network


def read_input(path):
    if not os.path.exists(path):
        raise FileNotFoundError
    with open(path, 'r') as f:
        input_content = f.read().splitlines()
        returned_list = [input_content[i].lower().rstrip().split(" ") for i in range(len(input_content))]
    return returned_list


if __name__ == "__main__":
    with open(pinyin_lib_path, 'r') as f:
        pinyin_lib = f.read()
    parser = CorpusParser()
    parser.load_count(word_count_path)
    parser.load_database(single_word_db_path, parser.single_word_db, 1)
    parser.load_database(double_word_db_path, parser.double_word_db, 2)
    parser.load_database(triple_word_db_path, parser.triple_word_db, 3)
    sentence_list = read_input(sys.argv[1])
    output_path = sys.argv[2]

    output_content = ""
    for sentence in sentence_list:
        network = Network(sentence, parser, pinyin_lib)
        output_sentence = network.viterbi_3gram()
        output_sentence = ''.join(output_sentence)
        output_content = output_content + output_sentence + "\n"
        print(output_sentence)
    with open(output_path, 'w') as f:
        f.write(output_content)
        print("successfully finished!")
