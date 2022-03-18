from matplotlib_venn import venn2, venn3_circles
from matplotlib import pyplot as plt
from Dados import Dados, Tipos
from datetime import datetime
import logging
import os

DIRETORIO_RELATORIOS = "Resultados"
ANO_ATUAL = datetime.now().year
ANO_MINIMO_DENGUE = 1822


def relatorioEducacao(dados):  # RELATÓRIO 1
    totalAlunos = 0
    totalDengue = 0
    totalAlunosDengue = 0
    for token in dados:
        pessoa = dados[token]
        if Tipos.ALUNO in pessoa and not Tipos.DENGUE in pessoa:
            totalAlunos += 1
        elif Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa:
            totalDengue += 1
        elif Tipos.ALUNO in pessoa and Tipos.DENGUE in pessoa:
            totalAlunosDengue += 1

    print("Relatório Educação - Conjuntos")
    print(f"Alunos = {totalAlunos}")
    print(f"Tiveram Dengue mas não são alunos = {totalDengue}")
    print(f"Alunos e tiveram dengue = {totalAlunosDengue}")
    v = venn2(subsets=(totalAlunos, totalDengue, totalAlunosDengue),
              set_labels=('Alunos', 'Dengue'))
    plt.title("Diagrama Educação")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "educacao.csv")
    header = "nome;data de nascimento;id base de dados alunos"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.ALUNO in pessoa and not Tipos.DENGUE in pessoa:
                file.write(
                    f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['id_base_alunos']}\n")


def relatorioSaude(dados):  # RELATÓRIO 2
    totalDengue = 0
    totalOnibus = 0
    totalDengueOnibus = 0
    totalInvalidosPorAnoDengue = 0

    for token in dados:
        pessoa = dados[token]

        if Tipos.DENGUE in pessoa:
            ano_dengue = int(pessoa["data_dengue"].split("/")[-1])
            if not ANO_MINIMO_DENGUE <= ano_dengue <= ANO_ATUAL:  # Valida Data que teve dengue
                print(
                    f"Idade de dengue inválida: {ano_dengue} - {pessoa['nome']}")
                totalInvalidosPorAnoDengue += 1
                continue

        if Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
            totalDengue += 1
        elif Tipos.ONIBUS in pessoa and not Tipos.DENGUE in pessoa:
            totalOnibus += 1
        elif Tipos.DENGUE in pessoa and Tipos.ONIBUS in pessoa:
            totalDengueOnibus += 1

    print("Relatório Saude - Conjuntos")
    print(f"Dengue = {totalDengue}")
    print(f"Usam onibus e não tiveram dengue = {totalOnibus}")
    print(f"Tiveram dengue e utilizam onibus = {totalDengueOnibus}")
    print(
        f"Foram retiradas {totalInvalidosPorAnoDengue} pessoas da base de dengue")
    v = venn2(subsets=(totalDengue, totalOnibus, totalDengueOnibus),
              set_labels=('Dengue', 'Onibus'))
    plt.title("Diagrama Saúde")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "saude.csv")
    header = "nome;data de nascimento;data dengue;id base de dados dengue"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]

            if Tipos.DENGUE in pessoa:
                ano_dengue = int(pessoa["data_dengue"].split("/")[-1])
                print(ano_dengue)
                if not ANO_MINIMO_DENGUE <= ano_dengue <= ANO_ATUAL:
                    continue

            if Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
                ano_dengue = int(pessoa["data_dengue"].split("/")[-1])
                if ANO_MINIMO_DENGUE <= ano_dengue <= ANO_ATUAL: 
                    file.write(
                        f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['data_dengue']};{pessoa['id_base_dengue']}\n")


def relatorioMobilidade(dados):  # RELATÓRIO 3
    totalOnibusSemDengue = 0
    totalDengueSemOnibus = 0
    intersecaoOnibusDengue = 0

    for token in dados:
        pessoa = dados[token]
        if Tipos.ONIBUS in pessoa and not Tipos.DENGUE in pessoa:
            totalOnibusSemDengue += 1
        elif Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
            totalDengueSemOnibus += 1
        elif Tipos.DENGUE in pessoa and Tipos.ONIBUS in pessoa:
            intersecaoOnibusDengue += 1

    print("Relatório de mobilidade - Conjuntos")
    print(f"Andam de Onibus e não tiveram dengue = {totalOnibusSemDengue}")
    print(f"Tiveram dengue e não andam de ônibus = {totalDengueSemOnibus}")
    print(f"Andam de ônibus e tiveram dengue = {intersecaoOnibusDengue}")

    v = venn2(subsets=(totalDengueSemOnibus, totalOnibusSemDengue,
              intersecaoOnibusDengue), set_labels=('Dengue', 'Onibus'))
    plt.title("Diagrama de Mobilidade")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "mobilidade.csv")
    header = "nome;data de nascimentop;id base de onibus;linhas de onibus"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.ONIBUS in pessoa and not Tipos.DENGUE in pessoa:
                file.write(
                    f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['id_base_onibus']};{str(pessoa['onibus'])}\n")


