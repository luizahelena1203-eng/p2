import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Pesquisa de Projetos de Lei — Câmara dos Deputados")
st.write("Aplicação que consulta projetos de lei reais usando a API oficial da Câmara dos Deputados.")

# ------------------------------
# Função para consultar a API
# ------------------------------
def buscar_projetos(termo):
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "ordenarPor": "ano",
        "ordem": "DESC",
        "keywords": termo,
        "itens": 200  # máximo que a API aceita
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("dados", [])
    except Exception as e:
        st.error(f"Erro ao consultar a API da Câmara: {e}")
        return []


# ------------------------------
# Interface
# ------------------------------
termo = st.text_input("Digite um tema jurídico (ex: 'violência', 'tributário', 'família', 'penal'): ")

if st.button("Buscar"):
    if not termo:
        st.warning("Digite um termo para pesquisar.")
    else:
        st.info("Buscando projetos de lei reais...")

        resultados = buscar_projetos(termo)

        if not resultados:
            st.warning("Nenhum resultado encontrado.")
        else:
            st.success(f"{len(resultados)} projetos encontrados!")

            # Mostrar apenas os 10 mais recentes
            for item in resultados[:10]:
                st.markdown(f"""
                ### {item.get('siglaTipo', '')} {item.get('numero', '')}/{item.get('ano', '')}
                **Ementa:** {item.get('ementa', 'Sem ementa disponível')}
                ---
                """)

            # -------------------------------------
            # GRÁFICO OBRIGATÓRIO — Projetos por ano
            # -------------------------------------
            anos = [item.get("ano") for item in resultados if item.get("ano")]

            df = pd.DataFrame(anos, columns=["ano"])
            contagem = df["ano"].value_counts().sort_index()

            st.subheader("Quantidade de Projetos por Ano")

            fig, ax = plt.subplots()
            contagem.plot(kind="bar", ax=ax)
            ax.set_xlabel("Ano")
            ax.set_ylabel("Número de Projetos")
            ax.set_title("Distribuição anual dos Projetos encontrados")

            st.pyplot(fig)
