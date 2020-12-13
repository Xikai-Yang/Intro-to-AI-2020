#include <iostream>
#include <array>
#include <cmath>
using namespace std;
#define MAX_WIDTH 12

#ifndef NODE_H_
#define NODE_H_


class Node {
public:
    Node* parent;
    Node* children[MAX_WIDTH];
    int x,y;
    double winning_times;
    double visit_times;
    void addChild(Node &node, int index);
    double upperConfidence();
    Node():parent(NULL),winning_times(0),visit_times(0),children{NULL}{};
    Node(int x_, int y_):parent(NULL),winning_times(0),visit_times(0),children{NULL},x(x_),y(y_){};
    void setPosition(int x_, int y_) {
        this->x = x_;
        this->y = y_;
    }
    
};

#endif


