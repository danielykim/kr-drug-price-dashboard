from pathlib import Path

import pandas as pd

from config import BBS_URL, PARAMS, PARSER
from config import brdBltNo_start, brdBltNo_latest

import downloader
import preprocessing
import updater



def date_str_extractor(raw_sentence):
    title = (
        raw_sentence
        .strip()
        .replace(' ', '')
        .split('\r\n')[0]
    )

    drug_price_sentence = '현재 약제 급여목록 및 급여상한금액표'.replace(' ', '')

    if drug_price_sentence in title:
        title = (
            title
            .split(drug_price_sentence)[0][:-1]
            .replace('.', '-')
        )
    else:
        title = None

    return title


def row_cleaner(r):
    values = set([
        v
        for c, v in zip(r.index, r.values)
        if '비고' in c
    ])

    if len(values) == 1:
        return list(values)[0]
    else:
        return ' | '.join(map(str,values))


def read_data(data_path):
    date_str = data_path.name.split('.')[0]

    selected_columns = [
        '투여',
        '식약분류',
        '주성분코드',
        '제품코드',
        '목록정비전코드',

        '제품명',
        '업체명',
        '규격',
        '단위',
        '전문/일반',

        '비고',
        '상한금액'
    ]

    df = (
        pd.read_excel(
            data_path,
            dtype={'주성분코드':str, '목록정비전코드':str}
        )
        .rename({
            '전일':'전문/일반',

            '식약처분류번호':'식약분류',
            '분류':'식약분류',

            '비고':'비고0',
            '비고_위험분담등관련':'비고1',
            '비고_위험분담':'비고2',
            "'18.10.6.\n삭제품목":'비고3',
            '8월 중 변경사항':'비고4',
            '위험분담':'비고5'
        }, axis='columns')
        .assign(비고=lambda x:
            x.apply(lambda r:
                row_cleaner(r),
                axis='columns'
            )
        )
        [selected_columns]
        .assign(Date=date_str)
    )

    df_product_price = (
        df
        .loc[lambda x: ~x.제품명.isna()]
        .reset_index()
        .drop(['index'], axis='columns')
    )

    df_compound = (
        df
        .loc[lambda x: x.제품명.isna()]
        .rename({
            '제품코드':'주성분설명'}, axis='columns')
        [['주성분코드', '식약분류', '투여', '주성분설명', 'Date']]
        .reset_index()
        .drop('index', axis='columns')
    )

    return df_product_price, df_compound


def check_data_raw():
    if not Path('data-raw').is_dir():
        for brdBltNo in range(brdBltNo_start, brdBltNo_latest+1):
            downloader.download(str(brdBltNo))

        preprocessing.initialize()
    else:
        updater.update_tables()
