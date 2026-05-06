import pandas as pd

df = pd.read_excel("data/banking_dataset.xlsx")

print(df.head())

print("\nColumns:")
print(df.columns)

print("\nDataset Shape:")
print(df.shape)