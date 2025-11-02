import os
import gzip
from utils import unzip_gz

def test_unzip_gz(tmp_path: str):
    input_path = tmp_path / "test.csv.gz"
    output_path = tmp_path / "test.csv"
    print('coucou')
    print('coucou2')

