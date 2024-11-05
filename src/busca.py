from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "JSS"
password = "Grafos1-UnB"

driver = GraphDatabase.driver(uri, auth=(user, password))


def execute_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]


def build_adjacency_list(query):
    adjacency_list = {}
    results = execute_query(query)

    for record in results:
        caminho = record["caminho"]
        nodes = caminho.nodes
        for i in range(len(nodes) - 1):
            current_node = nodes[i]["codigo"]
            next_node = nodes[i + 1]["codigo"]

            if current_node not in adjacency_list:
                adjacency_list[current_node] = []
            if next_node not in adjacency_list[current_node]:
                adjacency_list[current_node].append(next_node)

    return adjacency_list


def print_adjacency_list(adjacency_list):
    for node, neighbors in adjacency_list.items():
        print(f"{node} -> {' -> '.join(neighbors)}")


query = """
MATCH caminho = (n {codigo: 'FGA0060'})-[:prerequisito|corequisito*0..]->(neighbor)
RETURN caminho
"""

adjacency_list = build_adjacency_list(query)
print_adjacency_list(adjacency_list)
