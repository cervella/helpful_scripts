import pandas as pd

file = 'nameoffile.xlsx'

xl = pd.ExcelFile(file)

print(xl.sheet_names)

for sheet_name in xl.sheet_names:
    df = xl.parse(sheet_name)
    df.to_csv('{}.csv'.format(sheet_name), index=False)
