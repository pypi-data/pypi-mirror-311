from functools import cache
from typing import Any, Protocol, TypeVar, overload
from collections.abc import Generator, Iterable, Iterator

import requests


T = TypeVar("T", covariant=True)


def strjoin(*args: str, sep: str = "/") -> str:
    return sep.join(map(lambda x: str(x).rstrip(sep), filter(lambda x: any(s != sep for s in x) and len(x), args)))


class SizedIndexableIterable(Protocol[T]):
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T]: ...
    @overload
    def __getitem__(self, key: int) -> T: ...
    @overload
    def __getitem__(self, key: slice) -> "SizedIndexableIterable"[T]: ...


@cache
def make_request(url: str) -> requests.Response:
    return requests.get(url)


def chunk_iterable(iterable: SizedIndexableIterable[T], chunk_size: int = 1) -> Generator[Iterable[T], Any, Any]:
    start = 0
    while start < len(iterable):
        end = start + chunk_size
        yield iterable[start:end]
        start = end
