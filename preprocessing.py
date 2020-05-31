from pathlib import Path

from tqdm import tqdm

import pandas as pd

import preprocessing

from config import data_raw_dir, data_cleaned_dir, MAX_NUMBER_OF_MONTHS
from config import data_compound_path, data_product_path, data_price_path

import tools



def initialize():
    if not Path(data_cleaned_dir).is_dir():
        Path(data_cleaned_dir).mkdir(parents=True, exist_ok=True)

        excel_file_paths = sorted(
            list(data_raw_dir.glob('**/*.xlsx')),
            reverse=True
        )[:MAX_NUMBER_OF_MONTHS]

        df_list = [
            tools.read_data(data_path)
            for data_path in tqdm(excel_file_paths)
        ]

        df_product_price, df_compound = map(pd.concat, list(zip(*df_list)))

        max_date = df_product_price.Date.max()

        df_compound = (
            df_compound
                .drop_duplicates()
                .loc[lambda x: x.Date == max_date]
        )

        selected_columns = [
            '투여',
            '식약분류',
            '주성분코드',
            '제품코드',
            '제품명',
            '업체명',
            '규격',
            '단위',
            '전문/일반',
            '비고'
        ]

        df_product = (
            df_product_price
                .loc[lambda x:
                    (x.비고.isna()) & (x.Date == max_date)
                ]
                [selected_columns]
                .drop_duplicates()
                .reset_index()
                .drop('index', axis='columns')
                .set_index('제품코드')
        )

        df_price = (
            df_product_price
                [['제품코드', 'Date', '상한금액']]
                .drop_duplicates()
                .reset_index()
                .drop('index', axis='columns')
                .assign(상한금액=lambda x:
                    pd.to_numeric(
                        x.상한금액.apply(lambda v:
                            None if type(v) is not int else v
                        ),
                        errors='coerce'
                    )
                )
                .set_index('제품코드')
        )

        df_compound.to_pickle(data_compound_path)
        df_product.to_pickle(data_product_path)
        df_price.to_pickle(data_price_path)



if __name__ == '__main__':
    initialize()
