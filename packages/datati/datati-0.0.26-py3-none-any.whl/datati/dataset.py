from __future__ import annotations
import warnings

from pandas import DataFrame, Series
from pandas import Index
from pandas._libs import lib

warnings.simplefilter(action="ignore", category=UserWarning)

import copy
from typing import Optional, Dict, TypeVar, Sequence, Tuple, Literal, Callable, Hashable, Mapping

import numpy
import pandas
from pandas._typing import IgnoreRaise, Axes, Dtype
from datasets.arrow_dataset import Dataset as ArrowDataset
from datasets import load_dataset as load_huggingface_dataset


T = TypeVar("T")
S = TypeVar("S")


class Dataset(DataFrame):
    """Dataset class.

    Attributes:
        one_hot_encoding_dictionary: Encoding dictionary for one-hot variables.
        bins_encoding_dictionary: Encoding dictionary for binned variables.
        target_encoding_dictionary: Encoding dictionary for target variables.
        target_feature: The target feature of this dataset.
    """
    def __init__(self, dataset: Optional[ArrowDataset, numpy.ndarray, DataFrame, str] = None,
                 load_from: Optional[str] = None, config: Optional[str] = None, split: Optional[str] = "train",
                 target_feature: Optional[str] = None,
                 loading_options: Optional[Dict] = None):
        """Create a Dataset.

        Args:
            dataset: Name or path of the dataset. Use the path for local datasets.
            load_from: None for given datasets, one of "huggingface" or "local" otherwise.
            config: Configuration, used for Huggingface datasets.
            split: Split, used for Huggingface datasets.
            target_feature: Target feature of the dataset.
            loading_options: Keyword arguments provided to pandas.read_X for loading the dataset if local.
        """
        warnings.simplefilter(action="ignore", category=UserWarning)

        if load_from is not None:
            match load_from:
                case "huggingface":
                    df = load_huggingface_dataset(dataset, config)[split].to_pandas().infer_objects()
                    categorical_features = [f for f in df.columns
                                            if df.dtypes[f].name in ("object", "string", "category")]
                    df = df.astype({f: "category" for f in categorical_features})
                    super(Dataset, self).__init__(data=df)

                case "local":
                    suffix = dataset.split("."[-1])
                    loading_options = loading_options if loading_options is not None else dict()
                    match suffix:
                        case "csv":
                            df = pandas.read_csv(dataset, **loading_options).infer_objects()
                        case "json":
                            df = pandas.read_json(dataset, **loading_options).infer_objects()
                        case _:
                            raise ValueError(f"Unknown dataset extension: {suffix}")

                    categorical_features = [f for f in df.columns
                                            if df.dtypes[f].name in ("object", "string", "category")]
                    df = df.astype({f: "category" for f in categorical_features})
                    super(Dataset, self).__init__(data=df)
                case _:
                    raise NotImplementedError()
        else:
            if isinstance(dataset, Dataset):
                df = copy.deepcopy(dataset)
                super(Dataset, self).__init__(data=df.to_pandas())
                self.copy_metadata_from(dataset)

            elif isinstance(dataset, DataFrame):
                categorical_features = [f for f in dataset.columns
                                        if dataset.dtypes[f].name in ("object", "string", "category")]
                df = dataset.astype({f: "category" for f in categorical_features})
                super(Dataset, self).__init__(data=df)

            elif isinstance(dataset, numpy.ndarray):
                # can't use PA array since it can't handle non-numeric numpy arrays
                df = DataFrame(dataset).infer_objects()
                categorical_features = [f for f in df.dtypes
                                        if df.dtypes[f].name in ("object", "string", "category")]
                df = dataset.astype({f: "category" for f in categorical_features})
                super(Dataset, self).__init__(data=df)

            elif isinstance(dataset, ArrowDataset):
                df = dataset.to_pandas().infer_objects()
                categorical_features = [f for f in df.dtypes
                                        if df.dtypes[f].name in ("object", "string", "category")]
                df = df.astype({f: "category" for f in categorical_features})
                super(Dataset, self).__init__(data=df)
            else:
                raise ValueError(f"Invalid type: {type(dataset)}")

        self.target_feature = target_feature
        self.one_hot_encoding_dictionary = dict()
        self.bins_encoding_dictionary = dict()
        self.target_encoding_dictionary = dict()

    def __eq__(self, other):
        if not isinstance(other, Dataset):
            return False
        return len(self) == len(other) \
            and all(self.iloc[i] == other.iloc[i] for i in range(len(self)))

    def __hash__(self):
        return hash(str(self.to_pandas()))

    def __copy__(self, **kwargs) -> Dataset:
        dataset = Dataset(self.copy())
        dataset.copy_metadata_from(self)

        return dataset

    def __deepcopy__(self, memodict=None) -> Dataset:
        dataset = Dataset(self.copy())
        dataset.copy_metadata_from(self)

        return dataset

    def __getitem__(self, item):
        return super(Dataset, self).__getitem__(item)

    def __delitem__(self, key):
        new_dataframe = copy.deepcopy(self)
        new_dataframe.drop(key, axis="index", inplace=True)
        new_dataframe = Dataset(new_dataframe)
        new_dataframe.copy_metadata_from(self)

        return new_dataframe

    ################
    ## Conversion ##
    ################
    def to_pandas(self):
        return DataFrame(self)

    def to_array(self):
        return self.values

    def to_list(self):
        return [tuple(row) for row in self.itertuples()]

    ###########
    ## Types ##
    ###########

    def copy_metadata_from(self, dataset: Dataset) -> Dataset:
        """Copy metadata from the given dataset.

        Args:
            dataset: The dataset to copy metadata from.

        Returns:
            This dataset, with overwritten metadata.
        """
        self.bins_encoding_dictionary = copy.deepcopy(dataset.bins_encoding_dictionary)
        self.one_hot_encoding_dictionary = copy.deepcopy(dataset.one_hot_encoding_dictionary)
        self.target_encoding_dictionary = copy.deepcopy(dataset.target_encoding_dictionary)
        self.target_feature = copy.deepcopy(dataset.target_feature)

        return self

    def astype(self, dtype, copy: bool = True, errors: IgnoreRaise = "raise") -> Dataset:
        processed_dataset = Dataset(super(Dataset, self).astype(dtype))
        processed_dataset.copy_metadata_from(self)

        return processed_dataset

    @classmethod
    def from_dict(cls, data: dict, orient: str = "columns", dtype: Dtype | None = None,
                  columns: Axes | None = None) -> Dataset:
        return Dataset(DataFrame.from_dict(data, orient, dtype, columns))

    @classmethod
    def from_records(cls, data, index=None, exclude=None, columns=None, coerce_float: bool = False,
                     nrows: int | None = None) -> Dataset:
        return Dataset(DataFrame.from_records(data, index, exclude, columns, coerce_float, nrows))

    ################
    ## Data stuff ##
    ################
    def train_test_split(self, test_size: float = 0.2,
                         stratify: Optional[str | Sequence[str]] = None) -> Tuple[numpy.array, numpy.array]:
        """Split this dataset into two, possibly stratifying with a set of given features.

        Args:
            test_size: Size of the test set, in a [0, 1] percentage.
            stratify: Optional feature(s) to stratify the split.

        Returns:
            Indexes of each split.
        """
        df = self.to_pandas()
        nr_records = df.shape[0]
        if stratify is not None:
            unique_stratify_values, stratify_balance = numpy.unique(df[stratify].values, return_counts=True)
            stratify_balance = stratify_balance / len(self)
            indexes_per_value = [numpy.argwhere(df[stratify].values == stratify_value).squeeze()
                                  for stratify_value in unique_stratify_values]
            train_indexes = numpy.hstack([numpy.random.choice(indexes_of_value,
                                                              int(indexes_of_value.size * (1 - test_size)),
                                                              replace=False)
                                          for indexes_of_value, percentage in zip(indexes_per_value, stratify_balance)])
            test_indexes = numpy.array([i for i in range(nr_records) if i not in train_indexes])
        else:
            train_indexes = numpy.random.choice(numpy.arange(nr_records), nr_records * (1 - test_size))
            test_indexes = numpy.array([i for i in range(nr_records) if i not in train_indexes])
        indexes = (train_indexes, test_indexes)

        return indexes
