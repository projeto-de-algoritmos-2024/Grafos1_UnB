from collections import deque
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx
from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import messagebox

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

def menor_caminho(grafo, inicio, destino):
    fila = deque([[inicio]])
    visitados = set()

    while fila:
        caminho = fila.popleft()
        no_atual = caminho[-1]

        if no_atual == destino:
            return caminho

        if no_atual not in visitados:
            visitados.add(no_atual)
            for vizinho in grafo.get(no_atual, []):
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)

    return None

def plot_graph(caminho_filtrado, grafo):
    G = nx.DiGraph()

    for i in range(len(caminho_filtrado) - 1):
        G.add_edge(caminho_filtrado[i], caminho_filtrado[i + 1])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=12, font_weight="bold",
            arrows=True)
    plt.title("Menor Caminho - Grafo")
    plt.show()

def buscar_caminho(cod):
    query = f"""
    MATCH caminho = (n {{codigo: '{cod}'}})-[:prerequisito|corequisito|equivalencia*0..]->(neighbor)
    RETURN caminho
    """
    adjacency_list = build_adjacency_list(query)
    destino = "END00"
    caminho = menor_caminho(adjacency_list, cod, destino)

    if caminho:
        caminho_filtrado = [node for node in caminho if not node.startswith("OR") and not node.startswith("END") and not node.startswith("AND")]
        resultado = " -> ".join(caminho_filtrado)
        print(f"O menor caminho até {destino} é: {resultado}")
        plot_graph(caminho_filtrado, adjacency_list)
    else:
        messagebox.showwarning("Caminho Não Encontrado", f"Não há caminho acessível até {destino} a partir de {cod}.")

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def salvar_input():
    global cod
    cod = entrada.get()
    buscar_caminho(cod)

janela = ThemedTk(theme="adapta")
janela.title("Grafo-UnB")
janela.configure(bg="white")

largura = 400
altura = 200
centralizar_janela(janela, largura, altura)

label = ttk.Label(janela, text="Grafo UnB", font=("Arial", 24))
label.pack(pady=20)

entrada = ttk.Entry(janela, font=("Arial", 14), justify='center')
entrada.pack(pady=10)

botao = ttk.Button(janela, text="Buscar", command=salvar_input)
botao.pack(pady=10)

janela.mainloop()