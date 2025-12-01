import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🔎 Buscador de Leis e Normas – API LexML")
st.write("Aplicação que consulta leis reais utilizando a API pública do LexML.")

# Função para consultar a API
def buscar_lexml(consulta):
    url = "https://www.lexml.gov.br/api/busca"
    params = {"q": consulta, "formato": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao consultar API: {e}")
        return None

# Interface
tema = st.text_input("Digite um tema jurídico para buscar nas leis:", "")

if tema:
    dados = buscar_lexml(tema)

    if dados and "resultado" in dados:
        itens = dados["resultado"]["item"]

        if itens:
            st.subheader("📄 Resultados encontrados:")

            # Mostrar lista
            for item in itens[:10]:
                st.write(f"**{item['urn']}** — {item.get('titulo', 'Sem título')}")

            # Criar gráfico por tipo de documento
            tipos = [item["tipo"] for item in itens]

            df = pd.DataFrame({"tipo": tipos})
            graf = df["tipo"].value_counts()

            st.subheader("📊 Distribuição por Tipo de Norma")
            fig, ax = plt.subplots()
            graf.plot(kind="bar", ax=ax)
            st.pyplot(fig)

        else:
            st.warning("Nenhuma norma encontrada para esse tema.")