def relatorioEducacaoSaude(dados):  #RELATÓRIO 4
    filename = os.path.join(DIRETORIO_RELATORIOS, "educacao_saude.csv")
    header = "nome;data de nascimento;id base de dados dengue;data dengue"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]

            if Tipos.DENGUE in pessoa:
                ano_dengue = int(pessoa["data_dengue"].split("/")[-1])
                if not ANO_MINIMO_DENGUE <= ano_dengue <= ANO_ATUAL:  # Valida Data que teve dengue
                    continue

            if Tipos.ALUNO in pessoa and Tipos.DENGUE in pessoa:
                ano_dengue = int(pessoa["data_dengue"].split("/")[-1])
                if ANO_MINIMO_DENGUE <= ano_dengue <= ANO_ATUAL:  # Valida Ano que teve dengue
                    file.write(
                        f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['id_base_dengue']};{pessoa['data_dengue']}\n")


def relatorioEducacaoMobilidade(dados):  # RELATÓRIO 5
    totalAlunos = 0
    totalOnibus = 0
    intersecaoAlunosOnibus = 0

    for token in dados:
        pessoa = dados[token]

        if Tipos.ALUNO in pessoa and not Tipos.ONIBUS in pessoa:
            totalAlunos += 1
        elif Tipos.ONIBUS in pessoa and not Tipos.ALUNO in pessoa:
            totalOnibus += 1
        elif Tipos.ALUNO in pessoa and Tipos.ONIBUS in pessoa:
            intersecaoAlunosOnibus += 1

    print("Relatório de Educação e mobilidade - Conjuntos")
    print(f"Educação = {totalAlunos}")
    print(f"Ônibus = {totalOnibus}")
    print(f"Alunos que utilizam onibus = {intersecaoAlunosOnibus}")

    v = venn2(subsets=(totalOnibus, totalAlunos,
              intersecaoAlunosOnibus), set_labels=('Ônibus', 'Alunos'))
    plt.title("Diagrama de Educação e Mobilidade")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "EducacaoMobilidade.csv")
    header = "nome;data de nascimento;id base de onibus;linhas de onibus"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.ALUNO in pessoa and Tipos.ONIBUS in pessoa:
                file.write(
                    f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['id_base_onibus']};{str(pessoa['onibus'])}\n")


def relatorioSaudeMobilidade(dados): # RELATÓRIO 6
    totalDengueSemOnibus = 0
    totalOnibusSemDengue = 0
    totalDengueOnibus    = 0
    totalInvalidosPorAnoDengue = 0

    for token in dados:
        pessoa = dados[token]

        if Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
            totalDengueSemOnibus += 1
        elif Tipos.ONIBUS in pessoa and not Tipos.DENGUE in pessoa:
            totalOnibusSemDengue += 1
        elif Tipos.DENGUE in pessoa and Tipos.ONIBUS in pessoa:
            totalDengueOnibus += 1


    print("Relatório Relatório Saúde e Mobilidade - Conjuntos")
    print(f"Dengue mas não em onibus = {totalDengueSemOnibus}")
    print(f"Tiveram Dengue mas não são alunos = {totalDengueSemOnibus}")
    print(f"usam onibus mas não tiveram dengue = {totalOnibusSemDengue}")
    venn2(subsets=(totalDengueSemOnibus, totalOnibusSemDengue, totalDengueOnibus), 
            set_labels=('Posto', 'Onibus'))
    plt.title("Diagrama Saúde e Mobilidade")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "RelatorioSeisSaudeMobilidade.csv")
    header = "nome;data de nascimento;data dengue;linhas de ônibus;id base de dados dengue;id base de dados onibus"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.DENGUE in pessoa and Tipos.ONIBUS in pessoa:
                file.write(f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['data_dengue']};{str(pessoa['onibus'])};{pessoa['id_base_dengue']};{pessoa['id_base_onibus']}\n")





def relatorioSaudeMobilidadeEducacao(dados): #RELATÓRIO 7
    filename = os.path.join(DIRETORIO_RELATORIOS, "SaudeMobilidadeEducacao.csv")
    header = "nome;data de nascimento;data da dengue;linhas de onibus"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.ONIBUS in pessoa and Tipos.ALUNO in pessoa and Tipos.DENGUE in pessoa:
                file.write(f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['data_dengue']};{str(pessoa['onibus'])}\n")


