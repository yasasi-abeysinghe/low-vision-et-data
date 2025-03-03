import pandas as pd
import os


indir = "data/raw/new-experiment"
outdir = "data/processed/new-experiment"
first_timestamp = 0


# These data are collected using Gazepoint GP3
# This data is already normalized


# Filter out invalid data
def filter_valid_eye_movement_data(df):
    df = df[df.gv == 1.0]
    return df


def update_timestamp(row):
    t = row['timestamp'] - first_timestamp
    return t


def process_data(file):
    global first_timestamp

    df = pd.read_csv(indir + "/" + file + ".csv")
    et_df = filter_valid_eye_movement_data(df)
    et_df = et_df[['gx', 'gy', 'timestamp']]
    et_df = et_df.dropna(axis=0, how="all", subset=["gx", "gy"], inplace=False)
    et_df = et_df.rename(columns={'gx': 'x', 'gy': 'y'})

    first_timestamp = et_df['timestamp'].iloc[0]
    et_df["t"] = et_df.apply(update_timestamp, axis=1)
    et_df.drop(columns=['timestamp'], inplace=True)

    et_df['d'] = 0 # set pupil diameter values to 0

    column_order = ['x', 'y', 'd', 't']
    et_df = et_df[column_order]

    et_df.to_csv(outdir + "/" + file + ".csv", index=False)


if os.path.isdir(indir):
    for top, dirs, listing in os.walk(indir):
        for file in listing:
            path = os.path.join(top, file)
            dname = path.split('/')[2]
            base = os.path.basename(path)
            if base.endswith('.csv'):
                basename = base[:base.rfind('.csv')]
                process_data(basename)