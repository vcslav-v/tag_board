import re
from typing import Any

import pandas as pd
from fastapi import UploadFile
from tags_agr import db_tools


def push_xls_to_db(file_data: UploadFile):
    excel_data_df = pd.read_excel(file_data.file.read(), sheet_name='For Contributors')
    num_batch_list = re.findall(r'(?<=batch)\d+', file_data.filename, re.I)
    if num_batch_list:
        num_batch: Any[int, None] = int(num_batch_list[-1])
    else:
        num_batch = None
    df = excel_data_df[['Title']].dropna()
    df['Keywords'] = excel_data_df[
        'Keywords\n\n (0-10 maximum)'
    ].dropna().str.strip().str.lower().str.split(', ')
    df['Batch'] = num_batch
    for row in df.itertuples():
        db_tools.push(row.Title, row.Keywords, row.Batch)
