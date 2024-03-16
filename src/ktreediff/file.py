import os
import dataclasses
from types import NoneType
from ktreediff.util import Util
from ktreediff.node import Node



class DiffNode(Node):
    """ compare files in 2 folders
    
    Example:
    left_dir = "..."
    right_dir = "..."
    
    
    root = DiffNode(None, left_dir, right_dir)
    
    ## do folder matching
    root.do_folder_matching()
    
    ## do folder matching for also subfolders
    root.do_folder_matching(filter=None, recursive=True)
    
    ## do folder matching with filter and recursive
    root.do_folder_matching(filter=('.psd', '.txt'), recursive=True)
    
    """
    def __init__(self, parent, left, right) -> None:
        assert isinstance(parent, (DiffNode, NoneType))
        super().__init__(parent, "", None)
        self._left = left
        self._right = right
        
    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right
    
    def is_file_pair(self):
        if self.left and self.right:
            return os.path.isfile(self.left) and os.path.isfile(self.right)
        return False
    
    def is_different(self):
        if not self.left or not self.right:
            return True
        
        if os.path.isfile(self.left) and os.path.isfile(self.right):
            return not Util.compare_files(self.left, self.right)

        ## 2 folders
        for child in self.children:
            assert isinstance(child, DiffNode)
            if child.is_different():
                return True
        
        return False
    
    
    def do_folder_matching(self, filter:list[str]=None, recursive:bool=False):
        if not os.path.isdir(self.left) or not os.path.isdir(self.right):
            return

        #
        # get file list first
        #
        
        # no recursive here, just direct children
        l_file_list = Util.list_files(self.left, filter, False)
        r_file_list = Util.list_files(self.right, filter, False)
        
        ## name only list
        llist_name = list(map(lambda x: x.replace(self.left + os.sep, ""), l_file_list))
        rlist_name = list(map(lambda x: x.replace(self.right + os.sep, ""), r_file_list))

        same = set(llist_name) & set(rlist_name)
        left_only = set(llist_name) - set(rlist_name)
        right_only = set(rlist_name) - set(llist_name)
        all = list(set(llist_name) | set(rlist_name))
        
        all.sort()
        
        for item in all:
            if item in same:
                left_path = os.path.join(self.left, item)
                right_path = os.path.join(self.right, item)
                
                # both are files or file vs dir with same name
                child_node = DiffNode(self, left_path, right_path)
                self.add_child(child_node)           
                
            elif item in left_only:
                left_path = os.path.join(self.left, item)
                child_node = DiffNode(self, left_path, None)
                self.add_child(child_node)
            
            elif item in right_only:
                right_path = os.path.join(self.right, item)
                child_node = DiffNode(self, None, right_path)
                self.add_child(child_node)
            else:
                raise RuntimeError("Invalid branch")
            
        #
        # get dir list
        #
        l_dir_list = list()
        for item in os.listdir(self._left):
            item_path = os.path.join(self._left, item)
            if os.path.isdir(item_path):
                l_dir_list.append(item_path)
        l_names = list(map(lambda x: x.replace(self.left + os.sep, ""), l_dir_list))
            
        r_dir_list = list()    
        for item in os.listdir(self._right):
            item_path = os.path.join(self._right, item)
            if os.path.isdir(item_path):
                r_dir_list.append(item_path)
        r_names = list(map(lambda x: x.replace(self.right + os.sep, ""), r_dir_list))
                
                
        same = set(l_names) & set(r_names)
        left_only = set(l_names) - set(r_names)
        right_only = set(r_names) - set(l_names)
        
        for item in left_only:
            path = os.path.join(self.left, item)
            self.add_child(DiffNode(self, path, None))
            
        for item in right_only:
            path = os.path.join(self.right, item)
            self.add_child(DiffNode(self, path, None))
            
        for item in same:
            left_path = os.path.join(self.left, item)
            right_path = os.path.join(self.right, item)
            node = DiffNode(self, left_path, right_path)
            self.add_child(node)
            if recursive:
                node.do_folder_matching(filter, recursive)
        
        
    def get_max_child_name_length_and_max_depth(self):
        if self._left:
            name = os.path.basename(self._left)
        else:
            name = ""
        
        l_max = Util.get_east_asian_width_count(name)
        d_max = 0
        for child in self.walk_child():
            assert isinstance(child, DiffNode)
            if child.left:
                name = os.path.basename(child.left)
            else:
                name = ""
                
            l = Util.get_east_asian_width_count(name) + 1  ## dir '/'
            d = child.depth
            
            if l_max < l:
                l_max = l
                
            if d_max < d:
                d_max = d

        return l_max, d_max

    def pprint(self, max_name_length, max_depth, space="    "):
        if self.left:
            left_name =  os.path.basename(self.left)
            if os.path.isdir(self.left):
                left_name = left_name + "/"
        else:
            left_name = "..."

        if self.right:
            right_name = os.path.basename(self.right)
            if os.path.isdir(self.right):
                right_name = right_name + "/"
        else:
            right_name = "..."
        
        
        left_msg = space * self.depth + left_name
        margin = (max_name_length + max_depth * len(space)) - Util.get_east_asian_width_count(left_msg)
        left_msg = left_msg + " " * margin
        
        right_msg = space * self.depth + str(right_name)
        
        if self.is_different():
            print(left_msg, " != ", str(right_msg))
        else:
            print(left_msg, " == ", str(right_msg))
    
        for child in self.children:
            assert isinstance(child, DiffNode)
            child.pprint(max_name_length, max_depth, space)


