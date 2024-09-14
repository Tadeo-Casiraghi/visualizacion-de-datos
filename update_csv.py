import pandas as pd

df = pd.read_csv('migraciones.csv')
df2 = pd.read_csv('departamentos_data.csv')

for index, row in df.iterrows():
    temp = df.at[index, 'identifier']
    prov = df.at[index, 'name']
    if 'omuna' in temp:
        name = temp
    else:
        splited = temp.split()
        name = splited[1:]
        name = ' '.join(name)

    df.at[index, 'identifier'] = name
    
    index2 = df2[(df2['nombre'] == name) & (df2['provincia_nombre']==prov )].index.tolist()
    if index2 == []:
        print(name, prov)
        continue

    index2 = index2[0]

    df.at[index, 'latitude'] = df2.at[index2, 'centroide_lat']
    df.at[index, 'longitude'] = df2.at[index2, 'centroide_lon']



df.to_csv('migraciones_coord.csv', index=False)