def relatorioOitavo(dados):  # RELATÓRIO 8
    totalDengue = 0
    totalOnibus = 0
    totalDengueOnibus = 0

    for token in dados:
        pessoa = dados[token]
        if Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
            totalDengue += 1
        elif Tipos.ONIBUS in pessoa and not Tipos.DENGUE in pessoa:
            totalOnibus += 1
        elif Tipos.DENGUE in pessoa and Tipos.ONIBUS in pessoa:
            totalDengueOnibus += 1

    print("Relatório Numero Oito - Conjuntos")
    print(f"Dengue = {totalDengue}")
    print(f"Frequentam o posto de saúde e não utilizam onibus = {totalDengue}")
    v = venn2(subsets=(totalDengue, totalOnibus, totalDengueOnibus),
              set_labels=('Dengue', 'Onibus'))
    plt.title("Diagrama Oitavo")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "relatorioOito.csv")
    header = "nome;data de nascimento;data dengue;id base de dados dengue;id base de dados "
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
                file.write(
                    f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['data_dengue']};\n")


def relatorioNono(dados):  # RELATÓRIO 9
    totalDengue = 0
    totalAluno = 0
    totalDengueAluno = 0

    for token in dados:
        pessoa = dados[token]
        if Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa:
            totalDengue += 1
        elif Tipos.ALUNO in pessoa and not Tipos.DENGUE in pessoa:
            totalAluno += 1
        elif Tipos.DENGUE in pessoa and Tipos.ALUNO in pessoa:
            totalDengueAluno += 1

    print("Relatório Numero Nono - Conjuntos")
    print(f"Dengue = {totalDengue}")
    print(
        f"Frequentam o posto de saúde e não frequentam a escola = {totalDengue}")
    v = venn2(subsets=(totalDengue, totalAluno, totalDengueAluno),
              set_labels=('Dengue', 'Aluno'))
    plt.title("Diagrama Nono")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "relatorioNono.csv")
    header = "nome;data de nascimento;data dengue"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa:
                file.write(
                    f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['data_dengue']};\n")


def relatorioDez(dados): #RELATÓRIO 10
    totalDengueSemAlunoSemOnibus = 0
    totalAlunosSemDengueSemOnibus = 0
    totalOnibusSemAlunoSemDengue = 0
    intersecaoPostoOnibusAlunos = 0
    intersecaoPostoOnibus = 0
    intersecaoOnibusAlunos = 0
    intersecaoAlunoPosto = 0

    for token in dados:
        pessoa = dados[token]

        if Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa and not Tipos.ONIBUS in pessoa:
            totalDengueSemAlunoSemOnibus += 1
        elif Tipos.ALUNO in pessoa and not Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
            totalAlunosSemDengueSemOnibus += 1
        elif Tipos.ONIBUS in pessoa and not Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa:
            totalOnibusSemAlunoSemDengue += 1
        elif Tipos.ONIBUS in pessoa and Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa:
            intersecaoPostoOnibus += 1
        elif Tipos.ONIBUS in pessoa and Tipos.ALUNO in pessoa and not Tipos.DENGUE in pessoa:
            intersecaoOnibusAlunos += 1
        elif Tipos.ALUNO in pessoa and Tipos.DENGUE in pessoa and not Tipos.ONIBUS in pessoa:
            intersecaoAlunoPosto += 1
        elif Tipos.ONIBUS in pessoa and Tipos.DENGUE in pessoa and Tipos.ALUNO in pessoa:
            print(pessoa)
            intersecaoPostoOnibusAlunos += 1

    print("Relatório dez - Conjuntos")
    print(f"Educação = {totalAlunosSemDengueSemOnibus}")
    print(f"Ônibus = {totalOnibusSemAlunoSemDengue}")
    print(f"Posto = {totalDengueSemAlunoSemOnibus}")


    venn2(subsets=(
        totalOnibusSemAlunoSemDengue,
        totalAlunosSemDengueSemOnibus,
        intersecaoOnibusAlunos,
        totalDengueSemAlunoSemOnibus,
        intersecaoPostoOnibus,
        intersecaoAlunoPosto,
        intersecaoPostoOnibusAlunos), 
       set_labels=('Ônibus', 'Alunos', 'Posto'))

    plt.title("Diagrama da questão 10")
    plt.show()

    filename = os.path.join(DIRETORIO_RELATORIOS, "RelatorioDez.csv")
    header = "nome;data de nascimento;data da dengue;id base dengue"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(header + "\n")
        for token in dados:
            pessoa = dados[token]
            if Tipos.DENGUE in pessoa and not Tipos.ALUNO in pessoa and not Tipos.ONIBUS in pessoa:
                file.write(f"{pessoa['nome']};{pessoa['data_nascimento']};{pessoa['data_dengue']};{pessoa['id_base_dengue']}\n")

if __name__ == "__main__":
    dados = Dados().getDados()
    
    #relatorioEducacao(dados)
    #relatorioSaude(dados)
    #relatorioMobilidade(dados)
    #relatorioEducacaoSaude(dados)
    #relatorioEducacaoMobilidade(dados)
    #relatorioSaudeMobilidade(dados)
    #relatorioSaudeMobilidadeEducacao(dados)
    #relatorioOitavo(dados)
    #relatorioNono(dados)
    #relatorioDez(dados)
