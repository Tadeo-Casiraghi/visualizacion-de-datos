import pandas as pd
import os

directory_path = 'datos_migracion\detalle'
all_files = os.listdir(directory_path)

names = {}
for file in all_files:
    names[file.split('_')[1]] = os.path.join(directory_path, file)

dataset = {}

edades = list(range(22, 90, 5))

for name, path in names.items():
    print(f'Working on {name}')
    excel_file = pd.ExcelFile(path)

    dataset[name] = {}
    for sheet in range(3, len(excel_file.sheet_names)):
        df = pd.read_excel(path, engine = 'openpyxl', sheet_name=sheet)
        texto = df.iloc[0,0]
        index1 = texto.find(',')+2
        index2 = texto.find('.', index1)
        identifier = texto[index1:index2]

        print(f'Working on {name} - {identifier}')

        total = (df.iloc[3,2] if df.iloc[3,2] != '-' else 0) - \
                (df.iloc[4,2] if df.iloc[4,2] != '-' else 0) - \
                (df.iloc[5,2] if df.iloc[5,2] != '-' else 0) - \
                (df.iloc[6,2] if df.iloc[6,2] != '-' else 0) - \
                (df.iloc[7,2] if df.iloc[7,2] != '-' else 0)
        
        esta = (df.iloc[3,3] if df.iloc[3,3] != '-' else 0) - \
                (df.iloc[4,3] if df.iloc[4,3] != '-' else 0) - \
                (df.iloc[5,3] if df.iloc[5,3] != '-' else 0) - \
                (df.iloc[6,3] if df.iloc[6,3] != '-' else 0) - \
                (df.iloc[7,3] if df.iloc[7,3] != '-' else 0)

        otra = (df.iloc[3,4] if df.iloc[3,4] != '-' else 0) - \
                (df.iloc[4,4] if df.iloc[4,4] != '-' else 0) - \
                (df.iloc[5,4] if df.iloc[5,4] != '-' else 0) - \
                (df.iloc[6,4] if df.iloc[6,4] != '-' else 0) - \
                (df.iloc[7,4] if df.iloc[7,4] != '-' else 0)
        
        fuera = (df.iloc[3,5] if df.iloc[3,5] != '-' else 0) - \
                (df.iloc[4,5] if df.iloc[4,5] != '-' else 0) - \
                (df.iloc[5,5] if df.iloc[5,5] != '-' else 0) - \
                (df.iloc[6,5] if df.iloc[6,5] != '-' else 0) - \
                (df.iloc[7,5] if df.iloc[7,5] != '-' else 0)
        
        edad_total = 0
        edad_total_n = 0
        edad_total_esta = 0
        edad_total_esta_n = 0
        edad_total_otra = 0
        edad_total_otra_n = 0
        edad_total_fuera = 0
        edad_total_fuera_n = 0
        for i in range(8, 22):
            # edad_total += df.iloc[i,2]/total*edades[i-8] if df.iloc[i,2] != '-' else 0
            # if df.iloc[i,2] == '-':
            #     continue
            # edad_total_esta += df.iloc[i,3]/esta*edades[i-8] if df.iloc[i,3] != '-' else 0
            # edad_total_otra += df.iloc[i,4]/otra*edades[i-8] if df.iloc[i,4] != '-' else 0
            # edad_total_fuera += df.iloc[i,5]/fuera*edades[i-8] if df.iloc[i,5] != '-' else 0
            if df.iloc[i,2] != '-' and df.iloc[i,2] > edad_total_n:
                edad_total = edades[i-8]
                edad_total_n = df.iloc[i,2]
            if df.iloc[i,3] != '-' and df.iloc[i,3] > edad_total_esta_n:
                edad_total_esta = edades[i-8]
                edad_total_esta_n = df.iloc[i,3]
            if df.iloc[i,4] != '-' and df.iloc[i,4] > edad_total_otra_n:
                edad_total_otra = edades[i-8]
                edad_total_otra_n = df.iloc[i,4]
            if df.iloc[i,5] != '-' and df.iloc[i,5] > edad_total_fuera_n:
                edad_total_fuera = edades[i-8]
                edad_total_fuera_n = df.iloc[i,5]
        
        mujer = (df.iloc[23,2] if df.iloc[23,2] != '-' else 0) - \
                (df.iloc[24,2] if df.iloc[24,2] != '-' else 0) - \
                (df.iloc[25,2] if df.iloc[25,2] != '-' else 0) - \
                (df.iloc[26,2] if df.iloc[26,2] != '-' else 0) - \
                (df.iloc[27,2] if df.iloc[27,2] != '-' else 0)
        
        mujer_esta = (df.iloc[23,3] if df.iloc[23,3] != '-' else 0) - \
                (df.iloc[24,3] if df.iloc[24,3] != '-' else 0) - \
                (df.iloc[25,3] if df.iloc[25,3] != '-' else 0) - \
                (df.iloc[26,3] if df.iloc[26,3] != '-' else 0) - \
                (df.iloc[27,3] if df.iloc[27,3] != '-' else 0)
        
        mujer_otra = (df.iloc[23,4] if df.iloc[23,4] != '-' else 0) - \
                (df.iloc[24,4] if df.iloc[24,4] != '-' else 0) - \
                (df.iloc[25,4] if df.iloc[25,4] != '-' else 0) - \
                (df.iloc[26,4] if df.iloc[26,4] != '-' else 0) - \
                (df.iloc[27,4] if df.iloc[27,4] != '-' else 0)
        
        mujer_fuera = (df.iloc[23,5] if df.iloc[23,5] != '-' else 0) - \
                (df.iloc[24,5] if df.iloc[24,5] != '-' else 0) - \
                (df.iloc[25,5] if df.iloc[25,5] != '-' else 0) - \
                (df.iloc[26,5] if df.iloc[26,5] != '-' else 0) - \
                (df.iloc[27,5] if df.iloc[27,5] != '-' else 0)
        
        edad_mujer = 0
        edad_mujer_n = 0
        edad_mujer_esta = 0
        edad_mujer_esta_n = 0
        edad_mujer_otra = 0
        edad_mujer_otra_n = 0
        edad_mujer_fuera = 0
        edad_mujer_fuera_n = 0
        for i in range(28, 42):
            # edad_mujer += df.iloc[i,2]/mujer*edades[i-28] if df.iloc[i,2] != '-' else 0
            # if df.iloc[i,2] == '-':
            #     continue
            # edad_mujer_esta += df.iloc[i,3]/mujer_esta*edades[i-28] if df.iloc[i,3] != '-' else 0
            # edad_mujer_otra += df.iloc[i,4]/mujer_otra*edades[i-28] if df.iloc[i,4] != '-' else 0
            # edad_mujer_fuera += df.iloc[i,5]/mujer_fuera*edades[i-28] if df.iloc[i,5] != '-' else 0
            if df.iloc[i,2] != '-' and df.iloc[i,2] > edad_mujer_n:
                edad_mujer = edades[i-28]
                edad_mujer_n = df.iloc[i,2]
            if df.iloc[i,3] != '-' and df.iloc[i,3] > edad_mujer_esta_n:
                edad_mujer_esta = edades[i-28]
                edad_mujer_esta_n = df.iloc[i,3]
            if df.iloc[i,4] != '-' and df.iloc[i,4] > edad_mujer_otra_n:
                edad_mujer_otra = edades[i-28]
                edad_mujer_otra_n = df.iloc[i,4]
            if df.iloc[i,5] != '-' and df.iloc[i,5] > edad_mujer_fuera_n:
                edad_mujer_fuera = edades[i-28]
                edad_mujer_fuera_n = df.iloc[i,5]

        
        hombre = (df.iloc[43,2] if df.iloc[43,2] != '-' else 0) - \
                (df.iloc[44,2] if df.iloc[44,2] != '-' else 0) - \
                (df.iloc[45,2] if df.iloc[45,2] != '-' else 0) - \
                (df.iloc[46,2] if df.iloc[46,2] != '-' else 0) - \
                (df.iloc[47,2] if df.iloc[47,2] != '-' else 0)
        
        hombre_esta = (df.iloc[43,3] if df.iloc[43,3] != '-' else 0) - \
                (df.iloc[44,3] if df.iloc[44,3] != '-' else 0) - \
                (df.iloc[45,3] if df.iloc[45,3] != '-' else 0) - \
                (df.iloc[46,3] if df.iloc[46,3] != '-' else 0) - \
                (df.iloc[47,3] if df.iloc[47,3] != '-' else 0)
        
        hombre_otra = (df.iloc[43,4] if df.iloc[43,4] != '-' else 0) - \
                (df.iloc[44,4] if df.iloc[44,4] != '-' else 0) - \
                (df.iloc[45,4] if df.iloc[45,4] != '-' else 0) - \
                (df.iloc[46,4] if df.iloc[46,4] != '-' else 0) - \
                (df.iloc[47,4] if df.iloc[47,4] != '-' else 0)
        
        hombre_fuera = (df.iloc[43,5] if df.iloc[43,5] != '-' else 0) - \
                (df.iloc[44,5] if df.iloc[44,5] != '-' else 0) - \
                (df.iloc[45,5] if df.iloc[45,5] != '-' else 0) - \
                (df.iloc[46,5] if df.iloc[46,5] != '-' else 0) - \
                (df.iloc[47,5] if df.iloc[47,5] != '-' else 0)
                
        edad_hombre = 0
        edad_hombre_n = 0
        edad_hombre_esta = 0
        edad_hombre_esta_n = 0
        edad_hombre_otra = 0
        edad_hombre_otra_n = 0
        edad_hombre_fuera = 0
        edad_hombre_fuera_n = 0
        for i in range(48, 62):
            # edad_hombre += df.iloc[i,2]/hombre*edades[i-48] if df.iloc[i,2] != '-' else 0
            # if df.iloc[i,2] == '-':
            #     continue
            # edad_hombre_esta += df.iloc[i,3]/hombre_esta*edades[i-48] if df.iloc[i,3] != '-' else 0
            # edad_hombre_otra += df.iloc[i,4]/hombre_otra*edades[i-48] if df.iloc[i,4] != '-' else 0
            # edad_hombre_fuera += df.iloc[i,5]/hombre_fuera*edades[i-48] if df.iloc[i,5] != '-' else 0
            if df.iloc[i,2] != '-' and df.iloc[i,2] > edad_hombre_n:
                edad_hombre = edades[i-48]
                edad_hombre_n = df.iloc[i,2]
            if df.iloc[i,3] != '-' and df.iloc[i,3] > edad_hombre_esta_n:
                edad_hombre_esta = edades[i-48]
                edad_hombre_esta_n = df.iloc[i,3]
            if df.iloc[i,4] != '-' and df.iloc[i,4] > edad_hombre_otra_n:
                edad_hombre_otra = edades[i-48]
                edad_hombre_otra_n = df.iloc[i,4]
            if df.iloc[i,5] != '-' and df.iloc[i,5] > edad_hombre_fuera_n:
                edad_hombre_fuera = edades[i-48]
                edad_hombre_fuera_n = df.iloc[i,5]

        dataset[name][identifier] = {
            'total': edad_total,
            'mujer': edad_mujer,
            'hombre': edad_hombre,
            'total_esta': edad_total_esta,
            'total_otra': edad_total_otra,
            'total_fuera': edad_total_fuera,
            'mujer_esta': edad_mujer_esta,
            'mujer_otra': edad_mujer_otra,
            'mujer_fuera': edad_mujer_fuera,
            'hombre_esta': edad_hombre_esta,
            'hombre_otra': edad_hombre_otra,
            'hombre_fuera': edad_hombre_fuera,
        }

flag = True
with open('migraciones_edades.csv', 'w', encoding='utf8') as file:
    for name, data in dataset.items():
        for identifier, values in data.items():
            if flag:
                flag = False
                file.write('name,identifier,' + ','.join(values.keys()) + '\n')
            line = f'{name},{identifier},'
            for value in values.values():
                line += f'{value},'
            file.write(line[:-1] + '\n')