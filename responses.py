from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

# Initializing a GoogleAuth Object
# gauth = GoogleAuth()

# client_secrets.json file is verified
# and it automatically handles authentication
# gauth.LocalWebserverAuth()

# GoogleDrive Instance is created using
# authenticated GoogleAuth instance
# drive = GoogleDrive(gauth)

def importdata():
    """uses the google drive API to get responses and saves to spreadsheet, returns pandas dataframe"""

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        # First-time setup (will open browser ONCE)
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("credentials.json")
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)

    # Initialize GoogleDriveFile instance with file id
    file_obj = drive.CreateFile({'id': '1wQ3X325MVoMWYF96eHv0HwA_tvdWDt0YnWgTLz1o8xQ'})
    file_obj.GetContentFile('ourdata.xls',
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    dataframe = pd.read_excel('ourdata.xls')
    print(dataframe)
    return(dataframe)

if __name__ == "__main__":
    importdata()