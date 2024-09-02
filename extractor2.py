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
        self.poblacion = {}
        for index, prov in enumerate(self.provincias,7):
            self.latlong[prov] = (self.df.loc[index, 'Latitud'], self.df.loc[index, 'Longitud'])
            self.poblacion[prov] = self.df.loc[index, 'Poblacion']
       

    def custom_scale(self, value, min_val, max_val):
        # Normalization to range [0, 1]
        if value <= 1:
            normalized_value = (value - min_val) / (1 - min_val)
            normalized_value *= 0.5
        else:
            normalized_value = (value - 1) / (max_val - 1)
            normalized_value = 0.5 + normalized_value * 0.5
        
        return normalized_value
    
    def custom_scale2(self, value):
        # Normalization to range [0, 1]
                
        return 1 - 1/(value + 1)

    def rename_columns(self, df, columns):
        new_columns = {}
        for col, new in zip(df.columns, columns):
            new_columns[col] = new
        return df.rename(columns=new_columns)

    def create_edges(self, ponderated = False, maximum = 1, reference = 0, colors = 1):
        edges = []
        maxx = 0
        max_color = 0
        min_color = 100
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
                
                if colors == 0:
                    color = filtered_rows['Poblacion'].values[0]/filtered_rows2['Poblacion'].values[0]
                else:
                    color = filtered_rows2['Poblacion'].values[0]/filtered_rows['Poblacion'].values[0]

                if ponderated:
                    value = filtered_rows[provinciaB].values[0]/poblacion
                else:
                    value = filtered_rows[provinciaB].values[0]
                if value > maxx:
                    maxx = value
                if color > max_color:
                    max_color = color
                if color < min_color:
                    min_color = color
                edges.append((provinciaA, provinciaB, value, color))
        
        edges2 = []
        for a, b, c, d in edges:
            edges2.append((a, b, c/maxx*maximum, self.custom_scale(d, min_color, max_color)))
        return edges2