from pandas.core.algorithms import value_counts
from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np


def func_get_dict(x):
    branch = {
        "I am a developer by profession": "Profissional",
        "I am a student who is learning to code": "Estudante",
        "I am not primarily a developer, but I write code sometimes as part of my work": "Aventureiro",
        "I code primarily as a hobby": "Hobby",
        "I used to be a developer by profession, but no longer am": "Ex-profissional",
        "None of these": "Nenhum"
    }
    return branch.get(x, "Nenhum")

def grau_estudo(x):
    grau = {
        "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Ensino Médio",
        "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bacharelado",
        "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Mestrado",
        "Other doctoral degree (Ph.D., Ed.D., etc.)": "Doutorado",
        "Some college/university study without earning a degree": "Estudante Universitário",
        "Something else": "Outros",
        "Professional degree (JD, MD, etc.)": "Profissional",
        "Primary/elementary school": "Primário",
        "Associate degree (A.A., A.S., etc.)": "Tecnológo"
    }

    return grau.get(x, "Nenhum")
###
### Função que lê o csv e faz o processamento dos dados
### return df_survey -> dataframe com os dados lidos
def processa_dados():
    ## Lendo arquivo csv
    df_survey = pd.read_csv("trabalho/dados/survey_results_public.csv")
    
    colunas =  [
        "MainBranch","Employment","Country", "Age", "Age1stCode", "DevType", "EdLevel", "Gender", 
        "LanguageHaveWorkedWith", "OpSys", "OrgSize", "YearsCode", "YearsCodePro", "Currency", "ConvertedCompYearly"
    ]  

    novo_df = df_survey.loc[:, colunas]

    ### Simplificando os dados do ramo principal
    novo_df["MainBranchSimplified"] = novo_df["MainBranch"].apply(func_get_dict).astype("string")

    ### Deleta coluna MainBranch
    novo_df.drop("MainBranch", axis=1, inplace=True)

    ### Simplificando os dados de escolaridade
    novo_df["Escolaridade"] = novo_df["EdLevel"].apply(grau_estudo).astype("string")


    return novo_df

###
### Introdução
###
def introducao():

    st.title("Introdução")
    st.header("Contexto")
    st.write("Projeto referente ao trabalho prático da disciplina de Python para Ciência de Dados do curso de pós-graduação de Inteligência Artificial da PUC Minas.")

    st.header("Bem vindo")
    st.write("Esta é uma ferramenta de visualização de dados que utiliza as bibliotecas: streamlit e pandas. Através do menu de navegação ao lado você poderá encontrar"
    + " informações referentes ao processamento dos dados da pesquisa anual feita pelo site Stack Overflow no ano de 2021.")

    st.write("Inicialmente, foi feito o processamento do arquivo com o objetivo de filtrar as colunas das informações que foram utilizadas na plataforma.")
    st.write("Colunas filtradas: ramo principal, tipo de trabalho, país, idade, idade quando programou pela primeira vez, o tipo de desenvolvedor, "
    "nível educacional, o gênero, linguagens que trabalhou, sistema operacional, tamanho da organização, tempo programando, tempo programando como profissional,"
    "a moeda e o valor recebido durante o ano.")

    st.write("Os dados de ramo principal e escolaridade foram otimizados para uma melhor exibição.")
    

###
### Ramo principal
###
def ramo_principal():
    st.title("Ramo Principal")

    df = processa_dados()
    df = df.rename(columns={"MainBranchSimplified": "Ramo Principal (em %)"})

    st.write("Ramo principal consiste no que melhor descreve o participante em relação ao seu nível de profissional.")
    st.header("Passos")
    st.write("Mudança do nome da coluna de MainBranchSimplified para Ramo Principal (em %).")
    st.write("Agrupamento das informações por ramo principal e exibindo através da função `value.counts()` com o parâmetro `normalize` para transformar em porcentagem.")
    st.header("Resultado")
    st.dataframe(df["Ramo Principal (em %)"].value_counts(normalize=True) * 100)

