"""Drip tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_drip import streams


class TapDrip(Tap):
    """Drip tap class."""

    name = "tap-drip"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            title="Access Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "account_id",
            th.StringType,
            required=True,
            title="Account ID",
            description="The account ID to extract data against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.DripStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self),
        ]


if __name__ == "__main__":
    TapDrip.cli()
