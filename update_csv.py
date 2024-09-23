import pandas as pd
import unidecode

# df = pd.read_csv('migraciones.csv')
# df2 = pd.read_csv('departamentos_data.csv')

# for index, row in df.iterrows():
#     temp = df.at[index, 'identifier']
#     prov = df.at[index, 'name']
#     if 'omuna' in temp:
#         name = temp
#     else:
#         splited = temp.split()
#         name = splited[1:]
#         name = ' '.join(name)

#     df.at[index, 'identifier'] = name
    
#     index2 = df2[(df2['nombre'] == name) & (df2['provincia_nombre']==prov )].index.tolist()
#     if index2 == []:
#         print(name, prov)
#         continue

#     index2 = index2[0]

#     df.at[index, 'latitude'] = df2.at[index2, 'centroide_lat']
#     df.at[index, 'longitude'] = df2.at[index2, 'centroide_lon']



# df.to_csv('migraciones_coord.csv', index=False)

df = pd.read_csv('migraciones_edades.csv')
df2 = pd.read_json('departamentos_modified.json')


temp = {}

for index, row in df2.iterrows():
    temp[df2.iloc[index,1]['properties']['id']] = {'departamento': df2.iloc[index,1]['properties']['departamento'].lower(),
                                               'provincia': df2.iloc[index,1]['properties']['provincia'].lower()}
    
df2 = pd.DataFrame.from_dict(temp, orient='index').reset_index()
df2 = df2.rename(columns = {'index':'id'})
df2 = df2.replace('ñ', 'n', regex=True)

for index, row in df.iterrows():
    temp = unidecode.unidecode(df.at[index, 'identifier'].lower())
    prov = unidecode.unidecode(df.at[index, 'name'].lower())
    
    if 'omuna' in temp:
        name = temp
    else:
        splited = temp.split()
        name = splited[1:]
        name = ' '.join(name)

    df.at[index, 'identifier'] = name

    index2 = df2[(df2['departamento'] == name) & (df2['provincia']==prov )].index.tolist()
    if index2 == []:
        name = name.replace('.', '')
        prov = prov.replace('.', '')
        index2 = df2[(df2['departamento'] == name) & (df2['provincia']==prov )].index.tolist()
        if index2 == []:
            print(name, prov)
            continue

    index2 = index2[0]

    df.at[index, 'id'] = df2.at[index2, 'id']



df.to_csv('migraciones_edades_updated.csv', index=False)