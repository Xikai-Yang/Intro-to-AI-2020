#include "Node.h"

void Node::addChild(Node &node, int index) {
    if (this->children[index] == NULL) {
        this->children[index] = &node;
        node.parent = this;
    } else {
        cout << "already exist the children node" << endl;
    }
}

double Node::upperConfidence() {
    double left = this->winning_times / this->visit_times;
    
    double right = sqrt((log(this->parent->visit_times) * 2) / (this->visit_times));
    return left + right;
}








