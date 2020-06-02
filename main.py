import asyncio
import os
from datetime import datetime


def generateIndex():
    graphsPath = 'exported/'
    graphs = []                     # Holds paths of all graphs
    today = datetime.now()
    graphsCombined = '<p>last updated on : {}</p>'.format(today)             # Holds combined data of graphs

    # Get list of all graphs from ./graphs folder
    tree = os.walk('exported')
    for r, d, f in tree:
        graphs = f
    print('Paths received')

    # Read all flies in graphs folder and combine
    for graph in graphs:
        graphdata = open(graphsPath + graph, 'r')
        graphsCombined += '<div class="item">' + graphdata.read() + '</div>'
        graphdata.close()
    print('Graphs combined')

    # Use template and generate combined html
    index = open('template.html', 'r')
    data = index.read()
    data = data.replace('*AppendHere*', graphsCombined)
    index.close()
    print('Template generated')

    # Save combined graphs as template.html
    index = open('./site/public/index.html', 'w')
    index.write(data)
    index.close()
    print('template.html generated successfully :)')


def getData():
    os.system("python worldwide.py")
    os.system("python time_analysis.py")
    os.system("python statewise_cases.py")
    # os.system("python transmission.py")
    os.system("python statewise_tested.py")
    os.system("python statewise_daily.py")
    print('got data')


async def main():
    getData()
    # await asyncio.sleep(10)
    generateIndex()
    print('Starting to deploy..')
    await asyncio.sleep(10)
    os.system("cd site & firebase deploy")
    print('Site deployed to firebase successfully. Can be accessed at "https://zalak.stackmaze.com"')

asyncio.get_event_loop().run_until_complete(main())
