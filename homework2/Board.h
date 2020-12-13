#include <iostream>
#include "Node.h"
#include "Point.h"
#include <ctime>

using namespace std;
#define MAX_SIZE 12

class Board {
public:
    int ncol, nrow;
    int **board;
    bool pruning = false;
    int* top;    
    clock_t gamestart;
    int lastX, lastY;
    int children[MAX_SIZE];
    int childrenRow[MAX_SIZE];
    int childNum = 0;
    int used_num = 0;

    int **backUpBoard;
    int *backUpTop;
    Board(){
        this->board = new int*[MAX_SIZE];
        this->backUpBoard = new int*[MAX_SIZE];
    }
    ~Board();
    Board(const Board& Board_);
    void init(const int M, const int N, const int* top, const int* _board, 
	const int lastX, const int lastY, const int noX, const int noY);
    int getTop(int col);



    Node* selectBestChild(Node* node);

    
    void findEmptyPosition();
    int Judge(int cur_player, int x, int y);
    void playChess(int x, int y, int cur_player);
    double defaultPolicy(Node* node, int cur_player);
    void backWard(Node* node, double score);
    Node* decideChild(Node* node);
    Point* search(double time_limit = 2.93);
    void printBoard();
    
    Node* findWinOrLoss(Node* node, int cur_player);
    Node* treePolicy(Node* node, int& cur_player);
    Node* createNewNode(int x, int y);
    void backUp(); 
    int JudgeWinOrLoss(int x, int y);

};