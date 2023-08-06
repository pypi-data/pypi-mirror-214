# Lord of the Rings SDK

This SDK covers the movie and quote endpoints of the lord of the rings SDK that is at https://the-one-api.dev.

To install the package run pip install lottry.

## Usage

### The client

The API access sits behind the `LotrClient` class. This is a sync client. To instantiate one provide the
base url, the api version, the access token and optionally the client params.

```python
    client = LotrClient(
        base_url="https://the-one-api.dev",
        version=2,
        token="<token>",
        client_params=ClientParams(
            timeout=10,
            max_retries=3
        )
    )
```

The `ClientParams` class allows control to the timeout, the retry count and the retry strategy. The former
two can be any positive integer, while the latter is either `ConstantBackoff` or `ExponentialBackoff`.
Retry applies to transport layer errors and timeouts only, you should handle the retry logic of any applicaiton 
layer issues.

### Exceptions

The two main exception groups are `LotrApiException` and `LotrProtocolError`. `LotrApiException` has 
many subclasses covering the specific cases that can happen, see the code for more information.
`LotrProtocolError` is only thrown if the client couldn't get an HTTP response from the API due to transport
layer errors before the retries ran out.

### Simple examples

All API calls return the response documents in the `docs` array and
all pagination related data in the `pagination` field.


Get all/one movie:

```python
    client.get_movie()
    client.get_movie(id="5cd95395de30eff6ebccde58")
```

Get the quotes of a movie:

```python
    client.get_quotes_from_movie(movie_id="5cd95395de30eff6ebccde58")
        # movie_id="5cd95395de30eff6ebccde58",
        pagination=PageQuery(limit=2, page=2),
    )
```
Get all/one quote:

```python
    client.get_quote()
    client.get_quote(id="5cd96e05de30eff6ebcce7ec")
```

### Paging, sorting, filtering

You can apply filers, sorting and pagination to the queries. These follow a functional style where all these
operators are basically "functors". The actual full signature of all access operations include the arguments
to incorporate these operators. Concretely:

```python
    def get_quotes_from_movie(
            self, 
            *,
            movie_id: str,
            search: Optional[List[Search]] = None,
            sort: Optional[Sort] = None,
            pagination: Optional[PageQuery] = None
    ) -> PagedResource
```

If any of those are set, the arguments are translated to the format of the API and added to the call. 
An example to get some movies sorted, filtered and paginated. In this case 
1. all movies are returned that are shorter than 201 minutes
2. results are sorted by length ascending
3. and we requested the second page with the length of 2 entities.

```python
    client.get_movie(
        search=[LessThanEq(key="runtimeInMinutes", condition="200")],
        pagination=PageQuery(limit=2, page=2),
        sort=SortAsc(key="runtimeInMinutes")
    )
```

