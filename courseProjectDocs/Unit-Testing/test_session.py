import pytest
from pyinstrument.frame import Frame



def test_add_child_to_parent():
    parent = Frame("parent")  
    child = Frame ("child")  
    
    parent.add_child(child)  
    
    assert child in parent.children  
    
    
def test_parents_lenght():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert len(parent.children) == 1
    
    

def test_child_reference():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert hasattr(child, "parent")


def test_child_parent_reference():
    parent = Frame("parent")  
    child = Frame ("child")
    
    parent.add_child(child)  
    
    assert child.parent is parent
    
    
def test_add_multi_child_to_parent():
    parent = Frame("parent")  
    child = Frame("child")
    child2 = Frame("child2")
    
    
    parent.add_child(child)
    parent.add_child(child2)
    
    
    assert len(parent.children) == 2
    assert parent.children[0] == child
    assert parent.children[1] == child2