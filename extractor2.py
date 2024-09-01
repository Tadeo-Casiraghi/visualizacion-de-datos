import pandas as pd

class SheetExtractor:

    def __init__(self, path):
        self.path = path
        self.df = pd.read_excel(self.path, engine = 'openpyxl')
        self.columns = list(self.df.iloc[3,:].values)
        self.columns[0] = 'Hace 5 años'
        self.columns[1] = 'Poblacion'
        self.columns[-4] = 'Tierra del Fuego'
        col = self.columns
        self.df = self.df.iloc[4:,:]
        self.df = self.rename_columns(self.df, self.columns)
        self.df.iloc[col.index('Buenos Aires'), 1:] += self.df.iloc[col.index('Ciudad Autónoma de Buenos Aires'), 1:]
        self.provincias = [prov for prov in self.columns[2:-2] if 'Ciudad Aut' not in prov]
        self.df['Buenos Aires'] += self.df['Ciudad Autónoma de Buenos Aires']
        self.df.drop('Ciudad Autónoma de Buenos Aires', axis=1, inplace=True)
        self.df.drop(6, axis=0, inplace=True)
        self.latlong = {}
        for index, prov in enumerate(self.provincias,7):
            self.latlong[prov] = (self.df.loc[index, 'Latitud'], self.df.loc[index, 'Longitud'])

    def rename_columns(self, df, columns):
        new_columns = {}
        for col, new in zip(df.columns, columns):
            new_columns[col] = new
        return df.rename(columns=new_columns)

    def create_edges(self, ponderated = False, maximum = 1, reference = 0):
        edges = []
        maxx = 0
        for provinciaA in self.provincias:
            for provinciaB in self.provincias:
                if provinciaA == provinciaB or 'Ciudad Autónoma de Buenos Aires' in provinciaA or 'Ciudad Autónoma de Buenos Aires' in provinciaB:
                    continue

                filtered_rows = self.df[self.df['Hace 5 años'].str.contains(provinciaA, case=False, na=False)]
                filtered_rows2 = self.df[self.df['Hace 5 años'].str.contains(provinciaB, case=False, na=False)]
                if reference == 0:
                    poblacion = filtered_rows['Poblacion'].values[0]
                else:
                    poblacion = filtered_rows2['Poblacion'].values[0]
                if ponderated:
                    value = filtered_rows[provinciaB].values[0]/poblacion
                else:
                    value = filtered_rows[provinciaB].values[0]
                if value > maxx:
                    maxx = value
                edges.append((provinciaA, provinciaB, value))
        
        edges2 = []
        for a, b, c in edges:
            edges2.append((a, b, c/maxx*maximum))
        return edges2