from pylotree.tree import Tree, add_edges

def test_add_edges():

    nwk = "(((A,B)e1,(C,D)e2)e3,E)root;"
    nwk2= "(((A,B),(C,D)),E);"

    assert add_edges(nwk2) == '(((A,B)Edge1,(C,D)Edge2)Edge3,E)Root;'
    assert add_edges(nwk) == nwk

    add_edges("A");


def test_Tree():

    nwk = "(((A,B)e1,(C,D)e2)e3,E)root;"
    nwk2 = "(((A,B)e1,(C,D)e2)e3,E);"

    tree = Tree(nwk)
    tree2 = Tree(nwk2)
    tree3 = Tree(nwk2, name="Tree1")
    assert tree.name == 'root'
    assert tree.preorder[-1].name == "E"
    assert tree.postorder[-1].name == 'root'
    assert tree2.name == "Root"
    assert tree3.name == "Tree1"
    assert tree3.newick.endswith("Tree1;")

    assert tree["e1"].name == "e1"
    assert repr(tree).endswith("root>")

    assert tree.root.name == tree.tree.name

    

