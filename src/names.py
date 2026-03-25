from responses import importdata
import pandas as pd
from gemini import moderate_me
import json

DATA_FILE = "./data.json"

def getnames(only_new: bool = True) -> list[tuple]:
    """
    Fetches form responses, runs them through Gemini moderation,
    persists approved entries to data.json, and returns them as
    a list of (name, message) tuples.

    Args:
        only_new: Passed through to importdata(). True by default so we never
                  re-process entries we've already seen.
    """
    newnames = importdata(only_new=only_new)

    if newnames.empty:
        print("No new responses to process.")
        return []

    # Columns: index 1 = name submitted, index 2 = message submitted
    text_columns = newnames.iloc[:, [1, 2]]
    listnames = [tuple(row) for _, row in text_columns.iterrows()]

    print(f"Running {len(listnames)} response(s) through moderation...")
    approved = moderate_me(listnames)
    print(f"{len(approved)}/{len(listnames)} response(s) passed moderation.")

    with open(DATA_FILE, "w") as f:
        json.dump(approved, f, indent=2)

    return approved


if __name__ == "__main__":
    names = getnames()
    print(names)
