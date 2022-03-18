from Dados import Dados, Tipos
import logging

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  dados = Dados().getDados()

  for token in dados:
    if Tipos.DENGUE in dados[token] and Tipos.ONIBUS in dados[token]:
      print(dados[token]) 