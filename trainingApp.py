
class Node: pass



class Node:
    def __init__(self, value: str, parent: Node):
        self.children: list[Node] = []
        self.parent: Node = parent
        self.value = value

    def __str__(self):
        return self.value
    
    def next(self, value: str="") -> str:
        lst: list = [str(val) for val in self.children]

        if value in lst:
            return self.children[lst.index(value)]

    def addChild(self, value: str) -> Node:
        """Adds a child to parent class and returns a reference to it."""
        if value not in self.strchild():
            child: Node = Node(value, self)
            self.children.append(child)

            return child
        else:
            return self.getChild(value)
        
    def getChild(self, value: str) -> Node:
        if value in self.strchild():
            return self.children[self.strchild().index(value)]
    
    def strchild(self) -> list[str]:
        """Returns string list of children."""
        return [str(child) for child in self.children]

class Root(Node):
    def __init__(self, value: str):
        super().__init__(value, None)



class Tree:
    def __init__(self, root: Root):
        self.root: Root = root

    # merges a pgn into the tree
    def merge(self, pgn: str) -> bool:
        moves: list[str] = split_pgn(pgn)
        current: Node = self.root

        if str(current) != moves[0]:
            print("Cannot merge tree with root mismatch!")
            raise ValueError

        for move in moves[1:]:
            child: Node = current.getChild(move)

            if child:
                # move through present children
                current = child
            else:
                # create a new child
                child = current.addChild(move)
                current = child

    def __str__(self) -> str:
        def recurse(node: Node, depth: int) -> str:
            childstrs: list[str] = []
            out: str = ""

            for child in node.children:
                childstrs.append(recurse(child, depth + 1))
                
            out = f"{int(depth/2+1)}.{node.value} " if depth%2 == 0 else f"{node.value} "
                
            if len(childstrs) > 0:
                out += childstrs[0]
                spacer = "        "

                for childstr in childstrs[1:]:
                    out += '\n'

                    if depth%2 == 0:
                        out += spacer * int(depth/2)
                        out += f"{int(depth/2 + 1)}... {childstr}"
                    else:
                        
                        out += spacer * int((depth + 1)/2)
                        out += f"{childstr}"
                        

            # print(f"Interim result: {out}")

            return out

        return recurse(self.root, 0)

class Database:
    def __init__(self):
        self.trees: list[Tree] = []

    def getTree(self, root_value: str) -> Tree:
        strtrees: list[str] = [tree.root.value for tree in self.trees]

        if root_value in strtrees:
            return self.trees[strtrees.index(root_value)]



def split_pgn(pgn: str) -> list:
    parts = re.split(r'[.\s]', pgn)
    parts = [part for i, part in enumerate(parts) if i%3 != 0] # remove every 3rd index
    
    return parts

def pgn2dict(pgn: str) -> dict:
    moves: list = split_pgn(pgn)

    result = {}
    current_dict = result
    
    for move in moves:
        if move not in current_dict:
            current_dict[move] = {}

        current_dict = current_dict[move]
    
    return result

def merge_tree(tree: dict, pgn: str) -> bool:
    moves: list = split_pgn(pgn)
    current_dict: dict = tree

    for move in moves:
        if move not in current_dict:
            current_dict[move] = {}

        current_dict = current_dict[move]

def load_tree() -> Tree:
    """Load a tree from database using pickle."""

    with open(DATA_FILE, 'rb') as f:
        tree: Tree = pickle.load(f)
        
    return tree

def save_tree(tree: Tree) -> bool:
    """Save tree to database."""

    with open(DATA_FILE, 'wb') as f:
        pickle.dump(tree, f)



import re
import pickle

DATA_FILE: str = 'openings-repo.txt'


if __name__ == "__main__":
    # Reading a PGN
    pgns = []
    pgns.append("1.e4 e5 2.Nf3 Nc6 3.Bc5 Nf6 4.Ng5 d5")
    pgns.append("1.e4 e5 2.Nf3 Nc6 3.Bc5 Nf6 4.Nc3")
    pgns.append("1.e4 c6 2.d4 d5 3.f3 e6")

    root = Root("e4")

    tree: Tree = Tree(root)
    for pgn in pgns: tree.merge(pgn)


    # print tree
    print(str(tree))


    from main import *
    import pygame as p
    import graphics as g


    def getMouseRel(win_dims: tuple[int]) -> tuple[int]:
        return tuple([int(v) for v in array(p.mouse.get_pos()) - array(win_dims)])

    win = p.display.set_mode((800,800))
    p.init()
    g.init()

    win_x, win_y = (0,0)
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                exit()
            elif e.type in (p.MOUSEBUTTONDOWN, p.MOUSEBUTTONUP):
                updateGame(p.mouse.get_pressed(), getMouseRel((win_x, win_y)))
    
    
        screen = updateGraphics(getMouseRel((win_x, win_y)))
        win.blit(screen, (win_x, win_y))
        p.display.update()

        # track FPS
        time = time_ns()
        fps_tracker.pop(0)
        fps_tracker.append(nano/(time - last_time))
        
        last_time = time

        # draw avg fps at a custom rate (in Hz)
        if fps_count > TARGET_FPS//5:
            fps_count = 0

            g.clearLayer(g.extrasLayer)
            fps_avg: float = str(round(sum(fps_tracker)/len(fps_tracker)))
            g.drawSprite(g.extrasLayer, g.textSprite(str(fps_avg)), (2,2))
        else:
            fps_count += 1

        clock.tick(TARGET_FPS)
    
    