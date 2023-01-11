import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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

# Criando uma lista com todos os nós
nodes = brs + municipios

# 208 municípios
print(municipios)

# 23 BR's
print(brs)

# Criando o grafo
G = nx.MultiGraph()

# Adicionando os nós no grafo com seus respectivos nomes
for i in range (len(municipios)):
    G.add_node(municipios[i], tipo='municipio')
    
# Adicionando as BR's no grafo com seus respectivos nomes
for i in range(len(brs)):
    G.add_node(brs[i], tipo='br')
    
    
# nx.draw(G)
