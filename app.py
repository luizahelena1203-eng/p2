import streamlit as st
import requests
import pandas as pd

# ===========================
# CONFIGURAÇÃO DA PÁGINA
# ===========================
st.set_page_config(page_title="Analisador de Processos", layout="centered")
st.title("📄 Analisador Automático de Processos Jurídicos")

st.write("Cole o texto do processo e clique em **Analisar** para gerar um resumo automático e estatísticas.")

# ===========================
# INPUT DO USUÁRIO
# ===========================
processo_texto = st.text_area("Texto do processo:", height=300)

if st.button("Analisar"):
    if not processo_texto.strip():
        st.error("Por favor, cole o texto do processo.")
        st.stop()

    with st.spinner("Analisando..."):

        # ===========================
        # CHAMADA À SUA API
        # ===========================
        try:
            response = requests.post(
                "http://localhost:8000/analisar",   # <<< SEU ENDPOINT FASTAPI
                json={"texto": processo_texto}
            )

        except Exception as e:
            st.error("Erro ao conectar com a API.")
            st.exception(e)
            st.stop()

        if response.status_code != 200:
            st.error("A API retornou um erro:")
            st.write(response.text)
            st.stop()

        dados = response.json()

    st.success("Análise concluída!")

    # ===========================
    # EXIBE RESULTADO PRINCIPAL
    # ===========================
    st.subheader("📌 Resumo do Processo")
    st.write(dados.get("resumo", "Sem resumo."))

    st.subheader("📊 Pontos Principais Detectados")
    if "topicos" in dados and dados["topicos"]:
        for t in dados["topicos"]:
            st.markdown(f"- {t}")
    else:
        st.write("Nenhum tópico detectado.")

    # ===========================
    # GRÁFICO AUTOMÁTICO
    # ===========================
    st.subheader("📈 Gráfico de Frequência de Palavras (automático)")

    if "frequencia" in dados and dados["frequencia"]:

        # Converte o dict em DataFrame
        df = pd.DataFrame.from_dict(
            dados["frequencia"], 
            orient="index", 
            columns=["Frequência"]
        ).sort_values("Frequência", ascending=False)

        st.bar_chart(df)
    else:
        st.write("Não foi possível gerar gráfico para este processo.")
