import numpy as np


class CourseRecommender:

    def __init__(self, df):
        self.df = df.copy()

    def _normalize(self, col):
        return (col - col.min()) / (col.max() - col.min() + 1e-9)

    def feature_engineering(self):

        df = self.df

        df["rating_n"] = df["rating"] / 5

        df["students_n"] = np.log1p(df["students"])
        df["hours_n"] = np.log1p(df["hours"])
        df["lessons_n"] = np.log1p(df["lessons"])

        df["students_n"] = self._normalize(df["students_n"])
        df["hours_n"] = self._normalize(df["hours_n"])
        df["lessons_n"] = self._normalize(df["lessons_n"])

        df["efficiency"] = df["lessons"] / (df["hours"] + 1)
        df["efficiency_n"] = self._normalize(df["efficiency"])

        self.df = df
        return self

    def rank(self):

        df = self.df

        df["score"] = (
            df["rating_n"] * 0.35 +
            df["students_n"] * 0.20 +
            df["hours_n"] * 0.15 +
            df["lessons_n"] * 0.15 +
            df["efficiency_n"] * 0.15
        )

        self.df = df.sort_values("score", ascending=False)

        return self.df

    def top_unique(self):
        return self.df.drop_duplicates(subset=["link"])