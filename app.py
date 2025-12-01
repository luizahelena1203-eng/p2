import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import urllib3

# desativa avisos de SSL (necessário para a API do STF)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.title("Consulta de Jurisprudência do STF")
st.write("Aplicação que consulta decisões reais utilizando a API oficial de jurisprudência do STF.")

# ------------------------------------------
# Função para buscar jurisprudência no STF
# ------------------------------------------
def buscar_stf(termo):
    url = "https://jurisprudencia.stf.jus.br/api/v1/acordaos"
    params = {"palavra": termo}

    try:
        # verify=False para evitar erro de certificado SSL
        response = requests.get(url, params=params, timeout=20, verify=False)
        response.raise_for_status()
        data = response.json()
        return data.get("acordaos", [])
    except Exception as e:
        st.error(f"Erro ao consultar a API do STF: {e}")
        return []


# ------------------------------------------
# Interface
# ------------------------------------------
termo = st.text_input("Digite um tema para buscar no STF (ex: 'violência', 'tributário', 'dano moral'): ")

if st.button("Buscar"):
    if not termo:
        st.warning("Digite um termo de pesquisa.")
    else:
        st.info("Buscando na API do STF...")

        resultados = buscar_stf(termo)

        if not resultados:
            st.warning("Nenhum resultado encontrado.")
        else:
            st.success(f"{len(resultados)} resultados encontrados!")

            # Exibir lista (somente os 10 primeiros)
            for item in resultados[:10]:
                st.markdown(f"""
                ### Processo: {item.get('processo', 'Não informado')}
                **Relator:** {item.get('relator', 'Não informado')}  
                **Data do Julgamento:** {item.get('dataJulgamento', 'Sem data')}  
                **Ementa:**  
                {item.get('ementa', 'Sem ementa')}
                ---
                """)

            # ------------------------------------------
            # GRÁFICO OBRIGATÓRIO — Decisões por ano
            # ------------------------------------------
            anos = [
                item.get("dataJulgamento", "0000")[:4]
                for item in resultados
                if item.get("dataJulgamento")
            ]

            df = pd.DataFrame(anos, columns=["ano"])
            contagem = df["ano"].value_counts().sort_index()

            st.subheader("Quantidade de decisões por ano")

            fig, ax = plt.subplots()
            contagem.plot(kind="bar", ax=ax)
            ax.set_xlabel("Ano")
            ax.set_ylabel("Quantidade de acórdãos")
            ax.set_title("Distribuição anual das decisões encontradas")

            st.pyplot(fig)
