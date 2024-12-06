"""Stream type classes for tap-keyword."""

from __future__ import annotations
from singer_sdk import typing as th
from tap_keyword.client import KeywordStream


class KeywordStream(KeywordStream):
    """Define the keyword stream."""

    name = "keyword_keywords"
    path = "/groups/{project_name}/keywords/"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("type", th.StringType),
        th.Property("id", th.StringType, description="Unique keyword ID"),
        th.Property("attributes", th.ObjectType(additional_properties=True)),
        th.Property("profile_id", th.StringType),
    ).to_dict()
