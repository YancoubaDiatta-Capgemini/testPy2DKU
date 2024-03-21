import pandas as pd
import requests
from io import StringIO
import dataiku
# URL du fichier CSV sur GitHub
url = "https://raw.githubusercontent.com/YancoubaDiatta-Capgemini/testPy2DKU/main/testData.csv"

# Récupérer le contenu du fichier CSV à partir de l'URL
response = requests.get(url)
csv_data = StringIO(response.text)

# Charger le fichier CSV dans un DataFrame
out1 = pd.read_csv(csv_data)
# Créer un dataset à partir du DataFrame
output_dataset = dataiku.Dataset("output_prep8")
output_dataset.write_with_schema(data)
