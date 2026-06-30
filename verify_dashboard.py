import pandas as pd

df = pd.read_csv('results_enriched.csv')
print('rows', len(df))
print('status counts:')
print(df['status'].value_counts().to_string())
print('\ncountry counts top 5:')
print(df['country'].value_counts().head(5).to_string())
print('\nas_name counts top 5:')
print(df['as_name'].dropna().value_counts().head(5).to_string())
