import csv
import dataclasses
import gzip
from io import StringIO
from typing import Any, Callable, Dict, Iterator, List, Literal, Optional, Tuple, Type, TypeVar, Union, overload

from requests import Session

from queuery_client.cast import cast_row
from queuery_client.util import SizedIterator

try:
    import pandas
except ModuleNotFoundError:
    pandas = None


T = TypeVar("T")


@dataclasses.dataclass
class ResponseBody:
    id: int
    data_file_urls: List[str]
    error: Optional[str]
    status: str
    manifest_file_url: Optional[str] = None

    @classmethod
    def from_dict(cls, params: Dict[str, Any]) -> "ResponseBody":
        properties = set(field.name for field in dataclasses.fields(cls))
        params = {key: value for key, value in params.items() if key in properties}
        return cls(**params)


class Response:
    def __init__(
        self,
        response: ResponseBody,
        enable_cast: bool = False,
        session: Optional[Session] = None,
        use_manifest: Optional[bool] = None,
    ):
        if enable_cast and use_manifest is False:
            raise ValueError("enable_cast is not available when use_manifest is False.")

        self._response = response
        self._data_file_urls = response.data_file_urls
        self._parser = csv.reader
        self._session = Session()
        self._enable_cast = enable_cast
        self._use_manifest = use_manifest or enable_cast
        self._manifest: Optional[Dict[str, Any]] = None

    def __iter__(self) -> Iterator[List[Any]]:
        def get_iterator() -> Iterator[List[Any]]:
            for url in self._data_file_urls:
                for row in self._open(url):
                    if self._enable_cast:
                        yield cast_row(row, self.fetch_manifest())
                    else:
                        yield row

        if self._use_manifest:
            record_count = self.fetch_record_count()
            return SizedIterator(get_iterator(), record_count)

        return get_iterator()

    def _open(self, url: str) -> List[List[str]]:
        data = self._session.get(url).content
        response = gzip.decompress(data).decode()
        reader = csv.reader(StringIO(response), escapechar="\\")
        return list(reader)

    def fetch_manifest(self, force: bool = False) -> Dict[str, Any]:
        if not self._use_manifest:
            raise RuntimeError("Manifest file is not available.")
        if self._manifest is None or force:
            if not self._response.manifest_file_url:
                raise RuntimeError(
                    "Manifest is not available because response does not contain manifest_file_url."
                )

            manifest = self._session.get(self._response.manifest_file_url).json()
            assert isinstance(manifest, dict)
            self._manifest = manifest
        return self._manifest

    def fetch_record_count(self) -> int:
        manifest = self.fetch_manifest()
        return int(manifest["meta"]["record_count"])

    def fetch_column_names(self) -> List[str]:
        manifest = self.fetch_manifest()
        return [x["name"] for x in manifest["schema"]["elements"]]

    @overload
    def read(self) -> List[List[Any]]:
        ...

    @overload
    def read(self, use_pandas: Literal[True]) -> "pandas.DataFrame":
        ...

    @overload
    def read(self, use_pandas: Literal[False]) -> List[List[Any]]:
        ...

    def read(
        self,
        use_pandas: bool = False,
    ) -> Union[List[List[Any]], "pandas.DataFrame"]:
        elems = list(self)

        if use_pandas:
            if pandas is None:
                raise ModuleNotFoundError(
                    "pandas is not availabe. Please make sure that "
                    "pandas is successfully installed to use use_pandas option."
                )

            if self._use_manifest:
                return pandas.DataFrame(elems, columns=self.fetch_column_names())

            return pandas.DataFrame(elems)

        return elems

    def map(self, target: Union[Type[T], Callable[..., T]]) -> Iterator[T]:
        column_names = self.fetch_column_names() if self._use_manifest else None

        def convert_to_args(row: List[Any]) -> Tuple[List[Any], Dict[str, Any]]:
            if column_names is None:
                return row, {}
            return [], {name: value for name, value in zip(column_names, row)}

        def map_to_target(row: List[Any]) -> T:
            args, kwargs = convert_to_args(row)
            return target(*args, **kwargs)

        iterator = map(map_to_target, self)

        if self._use_manifest:
            record_count = self.fetch_record_count()
            return SizedIterator(iterator, record_count)

        return iterator
