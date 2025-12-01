import streamlit as st
import pandas as pd
import altair as alt
from api_service import buscar_decisoes

st.title("Consultor Jurídico com API Real (Brasil.io)")
st.write("Aplicação conectada a uma API pública com dados jurídicos reais.")

keyword = st.text_input("Digite uma palavra-chave para pesquisar decisões reais:")

if st.button("Buscar decisões"):
    if keyword:
        resposta = buscar_decisoes(keyword)

        if not resposta or len(resposta["results"]) == 0:
            st.warning("Nenhuma decisão encontrada para essa busca.")
        else:
            df = pd.DataFrame(resposta["results"])
            st.subheader("Resultados da API")
            st.dataframe(df)

            # Gera gráfico por tribunal
            if "court" in df.columns:
                st.subheader("Distribuição das decisões por tribunal")
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

            # Salva histórico
            try:
                df.to_csv("historico.csv", mode="a", index=False)
                st.info("Histórico salvo (historico.csv).")
            except:
                st.error("Não foi possível salvar o histórico.")
