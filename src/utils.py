import gzip
import logging
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def unzip_gz(input_path: str, output_path: str) -> None:
    with gzip.open(input_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    logger.info(f"✅ Fichier décompressé : {output_path}")