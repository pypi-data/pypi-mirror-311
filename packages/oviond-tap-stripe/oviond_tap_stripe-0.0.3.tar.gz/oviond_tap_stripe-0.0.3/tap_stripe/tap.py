"""Stripe tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th
from tap_stripe import streams


class TapStripe(Tap):
    """Stripe tap class."""

    name = "tap-stripe"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "secret_key",
            th.StringType,
            required=True,
            secret=True,
            title="Secret key",
            description="The Stripe secret key to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            title="Start Date",
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.StripeStream]:
        """Return a list of discovered streams."""
        return [
            streams.SubscriptionsStream(self),
            streams.BalanceTransactionsStream(self),
            streams.CustomersStream(self),
        ]


if __name__ == "__main__":
    TapStripe.cli()
