# scripts/make_temperature_plot.py

import pathlib
import pandas as pd
import plotly.express as px

def main():
    # 1) Données météo (fictives) : température moyenne mensuelle (°C)
    df = pd.DataFrame({
        "mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
                 "Juil", "Août", "Sep", "Oct", "Nov", "Déc"],
        "temperature": [5, 6, 9, 12, 16, 20, 23, 22, 19, 14, 9, 6],
    })

    # 2) Création du graphique Plotly
    fig = px.line(
        df,
        x="mois",
        y="temperature",
        markers=True,
        title="Température moyenne mensuelle (°C)",
    )

    # 3) Personnalisation du graphe
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate="<b>%{x}</b><br>Température: %{y} °C<extra></extra>",
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Mois",
        yaxis_title="Température (°C)",
        font=dict(family="system-ui, -apple-system, BlinkMacSystemFont, sans-serif", size=14),
        title=dict(x=0.5, xanchor="center"),  # centrer le titre
        margin=dict(l=40, r=40, t=60, b=40),
    )

    # Optionnel : zones de couleur pour les saisons
    fig.add_vrect(x0="Déc", x1="Fév", fillcolor="lightblue", opacity=0.15, layer="below", line_width=0)
    fig.add_vrect(x0="Juin", x1="Août", fillcolor="orange", opacity=0.10, layer="below", line_width=0)

    # 4) Générer un HTML complet prêt pour GitHub Pages
    dist_dir = pathlib.Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    html_path = dist_dir / "index.html"

    # Petite page avec un titre + le graphe au centre
    html_template = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <title>Températures mensuelles</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: linear-gradient(180deg, #f9fafb 0%, #ffffff 40%);
      color: #0f172a;
    }}
    header {{
      padding: 16px 24px;
      border-bottom: 1px solid #e5e7eb;
      background: rgba(255, 255, 255, 0.9);
      position: sticky;
      top: 0;
      backdrop-filter: blur(12px);
      z-index: 10;
    }}
    h1 {{
      margin: 0;
      font-size: 1.4rem;
    }}
    main {{
      max-width: 960px;
      margin: 24px auto 40px;
      padding: 0 16px;
    }}
    .card {{
      background: white;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
      padding: 16px;
    }}
    @media (min-width: 768px) {{
      .card {{
        padding: 24px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>🌡️ Températures mensuelles</h1>
  </header>
  <main>
    <div class="card">
      {fig.to_html(include_plotlyjs="cdn", full_html=False)}
    </div>
  </main>
</body>
</html>
"""

    html_path.write_text(html_template, encoding="utf-8")
    print(f"✅ Dashboard généré : {html_path.resolve()}")

if __name__ == "__main__":
    main()
