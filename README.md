# UnB

**Número da Lista**: 12<br>
**Conteúdo da Disciplina**: Grafos1<br>

## Alunos
| Matrícula  | Aluno                         |
|------------|-------------------------------|
| 22/1031149 | Danilo César Tertuliano Melo  |
| 22/1008150 | João Antonio Ginuino Carvalho |

## Sobre 

Realizamos uma busca em largura para encontrar o melhor caminho possível para conseguir concluir uma matéria, levando em
consideração os pré-requisitos, co-requisitos e equivalências, o grafo em si está num banco de dados de grafo chamado
Neo4j e para realizar a busca de menor caminho subimos o grafo na memória e realizamos a busca.

Os dados utilizados nesse projeto foram disponibilizados na página https://sigaa.unb.br/sigaa/public/turmas/listar.jsf no dia
23/09/2024.

> Para ver o video de apresentação clique [aqui](https://www.youtube.com/watch?v=0t8uElQ3kTg).

## Screenshots

<div align="center"><img src= "https://raw.githubusercontent.com/projeto-de-algoritmos-2024/Grafos1_UnB/refs/heads/main/Images/grafoperto.jpg?raw=true"/></div>

<center>
Figura 1 - Grafo no Neo4j
</center>

<div align="center"><img src= "https://raw.githubusercontent.com/projeto-de-algoritmos-2024/Grafos1_UnB/refs/heads/main/Images/busca.png?raw=true"/></div>

<center>
Figura 2 - Realizando a busca
</center>

<div align="center"><img src= "https://raw.githubusercontent.com/projeto-de-algoritmos-2024/Grafos1_UnB/refs/heads/main/Images/grafo.png?raw=true"/></div>

<center>
Figura 3 - Grafo plotado do menor caminho possível
</center>

[//]: # (<div align="center"><img src= "https://raw.githubusercontent.com/projeto-de-algoritmos-2024/Grafos1_UnB/refs/heads/main/Images/grafoaproximado.jpg?raw=true"/></div>)



## Instalação 
**Linguagem**: Python<br>
**Framework**: (caso exista)<br>

> pip install lark-parser
> pip install neo4j
> pip install networkx
> pip install ttkthemes
> pip install matplotlib

Além de ter o neo4j baixado.

## Uso 

Primeiro é necessario rodar o popula.py e com um database criado dentro do neo4j, com senha e usuário sendo "JSS" e "Grafos1-UnB" respectivamente,
Em seguida após inserir todos os nós é basta executar o busca.py que irá funcionar corretamente.

## Outros 

#### Mapa do Meistre

> Para complementar a nota foi realizada a questao "Mapa do Meistre" do moj, onde é possível ver o resultado clicando [aqui](/src/MapaDoMestre.md).

<div align="center"><img src= "https://raw.githubusercontent.com/projeto-de-algoritmos-2024/Grafos1_UnB/refs/heads/main/Images/mapaMestre.jpg?raw=true"/></div>


### Reconstruct Itinerary

> Para complementar a nota foi realizada a questao "Reconstruct Itinerary" do leetcode, onde é possível ver o resultado clicando [aqui](/src/ReconstructItinerary.md).

---

### Apresentação

> Para ver o video de apresentação clique [aqui](https://www.youtube.com/watch?v=0t8uElQ3kTg).
