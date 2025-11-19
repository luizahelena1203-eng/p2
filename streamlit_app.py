# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import io
import os

st.set_page_config(page_title="Rastreador de Andamentos - Versão com Dados Reais", page_icon="⚖️", layout="wide")
st.title("⚖️ Rastreador de Andamentos Processuais (com dados reais)")
st.write("Projeto: Luiza Lomba — Direito FGV")

# Paths dos arquivos (relativos ao diretório do app)
ANDAMENTOS_CSV = "andamentos_reais.csv"
HIST_CSV = "consultas_hist.csv"

# --- Carregar dados de andamentos reais ---
if os.path.exists(ANDAMENTOS_CSV):
    df_andamentos = pd.read_csv(ANDAMENTOS_CSV, dtype=str)
else:
    # cria exemplo mínimo se não existir
    df_andamentos = pd.DataFrame(columns=["numero","tribunal","data","descricao"])
    df_andamentos.to_csv(ANDAMENTOS_CSV, index=False)

# Normalizar colunas string (safe)
for col in ["numero","tribunal","data","descricao"]:
    if col in df_andamentos.columns:
        df_andamentos[col] = df_andamentos[col].astype(str)

# --- Função de busca ---
def buscar_andamentos(numero: str = None, tribunal: str = None):
    df = df_andamentos.copy()
    if numero:
        # busca exata (pode ajustar para contains)
        df = df[df["numero"].str.contains(numero, na=False)]
    if tribunal:
        df = df[df["tribunal"].str.contains(tribunal, case=False, na=False)]
    return df.sort_values(by="data", ascending=False)

# --- Interface: painel à esquerda para inputs ---
with st.sidebar:
    st.header("Consulta")
    numero_input = st.text_input("Número do processo (ex.: 0000000-00.2022.8.26.0100)")
    tribunal_input = st.text_input("Tribunal (ex.: TJSP / TRT2 / TRF3)", value="")
    buscar_btn = st.button("📡 Buscar andamentos")
    st.markdown("---")
    st.header("Download")
    # botão para baixar a base de andamentos reais
    csv_andamentos = df_andamentos.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar andamentos_reais.csv", csv_andamentos, file_name="andamentos_reais.csv", mime="text/csv")
    # botão para baixar histórico (se existir)
    if os.path.exists(HIST_CSV):
        with open(HIST_CSV, "rb") as f:
            st.download_button("⬇️ Baixar histórico de consultas", f, file_name="consultas_hist.csv", mime="text/csv")
    st.markdown("---")
    st.write("Observações:")
    st.write("- Dados de exemplo retirados de fontes públicas / anonimizados.")
    st.write("- Para persistência entre deploys automatizados, ver seção no README (opções: commit GitHub, BD externo).")

# --- Quando o usuário clica 'Buscar' ---
if buscar_btn:
    if not numero_input and not tribunal_input:
        st.warning("Insira número do processo ou tribunal para buscar.")
    else:
        resultados = buscar_andamentos(numero_input.strip(), tribunal_input.strip())
        st.success(f"{len(resultados)} andamentos encontrados")
        # exibir tabela (coluna data, descricao, tribunal, numero)
        st.dataframe(resultados[["numero","tribunal","data","descricao"]].reset_index(drop=True), use_container_width=True)

        # salvar histórico: append ao arquivo HIST_CSV com timestamp
        timestamp = datetime.datetime.utcnow().isoformat()
        row = {
            "timestamp": timestamp,
            "numero": numero_input,
            "tribunal": tribunal_input,
            "resultado_count": len(resultados)
        }
        # cria arquivo se não existir
        hist_df = pd.DataFrame([row])
        if os.path.exists(HIST_CSV):
            hist_df.to_csv(HIST_CSV, mode="a", header=False, index=False)
        else:
            hist_df.to_csv(HIST_CSV, index=False)

# --- Mostrar gráfico de frequência de consultas por tribunal (lê o histórico) ---
st.subheader("📊 Gráfico: frequência de consultas por tribunal")
if os.path.exists(HIST_CSV):
    hist_all = pd.read_csv(HIST_CSV, dtype=str)
    # preencher tribunais vazios
    hist_all["tribunal"] = hist_all["tribunal"].fillna("Não informado")
    # contar por tribunal
    counts = hist_all.groupby("tribunal").size().reset_index(name="contagem")
    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X("tribunal:N", sort="-y", title="Tribunal"),
        y=alt.Y("contagem:Q", title="Número de consultas"),
        tooltip=["tribunal","contagem"]
    ).properties(width=700, height=350)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Ainda não há histórico de consultas. Realize uma busca para gerar o gráfico.")

# --- Listar últimos 20 registros do histórico ---
st.subheader("📁 Histórico de consultas (últimos registros)")
if os.path.exists(HIST_CSV):
    hist_show = pd.read_csv(HIST_CSV, dtype=str)
    hist_show = hist_show.sort_values("timestamp", ascending=False).head(20)
    st.table(hist_show)
else:
    st.write("Nenhum histórico encontrado.")

# --- Botão de 'Salvar' (baixar o histórico atualizado) exibido também abaixo ---
if os.path.exists(HIST_CSV):
    with open(HIST_CSV, "rb") as f:
        st.download_button("⬇️ Baixar histórico de consultas (CSV)", f, file_name="consultas_hist.csv", mime="text/csv")

