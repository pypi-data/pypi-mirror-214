from abc import ABC, abstractmethod

import pandas as pd


class DataCollection(ABC):
    @abstractmethod
    def query(self, table_name: str, query: str) -> pd.DataFrame:
        pass
