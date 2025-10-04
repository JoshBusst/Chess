'''
1. Trie (Prefix Tree) - BEST CHOICE

Speed: O(depth) lookup, very fast
Memory: Optimal - shared prefixes use same nodes
Flexibility: Easy to add metadata (frequencies, evaluations)
Perfect for: Openings where sequences share common prefixes

2. Path Arrays with Hash Index

Speed: O(1) average lookup via hashing
Memory: More compact than trees for sparse data
Flexibility: Easy to store full game context
Perfect for: When you need fast access to complete lines

3. Flat Dictionary with String Keys

Speed: O(1) hashtable lookup
Memory: Very memory efficient
Flexibility: Simple to implement and debug
Perfect for: Simple apps with moderate datasets

4. Graph-Based Adjacency List

Speed: O(1) per transition
Memory: Efficient for complex branching patterns
Flexibility: Can handle transpositions easily
Perfect for: When positions can be reached via multiple move orders

5. SQLite Database - BEST FOR SCALE

Speed: Indexed queries, handles millions of positions
Memory: Disk-based, minimal RAM usage
Flexibility: SQL queries, statistics, user progress tracking
Perfect for: Large opening databases, multi-user apps

Recommendation: Start with the Trie for development - it's the most intuitive and efficient for typical opening trees. Migrate to SQLite if you need to handle large datasets or want features like user statistics and progress tracking.
The nested dictionary approach you started with becomes inefficient because Python dictionaries have overhead per object, and deep nesting creates many small objects. These alternatives reduce both memory usage and lookup time significantly.
'''





from collections import defaultdict
import sqlite3
from typing import List, Dict, Set

# 1. TRIE (Prefix Tree) - Best overall for this use case
class MoveTrie:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.metadata = {}  # Store stats, frequencies, etc.
    
    def insert(self, moves: List[str]):
        node = self
        for move in moves:
            if move not in node.children:
                node.children[move] = MoveTrie()
            node = node.children[move]
        node.is_end = True
    
    def get_continuations(self, moves: List[str]):
        node = self
        for move in moves:
            if move not in node.children:
                return []
            node = node.children[move]
        return list(node.children.keys())

# 2. Move Path Arrays with Hash Map Index
class PathArrayIndex:
    def __init__(self):
        self.paths = []  # List of move sequences
        self.index = defaultdict(list)  # move -> list of path indices
        
    def add_line(self, moves: List[str]):
        path_id = len(self.paths)
        self.paths.append(moves)
        
        # Index each prefix
        for i in range(1, len(moves) + 1):
            prefix = tuple(moves[:i])
            self.index[prefix].append(path_id)
    
    def get_continuations(self, moves: List[str]):
        prefix = tuple(moves)
        continuations = set()
        
        for path_id in self.index.get(prefix, []):
            path = self.paths[path_id]
            if len(path) > len(moves):
                continuations.add(path[len(moves)])
        
        return list(continuations)

# 3. Flat Dictionary with String Keys (Position Hash)
class FlatPositionDict:
    def __init__(self):
        self.positions = {}  # "e4.e5.Nf3" -> set of next moves
    
    def add_line(self, moves: List[str]):
        for i in range(len(moves)):
            key = ".".join(moves[:i+1])
            if key not in self.positions:
                self.positions[key] = set()
            
            if i < len(moves) - 1:
                next_move = moves[i + 1]
                self.positions[key].add(next_move)
    
    def get_continuations(self, moves: List[str]):
        key = ".".join(moves)
        return list(self.positions.get(key, set()))

# 4. Graph-Based Adjacency List
class MoveGraph:
    def __init__(self):
        self.nodes = {}  # move_sequence_hash -> node_data
        self.edges = defaultdict(set)  # from_hash -> set of to_hashes
        
    def _hash_position(self, moves: List[str]) -> str:
        return "|".join(moves)
    
    def add_line(self, moves: List[str]):
        for i in range(len(moves)):
            current_pos = self._hash_position(moves[:i+1])
            self.nodes[current_pos] = {
                'moves': moves[:i+1], 
                'move': moves[i]
            }
            
            if i < len(moves) - 1:
                next_pos = self._hash_position(moves[:i+2])
                self.edges[current_pos].add(next_pos)
    
    def get_continuations(self, moves: List[str]):
        current_hash = self._hash_position(moves)
        next_positions = self.edges.get(current_hash, set())
        
        continuations = []
        for next_hash in next_positions:
            next_node = self.nodes[next_hash]
            continuations.append(next_node['move'])
        
        return continuations

# 5. SQLite Database (Best for large datasets)
class SQLiteOpenings:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY,
                position_key TEXT UNIQUE,
                moves TEXT,
                depth INTEGER
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS continuations (
                position_id INTEGER,
                next_move TEXT,
                frequency INTEGER DEFAULT 1,
                FOREIGN KEY (position_id) REFERENCES positions (id)
            )
        ''')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_position_key ON positions(position_key)')
    
    def add_line(self, moves: List[str]):
        for i in range(len(moves)):
            position_key = "|".join(moves[:i+1])
            moves_json = ",".join(moves[:i+1])
            
            cursor = self.conn.execute(
                'INSERT OR IGNORE INTO positions (position_key, moves, depth) VALUES (?, ?, ?)',
                (position_key, moves_json, i + 1)
            )
            
            position_id = cursor.lastrowid or self.conn.execute(
                'SELECT id FROM positions WHERE position_key = ?', (position_key,)
            ).fetchone()[0]
            
            if i < len(moves) - 1:
                next_move = moves[i + 1]
                self.conn.execute('''
                    INSERT OR REPLACE INTO continuations (position_id, next_move, frequency)
                    VALUES (?, ?, COALESCE((SELECT frequency FROM continuations 
                                         WHERE position_id = ? AND next_move = ?), 0) + 1)
                ''', (position_id, next_move, position_id, next_move))
        
        self.conn.commit()
    
    def get_continuations(self, moves: List[str]):
        position_key = "|".join(moves)
        cursor = self.conn.execute('''
            SELECT c.next_move, c.frequency 
            FROM positions p 
            JOIN continuations c ON p.id = c.position_id 
            WHERE p.position_key = ?
            ORDER BY c.frequency DESC
        ''', (position_key,))
        
        return [row[0] for row in cursor.fetchall()]

# Performance comparison example
if __name__ == "__main__":
    # Test data
    openings = [
        ["e4", "e5", "Nf3", "Nc6", "Bb5"],
        ["e4", "e5", "Nf3", "Nc6", "Bc4"],
        ["e4", "e5", "f4", "exf4"],
        ["d4", "d5", "c4", "e6"]
    ]
    
    # Initialize all structures
    trie = MoveTrie()
    path_index = PathArrayIndex()
    flat_dict = FlatPositionDict()
    graph = MoveGraph()
    db = SQLiteOpenings()
    
    # Add test data
    for opening in openings:
        trie.insert(opening)
        path_index.add_line(opening)
        flat_dict.add_line(opening)
        graph.add_line(opening)
        db.add_line(opening)
    
    # Test queries
    test_position = ["e4", "e5"]
    
    print("Continuations after e4 e5:")
    print("Trie:", trie.get_continuations(test_position))
    print("Path Index:", path_index.get_continuations(test_position))
    print("Flat Dict:", flat_dict.get_continuations(test_position))
    print("Graph:", graph.get_continuations(test_position))
    print("SQLite:", db.get_continuations(test_position))