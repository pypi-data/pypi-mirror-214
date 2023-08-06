from __future__ import annotations

from typing import Any, Hashable

import numpy as np
from numpy.typing import NDArray
from pandas import DataFrame
from pandas._libs import lib
from pandas.api import extensions as pd_exts

from panda3s.arrays import VectorArray


@pd_exts.register_dataframe_accessor("fuse")
class FusionAccessor:
    def __init__(self, df: DataFrame) -> None:
        self._df = df

    def __call__(self, *columns: Hashable) -> VectorArray:
        for col in columns:
            if col not in self._df.columns:
                raise ValueError(
                    f"Column {col} not found in the DataFrame! Found: {self._df.columns}"
                )

        series = [self._df[col] for col in columns]
        arrays = np.stack([self._join(*zipped) for zipped in zip(*series)])
        return VectorArray(arrays)

    @staticmethod
    def _join(*values: Any) -> NDArray:
        return np.concatenate([FusionAccessor._to_sequence(value) for value in values])

    @staticmethod
    def _to_sequence(item: Any):
        if lib.is_list_like(item):
            return item

        return [item]
