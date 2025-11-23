# scripts/make_temperature_plot.py

import pathlib
import pandas as pd

from scripts.plot_graphics.plot_temperature import plot_temperature
from scripts.template import build_html_template


def main():
    # 1) Données météo (fictives) : température moyenne mensuelle (°C)
    df = pd.DataFrame({
        "mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
                 "Juil", "Août", "Sep", "Oct", "Nov", "Déc"],
        "temperature": [5, 6, 9, 12, 16, 20, 23, 22, 19, 14, 9, 6],
    })

    # 2) Création du graphique Plotly
    fig = plot_temperature(df)

    # 4) Générer un HTML complet prêt pour GitHub Pages
    dist_dir = pathlib.Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    html_path = dist_dir / "index.html"

    # Petite page avec un titre + le graphe au centre
    HTML_TEMPLATE = build_html_template(fig)

    html_path.write_text(HTML_TEMPLATE, encoding="utf-8")
    print(f"✅ Dashboard généré : {html_path.resolve()}")


if __name__ == "__main__":
    main()
