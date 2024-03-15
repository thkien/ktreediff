
from types import NoneType
from typing import Any



class Node(object):

    def __init__(self, parent, name:str="", data:Any=None) -> None:
        assert isinstance(parent, (Node, NoneType))   
        self._data = data
        self._parent = parent
        self._children = list()
        
        self._name = name
        self._child_index = 0
        
        self._prev_sibling = None
        self._next_sibling = None
        
        self._cell_row = 0
        self._cell_col = 0
        
        self._meta_data = {}
    
    @property
    def name(self):
        return self._name
    
    @property
    def qname(self, sep='/') -> str:
        name_stack = list()
        p = self
        while p:
            name_stack.append(p.name)
            p = p.parent
        
        name_stack.reverse()
        return sep.join(name_stack)

    @property
    def data(self):
        return self._data
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def children(self) -> list:
        return self._children        
    
    @property
    def root(self):
        p = self
        while True:
            if not p.parent:
                return p
            p = p.parent
    
    @property
    def depth(self) -> int:
        """Depth of this node from root"""
        depth = 0
        p = self.parent
        while p:
            depth += 1
            p = p.parent

        return depth

    @property
    def child_index(self) -> int:
        if self._parent:
            for idx, child in enumerate(self._parent.children):
                assert isinstance(child, Node)
                if id(child) == id(self):
                    return idx
        else:
            return 0
    
    @property
    def previous_sibling(self):
        return self._prev_sibling
    
    @property
    def next_sibling(self):
        return self._next_sibling
    
    @property
    def cell_column(self) -> int:
        return self.depth
    
    @property
    def cell_row(self) -> int:
        count = 0
        if not self.parent: # root node
            return 0
        
        for node in self.root.walk_child():
            count += 1      # plus 1 first because of 'root'
            if node == self:
                break
            
        return count

    def set_meta_data(self, key, value):
        self._meta_data[key] = value
        
    def get_meta_data(self) -> dict:
        return self._meta_data
    
    def _set_previous_sibling(self, node):
        assert isinstance(node, (Node, NoneType))
        self._prev_sibling = node
        
    def _set_next_sibling(self, node):
        assert isinstance(node, (Node, NoneType))
        self._next_sibling = node

    def add_child(self, child):
        assert isinstance(child, Node)
        
        ## set siblings
        if len(self.children) > 0:
            prev_s = self.children[-1] # current last one
            assert isinstance(prev_s, Node)
            prev_s._set_next_sibling(child)
        else:
            prev_s = None
        
        child._set_previous_sibling(prev_s)
        
        # add it now
        self._children.append(child)

    def walk_child(self):
        """ Walk through all children """
        for c in self.children:
            yield c
            for cc in c.walk_child():   # recursive call
                yield cc

    def pprint(self, level=0):
        msg = f"{self.name} (n:{self.name} idx:{self.child_index}, d/c:{self.depth}, r:{self.cell_row})"
        print("  " * level, msg)
        
        for child in self._children:
            child.pprint(level+1)
            


