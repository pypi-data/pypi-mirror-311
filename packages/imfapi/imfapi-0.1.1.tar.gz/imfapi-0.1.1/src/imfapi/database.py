import os
import time
from typing import (
    Literal,
    Optional,
    TypeVar,
)

import pandas as pd
from joblib import Parallel, delayed

from imfapi._constants import JSON_RESTFUL_ENDPOINT, DATAFLOW, DATA_STRUCTURE
from imfapi.utils import chunk_iterable, make_request, strjoin


T = TypeVar("T", covariant=True)


TIME_WINDOW = 5
MAX_REQUESTS_PER_TIME_WINDOW = 10


class DataBase:
    def __init__(self, name: str, database_id: str):
        self.name = name
        self.id = database_id


class DataBases:
    def __init__(self, databases_to_load: Literal["main", "all"] = "main"):
        self._load_db_ids()
        self.databases_to_load = databases_to_load
        self._load_db_indicators()

    def _load_db_ids(self):
        response = make_request(strjoin(JSON_RESTFUL_ENDPOINT, DATAFLOW))
        data_json = response.json()
        df = pd.json_normalize(data_json["Structure"]["Dataflows"]["Dataflow"])
        self._df = df
        self._all_ids = sorted(df["KeyFamilyRef.KeyFamilyID"].map(str))
        self.ids = [db_id for db_id in self._all_ids if not any([s.isnumeric() for s in db_id])]

    def _load_db_indicators(self):
        database_ids = self.ids if self.databases_to_load == "main" else self._all_ids

        all_indicators_json = []
        for ids in chunk_iterable(iterable=database_ids, chunk_size=MAX_REQUESTS_PER_TIME_WINDOW):
            all_indicators_json.extend(
                Parallel(n_jobs=os.cpu_count() - 1, prefer="threads")(
                    delayed(make_request)(strjoin(JSON_RESTFUL_ENDPOINT, DATA_STRUCTURE, db_id)) for db_id in ids
                )
            )
            time.sleep(TIME_WINDOW + 0.1)
        self._all_indicators_json = all_indicators_json


class Series:
    def __init__(self, database_ids: Optional[list[str]]):
        if database_ids is None:
            database_ids = DataBases().ids[:10]
        self.database_ids = database_ids
        response = make_request(strjoin(JSON_RESTFUL_ENDPOINT, DATA_STRUCTURE, strjoin(*self.database_ids, sep="+")))
        self.data_json = response.json()
