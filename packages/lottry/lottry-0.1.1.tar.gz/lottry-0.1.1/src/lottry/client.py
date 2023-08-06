import random
from abc import ABC, abstractmethod
from json import JSONDecodeError
from time import sleep
from typing import Optional, List, Type

import httpx
from httpx import Response, TimeoutException, HTTPError
from pydantic import ValidationError

from lottry.model.exceptions import LotrApiBusy, LotrNotFound, LotrServerError, LotrClientException, LotrApiException, \
    LotrProtocolError
from lottry.model.response import ApiResponse, PagedResource, Page
from lottry.querying.pagination import PageQuery
from lottry.querying.search import Search
from lottry.querying.sort import Sort


class Backoff(ABC):
    @abstractmethod
    def next_wait_period(self) -> float:
        ...


class ConstantBackoff(Backoff):
    def __init__(self, backoff_window: float = 5.0):
        self.backoff_window = backoff_window

    def next_wait_period(self) -> float:
        return self.backoff_window + 2 * random.random()


class ExponentialBackoff(Backoff):

    def __init__(self, base: int = 2):
        self.base = base
        self.iteration = 0
        self.step = 0.512

    def next_wait_period(self) -> float:
        limit = self.base ** self.iteration
        self.iteration += 1
        factor = random.randint(0, limit)
        return factor * self.step + 2 * random.random()


class ClientParams:

    def __init__(self, timeout: int = 30, max_retries: Optional[int] = 0, backoff: Type[Backoff] = ExponentialBackoff):
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_strategy = backoff


class Translator:

    def prepare_call(
            self,
            base_url: str,
            id: Optional[str] = None,
            search: Optional[List[Search]] = None,
            sort: Optional[Sort] = None,
            pagination: Optional[PageQuery] = None
    ) -> str:
        url = base_url
        if id:
            url = url + f"/{id}"
        query_params = []
        if search:
            for expr in search:
                query_params.append(expr.expression())
        if sort:
            query_params.append(sort.expression())
        if pagination:
            query_params += pagination.page_query()
        url = url + "?" + "&".join(query_params) if query_params else url
        return url

    def parse_response(self, response: Response) -> PagedResource:
        if not response.is_success:
            status_code = response.status_code
            if status_code == 429:
                raise LotrApiBusy()
            elif status_code == 404:
                raise LotrNotFound()
            else:
                raise LotrServerError()
        try:
            json = response.json()
            raw_response = ApiResponse.parse_obj(json)
            return PagedResource(
                docs=raw_response.docs,
                pagination=Page(
                    limit=raw_response.limit,
                    offset=raw_response.offset,
                    page=raw_response.page,
                    pages=raw_response.pages,
                    total=raw_response.total,
                )
            )
        except ValidationError:
            raise LotrClientException()
        except JSONDecodeError:
            raise LotrClientException()


class LotrClient:
    def __init__(self, *, base_url: str, version: int, token: str,
                 client_params: Optional[ClientParams] = ClientParams()):
        self.base_url = f"{base_url}/v{version}"
        self.translator = Translator()
        self.client_params = client_params
        self.token = {"Authorization": f"Bearer {token}"}

    def _get(self, url) -> Response:
        backoff = self.client_params.backoff_strategy()
        retries = 0
        max_retries = max(self.client_params.max_retries, 1)
        while retries < max_retries:
            retries += 1
            try:
                with httpx.Client(timeout=self.client_params.timeout) as client:
                    return client.get(url, headers=self.token)
            except TimeoutException:
                if retries >= max_retries:
                    raise LotrApiException()
            except HTTPError:
                if retries >= max_retries:
                    raise LotrProtocolError()
            to_sleep = backoff.next_wait_period()
            sleep(to_sleep)

    def get_movie(
            self,
            *,
            id: Optional[str] = None,
            search: Optional[List[Search]] = None,
            sort: Optional[Sort] = None,
            pagination: Optional[PageQuery] = None
    ) -> PagedResource:
        url = self.translator.prepare_call(f"{self.base_url}/movie", id, search, sort, pagination)
        raw_response = self.translator.parse_response(self._get(url))
        return raw_response

    def get_quotes_from_movie(
            self,
            *,
            movie_id: str,
            search: Optional[List[Search]] = None,
            sort: Optional[Sort] = None,
            pagination: Optional[PageQuery] = None
    ) -> PagedResource:
        url = self.translator.prepare_call(
            f"{self.base_url}/movie/{movie_id}/quote",
            search=search,
            sort=sort,
            pagination=pagination
        )
        raw_response = self.translator.parse_response(self._get(url))
        return raw_response

    def get_quote(
            self,
            *, id: str = None,
            search: Optional[List[Search]] = None,
            sort: Optional[Sort] = None,
            pagination: Optional[PageQuery] = None
    ) -> PagedResource:
        url = self.translator.prepare_call(
            f"{self.base_url}/quote",
            id,
            search,
            sort,
            pagination
        )
        raw_response = self.translator.parse_response(self._get(url))
        return raw_response
