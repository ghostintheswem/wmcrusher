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

    text_columns = newnames.iloc[:, [1,2]]

    listnames = [tuple(row) for _, row in text_columns.iterrows()]

    wrongI = []
    for i in range(0,len(listnames)):
        if len(listnames[i][0]) > 18:
            wrongI.append(i) 

    for j in wrongI:
        listnames.pop(i)

       
    return listnames

if __name__ == "__main__":
    listnames = getnames()
    print(listnames)

