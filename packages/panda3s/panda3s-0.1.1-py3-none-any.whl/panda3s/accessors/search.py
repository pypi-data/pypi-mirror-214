from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Any, Dict, Hashable, Literal, Sequence, TypeVar, Union

import faiss
import numpy as np
from faiss import Index
from numpy.typing import NDArray
from pandas import DataFrame
from pandas.api import extensions as pd_exts

from panda3s.arrays import VectorArray


class MetricType(str, Enum):
    INNER_PRODUCT = "INNER_PRODUCT"
    L_2 = "L_2"
    L_1 = "L_1"
    L_INF = "L_INF"
    L_P = "L_P"
    CANBERRA = "CANBERRA"
    BRAY_CURTIS = "BRAY_CURTIS"
    JENSON_SHANNON = "JENSON_SHANNON"
    JACCARD = "JACCARD"

    @classmethod
    def _faiss_mapping(cls):
        return {
            cls.INNER_PRODUCT: faiss.METRIC_INNER_PRODUCT,
            cls.L_2: faiss.METRIC_L2,
            cls.L_1: faiss.METRIC_L1,
            cls.L_INF: faiss.METRIC_Linf,
            cls.L_P: faiss.METRIC_Lp,
            cls.CANBERRA: faiss.METRIC_Canberra,
            cls.BRAY_CURTIS: faiss.METRIC_BrayCurtis,
            cls.JENSON_SHANNON: faiss.METRIC_JensenShannon,
            cls.JACCARD: faiss.METRIC_Jaccard,
        }

    @classmethod
    def _alt_names(cls):
        mapping = {
            cls.INNER_PRODUCT: {"DOT", "COS", "COSINE", "INNERPRODUCT"},
            cls.L_2: {"2", "L2", "EUCLIDEAN"},
            cls.L_1: {"1", "L1", "MANHATTAN"},
            cls.L_INF: {"INF", "LINF"},
            cls.L_P: {"P", "LP"},
            cls.BRAY_CURTIS: {"BRAYCURTIS"},
            cls.JENSON_SHANNON: {"JENSONSHANNON"},
        }

        reverse = {
            alt: metric for metric, alt_list in mapping.items() for alt in alt_list
        }

        return reverse

    @classmethod
    def from_string(cls, string: str) -> MetricType:
        try:
            return cls(string)
        except ValueError:
            # No match.
            pass

        try:
            return cls._alt_names()[string]
        except KeyError:
            # No match.
            pass

        raise ValueError(f"{string} is not a valid string.")

    @classmethod
    def from_faiss(cls, faiss_metric: Any) -> MetricType:
        mapping_from_faiss = {
            faiss: metric for metric, faiss in cls._faiss_mapping().items()
        }

        try:
            return mapping_from_faiss[faiss_metric]
        except KeyError as ke:
            raise ValueError(f"{faiss_metric} is not supported yet.") from ke

    @classmethod
    def from_any(cls, metric) -> MetricType:
        if isinstance(metric, MetricType):
            return metric
        elif isinstance(metric, str):
            return MetricType.from_string(metric)
        elif metric in MetricType._faiss_mapping().values():
            return MetricType.from_faiss(metric)
        else:
            raise ValueError(f"{metric} should be of MetricType or a faiss metric.")

    def as_faiss(self):
        try:
            return self._faiss_mapping()[self]
        except KeyError as ke:
            raise AssertionError(
                f"Unreachable code: {self} unsupported by faiss."
            ) from ke


@pd_exts.register_dataframe_accessor("search")
class SearchAccessor:
    def __init__(self, df: DataFrame) -> None:
        self._df = df
        self._indices: Dict[Hashable, Index] = {}

    def create_index(
        self, column: Hashable, factory: str = "Flat", metric: Any = MetricType.L_2
    ):
        metric_typ = MetricType.from_any(metric)

        # HACK: Only allow VectorArray for now.
        col = VectorArray(self._df[column], copy=False)

        index: Index = faiss.index_factory(col.dims, factory, metric_typ.as_faiss())

        numpy_data = col.numpy
        index.train(numpy_data)

        assert index.is_trained, "Index should be trained by this point."
        index.add(numpy_data)

        self._indices[column] = index

    def __call__(
        self, column: Hashable, query: Sequence[float] | NDArray, top_k: int = 1
    ) -> DataFrame:
        if column not in self._indices:
            self.create_index(column)

        index = self._indices[column]
        col = self._df[column]

        search_query = np.array(query)

        if search_query.ndim == 1:
            search_query = search_query[np.newaxis, :]
        else:
            raise ValueError("Batched queries not supported yet.")

        # D, I are of the shape
        # batch, top_k
        D, I = index.search(search_query, k=top_k)

        D = np.array(D).squeeze()
        I = np.array(I).squeeze()

        return DataFrame({"distance": D, "indices": I, "data": col.iloc[I]})
