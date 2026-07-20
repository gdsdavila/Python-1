import streamlit as st
import pandas as pd
import sqlalchemy as db

## cria uma conexão com o banco de dados sqlite dentro da mesma pasta
engine = db.create_engine("sqlite:///database.db")

## operações de configuração da página(mostram as mensagens)
st.set_page_config(page_title="Lista Inteligente")

st.markdown("# Lista de Compras Inteligente")

st.markdown("## Importar Historico")


## operações que fazem o upload do arquivo e leitura dele para mostrar ao usuario
open_file = st.file_uploader("Importar arquivo De Historico", type=["csv", "xlsx"])

if open_file:
    ## abrir o arquivo selecionado
    df = pd.read_csv(open_file)

    ## editar as informações do arquivo
    df = st.data_editor(df)


    if st.button("Registrar Dados"):
        ## aqui temos aparte do IF que ve se existe a tabela no bd e diz o que deve ser feito(adicionar, escrever ou erro se existir)
        df.to_sql("compras", engine, if_exists="append", index=False)## não salva o index junto
        st.success("Dados Registrados com Sucesso!")