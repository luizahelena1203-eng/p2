import streamlit as st
import sqlite3
import datetime

# ------------------ CONFIGURAÇÃO ------------------
st.set_page_config(page_title="Rastreador Processual", page_icon="⚖️")
st.title("⚖️ Rastreador de Andamentos Processuais")
st.write("Ferramenta jurídica desenvolvida por **Luiza Lomba**")

# ------------------ BANCO DE DADOS ------------------
con = sqlite3.connect("processos.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS processos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT,
    tribunal TEXT,
    data_consulta TEXT,
    andamento TEXT
)
""")
con.commit()

# ------------------ FUNÇÃO DE CONSULTA ------------------
def consultar_andamentos(numero, tribunal):
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    return [
        {"data": hoje, "descricao": "Petição protocolada pela defesa"},
        {"data": hoje, "descricao": "Conclusos ao juiz"},
        {"data": hoje, "descricao": "Despacho proferido"},
    ]

# ------------------ INTERFACE STREAMLIT ------------------
st.subheader("🔍 Consultar Processo")

numero = st.text_input("Número do processo")
tribunal = st.text_input("Tribunal", value="TJSP")

if st.button("Consultar"):
    if not numero.strip():
        st.warning("Digite o número do processo.")
    else:
        resultados = consultar_andamentos(numero, tribunal)
        st.success("Consulta realizada com sucesso!")

        for r in resultados:
            st.write(f"- **{r['data']}** — {r['descricao']}")

        for r in resultados:
            cur.execute(
                "INSERT INTO processos (numero, tribunal, data_consulta, andamento) VALUES (?, ?, ?, ?)",
                (numero, tribunal, r["data"], r["descricao"])
            )
        con.commit()

# ------------------ HISTÓRICO ------------------
st.subheader("📁 Histórico de Consultas")
cur.execute("SELECT numero, tribunal, data_consulta, andamento FROM processos ORDER BY id DESC")
dados = cur.fetchall()

if dados:
    for d in dados:
        st.write(f"**{d[0]}** ({d[1]}) — {d[2]}: {d[3]}")
else:
    st.info("Nenhum processo consultado ainda.")
