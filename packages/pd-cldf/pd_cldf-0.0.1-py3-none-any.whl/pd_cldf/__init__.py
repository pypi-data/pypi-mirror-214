"""Top-level package for pd-cldf."""
import json
import logging
from pathlib import Path
import pandas as pd


# handler = colorlog.StreamHandler(None)
# handler.setFormatter(
#     colorlog.ColoredFormatter("%(log_color)s%(levelname)-7s%(reset)s %(message)s")
# )
log = logging.getLogger(__name__)
# log.propagate = True
# log.addHandler(handler)

__author__ = "Florian Matter"
__email__ = "fmatter@mailbox.org"
__version__ = "0.0.1"


def load(metadata):
    metadata = Path(metadata)
    assert metadata.is_file()
    with open(metadata, "r", encoding="utf-8") as f:
        md = json.load(f)
    dfs = {}
    for table in md["tables"]:
        dfs[table["url"]] = pd.read_csv(
            metadata.parents[0] / table["url"], keep_default_na=False, index_col="ID"
        )
    return dfs
