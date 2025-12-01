import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "https://api.jurispect.com/v1/search"
API_KEY = st.secrets["JURIS_API_KEY"]

# -----------------------------
# Função: buscar jurisprudência
# -----------------------------
def buscar_jurisprudencia(tema):
    params = {
        "query": tema,
        "size": 50,   # quantidade de decisões retornadas
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(API_URL, params=params, headers=headers)

    if response.status_code != 200:
        return None

    return response.json()


# -----------------------------
# INTERFACE DO APP
# -----------------------------
st.title("🔎 Pesquisa Jurídica Inteligente")
st.write("Aplicação que busca jurisprudência real em tribunais brasileiros usando a API do Jurispect.")

tema = st.text_input("Digite um tema jurídico para pesquisar:")
botao = st.button("Pesquisar")

if botao and tema:
    st.info("Buscando decisões reais na API...")

    resultado = buscar_jurisprudencia(tema)

    if not resultado or "results" not in resultado:
        st.error("Nenhuma decisão encontrada ou erro na API.")
        st.stop()

    df = pd.DataFrame(resultado["results"])

    st.success(f"{len(df)} decisões encontradas!")

    # -----------------------------
    # Mostra tabela de decisões
    # -----------------------------
    st.subheader("📄 Decisões encontradas")
    st.dataframe(df[["title", "court", "date", "summary"]])

    # -----------------------------
    # Gráfico obrigatório
    # Distribuição por tribunal
    # -----------------------------
    st.subheader("📊 Distribuição das decisões por tribunal")

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="court:N",
            y="count():Q",
            tooltip=["court", "count()"]
        )
    )

    st.altair_chart(chart, use_container_width=True)

    # -----------------------------
    # Palavra mais frequentes
    # -----------------------------
    st.subheader("🧩 Palavras mais citadas nas decisões")

    texto_completo = " ".join(df["summary"].fillna(""))
    palavras = pd.Series(texto_completo.split()).value_counts().head(15)

    st.bar_chart(palavras)

    # -----------------------------
    # Salva histórico
    # -----------------------------
    try:
        df.to_csv("historico_juris.csv", mode="a", index=False)
        st.info("Histórico salvo com sucesso!")
    except:
        st.warning("Não foi possível salvar o histórico no Streamlit Cloud.")
