import json
from typing import Any, Optional, Sequence
import polars as pl

@pl.api.register_dataframe_namespace("flatten")
class FlattenFrame:
    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df
    
    def _normalize_json_ordered(
        self,
        data: dict[str, Any], 
        separator: str, 
        max_level: int
    ) -> dict[str, Any]:
        """
        Order the top level keys and then recursively go to depth.

        Parameters
        ----------
        data
            dict or list of dicts
        separator
            str, default '.'
            Nested records will generate names separated by sep,
            e.g., for sep='.', { 'foo' : { 'bar' : 0 } } -> foo.bar
        max_level
            max recursing level

        Returns
        -------
        dict or list of dicts, matching `normalised_json_object`
        """
        
        #top_dict_ = {k: v for k, v in data.items() if not isinstance(v,dict) or not isinstance(v, list) }
        nested_dict_ = {
            k2: v2
            for k, v in data.items()
            for k2, v2 in (
                self.normalize_json(
                    data=v,
                    key_string=k,
                    normalized_dict={},
                    separator=separator,
                    max_level=max_level,
                ).items()
                if isinstance(v, (dict, list))
                else {k: v}.items()
            )
        }
        return {**nested_dict_}

    def _simple_json_normalize(
        self,
        data: dict[Any, Any] | Sequence[dict[Any, Any] | Any],
        separator: str,
        max_level: int,
    ) -> dict[Any, Any] | list[dict[Any, Any]] | Any:
        if max_level > 0:
            normalized_json_object = {}
            # expect a dictionary, as most jsons are. However, lists are perfectly valid
            if isinstance(data, dict):
                normalized_json_object = self._normalize_json_ordered(
                    data=data, separator=separator, max_level=max_level
                )
            
            elif isinstance(data, list):
                normalised_json_list = [
                    self._simple_json_normalize(row, separator=separator, max_level=max_level)
                    for row in data
                ]
                return normalised_json_list
            return normalized_json_object
        else:
            return data
        
    def normalize_json(
        self,
        data: Any,
        key_string: str,
        normalized_dict: dict[str, Any],
        separator: str,
        max_level: int,
    ) -> dict[str, Any]:
        """
        Main recursive function.

        Designed for the most basic use case of pl.json_normalize(data)
        intended as a performance improvement.

        Parameters
        ----------
        data : Any
            Type dependent on types contained within nested Json
        key_string : str
            New key (with separator(s) in) for data
        normalized_dict : dict
            The new normalized/flattened Json dict
        separator : str, default '.'
            Nested records will generate names separated by sep,
            e.g., for sep='.', { 'foo' : { 'bar' : 0 } } -> foo.bar
        max_level
            recursion depth
        """
        if isinstance(data, dict) and key_string in ['geometry']:
            for key, value in data.items():
                new_key = f"{key_string}{separator}{key}" if key_string else key
                if isinstance(value,dict):
                    self.normalize_json(
                        data= value,
                        key_string=new_key,
                        normalized_dict=normalized_dict,
                        separator=separator,
                        max_level=max_level - 1 if max_level > 0 else 0,
                    ) 
                else:
                    normalized_dict[new_key] = value
            return {**normalized_dict}
        elif isinstance(data, dict) and key_string in ['geometry']:
            normalized_dict[key_string] =  json.dumps(data)
            return {**normalized_dict}
        else:
            for i,v in enumerate(data):
                self.normalize_json(
                    data= v,
                    key_string=f"{key_string}{separator}{i}",
                    normalized_dict=normalized_dict,
                    separator=separator,
                    max_level=max_level - 1 if max_level > 0 else 0,
                ) 
        return normalized_dict
    
    def json_normalize(
        self,
        data: Optional[dict[Any, Any] | Sequence[dict[Any, Any] | Any]]=[],
        separator: str = "_",
        max_level: int = 10
    ) -> pl.DataFrame:
        """
        Normalize semi-structured deserialized JSON data into a flat table.

        Dictionary objects that will not be unnested/normalized are encoded
        as json string data. Unlike it pandas' counterpart, this function will
        not encode dictionaries as objects at any level.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        data
            Deserialized JSON objects.
        separator
            Nested records will generate names separated by sep. e.g.,
            for `separator=".", {"foo": {"bar": 0}}` -> foo.bar.
        max_level
            Max number of levels(depth of dict) to normalize.
            If None, normalizes all levels.
        schema
            Overwrite the `Schema` when the normalized data is passed to
            the `DataFrame` constructor.
        strict
            Whether Polars should be strict when constructing the DataFrame.
        infer_schema_length
            Number of rows to take into consideration to determine the schema.

        Examples
        --------
        >>> data = [
        ...     {
        ...         "id": 1,
        ...         "name": "Cole Volk",
        ...         "fitness": {"height": 130, "weight": 60},
        ...     },
        ...     {"name": "Mark Reg", "fitness": {"height": 130, "weight": 60}},
        ...     {
        ...         "id": 2,
        ...         "name": "Faye Raker",
        ...         "fitness": {"height": 130, "weight": 60},
        ...     },
        ... ]
        >>> pl.json_normalize(data, max_level=1)
        shape: (3, 4)
        ┌──────┬────────────┬────────────────┬────────────────┐
        │ id   ┆ name       ┆ fitness.height ┆ fitness.weight │
        │ ---  ┆ ---        ┆ ---            ┆ ---            │
        │ i64  ┆ str        ┆ i64            ┆ i64            │
        ╞══════╪════════════╪════════════════╪════════════════╡
        │ 1    ┆ Cole Volk  ┆ 130            ┆ 60             │
        │ null ┆ Mark Reg   ┆ 130            ┆ 60             │
        │ 2    ┆ Faye Raker ┆ 130            ┆ 60             │
        └──────┴────────────┴────────────────┴────────────────┘
        >>> pl.json_normalize(data, max_level=0)
        shape: (3, 3)
        ┌──────┬────────────┬───────────────────────────────┐
        │ id   ┆ name       ┆ fitness                       │
        │ ---  ┆ ---        ┆ ---                           │
        │ i64  ┆ str        ┆ str                           │
        ╞══════╪════════════╪═══════════════════════════════╡
        │ 1    ┆ Cole Volk  ┆ {"height": 130, "weight": 60} │
        │ null ┆ Mark Reg   ┆ {"height": 130, "weight": 60} │
        │ 2    ┆ Faye Raker ┆ {"height": 130, "weight": 60} │
        └──────┴────────────┴───────────────────────────────┘
        
        >>> pl.json_normalize(
                data= data
            ).flatten.json_normalize(data,max_level=1)

        """
        return pl.DataFrame(
            self._simple_json_normalize(data=data, separator=separator, max_level=max_level)
        )