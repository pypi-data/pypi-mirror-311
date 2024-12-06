"""REST client handling, including KeywordStream base class."""

from __future__ import annotations
import typing as t
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class KeywordStream(RESTStream):
    """Keyword stream class."""

    records_jsonpath = "$.data[*]"

    @property
    def url_base(self) -> str:
        """Return the base URL for the API."""
        return "https://app.keyword.com/api/v2"

    def get_url_params(
        self, context: Context | None, next_page_token: t.Any | None
    ) -> dict[str, t.Any]:
        """Return a dictionary of URL query parameters.

        Args:
            context: Stream context.
            next_page_token: Pagination token for next page.

        Returns:
            A dictionary of query parameters.
        """
        params = {
            "api_token": self.config["api_token"],  # Add API token as a query parameter
        }
        if next_page_token:
            params["page"] = next_page_token
        return params

    def prepare_request_headers(self, context: Context | None) -> dict[str, str]:
        """Prepare headers for the HTTP request."""
        return {
            "Accept": "application/json",
        }

    def get_next_page_token(
        self, response: t.Any, previous_token: t.Any | None
    ) -> t.Any | None:
        """Extract the next page token from the API response."""
        if response.json().get("meta", {}).get("pagination", {}).get(
            "current_page"
        ) < response.json().get("meta", {}).get("pagination", {}).get("total_pages"):
            return response.json()["meta"]["pagination"]["current_page"] + 1
        return None

    def parse_response(self, response: t.Any) -> t.Iterable[dict]:
        """Parse the API response.

        Args:
            response: The HTTP response object.

        Yields:
            Parsed records.
        """
        project_id = self.config["project_id"]

        for record in extract_jsonpath(self.records_jsonpath, input=response.json()):
            yield {**record, "profile_id": project_id}

    def get_url(self, context: Context | None) -> str:
        """Construct the URL for the API request.

        Args:
            context: The stream context.

        Returns:
            Full URL for the request.
        """
        return self.url_base + self.path.format(
            project_name=self.config["project_name"]
        )