###
### Localidade
###
def localidade():
    st.title("Localidade")

    df = processa_dados()
    df = df.rename(columns={"Country": "País (em %)"})
    qtd_paises = len(df["País (em %)"].value_counts())

    st.write("Localidade consiste nos países de moradia dos participantes.")
    st.header("Passos")
    st.write("Mudança do nome da coluna de Country para País (em %).")
    st.write("Calculo da quantidade de países existentes nos dados.")
    st.write("Agrupamento das informações por país e exibindo através da função `value.counts()` com o parâmetro `normalize` para transformar em porcentagem.")
    st.write("Recuperando e exibindo primeiro e último país da lista.")

    st.header("Resultado")
    st.dataframe(df["País (em %)"].value_counts(normalize=True) * 100)
    st.write("O país com o maior número de participações foi: " + str(df["País (em %)"].value_counts(normalize=True).index[0]) + " com um total de " + str(df["País (em %)"].value_counts()[0]) 
    + " participações, o que equivale à " + str(df["País (em %)"].value_counts(normalize=True)[0] * 100) + str("%") + " das participações.")
    st.write("O país com o menor número de participações foi: " + str(df["País (em %)"].value_counts(normalize=True).index[qtd_paises-1]) + " com um total de " + str(df["País (em %)"].value_counts()[qtd_paises-1]) 
    + " participação, o que equivale à " + str(df["País (em %)"].value_counts(normalize=True)[qtd_paises-1] * 100) + str("%") + " das participações.")

###
### Nível de estudo
###
def nivel_estudo():
    st.title("Nível de estudo")

    st.write("Consiste no nível de estudo dos participantes.")

    st.header("Passos")
    st.write("Agrupamento dos dados de acordo com o nível de estudo através da função `value.counts()`.")
    st.write("Agrupamento dos dados de acordo com o nível de estudo através da função `value.counts()` com o parâmetro `normalize` para transformar em porcentagem.")

    df = processa_dados()

    st.header("Resultado")
    st.header("Escolaridade por número de participantes")

    st.dataframe(df["Escolaridade"].value_counts())

    df = df.rename(columns={"Escolaridade": "Escolaridade (em %)"})

    st.header("Escolaridade em porcentagem")

    st.dataframe(df["Escolaridade (em %)"].value_counts(normalize=True) * 100)

###
### Tempo de trabalho
###
def tempo_trabalho():
    st.title("Tempo de trabalho")
    st.write("Consiste no tempo de trabalho como profissional em anos dos participantes.")

    st.header("Passos")
    st.write("Mudança do nome da coluna YearsCodePro para Tempo de trabalho (em anos) através da função `rename()`.")
    st.write("Agrupamento dos dados de acordo com o ramo principal através da função `groupby()` e somando a quantidade de anos por ramos com a função `count()`.")

    st.header("Resultado")
    df = processa_dados()

    df = df.rename(columns={"YearsCodePro": "Tempo de trabalho (em anos)"})

    st.dataframe(df.dropna(subset=["MainBranchSimplified"], axis=0).groupby(by="MainBranchSimplified")["Tempo de trabalho (em anos)"].count())

###
### Informações sobre os profissionais
###
def info_profissionais():
    st.title("Informações sobre os profissionais")

    st.write("Consiste nas informações dos participantes que declararam exercer a função profissionalmente.")

    st.header("Passos")

    st.write("Instanciando uma máscara de Profissional para filtrar somente aqueles que exercem a função profissionalmento.")
    st.write("Separando os profissionais pelo seu tipo de contrato através da função `unique()`.")
    st.write("Separando os profissionais pela sua escolaridade através da função `unique()`.")
    st.write("Separando os profissionais pelo tamanho da organização através da função `unique()`.")

    st.header("Resultado")

    df = processa_dados()

    mascara = df["MainBranchSimplified"] == "Profissional"

    st.header("Tipo de contrato")
    st.dataframe(df[mascara]["Employment"].dropna().unique())

    st.header("Escolaridade")
    st.dataframe(df[mascara]["Escolaridade"].dropna().unique())

    st.header("Tamanho da organização")
    st.dataframe(df[mascara]["OrgSize"].dropna().unique())

###
### Salários
###
def salarios():
    st.title("Salários")

    st.write("Consiste na média salarial de acordo com a moeda de cada país.")

    st.header("Passos")
    st.write("Conversão do tipo de variável da coluna ConvertedCompYearly para float através da função `apply()`, com o parâmetro `pd.to_numeric`.")
    st.write("Remoção dos valores nulos através da função `dropna()`.")
    st.write("Mudança do nome da coluna ConvertedCompYearly para Salário (Montante anual) através da função `rename()`.")
    st.write("Agrupando os dados pela moeda através da função `groupby()` e calculando a média de salários de cada moeda pelo montante anual através da função `mean()`.")

    st.header("Resultado")
    df = processa_dados()

    df.loc[:, "ConvertedCompYearly"] = df.loc[:, "ConvertedCompYearly"].apply(pd.to_numeric, args=("coerce",))
    df.loc[:, "ConvertedCompYearly"] = df.loc[:, "ConvertedCompYearly"].dropna()

    st.header("Média Salarial")

    df = df.rename(columns={"ConvertedCompYearly": "Salário (Montante anual)"})

    st.dataframe(df.dropna(subset=["Currency"], axis=0).groupby(by="Currency")["Salário (Montante anual)"].mean())

