import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc # for Graphs
import dash_html_components as html
import dash_table
import pandas as pd
# for date-Slider
import math
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load the data from remote file 
toc_url = 'https://haverford.box.com/shared/static/jwp9pd68ffl7tneh9hjob943ikcqg6x4.csv'
df = pd.read_csv(toc_url, error_bad_lines=False,)


# Load styles
#css_url = 'https://codepen.io/IvanNieto/pen/bRPJyb.css'
css_url = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
css_bootstrap_url = 'https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
app.css.append_css({
    "external_url": [css_bootstrap_url, css_url],
})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# for date-Slider
uniqueYear = set()
for date in df['year'].unique():
    uniqueYear.add(int(date))
    
uniqueYear = sorted(uniqueYear)

yearDict = {}
keys = range(len(uniqueYear))
for i in keys:
    yearDict[i] = uniqueYear[i]

#available_indicators = df['Indicator Name'].unique()


# Layout

app.layout = html.Div(children=[
    html.H1(
        children='Journals',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'margin-top': 10,
        }
    ),

    html.H6(
        children='A research dashboard for journalnyi zal',
        style={
        'textAlign': 'center',
        'color': colors['text'],
        'padding': 5,
    }),

    html.Div(
        className='container-fluid',
        children=[
            html.Div(
                # Slider
                className='container',
                children=[
                    html.Div(
                        children=[
                            dcc.Slider(
                                id='slider',
                                min=0,
                                max=len(uniqueYear)-1,
                                marks={str(k):str(v) for k, v in yearDict.items()},
                                # min=min(uniqueYear),
                                # max=max(uniqueYear),
                                # marks={str(date):str(date) for date in uniqueYear},
                                value=len(uniqueYear),
                            )
                        ]
                    ),
                ],
                style={
                    'margin-bottom':'50px',
                }
            ),

            html.Div(
                className='row',
                children=[
                    dcc.Graph(
                        # map
                        className='col-sm-6',
                        id='graph-with-slider',
                    ),

                    html.Div(
                        # Data table
                        className='col-sm-6',
                        id='datatable',
                    ),
                ]
            )
        ]
    ),
])

@app.callback(
    Output('datatable', 'children'),
    [Input('slider', 'value')])
def update_table(value):
    print("value:",value)
    
    newdf = df[df.year.isin(list(uniqueYear[:value+1]))]

    table = dash_table.DataTable(
        id='table',
        data=newdf.to_dict("rows"),
        columns=[{"name": i, "id": i} for i in newdf.columns], #if i not in ["order", "journal", "year", "issue","category","author","link","title","genre"]],
        n_fixed_rows=1,
        sorting=True,
        filtering=True,
        pagination_mode="fe",
                pagination_settings={
                    "displayed_pages": 2,
                    "current_page": 0,
                    "page_size": 35,
                },
                navigation="page",
        style_cell={
            'whiteSpace': 'normal',
            'padding': '5px',
            'minWidth': '150px',
            'width': '150px',
            'maxWidth': '150px',
            'textAlign': 'left',
        },
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_table={
            'overflowX': 'scroll', # Horizontal scroll
            'maxHeight': '500',
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
    )
    return table

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('slider', 'value')])
def update_figure(value):
    filtered_df = df[df.year.isin(list(uniqueYear[:value+1]))]
    year = filtered_df['year'].value_counts().to_frame()

    traces = []
    for i in filtered_df.journal.unique():
            df_by_continent = filtered_df[filtered_df['journal'] == i]
            traces.append(go.Scatter(
                x=df_by_continent['author'],
                y=df_by_continent.count(),
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))
    

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Author'},
            yaxis={'title': 'Count',},
            legend={'x': 1, 'y': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
