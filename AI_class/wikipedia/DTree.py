__author__ = "Lina Brilliantova, RIT"
"""This is the implementation of decision tree data structure,
 Left is NO, right is YES"""

class DTree:
    __slots__ = 'root', 'size'

    def __init__(self, root=None):
        self.root = root
        self.size = 1
