import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import approximation
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
Confirmar depois se conjunto dominante realmente tem sentido
"""
#print(approximation.min_edge_dominating_set(G))


# É possível verificar a quantidade de acidentes em um nó utilizando o comando abaixo
print(G["UBERLANDIA"])
# Resultado: {50: {'weight': 199}, 365: {'weight': 195}},
# ou seja, 50 acidentes na altura de UBERLANDIA da BR 50, e 195 na altura de UBERLANDIA da BR 365.


# Verifica o menor caminho entre dois nós, mostrando o caminho com menos acidentes entre eles
print(shortest_paths.dijkstra_path(G, source='PLANURA', target='CAPIM BRANCO'))
# Resultado: ['PLANURA', 364, 'FRUTAL', 365, 'SAO GONCALO DO ABAETE', 40, 'CAPIM BRANCO']

# Plotando o grafo
plt.figure(3,figsize=(8,8), dpi=250)
nx.draw(G, with_labels=True, node_color=cores_tipo, node_size=120, font_size=8)
plt.show()
