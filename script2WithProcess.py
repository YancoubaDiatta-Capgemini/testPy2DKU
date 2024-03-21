import pandas as pd
import requests
from io import StringIO

# URL du fichier CSV sur GitHub
url = "https://raw.githubusercontent.com/YancoubaDiatta-Capgemini/testPy2DKU/main/testData.csv"

# Récupérer le contenu du fichier CSV à partir de l'URL
response = requests.get(url)
csv_data = StringIO(response.text)

# Charger le fichier CSV dans un DataFrame
out1 = pd.read_csv(csv_data)

# Créer une nouvelle colonne en multipliant la colonne "age" par 2
out2=out1
out1['age_doubled'] = out1['Age'] * 2
out2['age_triple']=  out1['Age'] * 3
#print(data.head())
