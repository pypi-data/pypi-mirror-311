"""REST client handling, including DripStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class DripStream(RESTStream):
    """Drip stream class."""

    records_jsonpath = "$.campaigns[*]"
    next_page_token_jsonpath = "$.meta.pagination.page"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.getdrip.com/v2"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("access_token", ""),
        )

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = {}

        if next_page_token:
            params["page"] = next_page_token

        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        account_id = self.config["account_id"]

        for record in extract_jsonpath(self.records_jsonpath, input=response.json()):
            yield {**record, "profile_id": account_id}

    def get_next_page_token(
        self, response: requests.Response, previous_token: t.Any | None
    ) -> t.Any | None:
        """Return the next page token if available."""
        pagination = response.json().get("meta", {}).get("pagination", {})
        current_page = pagination.get("current_page")
        total_pages = pagination.get("total_pages")

        # If there are more pages, return the next page number
        if current_page and total_pages and current_page < total_pages:
            return current_page + 1
        return None

    def get_url(self, context: Context | None) -> str:
        """Construct the URL for the API request.

        Args:
            context: The stream context.

        Returns:
            Full URL for the request.
        """
        return self.url_base + self.path.format(account_id=self.config["account_id"])
