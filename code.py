import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import coloring
from networkx.algorithms import community

# Removendo todas as linhas que possuem "NA" como BR
with open('E:/Datasets ED2/dados_datatran2020.csv', 'r') as input_file, open('output.csv', 'w') as output_file:
        for line in input_file:
            if "NA" not in line:
                output_file.write(line)

# Lendo o banco de dados usando Pandas
bd = pd.read_csv('E:/Datasets ED2/dados_sem_na.csv')

# Pegando os municípios do arquivo CSV
municipios = bd['municipio'].tolist()
municipios = list(dict.fromkeys(municipios))

# Pegando as BR's do arquivo CSV
brs = bd['br'].tolist()
brs = list(dict.fromkeys(brs))

# Criando uma lista com todos os vértices
nodes = brs + municipios

# 184 municípios
print(municipios)

# 15 BR's
print(brs)

# Criando o grafo
G = nx.MultiGraph()

# Adicionando os municípios no grafo com seus respectivos nomes
for i in range (len(municipios)):
    G.add_node(municipios[i], tipo='municipio', node_color='blue')
    
# Adicionando as BR's no grafo com seus respectivos nomes
for i in range(len(brs)):
    G.add_node(brs[i], tipo='br', node_color='red')
    
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
    linha = bd.iloc[i]
    G.add_edge(linha['br'], linha['municipio'], data=linha['data_inversa'], acidente=linha['tipo_acidente'])
    
#print(coloring.strategy_largest_first(G, None))
"""
A função strategy_largest_first acima retorna uma lista dos graus dos nós do grafo G em ordem descresente.
Nos permite verificar quais nós possuem mais arestas, ou seja, um maior número de acidentes.
"""

#print(community.kernighan_lin_bisection(G))
"""
A funçaõ kernighan_lin_biscetion acima retorna uma tupla contendo duas partições de um grafo G. Essas partiçoes
são feitas de modo que haja o mínimo de arestas possíveis cruzando de uma partição a outra.
"""



# Plotando o grafo
nx.draw(G, with_labels=True, node_color=cores_tipo)
plt.show()
