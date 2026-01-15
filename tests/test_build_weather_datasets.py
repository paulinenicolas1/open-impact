# test_pipeline.py
import pandas as pd
import pandas.testing as pdt
import numpy as np


import data_processing.build_weather_datasets as build_weather_datasets
from data_processing.build_weather_datasets import add_ma5, build_yearly


def test_add_ma5_basic():
    # GIVEN
    df = pd.DataFrame({
        "NOM_USUEL": ["A"] * 7,
        "AAAA": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "TMM": [10, 11, 12, 13, 14, 15, 16],
    })

    # WHEN
    result = add_ma5(
        df,
        value_col="TMM",
        group_col="NOM_USUEL",
        order_cols=["NOM_USUEL", "AAAA"],
        window=5,
        min_periods=5,
    )

    # THEN
    expected_ma5 = [np.nan, np.nan, np.nan, np.nan, 12.0, 13.0, 14.0]

    assert "TMM_ma5" in result.columns
    assert np.array_equal(result["TMM_ma5"].tolist(), expected_ma5, equal_nan=True)


def test_build_yearly_groups_by_year_and_city_and_aggregates(monkeypatch):
    # On remplace AGG_SPEC par une agg simple et déterministe
    # Ici: TMM = moyenne par (AAAA, NOM_USUEL)
    monkeypatch.setattr(build_weather_datasets, "AGG_SPEC", {"TMM": ("TMM", "mean")})

    # On remplace add_ma5 par une fonction identity pour isoler le groupby/round
    monkeypatch.setattr(build_weather_datasets, "add_ma5", lambda df, **kwargs: df)

    df = pd.DataFrame({
        "AAAA":      [2000, 2000, 2000, 2001],
        "NOM_USUEL": ["Paris", "Paris", "Lyon", "Paris"],
        "TMM":       [10.0, 12.0, 7.0, 20.0],
    })

    out = build_yearly(df)

    # Attendu: une ligne par couple (AAAA, NOM_USUEL)
    # 2000-Paris: mean(10,12)=11 ; 2000-Lyon: 7 ; 2001-Paris: 20
    expected = pd.DataFrame({
        "AAAA":      [2000, 2000, 2001],
        "NOM_USUEL": ["Lyon", "Paris", "Paris"],
        "TMM":       [7.0, 11.0, 20.0],
    }).sort_values(["AAAA", "NOM_USUEL"]).reset_index(drop=True)

    out_sorted = out.sort_values(["AAAA", "NOM_USUEL"]).reset_index(drop=True)

    pd.testing.assert_frame_equal(out_sorted, expected)


def test_build_yearly_aggregates_rounds_and_adds_ma5():
    # Données: 2 villes, plusieurs lignes par année => test du groupby/agg
    df = pd.DataFrame({
        "AAAA":      [2000, 2001, 2002, 2003, 2004, 2005, 2002, 2003, 2004, 2004, 2005, 2006],
        "NOM_USUEL": ["Paris"] * 6 + ["Lyon"] * 6,
        # valeurs volontairement avec décimales pour vérifier round({'TMM': 1})
        "TMM":       [10.04, 10.06, 11.14, 11.16, 12.24, 12.26, 13.34, 13.36, 14.44, 14.46, 15.54, 15.56],
        "NBJTX25": [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2],
        "RR": [100.0, 120.0, 90.0, 100.0, 120.0, 90.0, 100.0, 120.0, 90.0, 100.0, 120.0, 90.0],
        "RRAB": [0, 0, 1, 0, 4, 1, 0, 2, 7, 12, 22, 1],
        "TXAB": [0, 1, 24, 30, 1, 1, 0, 45, 23, 22, 1, 18],
        "TXMIN": [2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0]
    })

    out = build_yearly(df)

    # 1) Colonnes attendues
    assert "AAAA" in out.columns
    assert "NOM_USUEL" in out.columns
    assert "TMM" in out.columns

    # 2) Il doit y avoir une ligne par (AAAA, NOM_USUEL)
    assert len(out) == out[["AAAA", "NOM_USUEL"]].drop_duplicates().shape[0]

    # 3) Arrondi à 1 décimale sur TMM
    # On vérifie que toutes les valeurs TMM ont une seule décimale "effective"
    # (ex: 10.1, 11.2, etc). Trick: comparer à un arrondi 1 décimale.
    assert np.allclose(out["TMM"].to_numpy(), np.round(out["TMM"].to_numpy(), 1), equal_nan=True)

    # 4) Vérifier que MA5 a bien été ajoutée (nom de colonne: on essaie les deux conventions les + courantes)
    ma_cols = [c for c in out.columns if "ma5" in c.lower()]
    assert len(ma_cols) == 1, f"Expected exactly one MA5 column, found: {ma_cols}"
    ma_col = ma_cols[0]

    # 5) Vérifier le tri par NOM_USUEL puis AAAA (important pour MA)
    sorted_out = out.sort_values(["NOM_USUEL", "AAAA"]).reset_index(drop=True)
    pdt.assert_frame_equal(out.reset_index(drop=True), sorted_out)

    # 6) Vérifier que la MA5 est calculée par ville (les 4 premières années NaN pour chaque ville)
    for city in out["NOM_USUEL"].unique():
        s = out.loc[out["NOM_USUEL"] == city].sort_values("AAAA")
        # les 4 premières valeurs doivent être NaN si MA5 exige 5 périodes (cas standard)
        first4 = s[ma_col].head(4).to_numpy()
        assert np.all(np.isnan(first4)), f"{city}: expected first 4 MA values to be NaN, got {first4}"

        # et à partir de la 5e, on doit avoir des nombres (si suffisamment d'années)
        fifth = s[ma_col].iloc[4]
        assert not np.isnan(fifth), f"{city}: expected 5th MA value to be non-NaN"
