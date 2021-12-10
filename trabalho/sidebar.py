import streamlit as st
import processamento_dados as pcd

def display_sidebar():
    with st.sidebar:
        st.title("Menu de navegação")

        opcoes = {
            "Introdução": pcd.introducao,
            "Ramo Principal": pcd.ramo_principal,
            "Localidade": pcd.localidade,
            "Nível de estudo": pcd.nivel_estudo,
            "Tempo de trabalho": pcd.tempo_trabalho,
            "Informações sobre os profisionais": pcd.info_profissionais,
            "Salários": pcd.salarios,
            "Programadores Python": pcd.programadores_python,
            "Sistema operacional utilizado": pcd.so_utilizado,
            "Média de idade das pessoas": pcd.media_idade,
        }

        escolha = st.radio("Selecione a opção desejada", opcoes)

    opcoes[escolha]()

display_sidebar()