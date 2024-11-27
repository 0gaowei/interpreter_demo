class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type  # 节点类型（如 Statement, Expression）
        self.value = value          # 节点值（如常量值、变量名）
        self.children = children or []  # 子节点列表

    def __repr__(self, level=0):
        """递归地打印AST树"""
        indent = "     " * level    # 缩进
        result = f"{indent}{self.node_type}: {self.value}"
        if self.children:
            result += "\n"
            for child in self.children:
                result += child.__repr__(level+1) + "\n"
        return result

    def __str__(self):
        return self.__repr__()
