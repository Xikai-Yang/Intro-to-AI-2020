## Implement a Chinese pinyin input method

### input: qing hua da xue ji suan ji xi

### output: 清华大学计算机系

corpusParser.py：Able to process the original corpus, and count the frequency of single-word, double-word, and triple-word and save accordingly

Node.py: one single Node in the Viterbi algorithm

Layer.py: one layer in the Viterbi algorithm

Network.py: implement the entire network of the Viterbi algorithm, and can use the Viterbi algorithm to generate the corresponding answer.

main.py: Support the command line. We can run the input method such as: python main ../data/input.txt ../data/output.txt

path.py: Global variables holding some paths

test.py: Run Viterbi algorithm on the test set given online (or any other given test set)

parseCorpus.py: The model training may take a long time (5h+). If you want to skip the long training time, the model training results are saved at https://cloud.tsinghua.edu.cn/d/b16e531813bd4015b918/ And You can download the result.zip directly and put it under the result/ folder.

#===============================================================================

/data: The folder is used to store the initial corpus. However, due to the large size of initial corpus, I deleted some txt files in sina_news_gbk, and the initial corpus can be put back into the folder during runtime.

/result: This folder is empty, but it actually stores the results obtained from the training corpus including content.txt / single_word_db.txt / double_word_db.txt / triple_word_db.txt / word_count.txt. And as I said above, you can download them from my Tsinghua cloud share.

/test: The test folder is used to store the test set provided from the professor and the prediction output of our trained model on the test set, in which output_2gram is the output of the **2-gram model**, and output_3gram is the output of the **3-gram** model



