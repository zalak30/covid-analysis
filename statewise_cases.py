# storing and analysis
import pandas as pd

# visualization
import plotly.graph_objs as go
import plotly.express as px
import plotly

# hide warnings
import warnings

warnings.filterwarnings('ignore')

# read csv file
table = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
table.drop(table.index[0], inplace=True)
# print("\ntable columns\n", table.columns)
table.sort_values(by='Confirmed', inplace=True, ascending=False)
# print("\ntable\n", table.head())

table['Active Cases'] = table['Confirmed'] - table['Deaths'] - table['Recovered']
table['Recovered Rate'] = round((table['Recovered'] * 100) / table['Confirmed'], 2)
table['Death Rate'] = round((table['Deaths'] * 100) / table['Confirmed'], 2)
table['Active Cases Rate'] = round((table['Active Cases'] * 100) / table['Confirmed'], 2)

# bar graph(top 16 state with most confirmed cases)
x = table['State'][:16]

fig = go.Figure()
fig.add_trace(go.Bar(x=x, y=table['Confirmed'], name='Confirmed', marker_color='slateblue'))
fig.add_trace(go.Bar(x=x, y=table['Recovered'], name='Recovered', marker_color='mediumseagreen'))
fig.add_trace(go.Bar(x=x, y=table['Deaths'], name='Deaths', marker_color='firebrick'))
fig.update_layout(barmode='overlay', title='Statewise cases in India', height=400, showlegend=False)
fig.update_xaxes(tickangle=-45)

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
                    label="Confirmed",
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
            y=1.23,
            yanchor="top"
        ),
    ]
)

plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/state wise cases in india.html', auto_open=False)

# bar graph(state wise death and recovery rate)
x = table['State'][:16]

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=table['Active Cases Rate'], name='Active Cases Rate',
                         line=dict(color='slateblue', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=x, y=table['Death Rate'], name='Death Rate',
                         line=dict(color='firebrick', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=x, y=table['Recovered Rate'], name='Recovered Rate',
                         line=dict(color='mediumseagreen', width=2),
                         line_shape='spline'))

fig.update_layout(title='State wise death and recovered rate', height=400, showlegend=False)

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
                    args=[{"visible": [False, False, True]}],
                    label="Recoverey rate",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False]}],
                    label="Death rate",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False, False]}],
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
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/state wise death and recovery rate.html',
                    auto_open=False)

# pie chart
fig = px.pie(table, values='Confirmed', names='State', title='State wise percentage of confirmed cases in india', height=400,
             hole=.2, color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/State wise confirmed cases in india.html',
                    auto_open=False)

# pie chart
state_district = pd.read_csv("https://api.covid19india.org/csv/latest/district_wise.csv")
state_district.drop(['State_Code', 'SlNo', 'District_Notes', 'Last_Updated', 'Delta_Deceased', 'Delta_Recovered',
                     'Delta_Active', 'Delta_Confirmed', 'District_Key'], axis=1, inplace=True)
gujarat = state_district[state_district['State'] == 'Gujarat'].sort_values(by='Confirmed', ascending=False).head(15)

fig = px.pie(state_district, values=gujarat['Confirmed'],
             names=gujarat['District'],
             color_discrete_sequence=px.colors.sequential.RdBu,
             title='District wise confirmed cases in Gujarat')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/District wise confirmed cases in Gujarat.html',
                    auto_open=False)



fig = go.Figure()
x = gujarat['District']
fig.add_trace(go.Bar(x=x, y=gujarat['Active'],
             name='Active cases', marker_color='slateblue'))
fig.add_trace(go.Bar(x=x, y=gujarat['Recovered'],
             name='Recovered', marker_color='mediumseagreen'))
fig.add_trace(go.Bar(x=x, y=gujarat['Deceased'],
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

fig.update_layout(title='Numbers in different district of Gujarat',
                  barmode='overlay', height=400, showlegend=False)
fig.update_xaxes(tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Numbers in different district of Gujarat.html', auto_open=False)
print("successfully statewise_cases.py")