# import libraries
import pandas as pd

# visualization
import plotly.graph_objects as go
import plotly

import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import pandas as pd

# Data Scrape
async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN:en')

    html = await page.evaluate('''() => {
        return document.querySelector('body').innerHTML;
    }''')

    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    table_html = soup.find('table', attrs={'class': 'pH8O4c'})
    # print(table_html)

    rows = table_html.find_all('tr')
    # we got html objects of whole table

    table_list = []
    for row in rows:
        columns_html = row.find_all(['td', 'th'])
        columns = []
        for col_html in columns_html:
            columns.append(col_html.text.strip())
        table_list.append(columns)
    # print(table_list)

    # convert html to dataframe
    data = pd.DataFrame(table_list)
    header = data.iloc[0]
    table = pd.DataFrame(data.values[1:], columns=header)
    # print(table.columns)
    # print(table.head(2))

    # change data type
    table_int = table[['Confirmed', 'Recovered', 'Deaths', 'Cases per 1 million people']]\
        .apply(lambda x: x.replace({',': '', '—': '0','No data': '0'}, regex=True)).astype(float)

    # print(table_int.dtypes)

    table = pd.concat([table['Location'], table_int], axis=1)
    # print("\nprint head of table\n",table.head())
    # print("\nprint type of table\n",table.dtypes)

    # add column of active cases
    table['Active cases'] = table['Confirmed'] - table['Deaths'] - table['Recovered']
    table['Recovered rate'] = round((table['Recovered'] * 100) / table['Confirmed'], 2)
    table['Death rate'] = round((table['Deaths'] * 100) / table['Confirmed'], 2)
    table['Active cases rate'] = round((table['Active cases'] * 100) / table['Confirmed'], 2)
    # print("\nprint table\n", table.head())
    # print("\nprint table shape\n", table.shape)


    table.to_csv(r'corona_worldwide.csv', index=False)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

# read csv file
worldwide = pd.read_csv("corona_worldwide.csv")
worldwide.drop(worldwide.index[0], inplace=True)

# top 20 countries with most confirmed cases
worldwide_sort = worldwide.sort_values(by='Confirmed', ascending=False)
worldwide_top_20 = worldwide_sort.head(20)

# bar chart
x = worldwide_top_20['Location']
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=worldwide_top_20['Recovered rate'], name='Recovery rate',
                         line=dict(color='mediumseagreen', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=x, y=worldwide_top_20['Death rate'], name='Death rate',
                         line=dict(color='firebrick', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=x, y=worldwide_top_20['Active cases rate'], name='Active cases rate',
                         line=dict(color='slateblue', width=2),
                         line_shape='spline'))


recovery_annotations = [
    dict(
        x=list(worldwide_top_20[worldwide_top_20['Recovered rate'] == worldwide_top_20['Recovered rate'].max()]['Location'])[0],
        y=worldwide_top_20['Recovered rate'].max(),
        xref="x",
        yref="y",
        text="Highest Recovery Rate",
        showarrow=True,
        arrowhead=7
    )]
active_annotations = [
    dict(
        x=list(worldwide_top_20[worldwide_top_20['Active cases rate'] == worldwide_top_20['Active cases rate'].max()]['Location'])[0],
        y=worldwide_top_20['Active cases rate'].max(),
        xref="x",
        yref="y",
        text="Highest Active Cases Rate",
        showarrow=True,
        arrowhead=7
    )]
death_annotations = [
    dict(
        x=list(worldwide_top_20[worldwide_top_20['Death rate'] == worldwide_top_20['Death rate'].max()]['Location'])[0],
        y=worldwide_top_20['Death rate'].max(),
        xref="x",
        yref="y",
        text="Highest Death Rate",
        showarrow=True,
        arrowhead=7
    )]
fig.update_layout(title='Recoveries and death rate in top 20 countries with most confirmed cases', height=400,
                  showlegend=False)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"visible": [True, True, True]}],
                    label="All",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False, False]},
                          {"annotations": recovery_annotations}],
                    label="Recoverey rate",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False]},
                          {"annotations": death_annotations}],
                    label="Death rate",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, True]},
                          {"annotations": active_annotations}],
                    label="Active cases rate",
                    method="update"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.005,
            xanchor="left",
            y=1.23,
            yanchor="top"
        ),
    ]
)


fig.update_xaxes(tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Cases rate in the world.html', auto_open=False)


# bar chart of top 20 countries with most confirmed cases
fig = go.Figure()
fig.add_trace(go.Bar(x=worldwide_top_20['Location'], y=worldwide_top_20['Confirmed'],
                     text=worldwide_top_20['Confirmed'],
                     marker_color='slateblue'))
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(title='Top 20 countries with most confirmed cases')
fig.update_xaxes(tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Top 20 countries with most confirmed cases.html', auto_open=False)


# bar chart of numbers in top 20 countries with most confirmed cases top 20 countries with most confirmed cases
fig = go.Figure()
fig.add_trace(go.Bar(x=worldwide_top_20['Location'], y=worldwide_top_20['Active cases'],
             name='Active cases', marker_color='slateblue'))
fig.add_trace(go.Bar(x=worldwide_top_20['Location'], y=worldwide_top_20['Recovered'],
             name='Recovered', marker_color='mediumseagreen'))
fig.add_trace(go.Bar(x=worldwide_top_20['Location'], y=worldwide_top_20['Deaths'],
             name='Deaths', marker_color='firebrick'))

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"visible": [True, True, True]}],
                    label="All",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False, False]}],
                    label="Active cases",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False]}],
                    label="Recovered",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, True]}],
                    label="Deaths",
                    method="update"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.005,
            xanchor="left",
            y=1.20,
            yanchor="top"
        ),
    ]
)

fig.update_layout(title='Numbers in top 20 countries with most confirmed cases',
                  barmode='overlay', height=400, showlegend=False)
fig.update_xaxes(tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Numbers in top 20 countries with most confirmed cases.html', auto_open=False)
print("successfully worldwide.py")
