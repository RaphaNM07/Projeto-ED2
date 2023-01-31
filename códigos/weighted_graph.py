import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import shortest_paths
from networkx.algorithms import centrality
from networkx.algorithms import bipartite
from networkx.algorithms import community
import numpy as np

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
print(municipios)

# 15 BR's
print(brs)

# Criando o grafo
G = nx.Graph()

# Adicionando os municípios no grafo com seus respectivos nomes
for i in range (len(municipios)):
    G.add_node(municipios[i], tipo='municipio')
    
# Adicionando as BR's no grafo com seus respectivos nomes
for i in range(len(brs)):
    G.add_node(brs[i], tipo='br')
    
# 199 Nós
print(G.number_of_nodes())

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



"""
A conclusão do algoritmo abaixo não foi 100% precisa, ou seja,
os municípios que estão nos arredores do grafo não possuem 
necessariamente um maior número de closeness centrality
"""
print(centrality.closeness_centrality(G, 'BELO HORIZONTE'))


"""
O algoritmo abaixo nos mostra quais os nós predominantes nos caminhos mínimos de todos os outros nós.
Isso nos permite concluir quais 'áreas' são mais perigosas para se passar, consequentemente
possibilitando a escolha de um caminho mais seguro na maioria das vezes. A imagem esclarece isso.
"""
print(centrality.betweenness_centrality(G, weight='weight'))

print(nx.degree(G, 365, weight='weight'))

# É possível verificar a quantidade de acidentes em um nó utilizando o comando abaixo
print(G["UBERLANDIA"])
# Resultado: {50: {'weight': 199}, 365: {'weight': 195}},
# ou seja, 50 acidentes na altura de UBERLANDIA da BR 50, e 195 na altura de UBERLANDIA da BR 365.


# Verifica o menor caminho entre dois nós, mostrando o caminho com menos acidentes entre eles
print(shortest_paths.dijkstra_path(G, source='PLANURA', target='CAPIM BRANCO'))
# Resultado: ['PLANURA', 364, 'FRUTAL', 365, 'SAO GONCALO DO ABAETE', 40, 'CAPIM BRANCO']


# Código para fazer a projeção bipartida do grafo
B = bipartite.projected_graph(G, brs)
nx.draw_kamada_kawai(B, with_labels=True, node_size=120, font_size=8)

"""
O algoritmo de comunidades abaixo divide o nosso grafo em partições de acordo com a modularidade das comunidades,
que é uma escala que mede a densidade relativa entre as arestas dentro de uma comunidade em relação com as 
que estão fora dela. As comunidades encontradas são semelhantes ao plot do grafo original feito com o algoritmo kamada_kawai,
que faz com que as arestas do grafo cruzem o mínimo de outras arestas possível, formando um grafo limpo e,
no nosso caso, consequentemente, forma um grafo onde os nós próximos tendem a ser próximos também geograficamente.
"""
particao = community.louvain_communities(G)
grafo_comunidades = nx.Graph()

for i, com in enumerate(particao):
    for node in com:
        grafo_comunidades.add_node(node, community=i)

for node1, node2, data in G.edges(data=True):
    com1 = grafo_comunidades.nodes[node1]['community']
    com2 = grafo_comunidades.nodes[node2]['community']
    if com1 == com2:
        grafo_comunidades.add_edge(node1, node2, weight=data['weight'])

cores_comunidade = ['red', 'green', 'blue', 'yellow', 'purple', 'pink', 'orange', 'black', 'brown', 'gray']
cores_nodes_comunidade = [cores_comunidade[grafo_comunidades.nodes[node]['community']] for node in grafo_comunidades.nodes()]

pos = nx.spring_layout(grafo_comunidades, k=0.3*1/np.sqrt(len(grafo_comunidades.nodes())), iterations=20)

plt.figure(3,figsize=(8,8), dpi=250)
nx.draw(grafo_comunidades, pos=pos, node_color=cores_nodes_comunidade, with_labels=True, node_size=120, font_size=8)

# Plotando o grafo normal
plt.figure(3,figsize=(8,8), dpi=250)
nx.draw_kamada_kawai(G, with_labels=True, node_color=cores_tipo, node_size=120, font_size=8)
plt.show()
