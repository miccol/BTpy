from abc import ABCMeta
from LeafNode import LeafNode


class ConditionNode(LeafNode):
    __metaclass__ = ABCMeta  # abstract class
    def __init__(self, name):
        LeafNode.__init__(self,name)
        self.nodeType = 'Condition'
