from collections import deque


def find_generic_paths(graph, path_sequence):
    """
    # Example graph
    # graph = {
    #     'author_paper': {
    #         'Jonathan Amsterdam': ['Some Philosophical Problems with Formal Learning Theory.'],
    #         'Franz Baader': ['Terminological Cycles in KL-ONE-based Knowledge Representation Languages.']
    #     },
    #     'paper_author': {
    #         'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.': ['Franz Baader', 'harsh'],
    #         'Some Philosophical Problems with Formal Learning Theory.': ['Jonathan Amsterdam', 'jyoti']
    #     },
    #     # Add 'paper_conference' and 'conference_paper' if they exist in your graph
    # }

    # # Example path sequence
    # #path_sequence = ['author', 'paper', 'author']
    # path_sequence = ['author','paper','conference','paper','author']

    # # Find paths and aggregate them in a dictionary
    # paths_dict = find_generic_paths(edge_info, path_sequence)
    # print(paths_dict)
    """
    def traverse(node, path, depth):
        if depth == len(path_sequence):
            if path[0] not in paths_dict:
                paths_dict[path[0]] = []
            paths_dict[path[0]].append(path)
            return
        next_node_type = path_sequence[depth]
        edge = f'{path_sequence[depth - 1]}_{next_node_type}'
        if edge in graph and node in graph[edge]:
            for next_node in graph[edge][node]:
                if next_node not in path:  # Avoiding cycles
                    traverse(next_node, path + [next_node], depth + 1)

    paths_dict = {}
    start_node_type = path_sequence[0]
    next_node_type = path_sequence[1]

    for start_node in graph.get(f'{start_node_type}_{next_node_type}', {}):
        traverse(start_node, [start_node], 1)

    return paths_dict




def get_k_hop_neighbours(graph, start_node, k):
    """
    # # Example graph
    # graph = {
    #     'Jonathan Amsterdam': ['Some Philosophical Problems with Formal Learning Theory.'],
    #     'Franz Baader': ['Terminological Cycles in KL-ONE-based Knowledge Representation Languages.', 'Integrating Description Logics and Action Formalisms: First Results.'],
    #     'Some Philosophical Problems with Formal Learning Theory.': ['Jonathan Amsterdam', 'jyoti', 'AAAI'],
    #     'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.': ['Franz Baader', 'harsh', 'AAAI']
    # }

    # # Test the function
    # print("One-hop neighbour of 'Jonathan Amsterdam':", get_k_hop_neighbours(graph, 'Jonathan Amsterdam', 1))
    # print("Two-hop neighbour of 'Jonathan Amsterdam':", get_k_hop_neighbours(graph, 'Jonathan Amsterdam', 2))
    # print("One-hop neighbour of 'Franz Baader':", get_k_hop_neighbours(graph, 'Franz Baader', 1))
    # print("Two-hop neighbour of 'Franz Baader':", get_k_hop_neighbours(graph, 'Franz Baader', 2))

    """
    if start_node not in graph:
        return []

    visited = set([start_node])
    queue = deque([(start_node, 0)])  # Queue of (node, level)
    neighbours = set()

    while queue:
        current_node, level = queue.popleft()

        if level == k:
            if current_node != start_node:
                neighbours.add(current_node)
            continue

        for neighbour in graph.get(current_node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, level + 1))

    return list(neighbours)



