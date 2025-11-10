# make_dashboard.py
import plotly.express as px
import pandas as pd
import pathlib

df = pd.DataFrame({
    "mois": ["Jan","Fév","Mar","Avr","Mai","Juin","Juil","Août","Sep","Oct","Nov","Déc"],
    "revenu": [1200, 1340, 1420, 1550, 1510, 1700, 1650, 1720, 1800, 1900, 2000, 2100]
})
fig = px.line(df, x="mois", y="revenu", title="Revenus mensuels (€)")
fig.update_layout(template="plotly_white")

out = pathlib.Path("dist")
out.mkdir(parents=True, exist_ok=True)
fig.write_html(out / "index.html", include_plotlyjs="cdn")
print("✅ Généré : dist/index.html")
