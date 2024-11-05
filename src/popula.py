from lark import Lark, Transformer
from neo4j import GraphDatabase
import csv

uri = "bolt://localhost:7687"
user = "JSS"
password = "Grafos1-UnB"


driver = GraphDatabase.driver(uri, auth=(user, password))

grammar = """
    ?start: expr

    ?expr: expr "E" term        -> and_expr
         | expr "OU" term       -> or_expr
         | term

    ?term: "(" expr ")"         -> paren_expr
         | IDENT                -> ident

    IDENT: /[A-Z]{3}\\d{4}/

    %ignore " "
"""

parser = Lark(grammar, start='start')

or_counter = 0
and_counter = 0

class ExprTransformer(Transformer):
    def and_expr(self, items):
        global and_counter
        and_list = []
        for item in items:
            if isinstance(item, dict) and item["type"] == "AND":
                and_list.extend(item["children"])
            else:
                and_list.append(item)
        and_counter+=1
        return {"type": "AND", "children": and_list, "value": and_counter}

    def or_expr(self, items):
        global or_counter
        or_list = []
        for item in items:
            if isinstance(item, dict) and item["type"] == "OR":
                or_list.extend(item["children"])
            else:
                or_list.append(item)
        or_counter += 1
        return {"type": "OR", "children": or_list, "value": or_counter}

    def paren_expr(self, items):
        return items[0]

    def ident(self, items):
        return {"type": "IDENT", "value": str(items[0])}

def parse_expression(expression):
    tree = parser.parse(expression)
    transformed_tree = ExprTransformer().transform(tree)
    return transformed_tree

def execute_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]

def add_node(label, properties):
    query = f"CREATE (n:{label}) SET n = $properties"
    execute_query(query, {"properties": properties})

def create_discipline(code):
    label = "Disciplina"
    properties = {"codigo": code}
    add_node(label, properties)

def create_and_node(code):
    label = "AND"
    properties = {"codigo": code}
    add_node(label, properties)

def create_or_node(code):
    label = "OR"
    properties = {"codigo": code}
    add_node(label, properties)

def find_node(node_codigo):
    query = "MATCH (n) WHERE n.codigo = $node_codigo RETURN n"
    parameters = {"node_codigo": node_codigo}
    result = execute_query(query, parameters)
    return result if result else None

def create_relationship(node1_codigo, node2_codigo, relationship_type):
    if node1_codigo.startswith("IDENT"):
        node1_codigo = node1_codigo[5:]

    if node2_codigo.startswith("IDENT"):
        node2_codigo = node2_codigo[5:]

    if find_node(node1_codigo) is None:
        if node1_codigo.startswith("OR"):
            create_or_node(node1_codigo)
        elif node1_codigo.startswith("AND"):
            create_and_node(node1_codigo)
        else:
            create_discipline(node1_codigo)

    if find_node(node2_codigo) is None:
        if node2_codigo.startswith("OR"):
            create_or_node(node2_codigo)
        elif node2_codigo.startswith("AND"):
            create_and_node(node2_codigo)
        else:
            create_discipline(node2_codigo)

    query = (
        "MATCH (a {codigo: $node1_codigo}), (b {codigo: $node2_codigo}) "
        f"CREATE (a)-[r:{relationship_type}]->(b) "
        "RETURN type(r)"
    )

    parameters = {
        "node1_codigo": node1_codigo,
        "node2_codigo": node2_codigo
    }

    try:
        result = execute_query(query, parameters)
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def add_tree(node, root_name, type, parent=None, level=0):
    # indent = "  " * level
    if parent is None:
        parent_name = root_name
    else:
        parent_name = parent["type"]

    if parent is None:
        # print(f"{indent}{parent_name}-{node['type']}{node['value']}")
        create_relationship(parent_name, f"{node['type']}{node['value']}", type)
    elif node["type"] == "IDENT":
        # print(f"{indent}{parent_name}{parent['value']}-{node['value']}")
        create_relationship(f"{parent_name}{parent['value']}", node['value'], type)
    else:
        # print(f"{indent}{parent_name}{parent['value']}-{node['type']}{node['value']}")
        create_relationship(f"{parent_name}{parent['value']}", f"{node['type']}{node['value']}", type)

    for child in node.get("children", []):
        add_tree(child, root_name,type, node, level + 1)

with open('requisitos.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader, None)
    for row in csv_reader:
        if len(row) > 1:
            name = row[0]
            if row[1] != "":
                add_tree(parse_expression(row[1]), name, "prerequisito")
            if row[2] != "":
                add_tree(parse_expression(row[2]), name, "corequisito")
            if row[3] != "":
                add_tree(parse_expression(row[3]), name, "equivalencia")