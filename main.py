# http://geeks.redmart.com/2015/01/07/skiing-in-singapore-a-coding-diversion/

def load_data(filename):
    """Load all required data."""
    data_file = open(filename, "r")
    grid_size = data_file.readline().replace("\n","").split()
    grid_lines = data_file.readlines()
    grid = []
    for line in grid_lines:
        line = line.replace("\n","")
        grid.append(line.split())
    return grid_size, grid

def get_pot_paths(node, grid_size):
    """From a given node, determine which adjecent nodes are possible."""
    y = node.y
    x = node.x
    if y == 0 or node.height <= int(grid[y - 1][x]):
        up = None
    else:
        up = Node(y - 1, x)
    if x == int(grid_size[1]) - 1 or node.height <= int(grid[y][x + 1]):
        right = None
    else:
        right = Node(y, x + 1)
    if y == int(grid_size[0]) - 1 or node.height <= int(grid[y + 1][x]):
        down = None
    else:
        down = Node(y + 1, x)
    if x == 0 or node.height <= int(grid[y][x - 1]):
        left = None
    else:
        left = Node(y, x - 1)
    return up, right, down, left

class Node:
    """Node Class representing one point on the grid. A Node can be the root or
    an element of a tree, which represents all potential paths possible given
    a starting point."""
    def __init__(self, y, x):
        self.height = int(grid[y][x])
        self.y = y
        self.x = x
        self.prev_node = None
        self.children = {}
        self.depth = 1

    def add_children(self):
        """Creates all potential child notes, storing them in self.children."""
        up, right, down, left = get_pot_paths(self, grid_size)
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
            node_details = [child.height, child.depth]
            child_nodes.append(node_details)
            child_nodes.extend(child.line_up_child_nodes())
        return child_nodes

def get_best_path(root_node, child_nodes):
    """Given a root and a list of it's children, determines the maximum
    possible depth and height difference."""
    max_node_depth = max(child_nodes, key = lambda x: x[1])[1]
    deepest_child_nodes = []
    for n in child_nodes:
        if n[1] == max_node_depth:
            deepest_child_nodes.append(n)
    steepest_child_node = min(deepest_child_nodes, key = lambda x: x[0])
    height_diff = root_node.height - steepest_child_node[0]
    return [max_node_depth, height_diff]

def analyze_roots(grid_size, grid):
    """Determine the details of the best path for each potential root in a
    given grid."""
    y = 0
    grid_y = int(grid_size[0])
    grid_x = int(grid_size[1])
    root_results = []
    while y < grid_y:
        x = 0
        while x < grid_x:
            root = Node(y, x)
            root.add_children()
            child_nodes = root.line_up_child_nodes()
            if len(child_nodes) > 0:
                best_path = get_best_path(root, child_nodes)
                best_path.extend([y, x])
                root_results.append(best_path)
            x += 1
        y += 1
    return root_results

def evaluate_nodes(root_results):
    """Compare the best paths of each root and return the best one."""
    max_node_depth = max(root_results, key = lambda x: x[0])[0]
    deepest_roots = []
    for r in root_results:
        if r[0] == max_node_depth:
            deepest_roots.append(r)
    steepest_root = max(deepest_roots, key = lambda x: x[1])
    return steepest_root

def main():
    root_results = analyze_roots(grid_size, grid)
    steepest_root = evaluate_nodes(root_results)
    print steepest_root

grid_size, grid =  load_data("map.txt")
main()
