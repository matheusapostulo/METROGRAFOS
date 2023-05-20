"""
32092921 | MATHEUS HENRIQUE DA SILVA APOSTULO
32095971 | VALDIR LOPES JUNIOR
"""

from math import inf
import os
from copy import deepcopy # Usado nos métodos de cópia de lista. Opções 2 e 4!

infinito = inf

class Grafo:
  TAM_MAX_DEFAULT = 100  # qtde de vértices máxima default

  # construtor da classe grafo
  def __init__(self, n=TAM_MAX_DEFAULT):
    self.n = n  # número de vértices
    self.m = 0  # número de arestas
    # matriz de adjacência
    self.adj = [[infinito for i in range(n)] for j in range(n)]
    self.nomes_vertices = [] #Lista com nomes dos vértices, manipulação vai ser feita aqui  
            
  # Atribui nome a um número de vértice
  def atribuiVertice(self, nome_vertice, numero_vertice):
    self.nomes_vertices[numero_vertice] = nome_vertice

  #Percorre a lista de nomes e retorna a posição que o nome está
  def getPosicaoNome(self, nome_vertice):
    for i in range(len(self.nomes_vertices)): 
      if self.nomes_vertices[i] == nome_vertice:
        return i
       
    return -1

  def insereV_txt(self, nome_vertice): # Esse método é o usado para a leitura do txt apenas
    self.nomes_vertices.append(nome_vertice)  

  # b) Gravar dados no arquivo grafo.txt;
  def gravarDados(self):
    # Apaga o arquivo pois o grafo pode estar totalmente diferenre do original
    os.remove("grafo.txt")
    # Abre o arquivo 
    with open("grafo.txt", "w") as grf_r:
      # Laço que escreve os VÉRTICES EXISTENTES NO GRAFO
      for i in range(len(self.nomes_vertices)+2):# percorre linhas txt, line: conteúdo da linha
        match i: 
          case 0:
            grf_r.write("2\n")
          case 1:
            grf_r.write(f"{str(self.n)}\n")
          case _:
            string_vertice = f'{i-1} "{self.nomes_vertices[i-2]}"\n'
            grf_r.write(string_vertice)
      # Laço para percorrer a matriz principal para pegar as arestas 
      # Utilizaremos um matriz cópia auxiliar e iremos setando infinito no contrário da posição([i][j] -> [j][i])
      matriz_aux = deepcopy(self.adj) # usando lib copy para criar uma cópia
      for i in range(self.n):
        for j in range(self.n):
          if matriz_aux[i][j] != infinito: # verifica se não é infinito
            # Guarda os nomes dos vértice pela posição e também o peso
            vertice_i = self.nomes_vertices[i]
            vertice_j = self.nomes_vertices[j]
            peso = self.adj[i][j]
            string_aresta = f'{vertice_i}, {vertice_j}, {peso}\n'
            grf_r.write(string_aresta)
            # Agora iremos setar infinito na posição inversa para não pegarmos a mesma relação
            matriz_aux[j][i] = infinito

      #print(f"ASSIM FICOU A MATRIZ AUX: {matriz_aux}")      
      #print(f"ASSIM FICOU A LISTA ADJ: {self.adj}")  
      grf_r.close()

  
  # c) Insere vértice na lista que representa o grafo. Irá inserir na última posição, não fará diferença na lógica geral pois pesquisamos por nomes para fazer as operações dos métodos
  def insereV(self, nome_vertice): 
    # Se o vértice não existe, adiciona à última posição da lista de nomes e aumenta o tamanho de vértices do grafo
    if nome_vertice not in self.nomes_vertices:
      # Copia a matriz antiga para futuras operações no método
      matriz_copia = deepcopy(self.adj)
      # Add à lista de nomes de vértices
      self.nomes_vertices.append(nome_vertice)
      self.n += 1
      # Resetaremos a matriz do grafo com o novo tamanho 
      self.adj = [[infinito for i in range(self.n)] for j in range(self.n)]
      # Repaseremos os dados anteriores para a lista nova (somente onde tinha aresta) 
      for i in range(len(matriz_copia)):
        for j in range(len(matriz_copia)):
          if matriz_copia[i][j] != infinito:
            self.adj[i][j] = matriz_copia[i][j]
    
    else:
      print("ESSE VÉRTICE JÁ EXISTE NO GRAFO! Tente outro da próxima vez!")
      

  # d) Insere uma aresta no Grafo tal que v é adjacente a w (pega a posição pelo nome). Não precisamos saber a posição, apenas o nome para poder ligar dois vértices.
  def insereA(self, vertice_i, vertice_j, peso):
    if peso > 0:
      pos_i = self.getPosicaoNome(vertice_i)
      pos_j = self.getPosicaoNome(vertice_j)
      if pos_i != -1 and pos_j != -1:
        if self.adj[pos_i][pos_j] == infinito and self.adj[pos_j][pos_i] == infinito:
          self.adj[pos_i][pos_j] = peso
          self.adj[pos_j][pos_i] = peso
          self.m += 1  # atualiza qtd arestas
        elif self.adj[pos_i][pos_j] != infinito and self.adj[pos_j][pos_i] != infinito: # Atualizar com um novo peso caso já tenha um peso, condicional para n mudar qtd aresta
          self.adj[pos_i][pos_j] = peso
          self.adj[pos_j][pos_i] = peso
      else:
        print("Algum dos vértices digitados não existe!\n")
    else:
      print("Insira um peso positivo maior que 0!")
      
   # e) Método para remover vértice do grafo ND
  def removeV(self, vertice):
    if vertice in self.nomes_vertices:
      posicao_vertice = self.getPosicaoNome(vertice)
      # Removendo as arestas com todos os outros vértices primeiro antes de apagar as posições do vetor
      for i in range(self.n):
        vertice_2 = self.nomes_vertices[i] # variável que pega todos os nomes dos vértices existentes na lista de nomes
        self.removeA(vertice,vertice_2) # remove as ligações existentes com os outros vértices        
      # Atualiza a matriz (removendo os elementos)
      del self.adj[posicao_vertice] # Apaga o vértice 
      self.n -= 1 # Atualiza a quantidade de vértices  
      #Atualizando as colunas desalocando o espaço do antigo vértice
      for i in range(self.n):        
        del self.adj[i][posicao_vertice]

      # Apagando o vértice da lista de nomes 
      del self.nomes_vertices[posicao_vertice]
    else:
      print("Vértice não existente no grafo!")

  # f) remove uma aresta v->w do Grafo utiliza nome para achar a posição
  def removeA(self, vertice_i, vertice_j):
    pos_i = self.getPosicaoNome(vertice_i)
    pos_j = self.getPosicaoNome(vertice_j)
    if pos_i != -1 and pos_j != -1:
      # testa se temos a aresta
      if self.adj[pos_i][pos_j] != infinito and self.adj[pos_j][pos_i] != infinito:
        self.adj[pos_i][pos_j] = infinito
        self.adj[pos_j][pos_i] = infinito
        self.m -= 1
      # atualiza qtd arestas
    else:
      print("\nAlgum vértice digitado não existe!\n")

  # g) Verifica se o grafo é conexo ou não-conexo
  def conexidade(self, verticeInicio):
    print("VERIFICANDO CONEXIDADE")
    # Cria a pilha e array de nós marcados e contador para marcar os nós visitados
    quantidade_visitados = 0
    nosMarcados = []
    pilha = Pilha()
    # Visita o Nó
    print(f"Nó inicial visitado: {chr((verticeInicio+1)+96)}")
    quantidade_visitados += 1
    # Marca o nó inicial
    nosMarcados.append(verticeInicio)
    # Empilha o nó
    pilha.push(verticeInicio)

    while not pilha.isEmpty():
      n = pilha.pop()
      #print("Pilha está assim = ", pilha)

      adjacentesDeN = self.adjacenciasVertice(n, nosMarcados)
      #print(f"adjacentes de 0 = ", adjacentesDeN)
      
      while len(adjacentesDeN) > 0: # Roda em todos os adjacentes de "n" que ainda não foram marcados
        print("Nó m visitado = ", chr((adjacentesDeN[0]+1) + 96))
        quantidade_visitados += 1 # incrementa visitados
        pilha.push(n)
        #print("n colocado na pilha = ", pilha)
        nosMarcados.append(adjacentesDeN[0]) # "m é marcado = ", nosMarcados)
        n = adjacentesDeN[0] #"Troca o valor de n para m (n <- m(atribuição)) = ", n, "\n")
        adjacentesDeN = self.adjacenciasVertice(n, nosMarcados)

    # mostrando Percurso em profundidade
    print("O percurso em profundidade foi:", end = " ")
    for i in nosMarcados:
      print(chr((i+1)+96), end = " ")
    print("\n\n")

    # Tendo o percurso em profundidade, poderemos verifica a conexidade
    print(f"Qtd de vértices = {self.n}. Qtd_vistiados = {quantidade_visitados}")
    # Verifica se o grafo é conexo ou não 
    if(self.n == quantidade_visitados):
      print("O grafo é conexo!\n\n")
    else:
      print("O grafo é não conexo!\n\n")
  
  # h) Menor caminho entre dois vértices utilizando o algoritmo de Dijkstra
  def menor_caminho(self, v1, v2):
    # Criando o array A(abertos) e criando os vértices com ele
    A = []
    for i in range(self.n):
      A.append(i)
      
    # Criando o array de F(fechados)
    F = []

    # Criando o array S(Sucessores) de um vértice r
    S = []
    
    # Número de vértices já processados pelo algoritmo
    k = 0

    # Vetor rot
    rot = []

    # Enquanto A != de vazio 
    while len(A) != 0:
      k += 1
      
  
    
    
    
    
  
  # Exibe de forma reduzida devido a grande quantidade de vértices
  def show(self):
    print(f"\n n: {self.n:2d} ", end="")
    print(f"m: {self.m:2d}\n")
    for i in range(self.n):
      print(f"ESTAMOS NO VÉRTICE '{self.nomes_vertices[i]}': ")
      for w in range(self.n):
        if self.adj[i][w] != infinito:
          print(f" Adj[{self.nomes_vertices[i]}, {self.nomes_vertices[w]}] = {self.adj[i][w]}")
        '''
        Estamos exibindo apenas as arestas
        else:
          print(f" Adj[{self.nomes_vertices[i]}, {self.nomes_vertices[w]}] = {infinito}")
        '''
      print("\n")
    print("fim da impressao do grafo.\n\n")
