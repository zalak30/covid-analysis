# import libraries
import pandas as pd

# visualization
import plotly.express as px
import plotly

# hide warnings
import warnings
warnings.filterwarnings('ignore')

# read csv file
table = pd.read_csv("https://api.covid19india.org/csv/latest/raw_data.csv")

# let's replace NaN values with 'not available'
table['Notes'].fillna('not available', inplace=True)

# convert all string of notes in lower letter so we can find same location if any
table['Notes'] = table['Notes'].apply(lambda x: x.lower())

# we got same location with different style and spelling, so we replace them by unique name for accuracy in analysis
# get index of all usa passengers
usa = table[table['Notes'].str.contains('us|new york')].index
# change different sentences used for dubai passengers to 'travelled from usa'
for i in usa:
    table['Notes'].replace(table['Notes'][i], value='travelled from usa', inplace=True)

# get index of all middle east passengers
me = table[table['Notes'].str.contains('saudi arabia|qatar|abhudhabi|abu dhabi|oman|travelled from sharjah|travelle from middle east|uae')].index
# change different sentences used for dubai passengers to 'travelled from middle east'
for i in me:
    table['Notes'].replace(table['Notes'][i], value='travelled from middle east', inplace=True)

# get index of all uk passengers
uk = table[table['Notes'].str.contains('uk|united kingdom|london')].index
# change different sentences used for dubai passengers to 'travelled from uk'
for i in uk:
    table['Notes'].replace(table['Notes'][i], value='travelled from uk', inplace=True)

# get index of all dubai passengers
dubai = table[table['Notes'].str.contains('dubai')].index
# change different sentences used for dubai passengers to 'travelled from dubai'
for i in dubai:
    table['Notes'].replace(table['Notes'][i], value='travelled from dubai', inplace=True)

# get index of all contact transmission
contact = table[table['Notes'].str.contains('contact|co-passenger|contracted|locally transmitted|working with')].index
# change different sentences used for contact transmission to 'contact transmission'
for i in contact:
    table['Notes'].replace(table['Notes'][i], value='contact transmission', inplace=True)

# get index of all iran passengers
iran = table[table['Notes'].str.contains('iran')].index
# change different sentences used for dubai passengers to 'travelled from iran'
for i in iran:
    table['Notes'].replace(table['Notes'][i], value='travelled from iran', inplace=True)

# get index of all philippines passengers
philippines = table[table['Notes'].str.contains('philippines')].index
# change different sentences used for philippines passengers to 'travelled from philippines'
for i in philippines:
    table['Notes'].replace(table['Notes'][i], value='travelled from philippines', inplace=True)

# get index of all italy passengers
italy = table[table['Notes'].str.contains('italy')].index
# change different sentences used for dubai passengers to 'travelled from iran'
for i in italy:
    table['Notes'].replace(table['Notes'][i], value='travelled from italy', inplace=True)

# get index of all spain passengers
spain = table[table['Notes'].str.contains('spain')].index
# change different sentences used for dubai passengers to 'travelled from spain'
for i in spain:
    table['Notes'].replace(table['Notes'][i], value='travelled from spain', inplace=True)

# get index of all details awaited patients
details = table[table['Notes'].str.contains('details awaited|further details not|details yet to recieve|'
    'the detailed investigation is under process|no info')].index
# change different sentences used for dubai passengers to 'details awaited'
for i in details:
    table['Notes'].replace(table['Notes'][i], value='details awaited', inplace=True)

# get index of all details of delhi event
delhi = table[table['Notes'].str.contains('delhi event|travelled to delhi|attended delhi conference|delhi conference|indonesia|'
'Indonesian|Resident of Paheli Chouki, HYD;|visited delhi|travel history of delhi|travel history to delhi')].index
for i in delhi:
    table['Notes'].replace(table['Notes'][i], value='delhi event', inplace=True)

# get index of all patients who got infected by family member
family_member = table[table['Notes'].str.contains('family member|daughter|son|father|related previous patient|mother|'
    'wife|relative of|aunt|uncle|parents|brother-in-law|sister-in-law|related to|brother|sister|sister in law|'
     'roommate|friends|family|relatives|neighbour|friend|cook|tenant')].index
# change different sentences used for family to 'family member'
for i in family_member:
    table['Notes'].replace(table['Notes'][i], value='family member', inplace=True)

# get index of all patients from canada
canada = table[table['Notes'].str.contains('canada')].index
# change different sentences used for indonesian citizen to 'canada'
for i in canada:
    table['Notes'].replace(table['Notes'][i], value='travel from canada', inplace=True)

# get index of all sari patients
sari = table[table['Notes'].str.contains('sari')].index
# change different sentences used sari
for i in sari:
    table['Notes'].replace(table['Notes'][i], value='sari', inplace=True)

table['Notes'].replace(to_replace=['they work at a bakery in jawaharpur, dera bassi'], value='bakery in jawaharpur', inplace=True)

transmission_type = pd.DataFrame(table['Notes'].value_counts())
# print(transmission_type)

# drop rows 'details awaited' and 'not available'
transmission_type.drop(transmission_type.index[[0, 1]], inplace=True)

# reset index and give names to column
transmission_type.reset_index(inplace=True)
transmission_type.rename(columns={'index': 'type', 'Notes': 'patients'}, inplace=True)

# check the reason for only one person got infect
other_number = transmission_type[(transmission_type['patients'] == 1)]['patients'].count()

transmission_type = transmission_type[(transmission_type['patients'] > 1)]
# # we got (other_number) single reason to got infected, so we will add 'other' type for (other_number) patients
other = pd.DataFrame({'type': ['other'],
                      'patients': other_number})
transmission_type = transmission_type.append(other, ignore_index=True)
total_patients = transmission_type['patients'].sum()

# pie chart
fig = px.pie(transmission_type, values='patients', names='type', title='Transmission type for total number of patients {}'.format(total_patients)
             , height=400)
plotly.offline.plot(fig, include_plotlyjs=False, filename='exported/Transmission type for total number of patients.html', auto_open=False)
