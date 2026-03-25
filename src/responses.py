from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import json
import os

LAST_SEEN_FILE = "./last_seen.json"

def _load_last_seen() -> str | None:
    """Load the timestamp of the last processed response."""
    if os.path.exists(LAST_SEEN_FILE):
        with open(LAST_SEEN_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_seen")
    return None

def _save_last_seen(timestamp: str):
    """Persist the latest processed timestamp so we don't reprocess old rows."""
    with open(LAST_SEEN_FILE, "w") as f:
        json.dump({"last_seen": timestamp}, f)

def importdata(only_new: bool = True) -> pd.DataFrame:
    """
    Uses the Google Drive API to fetch form responses, saves to spreadsheet,
    and returns a pandas DataFrame.

    Args:
        only_new: If True (default), only return rows newer than the last run.
                  Set to False to reprocess everything (e.g. for a full rebuild).
    """
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("./credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("./credentials.json")
    elif gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile("./credentials.json")
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)

    file_obj = drive.CreateFile({'id': '1wQ3X325MVoMWYF96eHv0HwA_tvdWDt0YnWgTLz1o8xQ'})
    file_obj.GetContentFile(
        'ourdata.xls',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    dataframe = pd.read_excel('./ourdata.xls')
    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])
    dataframe = dataframe.sort_values('Timestamp')

    if only_new:
        last_seen = _load_last_seen()
        if last_seen:
            cutoff = pd.to_datetime(last_seen)
            dataframe = dataframe[dataframe['Timestamp'] > cutoff]
            print(f"Filtering to {len(dataframe)} new responses since {last_seen}")
        else:
            print("No last_seen checkpoint found — processing all responses.")

    if not dataframe.empty:
        latest_ts = dataframe['Timestamp'].max().isoformat()
        _save_last_seen(latest_ts)
        print(f"Checkpoint updated to {latest_ts}")
    else:
        print("No new responses found.")

    return dataframe


if __name__ == "__main__":
    df = importdata()
    print(df)
