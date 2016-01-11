import node

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
            root = node.Node(y, x, grid_size, grid)
            root.add_children()
            child_nodes = root.line_up_child_nodes()
            if len(child_nodes) > 0:
                # best_path.extend([y, x])
                root_results.append(get_best_path(root, child_nodes))
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
    grid_size, grid =  load_data("map.txt")
    root_results = analyze_roots(grid_size, grid)
    steepest_root = evaluate_nodes(root_results)
    print steepest_root

main()
