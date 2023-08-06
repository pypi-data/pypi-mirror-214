from pd_cldf import load
import pandas as pd


def test_load(data):
    ds = load(data / "cldf" / "metadata.json")  # noqa: E501
    assert isinstance(ds["forms.csv"], pd.DataFrame)
