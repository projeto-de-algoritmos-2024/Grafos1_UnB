# Mapa do Meistre

#### **Questão**

 Sam encontrou um conjunto de mapas do velho Meistre Aemon que, a princípio, deviam mostrar, cada um, a localização de um baú com obsidiana. Entretanto, ao analisar, Sam percebeu que alguns mapas possuíam erros óbvios, e outros só mandando uma equipe para explorar para saber. É certo que alguns mapas apontam para uma localização absurda fora do mapa e alguns terminam em círculos, tornando estes mapas completamente inúteis. Como são muitos mapas, os irmãos da patrulha da noite são poucos e o inverno está chegando, o seu trabalho é fazer um programa para verificar se um mapa leva ou não a um ponto com um baú de obsidiana. Os mapas tem as seguintes características: O ponto de partida de todos os mapas é o canto superior esquerdo. São retangulares e em cada ponto apresenta um destes símbolos: Um espaco de terreno atravessável. Uma flecha, representando uma possível troca de direção; Um baú. Como os lugares que estes mapas descrevem são cheios de perigos, é vital que se siga o caminho descrito no mapa. 

**Entrada**

 Na primeira linha, está um inteiro positivo x < 100 que simboliza a largura do mapa. Na segunda linha, está um inteiro positivo y < 100 que simboliza a altura do mapa. As linhas seguintes contêm diversos caracteres respeitando as dimensões do mapa. Os caracteres válidos são: Uma flecha para a direita: > Uma flecha para a esquerda: < Uma flecha para baixo: v Uma flecha para cima: ^ Um espaco de terreno atravessável: . Um baú: * 

**Saída**

 A saída deve consistir de uma única linha com um único caracter ! ou * . ! significa que o mapa é inválido. * significa que o mapa é válido. Exemplos 

````
6 

1 
 
>....* 
````


**Saída**

````
*
````

**Entrada**
````
 7 
 
 5 
 
 >.....v 
 
 ....... 
 
 ....... 
 
 ....... 
 
 ^.....< 
````

**Saída**

````
 ! 
````

#### **Código**

```c

#include <stdio.h>

char mapa[100][100];
int visitado[100][100],
    largura, altura, fimFila = 0, inicioFila = 0;

int deltax[] = {1, -1, 0, 0}, deltay[] = {0, 0, 1, -1};

typedef struct No {
    int i, j;
} No;

No fila[10000];

void enfileirar(int i, int j) {
    fila[fimFila].i = i;
    fila[fimFila].j = j;
    fimFila = (fimFila+1) % (10000);
}

void desenfileirar() {
    inicioFila = (inicioFila+1) % (10000);
}

int bfs() {
    enfileirar(0, 0);
    visitado[0][0] = 1;
    char atual;
    while (inicioFila != fimFila) {
        int i = fila[inicioFila].i, j = fila[inicioFila].j;
        desenfileirar();
        atual = mapa[j][i];
        if(atual == '*') return 1;
        int direcao;
        switch (atual) {
            case '>':
                direcao = 0;
                break;
            case '<':
                direcao = 1;
                break;
            case 'v':
                direcao = 2;
                break;
            case '^':
                direcao = 3;
                break;
        }
        int x = i + deltax[direcao], y = j + deltay[direcao];
        if ((x >= 0 && y >= 0 && x < largura && y < altura) && !visitado[y][x]) {
            visitado[y][x] = 1;
            enfileirar(x, y);
        }
    }
    return 0;
}

int main() {
    scanf("%d %d", &largura, &altura);
    for (int i = 0; i < altura; ++i)
        for (int j = 0; j < largura; ++j)
            scanf(" %c", &mapa[i][j]);
    if (bfs()) printf("*\n");
    else printf("!\n");
    return 0;
}

```

#### **MOJ**

<div align="center"><img src= "https://raw.githubusercontent.com/projeto-de-algoritmos-2024/Grafos1_UnB/refs/heads/main/Images/mapaMestre.jpg?raw=true"/></div>

#### **LOG**

> O log da mesma pode ser verificado clicando [aqui](./1731020961_5af15afca05cba292be5553a80342b6f.md).
