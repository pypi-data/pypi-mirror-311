from pathlib import Path

import pandas as pd

from dsp_pandas.io import read_all_excel_sheets

DIR = Path(__file__).parent


def test_read_all_excel_sheets():
    """test both sheets with withspace in name and not."""
    fname = DIR / "data/test.xlsx"
    excel_file = read_all_excel_sheets(fname)
    assert excel_file.sheet_names == ["data", "meta data"]
    assert excel_file.sheet_names_attr == ["data", "meta_data"]

    assert excel_file.data.equals(
        pd.DataFrame(
            {
                "idx": ["a", "b", "c"],
                "feat1": [1, 2, 3],
            }
        ).set_index("idx")
    )

    assert excel_file.meta_data.equals(
        pd.DataFrame(
            {
                "idx": ["a", "b", "c"],
                "info": ["foo", "bla", "blub"],
            }
        ).set_index("idx")
    )
