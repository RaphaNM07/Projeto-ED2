import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import community
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


# Todos os municípios
print(municipios) # 184 municípios no total

# Todas as BR's
print(brs) # 15 BR's no total

# Criando o grafo
G = nx.MultiGraph()

# Adicionando os municípios no grafo com seus respectivos nomes
for i in range (len(municipios)):
    G.add_node(municipios[i], tipo='municipio')
    
# Adicionando as BR's no grafo com seus respectivos nomes
for i in range(len(brs)):
    G.add_node(brs[i], tipo='br')
    
# Número de nós do grafo
print(G.number_of_nodes()) # 199 Nós

# Definindo as cores dos vértices
cores_map = nx.get_node_attributes(G, "tipo")

for chave in cores_map:
    if cores_map[chave] == 'municipio':
        cores_map[chave] = 'red'
    else:
        cores_map[chave] = 'yellow'

cores_tipo = [cores_map.get(node) for node in G.nodes()]

# Adicionando as arestas do grafo
for i in range(len(bd.index)):
    linha_arq = bd.iloc[i]
    G.add_edge(linha_arq['br'], linha_arq['municipio'], data=linha_arq['data_inversa'], acidente=linha_arq['tipo_acidente'])
    
# Peso total do grafo, ou seja, quantidade de acidentes no total
print(G.size(weight='weight')) # 7394 acidentes

"""
- Menor grau - Município Nova Ponte: grau 0.00505, Maior grau - BR 381, grau 11.80303
- Os nós com as BR's são os que possuem um maior grau. Isso acontece pois são os nós com o maior número de interações, ou seja,
são os nós mais "importantes" do grafo. Alguns municípios estão com maior grau do que outras BR's, como por exemplo 
Betim, com grau 2.6161, Uberlandia, com grau 1.9898, Uberaba, com grau 1.6717, dentre outros. Isso pode ser explicado por serem municípios
populares e consequentemente mais visitados, o que aumenta a chance de acontecer acidentes nas BR's ligadas a estes municípios.
Além disso, esse mesmo resultado pode ser obtido ao verificar o grau de cada nó, já que um nó com o maior grau
também vai ser o nó com maior grau de centralidade.

Descobrindo e ordenando o grau de centralidade dos nós do grafo:
 """
dicionario = centrality.degree_centrality(G)
sorted_dicionario = sorted(dicionario.items(), key=lambda kv: kv[1])
print(sorted_dicionario) 
# [('NOVA PONTE', 0.005050505050505051), ... (381, 11.803030303030305)]


print(community.louvain_communities(G))

# Mostra a quantidade de acidentes em cada nó
print(nx.degree(G, weight='weight'))
# [('PERDOES', 61), ('UBERABA', 331), ('RIO MANSO', 10), (40, 1600), etc...

# Ou em um nó específico
print(nx.degree(G, 'UBERABA')) # 331 acidentes

# É possível verificar o tipo de acidente, a data e em qual BR/Município foi o acidente utilizando o comando abaixo.
print(G[265])
# {'JUATUBA': {0: {'data': '12/7/2020', 'acidente': 'Saída de leito carroçável'}}}

# Idéia de análise para o código abaixo: Poderíamos ir mais a fundo e ver qual tipo de acidente acontece mais em cada BR,
# e então aumentar sinalização sobre o tipo de acidente mais comum, visando a diminuição desse acidente.
print(G['PLANURA'])
#{364: {0: {'data': '1/10/2020', 'acidente': 'Colisão frontal'}, 
# 1: {'data': '2/22/2020', 'acidente': 'Atropelamento de Pedestre'}, 
# 2: {'data': '2/22/2020', 'acidente': 'Colisão com objeto estático'}, 
# 3: {'data': '2/23/2020', 'acidente': 'Tombamento'}, 
# 4: {'data': '3/1/2020', 'acidente': 'Colisão traseira'}, 
# 5: {'data': '5/13/2020', 'acidente': 'Saída de leito carroçável'}, 
# 6: {'data': '6/8/2020', 'acidente': 'Colisão com objeto estático'}, 
# 7: {'data': '7/6/2020', 'acidente': 'Danos eventuais'}, 
# 8: {'data': '8/2/2020', 'acidente': 'Colisão com objeto estático'}, 
# 9: {'data': '8/22/2020', 'acidente': 'Colisão com objeto estático'}, 
# 10: {'data': '9/10/2020', 'acidente': 'Saída de leito carroçável'}, 
# 11: {'data': '10/26/2020', 'acidente': 'Colisão frontal'}, 
# 12: {'data': '11/28/2020', 'acidente': 'Colisão lateral'}, 
# 13: {'data': '11/28/2020', 'acidente': 'Saída de leito carroçável'}}}

# Plotando o grafo
plt.figure(3,figsize=(8,8), dpi=250)

# O método Kamada Kawai abaixo plota o grafo de uma forma que as arestas dele 
# tendem a não cortar outras arestas do grafo, ou seja, os nós que estão juntos
# costumam estar próximos geograficamente.
nx.draw_kamada_kawai(G, node_color=cores_tipo, node_size=120, font_size=8)
plt.show()
