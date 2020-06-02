# import libraries
import pandas as pd
# visualization
import plotly.graph_objs as go
import plotly
import datetime as dt

# hide warnings
import warnings
warnings.filterwarnings('ignore')

# read csv file
table = pd.read_csv("https://api.covid19india.org/csv/latest/case_time_series.csv")
total_tested = pd.read_csv("https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv")
# print(total_tested.head())
# print(total_tested.columns)

# fill empty value with '0' in 'Total Samples Tested' and 'Total Positive Cases' columns
# total_tested['Total Samples Tested'] = total_tested['Total Samples Tested'].fillna(0).astype(int)
# total_tested['Total Positive Cases'] = total_tested['Total Positive Cases'].fillna(0)
#
# # update date format of 'Date' column and remove timestamp from date
# total_tested['Date'] = total_tested['Update Time Stamp'].apply(lambda x: dt.datetime.strptime(x, '%d/%m'))
# total_tested['Date'] = total_tested['Update Time Stamp'].apply(lambda x: x.split()[0])
#
# # we have multiple rows with same date so we drop same and keep only last date's row of same dates
# total_tested.drop_duplicates(['Date'], keep='last', inplace=True)
#
# # create DataFrame
# tested = pd.DataFrame(total_tested[['Date', 'Total Samples Tested', 'Total Positive Cases']]).reset_index(drop=True)
#
# # now we drop rows which has '0' values , from columns 'Total Samples Tested' and 'Total Positive Cases'
# tested.drop(tested.index[list(tested[tested['Total Samples Tested'] == 0].index)], inplace=True)
# tested.reset_index(inplace=True, drop=True)
# tested.drop(tested.index[list(tested[tested['Total Positive Cases'] == 0].index)], inplace=True)
# tested.reset_index(inplace=True, drop=True)
#
# # convert 'Total Positive Cases' to int from string
# tested['Total Positive Cases'] = tested['Total Positive Cases'].str.replace(',', '').astype(int)
#
# """         we have total number of 'tested number' , so get individual for each day
#             we have to subtract today's number from next day number
# """
# # create empty list 'Daily_Samples_Tested' and 'Daily_Positive_Cases' numbers
# Daily_Samples_Tested = []
# Daily_Positive_Cases = []
# Date = []
#
# for i in tested.index:
#     if i == 0:
#         Date.append(tested['Date'][i])
#         Daily_Samples_Tested.append(tested['Total Samples Tested'][i])
#         Daily_Positive_Cases.append(tested['Total Positive Cases'][i])
#     else:
#         Date.append(tested['Date'][i])
#         Daily_Samples_Tested.append(tested['Total Samples Tested'][i]-tested['Total Samples Tested'][i-1])
#         Daily_Positive_Cases.append(tested['Total Positive Cases'][i]-tested['Total Positive Cases'][i-1])
#
# # create DataFrame which has 'daily tested' and 'daily positive cases' numbers
# daily = pd.DataFrame(zip(Date, Daily_Samples_Tested, Daily_Positive_Cases),
#                      columns=['Date', 'Daily Samples Tested', 'Daily Positive Cases'])

#bar graph(total tested vs total positive cases)
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=daily['Date'], y=daily['Daily Samples Tested'], name='Daily Tested',
#                          line_shape='spline', mode='lines+markers'))
# fig.add_trace(go.Scatter(x=daily['Date'], y=daily['Daily Positive Cases'], name='Daily Positive',
#                          line_shape='spline', mode='lines+markers'))
# fig.update_layout(barmode='stack', title='Daily tested vs daily positive cases in India', height=400,
#                   legend=dict(
#                       x=0.1,
#                       y=1.15,
#                       orientation='h',
#                       font=dict(
#                           family="sans-serif",
#                           size=10,
#                           color="black"
#                       ),
#                   ),
# )
# fig.update_xaxes(nticks=20, rangeslider_visible=False, tickangle=-45)
# plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Daily tested vs daily positive cases in India.html', auto_open=False)

