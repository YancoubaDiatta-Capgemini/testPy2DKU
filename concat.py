# create a pandas dataframe to concatenate 2 csv files
import pandas as pd

# Create a pandas dataframe to concatenate 2 csv files
df1 = pd.read_csv("https://raw.githubusercontent.com/YancoubaDiatta-Capgemini/testPy2DKU/main/donnees1.csv")
df2 = pd.read_csv("https://raw.githubusercontent.com/YancoubaDiatta-Capgemini/testPy2DKU/main/donnees2.csv")

# Concatenate the 2 dataframes
df = pd.concat([df1, df2], axis=1)

# Print the concatenated dataframe
print("Concatenated DataFrame:\n", df)
