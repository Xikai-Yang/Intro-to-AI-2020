class Layer:
    def __init__(self, node_list = None):
        self.node_list = node_list
        self.pinyin = None

    def append(self, node):
        if (self.pinyin is not None) and (node.pinyin != self.pinyin):
            raise Exception("can only add nodes which have the same pinyin")
        if self.node_list is None:
            self.node_list = []
        if self.pinyin is None:
            self.pinyin = node.pinyin
        self.node_list.append(node)

    def delete_node(self, word):
        for i in range(len(self.node_list)):
            node = self.node_list[i]
            if node.word == word:
                del self.node_list[i]
