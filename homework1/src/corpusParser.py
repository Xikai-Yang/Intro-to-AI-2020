import os
import pandas as pd
import re
import json
from pypinyin import lazy_pinyin
import zhon.hanzi
import cn2an


class CorpusParser:
    def __init__(self):
        self.corpus = None
        self.removal = '[^\u4e00-\u9fff]+'
        self.single_word_db = {}
        self.double_word_db = {}
        self.triple_word_db = {}
        self.single_word_count = 0
        self.double_word_count = 0
        self.triple_word_count = 0
        self.content = []

    def load_corpus(self, directory_path):
        if self.corpus is not None:
            return self.corpus
        data_list = []
        for filename in os.listdir(directory_path):
            if filename != "README.txt":
                file_path = directory_path + filename
                tmp_data = pd.read_json(file_path, lines=True)
                data_list.append(tmp_data)
        corpus = pd.concat(data_list)
        corpus = pd.concat([corpus['html']], axis=0)
        corpus.index = range(len(corpus))
        self.corpus = corpus

    def corpus_to_content(self):
        content = []
        punctuation = zhon.hanzi.stops + "，;"
        for i in range(len(self.corpus)):
            try:
                processed_text = re.split(r"[%s]+" % punctuation, cn2an.transform(self.corpus[i], mode = 'an2cn'))
            except ValueError:
                pass
            processed_list = [re.sub(self.removal, '', processed_text[i]) for i in range(len(processed_text))]
            processed_list = ['B' + processed_list[i] + 'E' for i in range(len(processed_text)) if len(processed_list[i]) >= 2]
            # processed_list = ''.join(processed_list)
            content.extend(processed_list)
        self.content = content

    def write_content(self, content_path):
        if self.content is not None:
            with open(content_path, 'w') as f:
                for line in self.content:
                    f.write(line + "\n")

    def load_content(self, content_path):
        if os.path.exists(content_path):
            temp_list = []
            with open(content_path, 'r') as f:
                string = f.read()
                temp_list = string.splitlines()
                self.content = temp_list

    def write_database(self, path, db):
        with open(path, 'w') as f:
            f.write(json.dumps(db))

    def load_database(self, path, db, word_num=1):
        if not os.path.exists(path):
            raise FileNotFoundError
        with open(path, 'r') as f:
            string = f.read()
            db = json.loads(string)
        if word_num == 1:
            self.single_word_db = db
        elif word_num == 2:
            self.double_word_db = db
        elif word_num == 3:
            self.triple_word_db = db

    def write_count(self, path):
        count_dict = {'single_word_count': self.single_word_count, 'double_word_count': self.double_word_count,
                      "triple_word_count": self.triple_word_count}
        with open(path, "w") as f:
            f.write(json.dumps(count_dict))

    def load_count(self, path):
        with open(path, 'r') as f:
            string = f.read()
            count_dict = json.loads(string)
            self.single_word_count = count_dict['single_word_count']
            self.double_word_count = count_dict['double_word_count']
            self.triple_word_count = count_dict['triple_word_count']

    def parse(self):
        k = 0
        for item in self.content:
            if k % 1000000 == 0:
                print("%d th item is processing" % k)
            k += 1
            for idx in range(len(item)):
                word = item[idx]
                word_pinyin = lazy_pinyin(word)[0]
                if word_pinyin not in self.single_word_db:
                    self.single_word_db[word_pinyin] = {}
                if word not in self.single_word_db[word_pinyin]:
                    self.single_word_db[word_pinyin][word] = 0
                self.single_word_db[word_pinyin][word] += 1
                self.single_word_count += 1

                if idx >= 1:
                    # double word
                    if word == 'B':
                        continue
                    prev_word = item[idx - 1]
                    word_pair = prev_word + word
                    word_pair_pinyin = " ".join(lazy_pinyin(word_pair))
                    if word_pair_pinyin not in self.double_word_db:
                        self.double_word_db[word_pair_pinyin] = {}
                    if word_pair not in self.double_word_db[word_pair_pinyin]:
                        self.double_word_db[word_pair_pinyin][word_pair] = 0
                    self.double_word_db[word_pair_pinyin][word_pair] += 1
                    self.double_word_count += 1

                if idx >= 2:
                    prev_prev_word = item[idx - 2]
                    prev_word = item[idx - 1]
                    triple_word = prev_prev_word + prev_word + word
                    triple_word_pinyin = " ".join(lazy_pinyin(triple_word))
                    if triple_word_pinyin not in self.triple_word_db:
                        self.triple_word_db[triple_word_pinyin] = {}
                    if triple_word not in self.triple_word_db[triple_word_pinyin]:
                        self.triple_word_db[triple_word_pinyin][triple_word] = 0
                    self.triple_word_db[triple_word_pinyin][triple_word] += 1
                    self.triple_word_count += 1
