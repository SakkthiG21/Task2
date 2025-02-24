import pandas as pd
import os
if not os.path.exists('data'):
    os.makedirs('data')
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
df.to_csv('data/titanic.csv', index=False)
print("Dataset downloaded successfully!") 