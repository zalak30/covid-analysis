# storing and analysis
import pandas as pd
import plotly
from datetime import date
from datetime import timedelta

# visualization
import plotly.graph_objs as go

# hide warnings
import warnings

warnings.filterwarnings('ignore')

# read csv file
table = pd.read_csv("https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv")

# print("\n table columns\n", table.columns)

# drop NaN values from 'state' column
table.dropna(subset=['State'], inplace=True)
table['Updated On'] = pd.to_datetime(table['Updated On'])

# Get today's date
today = date.today()
# Yesterday date
yesterday = today - timedelta(days=2)
yesterday = yesterday.strftime('%d/%m/%y')
tested = table[table['Updated On'] == yesterday][['State', 'Updated On', 'Total Tested', 'Positive']]
# print(tested)
# create new column percentage of positive cases
tested['positive cases rate'] = round((tested['Positive'] * 100) / tested['Total Tested'], 2)
tested.sort_values(by='Total Tested', ascending=False, inplace=True)
tested.reset_index(inplace=True, drop=True)
# print(tested)

# create bar chart (tested vs positive)
x = tested['State'][:16]
fig = go.Figure()
fig.add_trace(go.Bar(x=x, y=tested['Total Tested'], name='total tested', text=tested['positive cases rate'],
                     textposition='outside', marker_color='slateblue'))
fig.add_trace(go.Bar(x=x, y=tested['Positive'], name='positive', marker_color='firebrick'))

fig.update_layout(barmode='overlay', title='Tested vs positive cases state wise in india', height=400,
                  legend=dict(
                      x=0.1,
                      y=1.15,
                      orientation='h',
                      font=dict(
                          family="sans-serif",
                          size=10,
                          color="black"
                      ),
                  ),
                  )

fig.update_xaxes(nticks=20, rangeslider_visible=False, tickangle=-45)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/tested vs positive cases state wise in india',
                    auto_open=False)
print("successfully statewise_tested.py")
