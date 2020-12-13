## homework1 Implement a Chinese pinyin input method

input: qing hua da xue ji suan ji xi

output: 清华大学计算机系

corpusParser.py：Able to process the original corpus, and count the frequency of single-word, double-word, and triple-word and save accordingly

Node.py: one single Node in the Viterbi algorithm

Layer.py: one layer in the Viterbi algorithm

Network.py: implement the entire network of the Viterbi algorithm, and can use the Viterbi algorithm to generate the corresponding answer.

main.py: Support the command line. We can run the input method such as: python main ../data/input.txt ../data/output.txt

path.py: Global variables holding some paths

test.py: Run Viterbi algorithm on the test set given online (or any other given test set)

parseCorpus.py: The model training may take a long time (5h+). If you want to skip the long training time, the model training results are saved at https://cloud.tsinghua.edu.cn/d/b16e531813bd4015b918/ And You can download the result.zip directly and put it under the result/ folder.
