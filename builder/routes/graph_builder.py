"""
Builder V3 Graph Builder

Constructs a graph of service patterns from the divergence data.
"""


def build_graph(patterns, divergences):
    """
    Build an in-memory graph of service patterns.
    """

    graph = {}

    # Create one node per pattern
    for pattern in patterns:
        graph[pattern["pattern_id"]] = {
            "pattern": pattern,
            "edges": [],
        }

    # Connect patterns using the divergence data
    for divergence in divergences:

        a = divergence["pattern_a"]
        b = divergence["pattern_b"]

        graph[a]["edges"].append(divergence)
        graph[b]["edges"].append(divergence)

    return graph


def report_graph(graph):
    """
    Print graph statistics.
    """

    node_count = len(graph)

    edge_count = (
        sum(len(node["edges"]) for node in graph.values()) // 2
    )

    isolated = sum(
        1
        for node in graph.values()
        if not node["edges"]
    )

    average_degree = (
        (edge_count * 2) / node_count
        if node_count else 0
    )

    print()
    print("=========================")
    print("Route Graph")
    print("=========================")
    print(f"Nodes            : {node_count:,}")
    print(f"Edges            : {edge_count:,}")
    print(f"Average degree   : {average_degree:.2f}")
    print(f"Isolated nodes   : {isolated:,}")

    report_isolated_nodes(graph)


def report_isolated_nodes(graph, limit=20):
    """
    Display the first few isolated service patterns.
    """

    print()
    print(f"First {limit} isolated patterns")
    print("--------------------------")

    count = 0

    for node in graph.values():

        if node["edges"]:
            continue

        pattern = node["pattern"]

        print(
            f'{pattern["pattern_id"]:8}  '
            f'{pattern["origin"]:3} → {pattern["destination"]:3}  '
            f'({len(pattern["stations"]):2} stations)'
        )

        count += 1

        if count >= limit:
            break