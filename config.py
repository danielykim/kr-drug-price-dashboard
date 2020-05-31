from pathlib import Path


META_TAGS = [
    {'charset':'UTF-8'},
    {
        'http-equiv':'X-UA-Compatible',
        'content':'IE=edge'
    },
    {
        'name':'viewport',
        'content':'width=device-width, initial-scale=1, shrink-to-fit=no'
    }
]

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css'
]


PARSER = 'lxml'

BASE_URL = 'https://www.hira.or.kr'

BBS_URL = f'{BASE_URL}/bbsDummy.do'
DOWNLOAD_URL = f'{BASE_URL}/bbs/bbsCDownLoad.do'

PARAMS = {
    'pgmid':'HIRAA030014050000',
    'brdScnBltNo':'4',
    'brdBltNo':'1576',
    'pageIndex':1
}

# 2016-07-01
brdBltNo_start = 1576

data_raw_dir = Path('data-raw/')
data_cleaned_dir = Path('data-cleaned')

data_compound_path = Path(data_cleaned_dir, 'compound.pickle')
data_product_path  = Path(data_cleaned_dir, 'product.pickle')
data_price_path    = Path(data_cleaned_dir, 'price.pickle')

MAX_NUMBER_OF_MONTHS = 60
