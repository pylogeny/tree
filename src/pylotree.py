import newick

__all__ = ['Tree', 'NodeLabels', "root_at"]


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


def get_i(nodeA, nodeB):
    return [i for i in range(2) if nodeA.descendants[i].name ==
            nodeB.name][0] 


def root_at(otree, node_name):
    """
    Root the tree at a specific node.
    """

    # TODO: Edge3 does not work yet!
    tree = Tree(otree.newick)
    node = tree[node_name]
    root = tree.root
    ancestor = node.ancestor
    if ancestor.name == root.name:
        return otree

    # split tree in half
    partA = [d for d in root.descendants if [x for x in d.get_leaf_names() if x
        in node.get_leaf_names()]][0]
    partB = [d for d in root.descendants if not [x for x in d.get_leaf_names() if x
        in node.get_leaf_names()]][0]
    if partA.name != ancestor.name:
        partA.ancestor = None

    partB.ancestor = None

    # assign new data the new root
    root.descendants = [node, ancestor]
    queue = [(ancestor, ancestor.ancestor)]
    aa = ancestor.ancestor
    ancestor.descendants[get_i(ancestor, node)] = aa #ancestor.ancestor
    node.ancestor, ancestor.ancestor = root, root

    while queue:
        nn, aa = queue.pop(0)
        if aa.ancestor:
            aa.descendants[get_i(aa, nn)] = aa.ancestor
            queue += [(aa, aa.ancestor)]
            aa.ancestor = nn
        else:
            aa.descendants[get_i(aa, nn)] = partB
            partB.ancestor = aa
            aa.ancestor = nn
    return tree



def swap_nodes(a, b, c, d, ab, cd, direction=1):
    print(a, b, c, d, ab, cd)
    if direction == 1:
        a.ancestor, c.ancestor = cd, ab
        idxA = [i for i in range(2) if ab.descendants[i].name == a.name][0]
        idxB = [i for i in range(2) if cd.descendants[i].name == c.name][0]
        ab.descendants[idxA] = c
        cd.descendants[idxB] = a
    elif direction == 2:
        swap_nodes(b, a, c, d, ab, cd, direction=1)
    elif direction == 3:
        swap_nodes(a, b, d, c, ab, cd, direction=1)


def nearest_neighbor_interchange(old_tree, node_name, direction=1):
    """
    Nearest neighbor interchange tree manipulation.

    .. note::
       
       Algorithm described in https://www.southgreen.fr/glossary/term/432.
    """
    tree = Tree(old_tree.newick)
    node = tree[node_name]
    assert node.descendants and node.ancestor
    nodeB = node.ancestor
    qA, qB = node.descendants
    if nodeB.name == tree.root.name:
        nodeC = [d for d in nodeB.descendants if d.name != node.name][0]
        if nodeC.descendants:
            qC, qD = nodeC.descendants
            swap_nodes(qA, qB, qC, qD, node, nodeC, direction=direction)
            return tree
        return 
    qC = [d for d in nodeB.descendants if d.name != node.name][0]
    qD = nodeB.ancestor
    if nodeB.descendants:
        swap_nodes(qA, qB, qC, qD, nodeB, node)
        return tree
    return


