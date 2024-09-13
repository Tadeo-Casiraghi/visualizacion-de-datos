import pandas as pd

columns = ['edad',
           'total:poblacion',
           'total:asistir',
           'sin_instruccion',
           'primaria:total',
           'primaria:incompleto',
           'primaria:completo',
           'EGB:total',
           'EGB:incompleto',
           'EGB:completo',
           'secundaria:total',
           'secundaria:incompleto',
           'secundaria:completo',
           'polimodal:total',
           'polimodal:incompleto',
           'polimodal:completo',
           'terciario_nu:total',
           'terciario_nu:incompleto',
           'terciario_nu:completo',
           'universitario:total',
           'universitario:incompleto',
           'universitario:completo',
           'postgrado:total',
           'postgrado:incompleto',
           'postgrado:completo']

class SheetExtractor:

    def __init__(self, path, sheet):
        self.path = path
        self.df = pd.read_excel(self.path, engine = 'openpyxl', sheet_name=sheet)
        self.name = self.get_name()

        self.total = self.df.iloc[5:48,1:(1+len(columns))]
        self.total = self.rename_columns(self.total)
        self.total_ranges = self.get_ranges(self.total)
        
        self.females = self.df.iloc[49:92,1:(1+len(columns))]
        self.females = self.rename_columns(self.females)
        self.females_ranges = self.get_ranges(self.females)

        self.males = self.df.iloc[93:136,1:(1+len(columns))]
        self.males = self.rename_columns(self.males)
        self.males_ranges = self.get_ranges(self.males)

    def get_name(self):
        texto = self.df.iloc[0,0]
        index1 = texto.find(',')+2
        index2 = texto.find('.', index1)
        return texto[index1:index2]

    def rename_columns(self, df):
        new_columns = {}
        for i in range(len(columns)):
            new_columns['Unnamed: '+str(i+1)] = columns[i]
        return df.rename(columns=new_columns)

    def get_ranges(self, df):
        filtered_df = df[df['edad'].str.contains('-')]
        return filtered_df

    def get(self, table, category, ponderated = False, ranged = True, start_from = None):
        if table == 'total' and ranged:
            df = self.total_ranges
        elif table == 'total':
            df = self.total
        elif table == 'females' and ranged:
            df = self.females_ranges
        elif table == 'females':
            df = self.females
        elif table == 'males' and ranged:
            df = self.males_ranges
        else:
            df = self.males
        
        flag = True
        if start_from:
            flag = False
        
        data = {}

        level = category.split(':')[0]

        for _, row in df.iterrows():
            if not flag:
                if row['edad'] == start_from:
                    flag = True
                else:
                    continue
            if not (str(row[category]).isnumeric()):
                value = 0
            else:
                value = row[category]
            if ponderated:
                if not str(row['total:poblacion']).isnumeric():
                    total = 1
                else:
                    total = row['total:poblacion']
                data[row['edad']] = value/total
            else:
                data[row['edad']] = value
        
        return data
