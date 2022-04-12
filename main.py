
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

URL = 'https://en.wikipedia.org/wiki/Road_safety_in_Europe'
TABLE_ID = 'wikitable sortable'

def create_csv():
    # Creating the page object
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    page = urlopen(URL)
    soup = BeautifulSoup(page, "lxml")

    # Getting the desired table from the page
    table = soup.find('table', {'class' : 'wikitable sortable'})

    # Getting all the rows from the table
    rows = table.find_all('tr')

    # Getting all the columns, which are in the first index of the rows array, since pretty much all headers have a \n we need to remove it
    columns = list(map(lambda column: column.text.replace('\n', ''), rows[0].find_all('th')))

    # Creating a dataframe, not necessarly needed but convenient
    df = pd.DataFrame(columns=columns)

    #Mapping the rows of the table
    for row in rows[1:]:
        tds = row.find_all('td')
        values_inside = list(map(lambda td: td.text.replace('\n',''), tds))
        df.loc[len(df)] = values_inside

    # Rename columns to the be equal to the challenge description and filter to just the ones needed
    df = df.rename(columns={
        'Area(thousands of km2)[21]':'Area',
        'Population in 2018[22]':'Population',
        'GDP per capita in 2018[23]':'GDP per capita',
        'Population density(inhabitants per km2) in 2017[24]':'Population density',
        'Vehicle ownership(per thousand inhabitants) in 2016[25]':'Vehicle ownership',
        'Total Road Deaths in 2018[27]':'Total road deaths',
        'Road deathsper Million Inhabitants in 2018[27]':'Road deaths per Million Inhabitants'}).filter(['Country','Area','Population', 'GDP per capita', 'Population density','Vehicle ownership','Total road deaths', 'Road deaths per Million Inhabitants'])
    
    # Add the year column to all as 2018
    df.insert(1, 'Year', 2018)

    #Sort the list 
    df['Road deaths per Million Inhabitants'] = df['Road deaths per Million Inhabitants'].astype('int')
    df = df.sort_values('Road deaths per Million Inhabitants')


    #Create the csv
    df.to_csv("data.csv", sep=',', index=False)

    #Print the dataframe, optional
    print(df)
    return df

create_csv()
