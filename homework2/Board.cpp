#include <iostream>
#include "Node.h"
#include "Judge.h"
#include "Point.h"
#include <ctime>
#include "Board.h"
#include <string.h>
using namespace std;

#define user 2
#define machine 1
#define empty 0
#define no 3
#define tie 0
#define cont -1
#define limit 1000000
Node tree[limit];

Node* Board::createNewNode(int x, int y) {

    Node* newNode = &tree[used_num++];
    newNode->parent = NULL;
    memset(newNode->children, 0, sizeof(newNode->children));
    newNode->visit_times = 0;
    newNode->winning_times = 0;
    newNode->x = x;
    newNode->y = y;
    return newNode;
}

Board::~Board() {
    delete[] top;
    delete[] backUpTop;
    for(int i = 0; i < this->nrow; i++) {
        delete[] this->board[i];
        delete[] this->backUpBoard[i];
        
    }
    delete[] this->board;
    delete[] this->backUpBoard;
}

Board::Board(const Board& Board_) {
        this->nrow = Board_.nrow;
        this->ncol = Board_.ncol;
        this->lastX = Board_.lastX;
        this->lastY = Board_.lastY;
        this->board = new int*[MAX_SIZE];
        for (size_t i = 0; i < Board_.nrow; i++)
        {
            this->board[i] = new int[MAX_SIZE];
            
            for (size_t j = 0; j < Board_.ncol; j++) {
                this->board[i][j] = Board_.board[i][j];
            }
        }

        memcpy(this->top, Board_.top, sizeof(Board_.top));
        memcpy(this->children, Board_.children, sizeof(Board_.children));
        memcpy(this->childrenRow, Board_.childrenRow, sizeof(Board_.childrenRow));

        this->childNum = Board_.childNum;
}

void Board::init(const int M, const int N, const int* top, const int* _board, 
const int lastX, const int lastY, const int noX, const int noY) {
    this->nrow = M;
    this->ncol = N;
    this->lastX = lastX;
    this->lastY = lastY;

    for (size_t i = 0; i < M; i++)
    {
        this->board[i] = new int[MAX_SIZE];
        this->backUpBoard[i] = new int[MAX_SIZE];
        for (size_t j = 0; j < N; j++) {
            this->board[i][j] = _board[i * N + j];
            this->backUpBoard[i][j] = _board[i * N + j];
        }
    }
    this->top = new int[MAX_SIZE];
    this->backUpTop = new int[MAX_SIZE];
    this->board[noX][noY] = no;
    this->backUpBoard[noX][noY] = no;

    copy(top, top+N, this->top);
    copy(top, top+N, this->backUpTop);

}


int Board::getTop(int col) {
    return this->top[col];
}



Node* Board::selectBestChild(Node* node) {
    double bestScore = INT32_MIN;

    int bestIndex = -1;
    for (int i = 0; i < this->childNum; ++i) {
        int index = this->children[i];
        double score = node->children[index]->upperConfidence();
        if (score > bestScore) {
            bestScore = score;
            bestIndex = index;
        }
    }
    return node->children[bestIndex];


}

Node* Board::treePolicy(Node* node, int& cur_player) {
    int row;
    int col;
    while (true)
    {
        //printBoard();
        findEmptyPosition();
        if (this->childNum == 0) {
            return node;
        }
        bool flag = false;
        for (size_t i = 0; i < this->childNum; i++)
        {
            row = this->childrenRow[i];
            col = this->children[i];
            int temp = board[row][col];
            board[row][col] = cur_player;
            int answer = Judge(cur_player, row, col);
            board[row][col] = temp;
            if (answer == user || answer == machine) {
                flag = true;
                break;
            }
        }
        if (flag) {
            if (!node->children[col]) {
                // Node* newNode = new Node(row, col);
                Node* newNode = createNewNode(row, col);
                node->addChild(*newNode, col);
                playChess(row, col, cur_player);
                return newNode;
            }
            if(node->children[col]) {
                pruning = true;
                // node = node->children[col];
                return node->children[col];
            }
        } else {
            
            for (int i = 0; i < this->childNum; ++i) {
                col = this->children[i];
                row = this->childrenRow[i];
                if (!node->children[col]) {
                    // Node* newNode = new Node(row, col);
                    Node* newNode = createNewNode(row, col);
                    node->addChild(*newNode, col);
                    playChess(row, col, cur_player);
                    return newNode;
                }
            }

            Node* selectedNode = selectBestChild(node);
            col = selectedNode->y;
            row = selectedNode->x;
            playChess(row, col, cur_player);
            node = selectedNode;
            cur_player = (user + machine) - cur_player;

        }  

    }

}


