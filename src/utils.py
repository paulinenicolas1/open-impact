import gzip
import logging
import shutil
from pathlib import Path
from typing import Iterable

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def unzip_gz(input_path: str, output_path: str) -> None:
    with gzip.open(input_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    logger.info(f"✅ Fichier décompressé : {output_path}")


def yearly_mean(
    data_dir: Path | str,
    files: Iterable[str],
    temp_column: str = "TX",
    date_column: str = "AAAAMM",
    location_column: str = "NOM_USUEL",
    location_value: str = "PARIS-MONTSOURIS",
) -> pd.DataFrame:
    """
    Load the monthly temperature files and return the yearly mean temperature for PARIS-MONTSOURIS.

    Parameters
    ----------
    data_dir: folder containing the unzipped CSVs.
    files: iterable of CSV filenames to load (ordered oldest -> newest).
    temp_column: column name holding temperature (monthly, typically `TX`).
    date_column: YYYYMM column (e.g. `AAAAMM`).
    location_column: column holding the station name (`NOM_USUEL`).
    location_value: station to keep (`PARIS-MONTSOURIS` by default).

    Returns
    -------
    pd.DataFrame with columns `year` and `yearly_mean_temperature`.
    """
    data_dir = Path(data_dir)
    frames = []
    for file_name in files:
        csv_path = data_dir / file_name
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing temperature file: {csv_path}")
        frames.append(pd.read_csv(csv_path, sep=";"))

    df = pd.concat(frames, ignore_index=True)
    required_cols = {temp_column, date_column, location_column}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns in data: {missing}")

    subset = df[df[location_column] == location_value].copy()
    if subset.empty:
        return pd.DataFrame(columns=["year", "yearly_mean_temperature"])

    subset[temp_column] = pd.to_numeric(subset[temp_column], errors="coerce")
    subset[date_column] = subset[date_column].astype(str).str.strip()
    subset = subset.dropna(subset=[temp_column, date_column])
    # subset = subset[subset[date_column].astype(str).str.fullmatch(r"\\d{6}")]
    subset["year"] = subset[date_column].str[:4].astype(int)

    yearly_mean = (
        subset.groupby("year")[temp_column]
        .mean()
        .reset_index()
        .rename(columns={temp_column: "yearly_mean_temperature"})
    )
    return yearly_mean
