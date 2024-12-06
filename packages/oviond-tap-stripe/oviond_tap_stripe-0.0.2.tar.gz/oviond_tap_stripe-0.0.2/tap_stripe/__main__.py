"""Stripe entry point."""

from __future__ import annotations

from tap_stripe.tap import TapStripe

TapStripe.cli()
