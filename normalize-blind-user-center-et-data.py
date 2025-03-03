import pandas as pd
import os

indir = "data/processed/blind-user-center"
outdir = "data/normalized/blind-user-center"

def getx(row):
    # data not already normalized, need to divide by screen size
    x = row['Gaze point X']/1920

    if x > 0.0:
        x = str(x)
    else:
        x = '-1'
    return x


def gety(row):
    # data not already normalized, need to divide by screen size
    y = row['Gaze point Y']/1080

    if y > 0.0:
        y = str(y)
    else:
        y = '-1'
    return y


def getpd(row):
    return 0


def reformat(path, basename):
    df = pd.DataFrame(columns=["x", "y", "d", "t"])
    dframe = pd.read_csv(path)
    df["x"] = dframe.apply(getx, axis=1)
    df["y"] = dframe.apply(gety, axis=1)
    df["d"] = dframe.apply(getpd, axis=1)
    df["t"] = dframe["Recording timestamp"]

    df.to_csv(outdir + "/" + basename + ".csv", index=False)


if os.path.isdir(indir):
    for top, dirs, listing in os.walk(indir):
        for file in listing:
            path = os.path.join(top, file)
            dname = path.split('/')[2]
            base = os.path.basename(path)
            if base.endswith('.csv'):
                basename = base[:base.rfind('.csv')]
                filepath = indir + "/" + basename + ".csv"
                reformat(filepath, basename)
