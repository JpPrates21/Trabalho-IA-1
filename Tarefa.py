import itertools
import heapq
from collections import deque

class No:
    def __init__(self, estado, pai=None, acao=None, custo_caminho=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo_caminho = custo_caminho

def funcao_sucessora(estado):
    esq, dir, tocha = estado
    sucessores = []
    
    lado_atual = esq if tocha == 'Esq' else dir
    movimentos = list(itertools.combinations(lado_atual, 1)) + list(itertools.combinations(lado_atual, 2))
    
    for movimento in movimentos:
        custo = max(movimento)
        movimento_set = frozenset(movimento)
        
        if tocha == 'Esq':
            novo_esq = esq - movimento_set
            novo_dir = dir | movimento_set
            nova_tocha = 'Dir'
        else:
            novo_esq = esq | movimento_set
            novo_dir = dir - movimento_set
            nova_tocha = 'Esq'
            
        novo_estado = (novo_esq, novo_dir, nova_tocha)
        sucessores.append((novo_estado, movimento, custo))
        
    return sucessores


#BUSCAS NÃO INFORMADAS

def busca_em_largura(estado_inicial, estado_objetivo, funcao_sucessora):
    no_inicial = No(estado_inicial)
    if estado_inicial == estado_objetivo:
        return no_inicial, 0
        
    fronteira = deque([no_inicial])
    explorados = set()
    nos_expandidos = 0
    
    while fronteira:
        no_atual = fronteira.popleft()
        explorados.add(no_atual.estado)
        nos_expandidos += 1
        
        for proximo_estado, acao, custo_acao in funcao_sucessora(no_atual.estado):
            if proximo_estado not in explorados and not any(n.estado == proximo_estado for n in fronteira):
                filho = No(proximo_estado, no_atual, acao, no_atual.custo_caminho + custo_acao)
                
                if proximo_estado == estado_objetivo:
                    return filho, nos_expandidos
                    
                fronteira.append(filho)
                
    return None, nos_expandidos

def busca_em_profundidade(estado_inicial, estado_objetivo, funcao_sucessora, limite_nos=10000):
    no_inicial = No(estado_inicial)
    fronteira = [no_inicial]
    explorados = set()
    nos_expandidos = 0
    
    while fronteira:
        if nos_expandidos >= limite_nos:
            return None, nos_expandidos
            
        no_atual = fronteira.pop()
        
        if no_atual.estado == estado_objetivo:
            return no_atual, nos_expandidos
            
        explorados.add(no_atual.estado)
        nos_expandidos += 1
        
        for proximo_estado, acao, custo_acao in funcao_sucessora(no_atual.estado):
            if proximo_estado not in explorados and not any(n.estado == proximo_estado for n in fronteira):
                filho = No(proximo_estado, no_atual, acao, no_atual.custo_caminho + custo_acao)
                fronteira.append(filho)
                
    return None, nos_expandidos


#BUSCAS DE CUSTO E A*

def heuristica(estado):
    esq, dir, tocha = estado
    if not esq:
        return 0
    return max(esq)

def busca_custo_uniforme(estado_inicial, estado_objetivo, funcao_sucessora):
    no_inicial = No(estado_inicial)
    contador = 0
    fronteira = [(0, contador, no_inicial)]
    explorados = set()
    nos_expandidos = 0
    
    while fronteira:
        custo_g, _, no_atual = heapq.heappop(fronteira)
        
        if no_atual.estado == estado_objetivo:
            return no_atual, nos_expandidos
            
        if no_atual.estado in explorados:
            continue
            
        explorados.add(no_atual.estado)
        nos_expandidos += 1
        
        for proximo_estado, acao, custo_acao in funcao_sucessora(no_atual.estado):
            if proximo_estado not in explorados:
                novo_custo_g = no_atual.custo_caminho + custo_acao
                filho = No(proximo_estado, no_atual, acao, novo_custo_g)
                contador += 1
                heapq.heappush(fronteira, (novo_custo_g, contador, filho))
                
    return None, nos_expandidos

def busca_a_estrela(estado_inicial, estado_objetivo, funcao_sucessora):
    no_inicial = No(estado_inicial)
    contador = 0
    custo_f_inicial = heuristica(estado_inicial)
    
    fronteira = [(custo_f_inicial, contador, no_inicial)]
    explorados = set()
    nos_expandidos = 0
    
    while fronteira:
        custo_f, _, no_atual = heapq.heappop(fronteira)
        
        if no_atual.estado == estado_objetivo:
            return no_atual, nos_expandidos
            
        if no_atual.estado in explorados:
            continue
            
        explorados.add(no_atual.estado)
        nos_expandidos += 1
        
        for proximo_estado, acao, custo_acao in funcao_sucessora(no_atual.estado):
            if proximo_estado not in explorados:
                novo_custo_g = no_atual.custo_caminho + custo_acao
                novo_custo_f = novo_custo_g + heuristica(proximo_estado)
                
                filho = No(proximo_estado, no_atual, acao, novo_custo_g)
                contador += 1
                heapq.heappush(fronteira, (novo_custo_f, contador, filho))
                
    return None, nos_expandidos

def imprimir_resultados(nome_busca, no_final, nos_expandidos):
    print(nome_busca)
    if not no_final:
        print("Sem solucao. Nos:", nos_expandidos)
        return
        
    caminho = []
    no_atual = no_final
    while no_atual:
        caminho.append(no_atual)
        no_atual = no_atual.pai
        
    caminho.reverse()
    
    print(f"Tempo: {no_final.custo_caminho} | Expandidos: {nos_expandidos}")
    for no in caminho:
        print(f"{no.acao} -> {list(no.estado[0])} | {list(no.estado[1])} | {no.estado[2]}")
    print() 

estado_inicial = (frozenset({1, 2, 5, 10}), frozenset(), 'Esq')
estado_objetivo = (frozenset(), frozenset({1, 2, 5, 10}), 'Dir')

#Executa todos os quatro algoritmos
no_bfs, exp_bfs = busca_em_largura(estado_inicial, estado_objetivo, funcao_sucessora)
imprimir_resultados("BFS", no_bfs, exp_bfs)

no_dfs, exp_dfs = busca_em_profundidade(estado_inicial, estado_objetivo, funcao_sucessora)
imprimir_resultados("DFS", no_dfs, exp_dfs)

no_cu, exp_cu = busca_custo_uniforme(estado_inicial, estado_objetivo, funcao_sucessora)
imprimir_resultados("CUSTO UNIFORME", no_cu, exp_cu)

no_a, exp_a = busca_a_estrela(estado_inicial, estado_objetivo, funcao_sucessora)
imprimir_resultados("A*", no_a, exp_a)
