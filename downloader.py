from pathlib import Path
from bs4 import BeautifulSoup as BS

import requests

from config import BBS_URL, DOWNLOAD_URL, PARAMS, PARSER
from config import data_raw_dir

import config
import tools
import updater



def date_str_extractor_BS(html_BS):
    raw_sentence = (
        html_BS
        .select('th.sbj.line_r_none')[0].text
    )

    date_str = tools.date_str_extractor(raw_sentence)

    return date_str


def generate_excel_file_parameters(html_BS):
    keys = ['apndNo', 'apndBrdBltNo', 'apndBrdTyNo', 'apndBltNo']

    values = (
        html_BS
        .select('ul.file_ulist')[0]
        .select('a')[0]
        ['onclick']
        .split('(')[1]
        .split(')')[0]
        .replace("'", '')
        .split(',')
    )

    parameters = dict(zip(keys, values))

    return parameters


def download(brdBltNo):
    PARAMS['brdBltNo'] = brdBltNo

    r = requests.get(BBS_URL, params=PARAMS)

    html_BS = BS(r.text, PARSER)

    date_str = date_str_extractor_BS(html_BS)

    if date_str is not None:
        parameters = generate_excel_file_parameters(html_BS)

        r = requests.get(DOWNLOAD_URL, params=parameters)

        year = date_str[:4]

        excel_file_dir = Path(data_raw_dir, year)

        Path(excel_file_dir).mkdir(parents=True, exist_ok=True)

        excel_file_path = f'{excel_file_dir}/{date_str}.xlsx'

        with open(excel_file_path, 'wb') as excel_file:
            excel_file.write(r.content)

        print(f'Successfully Saved (brdBltNo = {brdBltNo}): {excel_file_path}')



if __name__ == '__main__':
    check_data_raw()
