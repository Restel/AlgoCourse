__author__ = "Lina Brilliantova, RIT"
"""This is the implementation of node data structure for decision tree"""

class Node:
    """A Node Class for Decision Tree.
     - Attr is a question that the node asks
     - Chidren is a list of children Nodes
     - Answer is an answer that had led to this Node
     - Parent is a parenting Node"""
    __slots__ = 'attr', 'children', 'answer', 'parent'

    def __init__(self, attr=None, answer=None, children=None, parent = None):
        self.attr = attr
        self.children = children
        self.answer = answer
        self.parent = parent
        if self.children is not None:
            for child in children:
                child.parent = self

    def __str__(self):
        parent = self.parent
        children = self.return_children()
        if parent is not None:
            return 'Node:' + str(self.attr) + '\nparent ' + str(parent.attr) +\
                                        '\n answer ' + str(self.answer) + '\n children: ' + str(children)
        else:
            return 'Node:' + str(self.attr) + '\nparent ' + ' None \n' +\
                                        'answer ' + ' None \n' + 'children: ' + str(children)
    def return_children(self):
        list = []
        if self.children is not None:
            for child in self.children:
                list.append(child.attr)
        else: list.append("NoneType")
        return list

    def _get_root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def add_child(self, child, label):
        """
        :param child: A child Node to be append to self
        :param label: A an answer that connect self and the child nodes
        """
        if self.children is not None:
            self.children.append(child)
        else:
            self.children = [child]
        child.parent = self
        child.answer  = label

    def _find_by_answer(self, answer):
        """Returns the child Node with the corresponding answer to question self.attr"""
        for child in self.children:
                if child.answer == answer:
                    return child
        raise ValueError("There is no children with answer" + str(answer))

def testNode():
    """
    A test function for Node.
    :return: None
    """
    leaf1 = Node("Coffee")
    leaf2 = Node("Student")
    parent = Node("American")
    leaf1.parent = parent
    leaf2.parent = parent
    leaf1.answer = "Yes. American"
    leaf2.answer = "No American"
    parent.children = [leaf1, leaf2]
    print(leaf1)
    print(leaf2)
    print(leaf2._get_root())

    ###############
    node4 = Node('it', 'Yes')
    node5 = Node('nl', 'No')
    node2 = Node('American', 'Yes', children = [node4, node5])
    node3 = Node('it', 'No')
    node1 = Node('Vegetarian', children = [node2])
    print(node1)
    node1.add_child(node3, 'No')
    print(node1)
    print(node2)
    print(node3)
    print(node4)
    print(node2._find_by_answer('No'))

if __name__ == '__main__':
    testNode()