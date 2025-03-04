import io
import sys
import base64
from typing import List, Tuple, Dict, Any
import pandas as pd
import numpy as np

class DataProcessor:
    """Class to process data, including Excel file handling and data expansion."""
    @staticmethod
    def process_excel_data(contents: str,sheet_index: int) -> Tuple[pd.DataFrame, List[Dict[str, str]]]:
        """Process uploaded Excel file and return dataframe and sheet options."""
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        file_data = io.BytesIO(decoded)

        ef = pd.ExcelFile(file_data)
        sheet_options = [{'label': label, 'value': str(i)}
                         for i, label in enumerate(ef.sheet_names)]

        df = ef.parse(sheet_index)
        nan_idx = df[df.isnull().all(axis=1)].index[0] if not df[df.isnull().all(axis=1)].empty else len(df) # handle case where no nan rows
        df = df[:nan_idx]
        df = df.drop(columns=['Sr. No']) if 'Sr. No' in df.columns else df # handle case where no 'Sr. No' column

        return df, sheet_options

    @staticmethod
    def expand_data(df: pd.DataFrame, outer_dia: int, test_area: int, height: int, total_height: int) -> pd.DataFrame:
        """Expand the input data based on given parameters."""
        pv = df.to_numpy()
        total_circumference = np.pi * outer_dia
        expansion_factor_cols = total_circumference / test_area
        expansion_factor_rows = total_height / height

        rows, cols = pv.shape
        num_cols = int(expansion_factor_cols * cols)
        num_rows = int(expansion_factor_rows * rows)

        expanded_df = pd.DataFrame(columns=range(num_cols), index=range(num_rows))
        expanded_df.iloc[:rows, :cols] = df.values
        expanded_df.fillna(-1, inplace=True)

        return expanded_df