# bar graph(total tested vs total positive cases)
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=tested['Date'], y=tested['Total Samples Tested'], name='Total Tested',
#                          line_shape='spline', mode='lines+markers'))
# fig.add_trace(go.Scatter(x=tested['Date'], y=tested['Total Positive Cases'], name='Total Positive',
#                          line_shape='spline', mode='lines+markers'))
# fig.update_layout(barmode='stack', title='Total tested vs total positive cases in India', height=400,
# legend = dict(
#     x=0.1,
#     y=1.15,
#     orientation='h',
#     font=dict(
#         family="sans-serif",
#         size=10,
#         color="black"
#     ),
# ),
# )
# fig.update_xaxes(nticks=20, rangeslider_visible=False, tickangle=-45)
# plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Total tested vs total positive cases in India.html', auto_open=False)

# bar graph(daily cases)
fig = go.Figure()
fig.add_trace(go.Scatter(x=table['Date'], y=table['Daily Confirmed'], name='Daily Confirmed',
                         line=dict(color='slateblue', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=table['Date'], y=table['Daily Deceased'], name='Daily Deceased',
                         line=dict(color='firebrick', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=table['Date'], y=table['Daily Recovered'], name='Daily Recovered',
                         line=dict(color='mediumseagreen', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(
    x=['21 March ', '15 April ', '04 May ', '18 May'],
    y=[4000, 4000, 4000, 4000],
    text=["Lockdown 1.0",
          "Lockdown 2.0 ",
          "Lockdown 3.0",
          "Lockdown 4.0"],
    mode="text",
))

# Add shapes
fig.add_shape(
        # Rectangle reference to the axes
            type="line",
            xref="x",
            yref="y",
            x0='21 March ',
            y0=0,
            x1='21 March ',
            y1=4000,
            line=dict(
                color="RoyalBlue",
                width=1,
                dash='dot'
            ),
        )

fig.add_shape(
        # Rectangle reference to the axes
            type="line",
            xref="x",
            yref="y",
            x0='15 April ',
            y0=0,
            x1='15 April ',
            y1=4000,
            line=dict(
                color="RoyalBlue",
                width=1,
            ),
        )

fig.add_shape(
        # Rectangle reference to the axes
            type="line",
            xref="x",
            yref="y",
            x0='04 May ',
            y0=0,
            x1='04 May ',
            y1=4000,
            line=dict(
                color="RoyalBlue",
                width=1,
                dash='dot'
            ),
        )

fig.add_shape(
        # Rectangle reference to the axes
            type="line",
            xref="x",
            yref="y",
            x0='18 May ',
            y0=0,
            x1='18 May ',
            y1=4000,
            line=dict(
                color="RoyalBlue",
                width=1,
                dash='dot'
            ),
        )

max_confirmed = [
    dict(
        x=list(table[table['Daily Confirmed'] == table['Daily Confirmed'].max()]['Date'])[0],
        y=table['Daily Confirmed'].max(),
        xref="x",
        yref="y",
        text="Highest Daily Increase",
        showarrow=True,
        arrowhead=7
    )]
max_deaths = [dict(
        x=list(table[table['Daily Deceased'] == table['Daily Deceased'].max()]['Date'])[0],
        y=table['Daily Deceased'].max(),
        xref="x",
        yref="y",
        text="Highest Daily Deceased",
        showarrow=True,
        arrowhead=7
    )]
max_recoveries = [dict(
        x=list(table[table['Daily Recovered'] == table['Daily Recovered'].max()]['Date'])[0],
        y=table['Daily Recovered'].max(),
        xref="x",
        yref="y",
        text="Highest Daily Recoveries",
        showarrow=True,
        arrowhead=7
    )]

fig.update_layout(barmode='stack', title='Daily cases in India', height=400, showlegend=False)

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

fig.update_xaxes(nticks=20, rangeslider_visible=False, tickangle=-45)

plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Daily cases in India.html', auto_open=False)

# bar graph(total cases)
fig = go.Figure()
fig.add_trace(go.Scatter(x=table['Date'], y=table['Total Confirmed'], name='Total Confirmed',
                         line=dict(color='slateblue', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=table['Date'], y=table['Total Deceased'], name='Total Deceased',
                         line=dict(color='firebrick', width=2),
                         line_shape='spline'))
fig.add_trace(go.Scatter(x=table['Date'], y=table['Total Recovered'], name='Total Recovered',
                         line=dict(color='mediumseagreen', width=2),
                         line_shape='spline'))
fig.update_layout(barmode='stack', title='Total cases in India', height=400, showlegend=False)
fig.update_xaxes(nticks=20, rangeslider_visible=False, tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Total cases in India.html', auto_open=False)
print("successfully time_analysis.py")
