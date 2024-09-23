import pandas as pd
import unidecode

df = pd.read_csv('icv.csv')
df2 = pd.read_json('departamentos_modified.json')


temp = {}

for index, row in df2.iterrows():
    temp[df2.iloc[index,1]['properties']['id']] = {'departamento': df2.iloc[index,1]['properties']['departamento'].lower(),
                                               'provincia': df2.iloc[index,1]['properties']['provincia'].lower()}
    
df2 = pd.DataFrame.from_dict(temp, orient='index').reset_index()
df2 = df2.rename(columns = {'index':'id'})
df2 = df2.replace('ñ', 'n', regex=True)

for index, row in df.iterrows():
    name = unidecode.unidecode(df.at[index, 'Departamento'].lower())
    prov = unidecode.unidecode(df.at[index, 'Nombre de provincia'].lower())

    if "(" in name:
        name = name.split("(")[0].strip()

    if 'comuna' in name:
        name = name.split()[0].strip() + ' ' + str(int(name.split()[1].strip()))
    
    index2 = df2[(df2['departamento'] == name) & (df2['provincia'] == prov )].index.tolist()
    if index2 == []:
        name = name.replace('.', '')
        prov = prov.replace('.', '')
        index2 = df2[(df2['departamento'] == name) & (df2['provincia']==prov )].index.tolist()
        if index2 == []:
            print(name, prov)
            continue

    index2 = index2[0]

    df.at[index, 'id'] = df2.at[index2, 'id']


df.to_csv('icv_id.csv', index=False)
