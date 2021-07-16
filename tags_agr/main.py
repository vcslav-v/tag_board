import pandas as pd
import os
from tags_agr import db_tools, UPLOAD_FOLDER_ADOBE


def uploaded_files():
    for adobe_file_path in os.listdir(UPLOAD_FOLDER_ADOBE):
        yield os.path.join(UPLOAD_FOLDER_ADOBE, adobe_file_path)
        os.remove(os.path.join(UPLOAD_FOLDER_ADOBE, adobe_file_path))


def get_df(xlsx_file_path: str) -> pd.DataFrame:
    excel_data_df = pd.read_excel(xlsx_file_path, sheet_name='For Contributors')
    df = excel_data_df[['Title']].dropna()
    df['Keywords'] = excel_data_df['Keywords\n\n (0-10 maximum)'].dropna().str.strip().str.lower().str.split(', ')
    return df


def push_to_db(df: pd.DataFrame):
    for row in df.itertuples():
        db_tools.push(row.Title, row.Keywords)


def add_new_data():
    for adobe_file_path in uploaded_files():
        df = get_df(adobe_file_path)
        push_to_db(df)
