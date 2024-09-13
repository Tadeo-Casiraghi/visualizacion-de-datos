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
        self.edges = None
    
    def custom_scale2(self, value):
        # Normalization to range [0, 1]
                
        return 1 - 1/(value + 1)

    def rename_columns(self, df, columns):
        new_columns = {}
        for col, new in zip(df.columns, columns):
            new_columns[col] = new
        return df.rename(columns=new_columns)

    def save_edges(self,):
        edges = []
        maxx = 0
        for provinciaA in self.provincias:
            filtered_rows = self.df[self.df['Hace 5 años'].str.contains(provinciaA, case=False, na=False)]
            for provinciaB in self.provincias:
                if provinciaA == provinciaB or 'Ciudad Autónoma de Buenos Aires' in provinciaA or 'Ciudad Autónoma de Buenos Aires' in provinciaB:
                    continue

                value = filtered_rows[provinciaB].values[0]
                if value > maxx:
                    maxx = value
                
                edges.append((provinciaA, provinciaB, value))
        self.edges = edges
        self.maxx = maxx
        self.edges_normalized = [(a, b, c/maxx) for a, b, c in edges]
        self.edges_neto = self.get_neto(self.edges)
        self.edges_neto_normalized = self.get_neto(self.edges_normalized)

        

    def get_neto(self, edges):
        edges_neto = {}
        # Iterate through the list of tuples
        for name1, name2, value in edges:
            if (name1, name2) in edges_neto:
                edges_neto[(name1, name2)] += value
            else:
                # Add to the dictionary by sorting the pair to avoid ('B', 'A') being separate from ('A', 'B')
                if (name2, name1) in edges_neto:
                    edges_neto[(name2, name1)] -= value
                else:
                    edges_neto[(name1, name2)] = value

        # Create the resulting list with only positive net flows
        return [(name1, name2, flow) if flow > 0 else (name2, name1, -flow) for (name1, name2), flow in edges_neto.items() if flow != 0]  

        

    
    def save_importacion(self,):
        self.importacion = {}
        for provinciaA in self.provincias:
            if provinciaA == 'Ciudad Autónoma de Buenos Aires':
                continue            
            filter_import = self.df[self.df['Hace 5 años'].str.contains('En otro', case=False, na=False)]
            self.importacion[provinciaA] = filter_import[provinciaA].values[0]


    def create_edges(self, neto = False, ponderated = False, maximum = 1, reference = 0, colors = 1):
        if self.edges is None:
            self.save_edges()
            self.save_importacion()
        
        edges = []

        if not neto and not ponderated:
            for a, b, c in self.edges_normalized:
                if colors == 0:
                    color = self.poblacion[b]/self.poblacion[a]
                else:
                    color = self.poblacion[a]/self.poblacion[b]
                edges.append((a, b, c*maximum, self.custom_scale2(color)))
            return edges
        elif not neto and ponderated:
            maxi = 0
            for a, b, c in self.edges:
                if colors == 0:
                    color = self.poblacion[b]/self.poblacion[a]
                else:
                    color = self.poblacion[a]/self.poblacion[b]
                poblacion = self.poblacion[a] if reference == 0 else self.poblacion[b]
                edges.append((a, b, c/poblacion, self.custom_scale2(color)))
                if c/poblacion > maxi:
                    maxi = c/poblacion
            
            edges = [(a, b, c*maximum/maxi, color) for a, b, c, color in edges]
            
            return edges
        elif neto and not ponderated:
            for a, b, c in self.edges_neto_normalized:
                if colors == 0:
                    color = self.poblacion[b]/self.poblacion[a]
                else:
                    color = self.poblacion[a]/self.poblacion[b]
                edges.append((a, b, c*maximum, self.custom_scale2(color)))
            return edges
        elif neto and ponderated:
            maxi = 0
            for a, b, c in self.edges_neto:
                if colors == 0:
                    color = self.poblacion[b]/self.poblacion[a]
                else:
                    color = self.poblacion[a]/self.poblacion[b]
                poblacion = self.poblacion[a] if reference == 0 else self.poblacion[b]
                edges.append((a, b, c/poblacion, self.custom_scale2(color)))
                if c/poblacion > maxi:
                    maxi = c/poblacion
            edges = [(a, b, c*maximum/maxi, color) for a, b, c, color in edges]
            return edges