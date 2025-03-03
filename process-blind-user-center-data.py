import pandas as pd
import os


indir = "data/raw/blind-user-center"
outdir = "data/processed/blind-user-center"


def filter_eye_movement_data(df):
    df = df[df.Sensor == 'Eye Tracker']
    return df


def process_data(file):
    df = pd.read_csv(indir + "/" + file + ".csv")
    et_df = filter_eye_movement_data(df)
    et_df = et_df[['Gaze point X', 'Gaze point Y', 'Recording timestamp']]
    et_df = et_df.dropna(axis=0, how="all", subset=["Gaze point X", "Gaze point Y"], inplace=False)

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
