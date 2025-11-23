# scripts/make_temperature_plot.py

import os
import pathlib

import logging
import pandas as pd

from src.plot_graphics.plot_temperature import plot_temperature
from src.html_template import build_html_template
from src.config import PROJECT_ROOT
from src.utils import yearly_mean

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_TEMPERATURE_DIR = os.path.join(PROJECT_ROOT,"data", "meteo-france-75", "unzipped")
DEFAULT_TEMPERATURE_FILES = [
    "MENSQ_75_1816-1949.csv",
    "MENSQ_75_previous-1950-2023.csv",
    "MENSQ_75_latest-2024-2025.csv",
]



def main():
    # 1) Données météo (fictives) : température moyenne mensuelle (°C)
    df = yearly_mean(
        data_dir=DEFAULT_TEMPERATURE_DIR,
        files=DEFAULT_TEMPERATURE_FILES,
        temp_column="TX",
        date_column="AAAAMM",
        location_column="NOM_USUEL",
        location_value="PARIS-MONTSOURIS"
    )

    # 2) Création du graphique Plotly
    fig = plot_temperature(df,
                           year_column='year',
                           temperature_column='yearly_mean_temperature')

    # 4) Générer un HTML complet prêt pour GitHub Pages
    dist_dir = pathlib.Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    html_path = os.path.join(dist_dir, "index.html")
    html_path = pathlib.Path(html_path)

    HTML_TEMPLATE = build_html_template(fig)

    html_path.write_text(HTML_TEMPLATE, encoding="utf-8")
    print(f"✅ Dashboard généré : {html_path.resolve()}")


if __name__ == "__main__":
    main()
