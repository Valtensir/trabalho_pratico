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
        "MainBranch","Employment","Country", "Age", "Age1stCode", "CompFreq", "CompTotal", 
        "DatabaseHaveWorkedWith", "DevType", "EdLevel", "Gender", "LanguageHaveWorkedWith",
        "NEWCollabToolsHaveWorkedWith", "LearnCode", "NEWStuck", "OpSys", "OrgSize", "YearsCode", 
        "YearsCodePro", "Currency"
    ]  

    novo_df = df_survey.loc[:, colunas]

    ### Simplificando os dados do ramo principal
    novo_df["MainBranchSimplified"] = novo_df["MainBranch"].apply(func_get_dict).astype("string")

    ### Deleta coluna MainBranch
    novo_df.drop("MainBranch", axis=1, inplace=True)

    ### Simplificando os dados de escolaridade
    novo_df["Escolaridade"] = novo_df["EdLevel"].apply(grau_estudo).astype("string")


    return novo_df

def introducao():

    st.title("Introdução")
    st.write("Bem vindo")
    st.write("Processamento de informações do stackoverflow")


def ramo_principal():
    st.title("Ramo Principal")

    df = processa_dados()
    df = df.rename(columns={"MainBranchSimplified": "Ramo Principal (em %)"})

    st.dataframe(df["Ramo Principal (em %)"].value_counts(normalize=True) * 100)

def localidade():
    st.title("Localidade")

    df = processa_dados()
    df = df.rename(columns={"Country": "País (em %)"})
    qtd_paises = len(df["País (em %)"].value_counts())

    st.dataframe(df["País (em %)"].value_counts(normalize=True) * 100)
    st.write("O país com o maior número de participações foi: " + str(df["País (em %)"].value_counts(normalize=True).index[0]) + " com um total de " + str(df["País (em %)"].value_counts()[0]) 
    + " participações, o que equivale à " + str(df["País (em %)"].value_counts(normalize=True)[0] * 100) + str("%") + " das participações.")
    st.write("O país com o menor número de participações foi: " + str(df["País (em %)"].value_counts(normalize=True).index[qtd_paises-1]) + " com um total de " + str(df["País (em %)"].value_counts()[qtd_paises-1]) 
    + " participação, o que equivale à " + str(df["País (em %)"].value_counts(normalize=True)[qtd_paises-1] * 100) + str("%") + " das participações.")


def nivel_estudo():
    st.title("Nível de estudo")
    df = processa_dados()

    st.header("Escolaridade por número de participantes")

    st.dataframe(df["Escolaridade"].value_counts())

    df = df.rename(columns={"Escolaridade": "Escolaridade (em %)"})

    st.header("Escolaridade em porcentagem")

    st.dataframe(df["Escolaridade (em %)"].value_counts(normalize=True) * 100)

def tempo_trabalho():
    st.title("Tempo de trabalho")
    df = processa_dados()

    df = df.rename(columns={"YearsCodePro": "Tempo de trabalho (em anos)"})

    st.dataframe(df.dropna(subset=["MainBranchSimplified"], axis=0).groupby(by="MainBranchSimplified")["Tempo de trabalho (em anos)"].count())

def info_profissionais():
    st.title("Informações sobre os profisionais")

    df = processa_dados()

    mascara = df["MainBranchSimplified"] == "Profissional"

    st.dataframe(df[mascara]["Employment"].dropna().unique())

    st.dataframe(df[mascara]["Escolaridade"].dropna().unique())

    st.dataframe(df[mascara]["OrgSize"].dropna().unique())

def salarios():
    st.title("Salários")
    df = processa_dados()

    df.loc[:, "CompTotal"] = df.loc[:, "CompTotal"].apply(pd.to_numeric, args=("coerce",))

    st.header("Média Salarial")

    st.dataframe(df.dropna(subset=["Currency"], axis=0).groupby(by="Currency")["CompTotal"].mean())

def programadores_python():
    st.title("Programadores Python")

    st.header("Nível salarial")

def so_utilizado():
    st.title("Sistema operacional utilizado")

def media_idade():
    st.title("Média de idade das pessoas")
