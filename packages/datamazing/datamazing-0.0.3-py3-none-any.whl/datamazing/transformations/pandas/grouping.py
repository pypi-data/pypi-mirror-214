import pandas as pd

from . import resampling


def _concat(a, b):
    if not isinstance(a, list):
        a = [a]
    if not isinstance(b, list):
        b = [b]
    return a + b


class GrouperResampler:
    def __init__(self, gb: "Grouper", on: str, resolution: pd.Timedelta):
        self.gb = gb
        self.on = on
        self.resolution = resolution
        self.resampler = self._get_resampler()

    def _get_resampler(self):
        pdf = (
            self.gb.df.set_index(_concat(self.on, self.gb.by))
            .unstack(self.gb.by)
            .reset_index(self.on)
        )
        return resampling.resample(pdf, self.on, self.resolution)

    def agg(self, method: str):
        resampled_pdf = self.resampler.agg(method)
        return (
            resampled_pdf.set_index(self.on)
            .stack(self.gb.by, dropna=True)
            .swaplevel(i=0, j=-1)
            .sort_index()
            .reset_index(_concat(self.gb.by, self.on))
        )


class Grouper:
    def __init__(self, df: pd.DataFrame, by: list[str]):
        self.df = df
        self.by = by

    def agg(self, method: str):
        return (
            self.df.set_index(self.by)
            .groupby(self.by, dropna=False)
            .aggregate(method)
            .reset_index()
        )

    def resample(self, on: str, resolution: pd.Timedelta):
        return GrouperResampler(self, on, resolution)

    def pivot(self, on: list[str]):
        df = self.df.set_index(_concat(self.by, on)).unstack(on).reset_index()
        df.columns = df.columns.map(
            lambda cols: "_".join([str(col) for col in cols[1:]]) + "_" + str(cols[0])
        ).str.strip("_")
        return df

    def latest(self, on: str):
        return (
            self.df.set_index(_concat(self.by, on))
            .sort_index(level=on)
            .groupby(self.by, dropna=False)
            .tail(1)
            .reset_index()
        )


def group(df: pd.DataFrame, by: list[str]):
    return Grouper(df, by)
