from corpusParser import CorpusParser
from path import *
import os
from Network import Network
import numpy as np
parser = CorpusParser()
parser.load_count(word_count_path)
parser.load_database(single_word_db_path, parser.single_word_db,1)
parser.load_database(double_word_db_path, parser.double_word_db,2)
parser.load_database(triple_word_db_path, parser.triple_word_db, 3)


def read_input(path):
    if not os.path.exists(path):
        raise FileNotFoundError
    with open(path, 'r') as f:
        input_content = f.read().splitlines()
        returned_list = [input_content[i].lower().rstrip().split(" ") for i in range(len(input_content))]
    return returned_list


with open(pinyin_lib_path, 'r') as f:
    pinyin_lib = f.read()
sentence_list = read_input(test_input_path)
with open(test_answer_path, 'r') as f:
    answer_list = f.read().splitlines()


correct_num = 0
correct_sentence = 0
output = ""
for i in range(len(sentence_list)):
    try:
        sentence = sentence_list[i]
        benchmark = answer_list[i]
        network = Network(sentence, parser, pinyin_lib,3)
        out_put_sentence = network.viterbi()
        out_put_sentence = ''.join(out_put_sentence)
        output = output + out_put_sentence + "\n"
        print(out_put_sentence, benchmark)
        correct_sentence += (out_put_sentence == benchmark)
        for j in range(len(out_put_sentence)):
            correct_num += (out_put_sentence[j] == benchmark[j])
    except Exception as e:
        print("Error")


#
# with open(test_output_path,'w') as f:
#     f.write(output)

print(correct_sentence/len(sentence_list))
total_num = np.sum([len(answer_list[i]) for i in range(len(answer_list))])
print(correct_num / total_num)