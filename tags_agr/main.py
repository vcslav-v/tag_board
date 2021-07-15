import pandas as pd
import os
from tags_agr import db_tools


def get_xlsx_file_path(path: str):
    for xlsx_file in os.listdir(path):
        if os.path.splitext(xlsx_file)[-1] == '.xlsx':
            yield os.path.join(path, xlsx_file)


def get_df(xlsx_file_path: str) -> pd.DataFrame:
    excel_data_df = pd.read_excel(xlsx_file_path, sheet_name='For Contributors')
    df = excel_data_df[['Title']].dropna()
    df['Keywords'] = excel_data_df['Keywords\n\n (0-10 maximum)'].dropna().str.strip().str.lower().str.split(', ')
    return df


def push_to_db(df: pd.DataFrame):
    for row in df.itertuples():
        db_tools.push(row.Title, row.Keywords)


def new_data(files):
    for xlsx_file_path in files:
        if os.path.splitext(xlsx_file_path.filename)[-1] == '.xlsx':
            df = get_df(xlsx_file_path)
            push_to_db(df)
