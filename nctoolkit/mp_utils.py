import nctoolkit as nc
import pandas as pd
import re
import numpy as np


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_equation(x):
    regexp = re.compile(r"[+,\-,/, \* ]")
    return len(regexp.findall(x)) > 0


def get_timedf(x):
    times = x.times

    model_times_df = pd.DataFrame(
        {
            "year": [x.year for x in times],
            "month": [x.month for x in times],
            "day": [x.day for x in times],
        }
    )
    return model_times_df


def get_type(df):
    if df.groupby(["year", "month"]).size().max() > 1:
        if len(df.loc[:, ["year"]].drop_duplicates()) > 1:
            return ["day", "month", "year"]
        else:
            return ["day", "month"]

    if len(df.loc[:, ["year"]].drop_duplicates()) == len(df):
        return ["year"]

    if len(df.loc[:, ["month"]].drop_duplicates()) == len(df):
        return ["month"]

    if len(df.loc[:, ["year", "month"]].drop_duplicates()) == len(df):
        return ["month", "year"]

