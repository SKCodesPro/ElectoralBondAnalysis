import pandas as pd

test_dict = [{'name': 'sk', 'city': 'salem','points': 32},
             {'name': 'thangam', 'city': 'salem','points': 43},
             {'name': 'parkavi', 'city': 'bangalore','points': 20}]

df = pd.DataFrame(test_dict)
df1 = df.groupby(['city'])['points'].sum()
disct  = df1.to_dict()
print(disct)