from newick import loads
import attr


def add_edges(newick, edge="Edge", root="Root"):
    count, out = 1, ''
    for i in range(len(newick)-1):
        charA, charB = newick[i], newick[i+1]
        if charB == ';':
            if charA == ')':
                out += charA+root+charB
                return out
            else:
                return out+charA+charB;
        else:
            if charA == ')' and charB in [")", ","]:
                out += ')'+edge+str(count)
                count += 1
            else:
                out += charA
    return out


@attr.s(repr=False)
class Tree:

    newick = attr.ib(default=None)
    name = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.newick = add_edges(self.newick, root=self.name or "Root")
        self.tree = loads(self.newick)[0]
        if not self.name:
            self.name = self.tree.name
        self.tree_dict = {node.name: node for node in self.tree.walk()}

    @property
    def preorder(self):
        return list(self.tree.walk(mode="preorder"))
    
    @property
    def postorder(self):
        return list(self.tree.walk(mode="postorder"))

    @property
    def root(self):
        return self.tree

    def __getitem__(self, item):
        return self.tree_dict[item]

    def __repr__(self):
        return '<Tree'+self.name+'>'

