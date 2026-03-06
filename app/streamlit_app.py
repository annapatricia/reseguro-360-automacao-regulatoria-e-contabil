import streamlit as st
import pandas as pd
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_FILE = BASE_DIR / "reports" / "compliance_report.csv"

st.set_page_config(page_title="Reseguro 360", layout="wide")

st.title("Reseguro 360: Automação Regulatória e Contábil")

st.write("Dashboard de validação regulatória para contratos de resseguro")

st.subheader("Executar validação regulatória")

if st.button("Rodar validação"):
    subprocess.run(["python", "src/regulatory_rules.py"])
    st.success("Validação executada com sucesso")

st.subheader("Relatório de Conformidade")

if REPORT_FILE.exists():

    df = pd.read_csv(REPORT_FILE)

    conformes = (df["compliance_status"] == "CONFORME").sum()
    nao_conformes = (df["compliance_status"] == "NAO_CONFORME").sum()
    risco_total = int(df["risk_score"].sum())
    contratos_alto_risco = (df["risk_level"] == "ALTO").sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Contratos Conformes", conformes)
    col2.metric("Contratos Não Conformes", nao_conformes)
    col3.metric("Risco Regulatório Total", risco_total)
    col4.metric("Contratos de Alto Risco", contratos_alto_risco)

    if contratos_alto_risco > 0:
        st.error(f"Atenção: existem {contratos_alto_risco} contratos classificados como ALTO risco regulatório.")
    else:
        st.success("Nenhum contrato classificado como ALTO risco regulatório.")

    st.subheader("Filtros")

    col_filtro1, col_filtro2 = st.columns(2)

    risco_selecionado = col_filtro1.selectbox(
        "Selecione nível de risco",
        ["TODOS", "BAIXO", "MEDIO", "ALTO"]
    )

    conformidade_selecionada = col_filtro2.selectbox(
        "Selecione status de conformidade",
        ["TODOS", "CONFORME", "NAO_CONFORME"]
    )

    df_filtrado = df.copy()

    if risco_selecionado != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["risk_level"] == risco_selecionado]

    if conformidade_selecionada != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["compliance_status"] == conformidade_selecionada]

    st.subheader("Tabela de contratos")

    st.dataframe(df_filtrado, use_container_width=True)

    st.subheader("Distribuição de Conformidade")

    chart_data = df["compliance_status"].value_counts()

    st.bar_chart(chart_data)

    st.subheader("Distribuição de Nível de Risco")

    risk_chart = df["risk_level"].value_counts()

    st.bar_chart(risk_chart)

    st.subheader("Contratos com maior risco")

    top_risk = df.sort_values("risk_score", ascending=False)

    st.dataframe(
        top_risk[
            [
                "contract_id",
                "ceding_company",
                "reinsurer",
                "risk_score",
                "risk_level",
                "issues_found",
            ]
        ],
        use_container_width=True,
    )

    st.subheader("Download do relatório")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Baixar relatório CSV",
        data=csv,
        file_name="reinsurance_compliance_report.csv",
        mime="text/csv"
    )

else:

    st.warning("Relatório ainda não foi gerado")