import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import community
from networkx.algorithms import approximation
from networkx.algorithms import centrality
from networkx.algorithms import shortest_paths

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
G = nx.Graph()

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
    if G.get_edge_data(linha_arq['br'], linha_arq['municipio']) is None:
        G.add_edge(linha_arq['br'], linha_arq['municipio'], weight = 1)
    else:
        G[linha_arq['br']][linha_arq['municipio']]['weight'] += 1

nodes = G.nodes()

"""
Caso queira fazer com que o algoritmo de conjunto dominante (approximation.min_edge_dominating_set(G)) funcione, precisamos transformar o nosso multigrafo em um 
grafo não-direcionado, fazendo com que dois nós sejam ligados por apenas uma aresta e com um peso nessa aresta,
que seria a quantidade de acidentes entre uma BR e um município.


density() e deegres() também seriam interessantes ao usar um grafo não direcionado e com peso.
"""

print(approximation.min_edge_dominating_set(G))

print(centrality.closeness_centrality(G))

print(community.louvain_communities(G))

# É possível verificar a quantidade de acidentes em um nó utilizando o comando abaixo
print(G['JUATUBA'])

# Verifica o menor caminho entre dois nós, mostrando o caminho com menos acidentes entre eles
print(shortest_paths.dijkstra_path(G, source='PLANURA', target='CAPIM BRANCO'))

# Plotando o grafo
nx.draw(G, with_labels=True, node_color=cores_tipo)
plt.show()
