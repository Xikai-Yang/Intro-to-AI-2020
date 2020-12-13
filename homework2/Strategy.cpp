#include <iostream>
#include "Point.h"
#include "Strategy.h"
#include "Board.h"
#include "Node.h"
#include <ctime>
using namespace std;

/*
	���Ժ����ӿ�,�ú������Կ�ƽ̨����,ÿ�δ��뵱ǰ״̬,Ҫ�����������ӵ�,�����ӵ������һ��������Ϸ��������ӵ�,��Ȼ�Կ�ƽ̨��ֱ����Ϊ��ĳ�������
	
	input:
		Ϊ�˷�ֹ�ԶԿ�ƽ̨ά����������ɸ��ģ����д���Ĳ�����Ϊconst����
		M, N : ���̴�С M - ���� N - ���� ����0��ʼ�ƣ� ���Ͻ�Ϊ����ԭ�㣬����x��ǣ�����y���
		top : ��ǰ����ÿһ���ж���ʵ��λ��. e.g. ��i��Ϊ��,��_top[i] == M, ��i������,��_top[i] == 0
		_board : ���̵�һά�����ʾ, Ϊ�˷���ʹ�ã��ڸú����տ�ʼ���������Ѿ�����ת��Ϊ�˶�ά����board
				��ֻ��ֱ��ʹ��board���ɣ����Ͻ�Ϊ����ԭ�㣬�����[0][0]��ʼ��(����[1][1])
				board[x][y]��ʾ��x�С���y�еĵ�(��0��ʼ��)
				board[x][y] == 0/1/2 �ֱ��Ӧ(x,y)�� ������/���û�����/�г������,�������ӵ㴦��ֵҲΪ0
		lastX, lastY : �Է���һ�����ӵ�λ��, ����ܲ���Ҫ�ò�����Ҳ������Ҫ�Ĳ������ǶԷ�һ����
				����λ�ã���ʱ��������Լ��ĳ����м�¼�Է������ಽ������λ�ã�����ȫȡ�������Լ��Ĳ���
		noX, noY : �����ϵĲ������ӵ�(ע:��ʵ���������top�Ѿ����㴦���˲������ӵ㣬Ҳ����˵���ĳһ��
				������ӵ�����ǡ�ǲ������ӵ㣬��ôUI�����еĴ�����Ѿ������е�topֵ�ֽ�����һ�μ�һ������
				��������Ĵ�����Ҳ���Ը�����ʹ��noX��noY��������������ȫ��Ϊtop������ǵ�ǰÿ�еĶ�������,
				��Ȼ�������ʹ��lastX,lastY�������п��ܾ�Ҫͬʱ����noX��noY��)
		���ϲ���ʵ���ϰ����˵�ǰ״̬(M N _top _board)�Լ���ʷ��Ϣ(lastX lastY),��Ҫ���ľ�������Щ��Ϣ�¸������������ǵ����ӵ�
	output:
		������ӵ�Point
*/
Point* getPoint(const int M, const int N, const int* top, const int* _board, 
	const int lastX, const int lastY, const int noX, const int noY){
	/*
		��Ҫ������δ���
	*/
	// int x = -1, y = -1;//���ս�������ӵ�浽x,y��
	// int** board = new int*[M];
	// for(int i = 0; i < M; i++){
	// 	board[i] = new int[N];
	// 	for(int j = 0; j < N; j++){
	// 		board[i][j] = _board[i * N + j];
	// 	}
	// }

	Board mcts = Board();

	mcts.init(M,N,top,_board,lastX,lastY,noX,noY);
	// mcts.printBoard();
	Point* returnedPoint = mcts.search();
	return returnedPoint;
		/* code */
	

	
	
	
	
	/*
		�������Լ��Ĳ������������ӵ�,Ҳ���Ǹ�����Ĳ�����ɶ�x,y�ĸ�ֵ
		�ò��ֶԲ���ʹ��û�����ƣ�Ϊ�˷���ʵ�֣�����Զ����Լ��µ��ࡢ.h�ļ���.cpp�ļ�
	*/
	//Add your own code below
	
     //a naive example
	// for (int i = N-1; i >= 0; i--) {
	// 	if (top[i] > 0) {
	// 		x = top[i] - 1;
	// 		y = i;
	// 		break;
	// 	}
	// }
    
	
	
	/*
		��Ҫ������δ���
	*/
	// clearArray(M, N, board);
	
	// return new Point(x,y);
}


/*
	getPoint�������ص�Pointָ�����ڱ�dllģ���������ģ�Ϊ��������Ѵ���Ӧ���ⲿ���ñ�dll�е�
	�������ͷſռ䣬����Ӧ�����ⲿֱ��delete
*/
void clearPoint(Point* p){
	delete p;
	return;
}

/*
	���top��board����
*/
void clearArray(int M, int N, int** board){
	for(int i = 0; i < M; i++){
		delete[] board[i];
	}
	delete[] board;
}


/*
	������Լ��ĸ�������������������Լ����ࡢ����������µ�.h .cpp�ļ�������ʵ������뷨
*/



/*
int main() {
    const int M = 11;
    const int N = 11;
    int board[M][N] = {0};
	for (size_t i = 0; i < M; i++)
	{
		for (size_t j = 0; i < N; i++)
		{
			board[i][j] = 0;
		}
	}
	board[10][1] = 2;
	board[10][2] = 1;
	board[10][3] = 2;
	board[10][4] = 1;
	board[10][5] = 2;
	board[10][6] = 2;
	board[10][7] = 1;

	board[9][2] = 2;
	board[9][3] = 1;
	board[9][4] = 2;
	board[9][5] = 1;
	board[9][6] = 1;
	board[9][7] = 2;

	board[8][3] = 2;
	board[8][4] = 1;
	// board[8][5] = 2;
	board[7][4] = 1;

	int noX = 0;
	int noY = 10;
	int top[N];
    
	for (size_t i = 0; i < N; i++)
    {
        top[i] = M;
    }

	top[1] = 10;
	top[2] = 9;
	top[3] = 8;
	top[4] = 7;
	top[5] = 9;
	top[6] = 9;
	top[7] = 9;

	int lastX = -1;
	int lastY = -1;

    Point* startPoint = getPoint(M,N,top,*board,lastX,lastY,noX,noY);
    cout << startPoint->x << startPoint->y << endl;
    return 0;

}
*/