###
### Programadores Python
###
def programadores_python():
    st.title("Programadores Python")

    st.write("Consiste nas informações obtidas referentes aos participantes que utilizam a linguagem python.")

    st.header("Passos")

    st.write("Filtrando colunas que serão utilizadas.")
    st.write("Retirando valores nulos através da função `dropna()`.")
    st.write("Filtrando coluna LanguageHaveWorkedWith através da função `contais()` para localizar aqueles que utilizaram python.")
    st.write("Alterando nome da coluna de ConvertedCompYearly para Salário (Média montante anual).")
    st.write("Agrupando valores por país e calculando a média do salário anual através da função `mean()`.")
    st.write("Filtrando coluna Country através da função `contais()` para localizar aqueles que utilizaram python no Brasil.")
    st.write("Agrupando valores por país e calculando a média do salário anual através da função `mean()`.")

    df = processa_dados()

    colunas = [
        "LanguageHaveWorkedWith", "ConvertedCompYearly", "Currency", "Country"
    ]

    linguagem_df = df.loc[:, colunas]
    linguagem_df = linguagem_df.dropna()

    linguagem_df.loc[:, "LanguageHaveWorkedWith"] = linguagem_df.loc[:, "LanguageHaveWorkedWith"].str.contains("Python")

    linguagem_df = linguagem_df[linguagem_df["LanguageHaveWorkedWith"] == True]

    linguagem_df = linguagem_df.rename(columns={"ConvertedCompYearly": "Salário (Média montante anual)"})


    st.header("Nível salarial - Globalmente")

    st.dataframe(linguagem_df.groupby(by="Country")["Salário (Média montante anual)"].mean())

    st.header("Nível salarial - Brasil")

    brasil_df = linguagem_df.copy()

    brasil_df.loc[:, "Country"] = brasil_df.loc[:, "Country"].str.contains("Brazil")

    brasil_df = brasil_df[brasil_df["Country"] == True]

    st.dataframe(brasil_df.groupby(by="Country")["Salário (Média montante anual)"].mean())

###
### Sistema operacional utilizado
###
def so_utilizado():
    st.title("Sistema operacional utilizado")

    st.write("Consiste no sistema operacional utilizado pelo participantes.")

    st.header("Passos")

    st.write("Mudança do nome da coluna OpSys para quantidade de usuários através da variável `rename()`.")
    st.write("Agrupando os sistemas operacionais utilizados pela quantidade de usuários através das funções `groupby()` e `count()`.")

    st.header("Resultado")

    df = processa_dados()

    df = df.rename(columns={"OpSys": "Quantidade de usuários"})
    st.dataframe(df.dropna(subset=["Quantidade de usuários"], axis=0).groupby(by="Quantidade de usuários")["Quantidade de usuários"].count())

###
### Idade
###
def media_idade():
    st.title("Idade")

    st.write("Consiste nos intervalos de idade dos participantes.")

    st.header("Passos")

    st.write("Mudança do nome da coluna Age para quantidade de usuários através da variável `rename()`.")
    st.write("Agrupando os intervalos de idade pela quantidade de usuários através das funções `groupby()` e `count()`.")
    st.write("Filtrando usuários python através da função `contains()`.")
    st.write("Agrupando os intervalos de idade pela quantidade de usuários de python através das funções `groupby()` e `count()`.")

    st.header("Resultado")

    df = processa_dados()

    df = df.rename(columns={"Age": "Quantidade de usuários"})
    st.header("Quantidade de usuários por idade")
    st.dataframe(df.groupby(by="Quantidade de usuários")["Quantidade de usuários"].count())


    colunas = [
        "LanguageHaveWorkedWith", "Quantidade de usuários"
    ]

    linguagem_df = df.loc[:, colunas]
    linguagem_df = linguagem_df.dropna()

    linguagem_df.loc[:, "LanguageHaveWorkedWith"] = linguagem_df.loc[:, "LanguageHaveWorkedWith"].str.contains("Python")

    linguagem_df = linguagem_df[linguagem_df["LanguageHaveWorkedWith"] == True]

    st.header("Quantidade de usuários python por idade")

    st.dataframe(linguagem_df.groupby(by="Quantidade de usuários")["Quantidade de usuários"].count())


