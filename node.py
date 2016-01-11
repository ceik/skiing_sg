class Node:
    """Node Class representing one point on the grid. A Node can be the root or
    an element of a tree, which represents all potential paths possible given
    a starting point."""
    def __init__(self, y, x, grid_size, grid):
        self.height = int(grid[y][x])
        self.y = y
        self.x = x
        self.grid = grid
        self.grid_size = grid_size
        self.prev_node = None
        self.children = {}
        self.depth = 1

    def get_pot_paths(self):
        """From a given node, determine which adjecent nodes are possible."""
        y = self.y
        x = self.x
        if y == 0 or self.height <= int(self.grid[y - 1][x]):
            up = None
        else:
            up = Node(y - 1, x, self.grid_size, self.grid)
        if x == int(self.grid_size[1]) - 1 or self.height <= int(self.grid[y][x + 1]):
            right = None
        else:
            right = Node(y, x + 1, self.grid_size, self.grid)
        if y == int(self.grid_size[0]) - 1 or self.height <= int(self.grid[y + 1][x]):
            down = None
        else:
            down = Node(y + 1, x, self.grid_size, self.grid)
        if x == 0 or self.height <= int(self.grid[y][x - 1]):
            left = None
        else:
            left = Node(y, x - 1, self.grid_size, self.grid)
        return up, right, down, left

    def add_children(self):
        """Creates all potential child notes, storing them in self.children."""
        up, right, down, left = self.get_pot_paths()
        if up:
            self.children['up'] = up
            self.children['up'].prev_node = self
            self.children['up'].depth = self.children['up'].prev_node.depth + 1
            self.children['up'].add_children()
        if right:
            self.children['right'] = right
            self.children['right'].prev_node = self
            self.children['right'].depth = self.children['right'].prev_node.depth + 1
            self.children['right'].add_children()
        if down:
            self.children['down'] = down
            self.children['down'].prev_node = self
            self.children['down'].depth = self.children['down'].prev_node.depth + 1
            self.children['down'].add_children()
        if left:
            self.children['left'] = left
            self.children['left'].prev_node = self
            self.children['left'].depth = self.children['left'].prev_node.depth + 1
            self.children['left'].add_children()

    def line_up_child_nodes(self):
        """Puts all children of a root into a list for easy comparison."""
        child_nodes = []
        for direction, child in self.children.iteritems():
            child_nodes.append([child.height, child.depth])
            child_nodes.extend(child.line_up_child_nodes())
        return child_nodes
