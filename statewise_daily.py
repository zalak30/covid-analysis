import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly

daily = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
# print(daily.columns)

date = daily['Date'].unique()
confirmed = list(daily[daily['Status'] == 'Confirmed']['GJ'])
recovered = list(daily[daily['Status'] == 'Recovered']['GJ'])
deceased = list(daily[daily['Status'] == 'Deceased']['GJ'])

gujarat = pd.DataFrame(zip(date, confirmed, recovered, deceased),
                       columns=['Date', 'Confirmed', 'Recovered', 'Deceased'])

x = gujarat['Date']
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=gujarat['Confirmed'], name='Confirmed',
                         line=dict(color='slateblue', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=x, y=gujarat['Deceased'], name='Deceased',
                         line=dict(color='firebrick', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=x, y=gujarat['Recovered'], name='Recovered',
                         line=dict(color='mediumseagreen', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(
    x=['21-Mar-20', '15-Apr-20', '04-May-20', '18-May-20'],
    y=[400, 400, 400, 400],
    text=["Lockdown 1.0",
          "Lockdown 2.0",
          "Lockdown 3.0",
          "Lockdown 4.0"],
    mode="text",
))

# Add shapes
fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0='21-Mar-20',
            y0=0,
            x1='21-Mar-20',
            y1=400,
            line=dict(
                color="RoyalBlue",
                width=1,
                dash='dot'
            ),
        )

fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0='15-Apr-20',
            y0=0,
            x1='15-Apr-20',
            y1=400,
            line=dict(
                color="RoyalBlue",
                width=1,
                dash='dot'
            ),
        )

fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0='04-May-20',
            y0=0,
            x1='04-May-20',
            y1=400,
            line=dict(
                color="RoyalBlue",
                width=1,
            ),
        )

fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0='18-May-20',
            y0=0,
            x1='18-May-20',
            y1=400,
            line=dict(
                color="RoyalBlue",
                width=1,
            ),
        )

max_confirmed = [
    dict(
        x=list(gujarat[gujarat['Confirmed'] == gujarat['Confirmed'].max()]['Date'])[0],
        y=gujarat['Confirmed'].max(),
        xref="x",
        yref="y",
        text="Highest Daily Increase",
        showarrow=True,
        arrowhead=7
    )]
max_deaths = [dict(
        x=list(gujarat[gujarat['Deceased'] == gujarat['Deceased'].max()]['Date'])[0],
        y=gujarat['Deceased'].max(),
        xref="x",
        yref="y",
        text="Highest Daily Deaths",
        showarrow=True,
        arrowhead=7
    )]
max_recoveries = [dict(
        x=list(gujarat[gujarat['Recovered'] == gujarat['Recovered'].max()]['Date'])[0],
        y=gujarat['Recovered'].max(),
        xref="x",
        yref="y",
        text="Highest Daily Recoveries",
        showarrow=True,
        arrowhead=7
    ),
]

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
                    args=[{"visible": [False, False, True]},
                          {"annotations": max_recoveries}],
                    label="Recovered",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False]},
                          {"annotations": max_deaths}],
                    label="Deaths",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False, False]},
                          {"annotations": max_confirmed}],
                    label="Confirmed",
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

fig.update_layout(title='Daily cases in Gujarat', height=400, showlegend=False)

fig.update_xaxes(nticks=20, tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/daily cases in Gujarat.html', auto_open=False)
print("successfully statewise_daily.py")
