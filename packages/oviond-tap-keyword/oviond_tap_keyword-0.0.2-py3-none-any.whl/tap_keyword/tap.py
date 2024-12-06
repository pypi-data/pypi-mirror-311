"""keyword tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_keyword import streams


class TapKeyword(Tap):
    """Keyword tap class."""

    name = "tap-keyword"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_token",
            th.StringType,
            required=True,
            secret=True,
            title="API Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "project_id",
            th.StringType,
            required=True,
            title="Project ID",
            description="ID of the project or group being tracked.",
        ),
        th.Property(
            "project_name",
            th.StringType,
            required=True,
            title="Project Name",
            description="Name of the project or group being tracked.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.KeywordStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.KeywordStream(self),
        ]


if __name__ == "__main__":
    TapKeyword.cli()
