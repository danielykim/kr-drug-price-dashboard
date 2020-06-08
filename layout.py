from datetime import datetime as dt

import pandas as pd

import dash_table
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

from config import data_cleaned_dir
from config import data_compound_path, data_product_path, data_price_path

import tools



tools.check_data_raw()

df_compound = (
    pd.read_pickle(data_compound_path)
    [['주성분코드', '주성분설명']]
)

df_product = (
    pd.read_pickle(data_product_path)
        [['제품명', '업체명', '규격', '단위', '투여', '전문/일반', '식약분류', '주성분코드']]
        .reset_index()
        .merge(
            df_compound,
            how='left',
            on='주성분코드'
        )
        .set_index('제품코드')
)

df_price = (
    pd.read_pickle(data_price_path)
)

number_of_products = len(df_product.reset_index().제품코드.unique())

max_date = df_price.Date.max()

product_name_code_list = (
    df_product
    .reset_index()
    .loc[lambda x: x.제품코드.isin(df_price.reset_index().제품코드.unique())]
    [['제품명', '제품코드']]
    .sort_values(by='제품명')
    .values
)

product_selector_options = [
    {'label':name, 'value':code}
    for name, code in product_name_code_list
]



def draw_time_series_trace(product_code):
    if type(product_code) is str:
        d = (
            df_price
            .loc[product_code, ['Date', '상한금액']]
            .sort_values(by='Date')
        )

        t = go.Scatter(
            x=d.Date.values,
            y=d.상한금액.values,
            name=df_product.at[product_code, '제품명']
        )
    else:
        t = go.Scatter()

    return t


def draw_price_time_series(product_code_list):
    title_text = f"Drug Upper-bound Price Time Series 약품 상한 가격 시계열 (as of {max_date})"

    if type(product_code_list) is list and len(product_code_list) > 0:
        fig = go.Figure([
            draw_time_series_trace(product_code)
            for product_code in product_code_list
        ])

    else:
        fig = go.Figure()

        title_text = f'{title_text} (Select products first)'

    fig.update_layout(
        xaxis=dict(
            title='Date',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Drug Upper-bound Price (KRW)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        title=dict(
            text=title_text,
            font=dict(size=20)
        ),
        height=400,
    )

    return fig


def get_records(product_code_list):
    if type(product_code_list) is list:
        d = df_product.loc[product_code_list].to_dict('records')
    else:
        d = df_product.head(0).to_dict('records')

    return d


def initialize_layout():
    # 키트루다주(펨브롤리주맙,유전자재조합)_(0.1g/4mL)
    # 옵디보주100mg(니볼루맙,유전자재조합)_(0.1g/10mL)
    # 티쎈트릭주(아테졸리주맙)_(1.2g/20mL)
    initial_product_codes = ['655501901', '050400011', '645001441']
    initial_options = [
        o for o in product_selector_options
        if o['value'] in initial_product_codes
    ]

    layout = [
        html.Div(id='myContent', className='container', children=[
            html.H1('Drug Upper-bound Price Time Series in South Korea | 대한민국 약품 상한 가격 변동 시각화'),
            html.Br(),
            html.H2(f'Choose products | 제품명을 선택하세요 ({number_of_products}개 제품 선택 가능: {max_date} 데이터 기준)'),
            dcc.Dropdown(
                id='product-selector',
                options=initial_options,
                value=initial_product_codes,
                multi=True,
                placeholder="Type and select products: For example, 키트루다, 옵디보, 티쎈트릭, etc.",
            ),
            dcc.Graph(
                id='price-time-series',
                figure=draw_price_time_series(initial_product_codes)
            ),
            html.A(
                id='export-series',
                href=f'/download-series/?product-code-list={"|".join(initial_product_codes)}',
                target='_blank',
                children=[
                    html.Button(
                        id='button-download-series',
                        className='button',
                        type='button',
                        children=['Download time series of selected products']
                    )
                ]
            ),
            html.A(
                id='export-product-table',
                href=f'/download-product-table/',
                target='_blank',
                children=[
                    html.Button(
                        id='button-download-table',
                        className='button',
                        type='button',
                        children=['Download product info table (All)']
                    )
                ]
            ),
            dash_table.DataTable(
                id='product-info-table',
                columns=[
                    {"name": i, "id": i.replace(' ', '_')}
                    for i in df_product.columns
                ],
                data=get_records(initial_product_codes),
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            ),
            html.Br(),
            html.Div(children=[
                html.Ul(children=[
                    html.Li(children=[
                        'Data Source:',
                        html.A(
                            href='https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA030014050000',
                            children=['건강보험심사평가원 (HIRA) 약제급여목록표'])
                    ]),
                    html.Li(children=[
                        'Author:',
                        html.A(
                            href='https://www.linkedin.com/in/danielyounghokim/',
                            children=['Daniel Y Kim, PhD'])
                    ]),
                    html.Li(children=[
                        'Source Code:',
                        html.A(
                            href='https://github.com/danielykim/kr-drug-price-dashboard',
                            children=['GitHub repository'])
                    ]),
                ])
            ])
        ])
    ]
    return layout


layout = html.Section(
    className='section',
    children=initialize_layout()
)
