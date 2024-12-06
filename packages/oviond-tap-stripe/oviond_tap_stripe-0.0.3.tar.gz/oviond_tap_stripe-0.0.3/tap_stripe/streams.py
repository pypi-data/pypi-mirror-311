"""Stream type classes for tap-stripe."""

from __future__ import annotations
from tap_stripe.client import StripeStream
from singer_sdk import typing as th


class SubscriptionsStream(StripeStream):
    """Stream for fetching Stripe subscriptions."""

    name = "stripe_subscriptions"
    path = "subscriptions"
    primary_keys = ["id"]
    replication_key = "created"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("object", th.StringType),
        th.Property("application", th.StringType),
        th.Property("application_fee_percent", th.NumberType),
        th.Property(
            "automatic_tax",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("billing_cycle_anchor", th.IntegerType),
        th.Property("billing_thresholds", th.ObjectType(additional_properties=True)),
        th.Property("cancel_at", th.IntegerType),
        th.Property("cancel_at_period_end", th.BooleanType),
        th.Property("canceled_at", th.IntegerType),
        th.Property(
            "cancellation_details",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("collection_method", th.StringType),
        th.Property("created", th.IntegerType),
        th.Property("currency", th.StringType),
        th.Property("current_period_end", th.IntegerType),
        th.Property("current_period_start", th.IntegerType),
        th.Property("customer", th.StringType),
        th.Property("days_until_due", th.IntegerType),
        th.Property("default_payment_method", th.StringType),
        th.Property("default_source", th.StringType),
        th.Property(
            "default_tax_rates",
            th.ArrayType(
                th.ObjectType(additional_properties=True),
            ),
        ),
        th.Property("description", th.StringType),
        th.Property("discount", th.ObjectType(additional_properties=True)),
        th.Property("discounts", th.ArrayType(th.StringType)),
        th.Property("ended_at", th.IntegerType),
        th.Property(
            "invoice_settings",
            th.ObjectType(additional_properties=True),
        ),
        th.Property(
            "items",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("latest_invoice", th.StringType),
        th.Property("livemode", th.BooleanType),
        th.Property("metadata", th.ObjectType(additional_properties=True)),
        th.Property("next_pending_invoice_item_invoice", th.StringType),
        th.Property("on_behalf_of", th.StringType),
        th.Property("pause_collection", th.ObjectType(additional_properties=True)),
        th.Property(
            "payment_settings",
            th.ObjectType(additional_properties=True),
        ),
        th.Property(
            "pending_invoice_item_interval", th.ObjectType(additional_properties=True)
        ),
        th.Property("pending_setup_intent", th.StringType),
        th.Property("pending_update", th.ObjectType(additional_properties=True)),
        th.Property("schedule", th.ObjectType(additional_properties=True)),
        th.Property("start_date", th.IntegerType),
        th.Property("status", th.StringType),
        th.Property("test_clock", th.ObjectType(additional_properties=True)),
        th.Property("transfer_data", th.ObjectType(additional_properties=True)),
        th.Property("trial_end", th.IntegerType),
        th.Property(
            "trial_settings",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("trial_start", th.IntegerType),
    ).to_dict()


class BalanceTransactionsStream(StripeStream):
    """Stream for fetching Stripe balance transactions."""

    name = "stripe_balance_transactions"
    path = "balance_transactions"
    primary_keys = ["id"]
    replication_key = "created"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("object", th.StringType),
        th.Property("amount", th.IntegerType),
        th.Property("available_on", th.IntegerType),
        th.Property("created", th.IntegerType),
        th.Property("currency", th.StringType),
        th.Property("description", th.StringType),
        th.Property("exchange_rate", th.NumberType),
        th.Property(
            "fee_details",
            th.ArrayType(th.ObjectType(additional_properties=True)),
        ),
        th.Property("fee", th.IntegerType),
        th.Property("net", th.IntegerType),
        th.Property(
            "reporting_category",
            th.StringType,
        ),
        th.Property("source", th.ObjectType(additional_properties=True)),
        th.Property("status", th.StringType),
        th.Property(
            "type",
            th.StringType,
        ),
    ).to_dict()


class CustomersStream(StripeStream):
    """Stream for fetching Stripe customers."""

    name = "stripe_customers"
    path = "customers"
    primary_keys = ["id"]
    replication_key = "created"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("object", th.StringType),
        th.Property("address", th.ObjectType(additional_properties=True)),
        th.Property("balance", th.IntegerType),
        th.Property("created", th.IntegerType),
        th.Property("currency", th.StringType),
        th.Property("default_source", th.StringType),
        th.Property("delinquent", th.BooleanType),
        th.Property("description", th.StringType),
        th.Property("discount", th.ObjectType(additional_properties=True)),
        th.Property("email", th.StringType),
        th.Property("invoice_prefix", th.StringType),
        th.Property(
            "invoice_settings",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("livemode", th.BooleanType),
        th.Property("metadata", th.ObjectType(additional_properties=True)),
        th.Property("name", th.StringType),
        th.Property("next_invoice_sequence", th.IntegerType),
        th.Property("phone", th.StringType),
        th.Property(
            "preferred_locales",
            th.ArrayType(th.StringType),
        ),
        th.Property("shipping", th.ObjectType(additional_properties=True)),
        th.Property("tax_exempt", th.StringType),
        th.Property("test_clock", th.StringType),
    ).to_dict()
