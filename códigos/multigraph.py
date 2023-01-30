import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import community
from networkx.algorithms import approximation
from networkx.algorithms import centrality

# Removendo todas as linhas que possuem "NA" como BR
with open('dados_datatran2020.csv', 'r') as input_file, open('dados_sem_na.csv', 'w') as output_file:
        for line in input_file:
            if "NA" not in line:
                output_file.write(line)

# Lendo o banco de dados usando Pandas
bd = pd.read_csv('dados_sem_na.csv')

# Pegando os municípios do arquivo CSV
municipios = bd['municipio'].tolist()
municipios = list(dict.fromkeys(municipios))

# Pegando as BR's do arquivo CSV
brs = bd['br'].tolist()
brs = list(dict.fromkeys(brs))


# 184 municípios
#print(municipios)

# 15 BR's
#print(brs)

# Criando o grafo
G = nx.MultiGraph()

# Adicionando os municípios no grafo com seus respectivos nomes
for i in range (len(municipios)):
    G.add_node(municipios[i], tipo='municipio')
    
# Adicionando as BR's no grafo com seus respectivos nomes
for i in range(len(brs)):
    G.add_node(brs[i], tipo='br')
    
# 199 Nós
#print(G.number_of_nodes())

# Definindo as cores dos vértices
cores_map = nx.get_node_attributes(G, "tipo")

for chave in cores_map:
    if cores_map[chave] == 'municipio':
        cores_map[chave] = 'red'
    else:
        cores_map[chave] = 'blue'

cores_tipo = [cores_map.get(node) for node in G.nodes()]

# Adicionando as arestas do grafo
for i in range(len(bd.index)):
    linha_arq = bd.iloc[i]
    G.add_edge(linha_arq['br'], linha_arq['municipio'], data=linha_arq['data_inversa'], acidente=linha_arq['tipo_acidente'])
    


"""
Caso queira fazer com que o algoritmo de conjunto dominante (approximation.min_edge_dominating_set(G)) funcione, precisamos transformar o nosso multigrafo em um 
grafo não-direcionado, fazendo com que dois nós sejam ligados por apenas uma aresta e com um peso nessa aresta,
que seria a quantidade de acidentes entre uma BR e um município.


density() e deegres() também seriam interessantes ao usar um grafo não direcionado e com peso.
"""
print("Conjunto dominante: " + approximation.min_edge_dominating_set(G))

"""
# Descobrindo e ordenando o grau de centralidade dos nós do grafo.
dicionario = centrality.degree_centrality(G)
sorted_dicionario = sorted(dicionario.items(), key=lambda kv: kv[1])
print(sorted_dicionario) 

- Menor grau - Município Nova Ponte: grau 0.00505, Maior grau - BR 381, grau 11.80303
- Os nós com as BR's são os que possuem um maior grau. Isso acontece pois são os nós com o maior número de interações, ou seja,
são os nós mais "importantes" do grafo. Alguns municípios estão com maior grau do que outras BR's, como por exemplo 
Betim, com grau 2.6161, Uberlandia, com grau 1.9898, Uberaba, com grau 1.6717, dentre outros. Isso pode ser explicado por serem municípios
populares e consequentemente mais visitados, o que aumenta a chance de acontecer acidentes nas BR's ligadas a estes municípios.
 """

print(centrality.closeness_centrality(G))

print(community.louvain_communities(G))

# Mostra a quantidade de acidentes em cada nó
print(nx.degree(G))

# É possível verificar o tipo de acidente, a data e em qual BR/NÓ foi o acidente utilizando o comando abaixo.
print(G[265])

# Plotando o grafo
nx.draw_kamada_kawai(G, with_labels=True, node_color=cores_tipo)
plt.show()
