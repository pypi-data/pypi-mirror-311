class BigdataClientError(Exception):
    """
    Base exception for all BigdataClient exceptions.

    Contact support if this exception is raised.
    """

    pass


class RequestMaxLimitExceeds(BigdataClientError):
    """
    Request body size limit is set to 8KB (8192 bytes)
    In cases when request body size exceeds 8KB this exception will be thrown.

    Any method that sends requests can throw this exception.

    **Solution**: Please identify the method that caused the error and craft a smaller request.

    * **Search methods**: You could create several smaller and more concrete queries.
    * **Knowledge Graph methods or Watchlist methods**: You could split the list of parameters and call the same method multiple times.
    """

    def __init__(self, request_size: int, limit: int):
        super().__init__(f"Request body exceeds limit. Max Limit: {limit} bytes")
        self.request_size = request_size

    def __str__(self):
        return f"{self.args[0]} (Request Size: {self.request_size} bytes)"


class BigdataClientRateLimitError(BigdataClientError):
    """
    Too many requests in a short period of time. These are the current Bigdata.com platform rate limits:

    * 500 requests per minute per JWT session (We advise customers to instantiate a single Bigdata object per user).
    * 1500 requests per minute per IP.

    **Solution**: Adapt your code to make fewer requests.
    """
