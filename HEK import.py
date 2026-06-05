 from sunpy.net import Fido, attrs as a
    from sunpy.time import TimeRange
    import pandas as pd
    import datetime as dt  

    time_range = TimeRange("2025-11-13", "2026-02-28")

    result = Fido.search(
    a.Time(time_range.start, time_range.end),
    a.hek.EventType("FL"),
    a.hek.FL.GOESCls > "M5")

    hek_table = result["hek"]

    wanted_cols = [
        "event_starttime",
        "event_peaktime",
        "event_endtime",
        "fl_goescls",
        "ar_noaanum"]

    # Keep only columns that actually exist
    existing_cols = [col for col in wanted_cols if col in hek_table.colnames]

    df = hek_table[existing_cols].to_pandas()
    df = df[df["ar_noaanum"] != 0]

    df_cleaned = df.drop_duplicates(subset=["event_peaktime"])

    #only flares during daytime
    df_filtered = df_cleaned[
    (df_cleaned["event peaktime"].dt.time >= dt.time(6, 0)) &
    (df_cleaned["event peaktime"].dt.time <= dt.time(18, 0))]

    # Convert to datetime
    df_filtered["event starttime"] = pd.to_datetime(df_filtered["event starttime"])
    df_filtered["event peaktime"] = pd.to_datetime(df_filtered["event peaktime"])
    df_filtered["event endtime"] = pd.to_datetime(df_filtered["event endtime"])

    # Split into date + time
    df_filtered["date"] = df_filtered["event starttime"].dt.date

    df_filtered["start time"] = df_filtered["event starttime"].dt.time
    df_filtered["peak time"]  = df_filtered["event peaktime"].dt.time
    df_filtered["end time"]   = df_filtered["event endtime"].dt.time

    # Drop original datetime columns
    df_filtered = df_filtered.drop(columns=["event starttime", "event peaktime", "event endtime"])

    df_filtered = df_filtered[[
    "date",
    "start time",
    "peak time",
    "end time",
    "Flare Class", 
    "Active Region"]]

    df_filtered = df_filtered.reset_index(drop=True)
    df_filtered.to_latex("flares for test setup.tex", index=False)