void Board::findEmptyPosition() {
    
    
    memset(this->children, 0, sizeof(this->children));
    memset(this->childrenRow, 0, sizeof(this->childrenRow));
    this->childNum = 0;

    for (int i = 0; i < ncol; ++i) {

        int row = getTop(i);
        if (row == 0) {
            continue;
        }
        if (row == 1)
        {
            if(board[row - 1][i] == empty) {
                this->children[this->childNum] = i;
                this->childrenRow[this->childNum] = row - 1;
                this->childNum++;
            } else {
                continue;
            }
        }

        if (row >= 2) {
            
            if(this->board[row - 1][i] == empty) {
                this->children[this->childNum] = i;
                this->childrenRow[this->childNum] = row - 1;
                this->childNum++;
            }
            if (this->board[row - 1][i] == no) {
                this->children[this->childNum] = i;
                this->childrenRow[this->childNum] = row - 2;
                this->childNum++;
            }
        }

    }
}




int Board::Judge(int cur_player, int x, int y) {


    if (cur_player == user && machineWin(x,y,this->nrow, this->ncol, this->board)) {
        return user;
    }
    if (cur_player == machine && userWin(x, y, this->nrow, this->ncol, this->board)) {
        return machine;
    }
    if (isTie(this->ncol, this->top)) {
        return tie;
    }
    return cont;
}

void Board::playChess(int x, int y, int cur_player) {
    this->board[x][y] = cur_player;
    this->top[y] = x;
    if (x >= 1 && this->board[x - 1][y] == no) {
        this->top[y] = x - 1;
    }
}

double Board::defaultPolicy(Node* node, int cur_player) {

    int initPlayer = cur_player;
    int row = node->x;
    int col = node->y;
    int count = 0;
    while (true)
    {    
        int result = Judge(cur_player, row, col);
        if (result == 0) {
            return 0;
        }
        if (result == user || result == machine) {
            //printBoard();
            int score = count == 0 ? 5 : 1;
            return initPlayer == cur_player ? score:-score;
        }
        
        cur_player = (machine + user) - cur_player;
        count++;
        findEmptyPosition();
        /*
        bool winningFlag = false;
        for (size_t i = 0; i < this->childNum; i++)
        {
            row = this->childrenRow[i];
            col = this->children[i];
            int temp = this->board[row][col];
            this->board[row][col] = cur_player;
            int answer = Judge(cur_player, row, col);
            this->board[row][col] = temp;
            if (answer == cur_player) {
                playChess(row, col, cur_player);
                winningFlag = true;
                break;
            }
        }

        if (winningFlag) {
            playChess(row, col, cur_player);
            continue;
        }
        */
        int index = rand() % this->childNum;
        // 此处应该走必胜剪枝!

        col = this->children[index];
        row = this->childrenRow[index];
        playChess(row, col, cur_player);
        //printBoard();
        
    }

}

void Board::backWard(Node* node, double score) {
    // 要求整个Board的父节点为nullptr
    while(node) {
        node->visit_times++;
        node->winning_times += score;
        score=score > 1 ? (1 - score):(score < -1 ? -score - 1 : -score);
        node=node->parent;
    }
}


Node* Board::decideChild(Node* node) {
    double bestScore = INT32_MIN;
    Node* bestNode = NULL;
    for (size_t i = 0; i < MAX_SIZE; i++)
    {
        Node* child = node->children[i];
        if (child) {
            // double score = child->upperConfidence();
            double score = child->winning_times/child->visit_times;
            if(score > bestScore) {
                bestScore = score;
                bestNode = child;
            }
        }
    }
    return bestNode;
    
}


void Board::backUp() {
    for(int i = 0; i < this->nrow; i++) {
        for(int j = 0; j < this->ncol; j++){
            this->board[i][j] = this->backUpBoard[i][j];
        }
    }
    copy(this->backUpTop, this->backUpTop + MAX_SIZE, this->top);
}




Point* Board::search(double time_limit) {

    Node* root = this->createNewNode(-1,-1);
    int cur_player = user;
    clock_t begin = clock();
    srand(time(0));
    
    while (((clock() - begin)/(float)CLOCKS_PER_SEC) < time_limit) //satisfy the computation budget
    {
        cur_player = user;
        Node* expanded_node = this->treePolicy(root, cur_player); // return selected node, but don't know its side.
        if (pruning) {
            backWard(expanded_node, 5);
            this->backUp();
            pruning = false;
            continue;
        }
        double reward = this->defaultPolicy(expanded_node, cur_player);
        backWard(expanded_node, reward);
        this->backUp();

    }
    Node* bestChild = decideChild(root);
    Point* point = new Point(bestChild->x, bestChild->y);
    return point;

}



void Board::printBoard() {

    printf("\nboard:\n");
    for(int i = 0; i < this->nrow; i++) {
        for(int j = 0; j < this->ncol; j++) {
            printf("%d ", this->board[i][j]);
        }
        printf("\n");
    }
    for(int j = 0; j < this->ncol; j++) {
        printf("%d ", top[j]);
    }
    printf("\n==================\n");
}