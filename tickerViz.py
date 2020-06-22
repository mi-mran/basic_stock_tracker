import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from datetime import datetime
import pandas as pd
import pandas_datareader.data as web
import quandl

app = dash.Dash()

euronext = pd.read_csv('Euronext_Equities_2019-11-27.csv')
euronext.set_index('Symbol', inplace = True)

options = []

for tic in euronext.index:
	options.append({'label':'{} {}'.format(tic, euronext.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
						html.H1('Stock Ticker Dashboard'),
						html.Div([
								html.H3('Stock Input:', style = {'paddingRight': '30px'}),
								dcc.Dropdown(id = 'my_stock_picker',
									options = options,
									value = ['ABN'],
									multi = True)
								],
								style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%'}),

						html.Div([
								html.H3('Select a start and end date:'),
								dcc.DatePickerRange(id = 'my_date_picker',
													min_date_allowed = datetime(2010, 1, 1),
													max_date_allowed = datetime.today(),
													start_date = datetime(2019, 1, 1),
													end_date = datetime.today())
							],
							style = {'display': 'inline-block'}),

						html.Div([
								html.Button(id = 'submit_button',
											n_clicks = 0,
											children = 'Submit',
											style = {'fontSize': 24, 'marginLeft': '30px'})
							],
							style = {'display': 'inline-block'}),
						
						dcc.Graph(id = 'my_graph',
									figure = {'data': [
												{'x': [1, 2], 'y': [3, 1]}
												],
											'layout': {'title': 'Default Title'}
											},
									config = {'displaylogo': False},
									)
	])

@app.callback(Output('my_graph', 'figure'),
			[Input('submit_button', 'n_clicks')],
			[State('my_stock_picker', 'value'),
			State('my_date_picker', 'start_date'),
			State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):

	start = datetime.strptime(start_date[:10], '%Y-%m-%d')

	end = datetime.strptime(end_date[:10], '%Y-%m-%d')

	auth_tok = "###"

	traces = []

	for tic in stock_ticker:
		df = quandl.get("EURONEXT/{}".format(tic), trim_start = start, trim_end = end, authtoken = auth_tok)

		traces.append({'x': df.index, 'y': df['Last'], 'name': tic})

	updated_figure = {'data': traces,
					'layout': {'title': stock_ticker}
					}

	return updated_figure

if __name__ == '__main__':
	app.run_server(debug = False)