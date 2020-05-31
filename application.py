import io

import pandas as pd
import dash

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from flask import Flask, send_file, request

import tools

import layout
import config
import index_string



# Variable name below should be `application` for AWS Elastic Beanstalk
application = Flask(__name__)

@application.route('/download-series/')
def download_series():
    product_code_list = request.args.get('product-code-list').split('|')

    strIO = io.BytesIO()

    if len(product_code_list) >= 1 and product_code_list[0] != '':
        df = layout.df_price.loc[product_code_list]

        excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")

        df.to_excel(excel_writer, sheet_name="Sheet1")

        excel_writer.save()

        binary_data = strIO.getvalue()

        filename = 'selected-products.xlsx'
    else:
        filename = 'no-product.txt'

        strIO.write(b'\n')

        binary_data = strIO.getvalue()

    strIO.seek(0)

    return send_file(
        strIO,
        attachment_filename=filename,
        as_attachment=True
    )


@application.route('/download-product-table/')
def download_product_table():
    strIO = io.BytesIO()

    df = layout.df_product

    max_date = layout.max_date

    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")

    df.to_excel(excel_writer, sheet_name="Sheet1")

    excel_writer.save()

    binary_data = strIO.getvalue()

    filename = f'product-table-{max_date}.xlsx'

    strIO.seek(0)

    return send_file(
        strIO,
        attachment_filename=filename,
        as_attachment=True
    )



dashapp = dash.Dash(
    __name__,
    server=application,
    url_base_pathname='/',
    meta_tags=config.META_TAGS,
    external_stylesheets=config.external_stylesheets,
    suppress_callback_exceptions=True
)

dashapp.index_string = index_string.index_string

dashapp.title = 'KR Drug Price Dashboard'
dashapp.layout = layout.layout

# https://dash.plotly.com/dash-core-components/dropdown
@dashapp.callback(
    dash.dependencies.Output("product-selector", "options"),
    [dash.dependencies.Input("product-selector", "search_value")],
    [dash.dependencies.State("product-selector", "value")],
)
def update_multi_options(search_value, value):
    if not search_value:
        raise PreventUpdate

    return [
        o
        for o in layout.product_selector_options
        if search_value in o["label"] or o["value"] in (value or [])
    ]


@dashapp.callback(
    [
        Output('price-time-series', 'figure'),
        Output('product-info-table', 'data'),
        Output('export-series', 'href'),
    ],
    [
        Input('product-selector', 'value'),
    ]
)
def update(product_code_list):
    fig = layout.draw_price_time_series(product_code_list)
    tab = layout.get_records(product_code_list)

    if type(product_code_list) is list:
        joined_code_list = "|".join(product_code_list)
    else:
        joined_code_list = ''

    href = f'/download-series/?product-code-list={joined_code_list}'

    return fig, tab, href



if __name__ == '__main__':
    application.run(debug=False)
