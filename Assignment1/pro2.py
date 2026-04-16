from collections import deque

def bfs_tree(graph, start_node):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    # Dictionary to store the BFS tree (parent -> children)
    tree = {}
    
    while queue:
        current = queue.popleft()
        
        # Determine neighbors that haven't been visited yet
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
                # Add the edge to the tree
                if current not in tree:
                    tree[current] = []
                tree[current].append(neighbor)
    

    return tree

def dfs_tree(graph, start_node, visited=None, tree=None):
    if visited is None:
        visited = set()
        visited.add(start_node)
    if tree is None:
        tree = {}

    for neighbor in graph[start_node]:
        if neighbor not in visited:
            visited.add(neighbor)
            
            # Add edge to tree
            if start_node not in tree:
                tree[start_node] = []
            tree[start_node].append(neighbor)
            
            dfs_tree(graph, neighbor, visited, tree)
            
    return tree

def print_tree(tree):
    for parent, children in tree.items():
        print(f"{parent} -> {children}")

# Graph definition
graph = {
        "Raj": ["Sunil", "Neha_1"],
        "Sunil": ["Raj", "Akash", "Sneha", "Maya"],
        "Akash": ["Sunil", "Priya"],
        "Priya": ["Raj", "Akash", "Aarav"],
        "Neha_1": ["Raj", "Akash", "Sneha", "Aarav"],
        "Sneha": ["Sunil", "Rahul", "Neha_1"],
        "Maya": ["Sunil", "Rahul", "Arjun_1"],
        "Rahul": ["Sneha", "Maya", "Pooja", "Arjun_2", "Neha_2", "Neha_1"],
        "Arjun_1": ["Maya", "Pooja"],
        "Pooja": ["Arjun_1", "Rahul", "Arjun_2"],
        "Arjun_2": ["Rahul", "Aarav", "Neha_2"],
        "Neha_2": ["Rahul", "Aarav", "Arjun_2", "Neha_1", "Priya"],
        "Aarav": ["Neha_1", "Neha_2", "Arjun_2"]
    }

# Generate and print BFS tree starting from "Raj"
start_node = "Raj"
bfs_tree_result = bfs_tree(graph, start_node)
print(f"BFS Tree (Starting from {start_node}):")
print_tree(bfs_tree_result)

print("\n" + "-"*20 + "\n")

# Generate and print DFS tree starting from "Raj"
dfs_tree_result = dfs_tree(graph, start_node)
print(f"DFS Tree (Starting from {start_node}):")
print_tree(dfs_tree_result)
