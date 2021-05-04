import newick

__all__ = ['Tree', 'NodeLabels']


class NodeLabels:
    """
    Node visitor to label all un-labeled nodes in a `newick.Node`.

    >>> tree = newick.loads('((a,b),c)')[0]
    >>> tree.visit(NodeLabels(node_name_prefix='e', root_name='root'))
    >>> tree.newick
    '((a,b)e1,c)root'
    """
    def __init__(self, node_name_prefix='Edge', root_name='Root'):
        """
        :param node_name_prefix: `str` to be used as prefix for node names.
        :param root_name: `str` to be used as name for the root node.
        """
        self.node_name_prefix = node_name_prefix
        self.root_name = root_name
        self.count = 0

    def __call__(self, node):
        """
        This is called from `newick.Node.visit`.
        """
        if not node.name:
            if (not node.ancestor) and self.root_name:
                node.name = self.root_name
            else:
                self.count += 1
                node.name = '{}{}'.format(self.node_name_prefix, self.count)


class Tree:
    """
    Wraps a `newick.Node`, providing more convenient node access, etc.
    """
    def __init__(self, tree, name=None):
        if isinstance(tree, Tree):
            self.root = tree.root
        elif isinstance(tree, str):
            self.root = newick.loads(tree)[0]
        else:
            assert isinstance(tree, newick.Node)
            self.root = tree

        self.root.visit(NodeLabels())
        if name:
            self.root.name = name

    @classmethod
    def copy(cls, tree):
        """
        Copy a Tree, creating new `Node`s.
        """
        return cls(tree.newick, name=tree.name)

    @property
    def newick(self):
        return self.root.newick + ';'

    @property
    def name(self):
        return self.root.name

    @property
    def preorder(self):
        return list(self.root.walk())

    @property
    def postorder(self):
        return list(self.root.walk(mode="postorder"))

    def __iter__(self):
        return self.root.walk()

    def __contains__(self, item):
        for n in self.root.walk():
            if n.name == item:
                return True
        return False

    def __getitem__(self, item):
        for n in self.root.walk():
            if n.name == item:
                return n
        raise KeyError()

    def __repr__(self):
        return '<Tree "' + self.name + '">'
