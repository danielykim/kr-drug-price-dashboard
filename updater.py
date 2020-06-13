from pathlib import Path

import pandas as pd

from config import data_raw_dir, data_cleaned_dir
from config import MAX_NUMBER_OF_MONTHS, brdBltNo_latest
from config import data_compound_path, data_product_path, data_price_path

import downloader
import tools



def check():
    brdBltNo = brdBltNo_latest

    downloader.download(brdBltNo)


def update_tables():
    if Path(data_cleaned_dir).is_dir():
        check()

        print('Updating tables...')
        excel_file_paths = sorted(
            data_raw_dir.glob('**/*.xlsx'),
            reverse=True
        )[:MAX_NUMBER_OF_MONTHS]

        latest_excel_file_path = excel_file_paths[0]

        max_date = latest_excel_file_path.name.split('.')[0]

        date_str_list = [p.name.split('.')[0] for p in excel_file_paths[1:]]

        df_product_price, df_compound = tools.read_data(latest_excel_file_path)

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

        df_price_new = (
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
        )

        df_price_old = (
            pd.read_pickle(f'{data_cleaned_dir}/price.pickle')
            .reset_index()
            .loc[lambda x: x.Date.isin(date_str_list)]
        )

        df_price = (
            pd.concat([df_price_new, df_price_old])
                .set_index('제품코드')
        )

        df_compound.to_pickle(data_compound_path)
        df_product.to_pickle(data_product_path)
        df_price.to_pickle(data_price_path)

        print('Tables have been updated.')
    else:
        tools.check_data_raw()



if __name__ == '__main__':
    update_tables()
