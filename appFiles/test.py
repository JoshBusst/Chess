def print_opening_lines(root):
    """Print opening lines in a visually appealing tree format"""
    
    def get_path_to_node(node):
        """Get the full move sequence from root to this node"""
        path = []
        current = node
        while current.parent is not None:
            path.append(current.value)
            current = current.parent
        return list(reversed(path))
    
    def format_moves(moves, indent_level=0):
        """Format a sequence of moves with move numbers"""
        result = []
        for i, move in enumerate(moves):
            move_num = (i // 2) + 1
            if i % 2 == 0:  # White's move
                result.append(f"{move_num}.{move}")
            else:  # Black's move
                result.append(move)
        return " ".join(result)
    
    def find_branch_point(path1, path2):
        """Find where two paths diverge"""
        for i in range(min(len(path1), len(path2))):
            if path1[i] != path2[i]:
                return i
        return min(len(path1), len(path2))
    
    def dfs_collect_lines(node, current_path, lines):
        """Collect all complete lines (leaf nodes) in the tree"""
        current_path.append(node)
        
        if not node.children:  # Leaf node
            lines.append(list(current_path))
        else:
            for child in node.children:
                dfs_collect_lines(child, current_path, lines)
        
        current_path.pop()
    
    # Collect all lines
    lines = []
    for child in root.children:
        dfs_collect_lines(child, [], lines)
    
    if not lines:
        return
    
    # Convert node paths to move sequences
    move_lines = [[node.value for node in line] for line in lines]
    
    # Print first line completely
    print(format_moves(move_lines[0]))
    
    # Print subsequent lines with proper indentation
    for i in range(1, len(move_lines)):
        prev_line = move_lines[i - 1]
        curr_line = move_lines[i]
        
        branch_idx = find_branch_point(prev_line, curr_line)
        
        # Calculate indent based on where the branch occurs
        indent_moves = prev_line[:branch_idx]
        indent = len(format_moves(indent_moves))
        
        # Format the diverging portion
        diverging_moves = curr_line[branch_idx:]
        
        # Determine if we need to show the move number for black
        move_num = (branch_idx // 2) + 1
        if branch_idx % 2 == 1:  # Branching on black's move
            formatted = f"{move_num}... {format_moves(diverging_moves)}"
        else:
            formatted = format_moves(diverging_moves, indent_level=branch_idx)
        
        print(" " * indent + formatted)


# Test with your example
class Node:
    def __init__(self, value: str, parent=None):
        self.children = []
        self.parent = parent
        self.value = value

    def __str__(self):
        return self.value
    
    def next(self, value: str=""):
        lst = [str(val) for val in self.children]
        if value in lst:
            return self.children[lst.index(value)]

    def addChild(self, value: str):
        if value not in self.strchild():
            child = Node(value, self)
            self.children.append(child)
            return child
        else:
            return self.getChild(value)
        
    def getChild(self, value: str):
        if value in self.strchild():
            return self.children[self.strchild().index(value)]
    
    def strchild(self):
        return [str(child) for child in self.children]


# Build test tree
root = Node("ROOT")
n = root.addChild("e4")
n = n.addChild("d3")
n = n.addChild("e5")

# First line: 1.e4 d3 2.e5 d6 3.c7
n1 = n.addChild("d6")
n1 = n1.addChild("c7")

# Second line: 1.e4 d3 2.e5 c6 3.Nf4 Qc5
n2 = n.addChild("c6")
n2a = n2.addChild("Nf4")
n2a = n2a.addChild("Qc5")

# Third line: 1.e4 d3 2.e5 c6 3.Qf4 Qf5
n2b = n2.addChild("Qf4")
n2b = n2b.addChild("Qf5")

print_opening_lines(root)