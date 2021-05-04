import pytest

import newick
from pylotree import *


@pytest.mark.parametrize(
    'nwk,kw,res',
    [
        ('((a,b),c)', dict(), '((a,b)Edge1,c)Root'),
        ('((a,b),c)', dict(root_name=None), '((a,b)Edge2,c)Edge1'),
        ('((a,b),c)', dict(node_name_prefix='e', root_name='r'), '((a,b)e1,c)r'),
    ]
)
def test_NodeLabels(nwk, kw, res):
    tree = newick.loads(nwk)[0]
    tree.visit(NodeLabels(**kw))
    assert tree.newick == res


def test_Tree():
    nwk = "(((A,B)e1,(C,D)e2)e3,E)root;"
    nwk2 = "(((A,B)e1,(C,D)e2)e3,E);"

    tree = Tree(nwk)
    assert len(list(tree)) == 9
    tree2 = Tree(nwk2)
    tree3 = Tree(newick.loads(nwk2)[0], name="Tree1")
    assert tree.name == 'root'
    assert tree.preorder[-1].name == "E"
    assert tree.postorder[-1].name == 'root'
    assert tree2.name == "Root"
    assert tree3.name == "Tree1"
    assert tree3.newick.endswith("Tree1;")

    assert tree["e1"].name == "e1"
    assert repr(tree).endswith('"root">')

    assert 'e1' in tree
    tree['e1'].name = 'ex'
    assert ('ex' in tree) and ('e1' not in tree)

    with pytest.raises(KeyError):
        _ = tree['e1']


def test_Tree_copy():
    nwk = "(((A,B)e1,(C,D)e2)e3,E)root;"
    tree1 = Tree(nwk)
    # copying creates new Nodes:
    tree2 = Tree.copy(tree1)
    tree2['e1'].name = 'ex'
    assert 'ex' in tree2 and 'e1' in tree1
    # __init__ does not:
    tree3 = Tree(tree1)
    tree3['e1'].name = 'ex'
    assert 'ex' in tree1
