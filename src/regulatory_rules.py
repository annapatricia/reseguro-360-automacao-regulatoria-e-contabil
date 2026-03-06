import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "reference" / "contracts.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "compliance_report.csv"

df = pd.read_csv(INPUT_FILE)

issues_list = []
status_list = []
risk_score_list = []
risk_level_list = []

for _, row in df.iterrows():

    issues = []
    risk_score = 0

    if pd.isna(row["reinsurer"]) or str(row["reinsurer"]).strip() == "":
        issues.append("Resseguradora ausente")
        risk_score += 3

    if row["premium_ceded"] <= 0:
        issues.append("Premio cedido invalido")
        risk_score += 2

    if row["claim_limit"] <= 0:
        issues.append("Limite de sinistro invalido")
        risk_score += 2

    start_date = pd.to_datetime(row["start_date"], errors="coerce")
    end_date = pd.to_datetime(row["end_date"], errors="coerce")

    if pd.isna(start_date) or pd.isna(end_date):
        issues.append("Datas invalidas")
        risk_score += 2
    elif end_date < start_date:
        issues.append("Data final anterior a data inicial")
        risk_score += 2

    if str(row["status"]).strip().upper() != "ATIVO":
        issues.append("Contrato nao esta ativo")
        risk_score += 1

    if risk_score >= 3:
        risk_level = "ALTO"
    elif risk_score >= 1:
        risk_level = "MEDIO"
    else:
        risk_level = "BAIXO"

    if issues:
        status_list.append("NAO_CONFORME")
        issues_list.append(" | ".join(issues))
    else:
        status_list.append("CONFORME")
        issues_list.append("Sem inconsistencias")

    risk_score_list.append(risk_score)
    risk_level_list.append(risk_level)

df["compliance_status"] = status_list
df["issues_found"] = issues_list
df["risk_score"] = risk_score_list
df["risk_level"] = risk_level_list

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("Relatorio gerado:")
print(OUTPUT_FILE)