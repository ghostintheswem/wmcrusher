from responses import importdata
import pandas as pd
from datetime import datetime, timedelta

def getnames():
    """calls import and returns tuples in list"""

    newnames = importdata()
    newnames['Timestamp'] = pd.to_datetime(newnames['Timestamp'])

    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    past_week_df = newnames[newnames['Timestamp'] >= one_week_ago]
    print(past_week_df)

    text_columns = newnames.iloc[:, [1,2]]

    listnames = [tuple(row) for _, row in text_columns.iterrows()]

 

       
    return listnames

if __name__ == "__main__":
    listnames = getnames()
    print(listnames)

