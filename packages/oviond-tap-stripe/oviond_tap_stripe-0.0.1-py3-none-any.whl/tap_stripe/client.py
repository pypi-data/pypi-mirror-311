"""REST client handling, including StripeStream base class."""

from __future__ import annotations
from typing import Any, Iterable, Optional
from singer_sdk.streams import Stream
from datetime import datetime, timezone
from singer_sdk.helpers.jsonpath import extract_jsonpath
import stripe


class StripeStream(Stream):
    """Base class for Stripe streams."""

    records_jsonpath = "$.data[*]"

    @property
    def stripe_client(self) -> stripe:
        """Initialize and return a Stripe client."""
        stripe.api_key = self.config["secret_key"]
        return stripe

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Fetch records from the Stripe API using the client library."""

        # Pagination parameters
        params = {"limit": 100}

        # Map specific resources explicitly
        if self.path == "subscriptions":
            params["status"] = "all"
            api_function = self.stripe_client.Subscription
        elif self.path == "balance_transactions":
            params["expand"] = ["data.source"]
            api_function = self.stripe_client.BalanceTransaction
        else:
            raise ValueError(f"Unknown path: {self.path}")

        # Include start_date from config if present
        if "start_date" in self.config:
            params["created"] = {
                "gte": int(
                    datetime.fromisoformat(self.config["start_date"]).timestamp()
                )
            }

        # Include replication key value if present (for incremental sync)
        if self.replication_key and self.get_starting_replication_key_value(context):
            replication_value = self.get_starting_replication_key_value(context)
            if isinstance(replication_value, str):
                replication_value = int(
                    datetime.fromisoformat(replication_value).timestamp()
                )
            params["created"]["gte"] = replication_value

        # Fetch paginated data
        while True:
            response = api_function.list(**params)
            records = response["data"]

            # Sort records by `created` field
            # sorted_records = sorted(records, key=lambda x: x["created"])

            # Yield each record in the response
            for record in records:
                yield record

            # Handle pagination: Check if there’s a `has_more` flag
            if response.get("has_more"):
                params["starting_after"] = records[-1]["id"]
            else:
                break

    def parse_response(self, response: Any) -> Iterable[dict]:
        """No parsing needed; data is directly handled in `get_records`."""
        yield from extract_jsonpath(self.records_jsonpath, input=response)
