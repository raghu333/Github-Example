from bs4 import BeautifulSoup
import requests
import pandas as pd 

URL = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class':'wikitable sortable'}).tbody  # Obtained from inspect (wiki - right click)

#print(table)

rows = table.find_all('tr')
columns = [v.text.replace('\n', '') for v in rows[0].find_all('th')]

#print(columns)

df = pd.DataFrame(columns = columns)

for i in range(1, len(rows)):
    tds = rows[i].find_all('td')

    if len(tds) == 3:
        values = [tds[0].text, tds[1].text, tds[2].text.replace('\n', '')]
    else:
        values = [td.text for td in tds]
    #print(values)
    #break

    df = df.append(pd.Series(values, index=columns), ignore_index = True)

    #print(df)
    
    
    # Getting the names of the indexes for which the Borough has a value - Not assigned
    indexNames = df[df['Borough'] == 'Not assigned'].index
    # Delete these rows index from the Data Frame
    df.drop(indexNames, inplace = True)

    #print(df)
    

# Replacing the Neighbourhood = "Not Assigned" to Borough values
df.loc[(df.Neighbourhood == 'Not assigned'), 'Neighbourhood'] = df['Borough']


# Grouping different neighbourhood based on the postcode.
df = df.groupby('Postcode').agg({'Borough':'first', 
                                    'Neighbourhood': ','.join}).reset_index()
    

#print(df)

df.to_csv('C:/Users/ragha/Desktop/Projects/PostalCode_Canada.csv', index = False)

print(df.shape)




