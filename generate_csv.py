import pandas as pd
import os

directory_path = 'datos_migracion\detalle'
all_files = os.listdir(directory_path)

names = {}
for file in all_files:
    names[file.split('_')[1]] = os.path.join(directory_path, file)

dataset = {}

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

        total = df.iloc[3,2]
        total_esta = df.iloc[3,3] if df.iloc[3,3] != '-' else 0
        total_otra = df.iloc[3,4] if df.iloc[3,4] != '-' else 0
        total_fuera = df.iloc[3,5] if df.iloc[3,5] != '-' else 0

        mujer = df.iloc[23,2]
        mujer_esta = df.iloc[23,3] if df.iloc[23,3] != '-' else 0
        mujer_otra = df.iloc[23,4] if df.iloc[23,4] != '-' else 0
        mujer_fuera = df.iloc[23,5] if df.iloc[23,5] != '-' else 0

        hombre = df.iloc[43,2]
        hombre_esta = df.iloc[43,3] if df.iloc[43,3] != '-' else 0
        hombre_otra = df.iloc[43,4] if df.iloc[43,4] != '-' else 0
        hombre_fuera = df.iloc[43,5] if df.iloc[43,5] != '-' else 0

        dataset[name][identifier] = {
            'total': total,
            'total_esta': total_esta,
            'total_otra': total_otra,
            'total_fuera': total_fuera,
            'mujer': mujer,
            'mujer_esta': mujer_esta,
            'mujer_otra': mujer_otra,
            'mujer_fuera': mujer_fuera,
            'hombre': hombre,
            'hombre_esta': hombre_esta,
            'hombre_otra': hombre_otra,
            'hombre_fuera': hombre_fuera,
            'total_esta_p': total_esta/total,
            'total_otra_p': total_otra/total,
            'total_fuera_p': total_fuera/total,
            'mujer_esta_p': mujer_esta/mujer,
            'mujer_otra_p': mujer_otra/mujer,
            'mujer_fuera_p': mujer_fuera/mujer,
            'hombre_esta_p': hombre_esta/hombre,
            'hombre_otra_p': hombre_otra/hombre,
            'hombre_fuera_p': hombre_fuera/hombre 
        }

flag = True
with open('migraciones.csv', 'w', encoding='utf8') as file:
    for name, data in dataset.items():
        for identifier, values in data.items():
            if flag:
                flag = False
                file.write('name,identifier,' + ','.join(values.keys()) + '\n')
            line = f'{name},{identifier},'
            for value in values.values():
                line += f'{value},'
            file.write(line[:-1] + '\n')