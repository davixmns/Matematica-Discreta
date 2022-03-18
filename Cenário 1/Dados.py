from collections import Counter
import logging
import csv
import os
import json

DIRETORIO_DADOS = "cadastros"

class Tipos:
  DENGUE = "isOnDengue"
  ALUNO  = "isOnAlunos"
  ONIBUS = "isOnOnibus"

class Dados(object):
  def __init__(self, limiar_token=0.9):
    self.dados = {}
    self.limiar_token = limiar_token
    self.loadDados()

  def getDados(self):
    return self.dados

  def getJson(self):
    return json.dumps(self.dados)

  def loadDados(self):
    self.loadDadosAlunos()
    self.loadDadosDengue()
    self.loadDadosOnibus()

  def loadDadosAlunos(self):
    ARQUIVO_ALUNOS = os.path.join(DIRETORIO_DADOS, "Base de Alunos4.csv")
    with open(ARQUIVO_ALUNOS, "r", encoding="utf8") as arquivo:
      csvreader = csv.reader(arquivo, delimiter=";")
      next(csvreader)
      for id, nome, nome_pai, nome_mae, sexo, data_nascimento in csvreader:
        token = f"{nome.lower()};{nome_pai.lower()};{nome_mae.lower()}"

        if not token in self.dados:
          # Percorre todos os tokens em busca por um token semelhante
          # Adiciona se resultado da comparação >= self.limiar_token
          achou_token_similar = False
          for t in self.dados:
            if Dados.comparaTokens(token, t) >= self.limiar_token:
              logging.debug("TOKENS MUITO SIMILARES!!!")
              achou_token_similar = True
              logging.debug(t)
              logging.debug(token)
              token = t

          if not achou_token_similar:
            self.dados[token] = {}


        self.dados[token]["id_base_alunos"] = id
        self.dados[token]["nome"] = nome
        self.dados[token]["mae"]  = nome_mae
        self.dados[token]["pai"]  = nome_pai
        self.dados[token]["sexo"] = sexo
        self.dados[token]["data_nascimento"] = data_nascimento
        self.dados[token]["isOnAlunos"] = True


  def loadDadosDengue(self):
    ARQUIVO_DENGUE = os.path.join(DIRETORIO_DADOS, "Base de Dengue4.csv")

    with open(ARQUIVO_DENGUE, "r", encoding="utf8") as arquivo:
      csvreader = csv.reader(arquivo, delimiter=";")
      next(csvreader)
      for id, nome, nome_pai, nome_mae, sexo, data_nascimento, data_dengue in csvreader:
        token = f"{nome.lower()};{nome_pai.lower()};{nome_mae.lower()}"
        
        if not token in self.dados:
          # Percorre todos os tokens em busca por um token semelhante
          # Adiciona se resultado da comparação >= self.limiar_token
          achou_token_similar = False
          for t in self.dados:
            if Dados.comparaTokens(token, t) >= self.limiar_token:
              logging.debug("TOKENS MUITO SIMILARES!!!")
              achou_token_similar = True
              logging.debug(t)
              logging.debug(token)
              token = t

          if not achou_token_similar:
            self.dados[token] = {}

        self.dados[token]["id_base_dengue"] = id
        self.dados[token]["nome"] = nome
        self.dados[token]["mae"]  = nome_mae
        self.dados[token]["pai"]  = nome_pai
        self.dados[token]["sexo"] = sexo
        self.dados[token]["data_nascimento"] = data_nascimento
        self.dados[token]["data_dengue"] = data_dengue
        self.dados[token]["isOnDengue"]  = True


  def loadDadosOnibus(self):

    ARQUIVO_ONIBUS = os.path.join(DIRETORIO_DADOS, "Base de Onibus4.csv")

    with open(ARQUIVO_ONIBUS, "r", encoding="utf8") as arquivo:
      csvreader = csv.reader(arquivo, delimiter=";")
      next(csvreader)
      for id, nome, nome_pai, nome_mae, sexo, data_nascimento, onibus in csvreader:
        token = f"{nome.lower()};{nome_pai.lower()};{nome_mae.lower()}"

        if not token in self.dados:
          # Percorre todos os tokens em busca por um token semelhante
          # Adiciona se resultado da comparação >= self.limiar_token
          achou_token_similar = False
          for t in self.dados:
            if Dados.comparaTokens(token, t) >= self.limiar_token:
              logging.debug("TOKENS MUITO SIMILARES!!!")
              achou_token_similar = True
              logging.debug(t)
              logging.debug(token)
              token = t

          if not achou_token_similar:
            self.dados[token] = {}

        self.dados[token]["id_base_onibus"] = id
        self.dados[token]["nome"] = nome
        self.dados[token]["mae"]  = nome_mae
        self.dados[token]["pai"]  = nome_pai
        self.dados[token]["sexo"] = sexo
        self.dados[token]["data_nascimento"] = data_nascimento
        self.dados[token]["onibus"] = [int(v) for v in onibus.split(",")]
        self.dados[token]["isOnOnibus"] = True


  def comparaTokens(token1, token2):
    token1, token2 = token1.lower(), token2.lower()
    pontos = 0
    qntMaximaDePontos = 0

    for subelemento in zip(token1.split(";"), token2.split(";")):
      bloco, bloco2 = subelemento

      for tupla_elementos in zip(bloco.split(" "), bloco2.split(" ")):
        elem, elem2 = tupla_elementos
        #print(f'{elem} - {elem2}')
        tam_elem, tam_elem2 = len(elem), len(elem2)
        qntMaximaDePontos += max(tam_elem, tam_elem2)
        for i in range(min(tam_elem, tam_elem2)):
          if elem[i] == elem2[i]:
            pontos += 1

    return pontos / qntMaximaDePontos
