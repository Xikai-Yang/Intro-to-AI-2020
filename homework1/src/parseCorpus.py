from src.corpusParser import CorpusParser

from src.path import *

if __name__ == "__main__":
    """
    pay attention: this file may take you several hours depending on your computer.
    it takes me more than 5 hours to run this file.
    """
    parser = CorpusParser()
    parser.load_corpus(corpus_directory_path)  # load the corpus
    parser.corpus_to_content()                 # convert the corpus into correct format
    parser.write_content(content_path)         # store the content

    parser.parse()                             # calculate the single-word frequency/double-word frequency/triple-word frequency
    print("parse successfully!")
    parser.write_count(word_count_path)
    parser.write_database(single_word_db_path, parser.single_word_db)
    parser.write_database(double_word_db_path, parser.double_word_db)
    parser.write_database(triple_word_db_path, parser.triple_word_db)