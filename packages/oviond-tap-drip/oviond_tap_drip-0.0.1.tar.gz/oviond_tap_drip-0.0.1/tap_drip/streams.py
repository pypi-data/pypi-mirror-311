"""Stream type classes for tap-drip."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_drip.client import DripStream


class CampaignsStream(DripStream):
    """Define custom stream."""

    name = "drip_campaigns"
    path = "/{account_id}/campaigns"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="Unique ID of the campaign"),
        th.Property("status", th.StringType, description="Status of the campaign"),
        th.Property("name", th.StringType, description="Name of the campaign"),
        th.Property("from_name", th.StringType, description="Name of the sender"),
        th.Property(
            "from_email", th.StringType, description="Email address of the sender"
        ),
        th.Property(
            "postal_address", th.StringType, description="Postal address of the sender"
        ),
        th.Property(
            "minutes_from_midnight",
            th.IntegerType,
            description="Number of minutes from midnight when sending starts",
        ),
        th.Property(
            "localize_sending_time",
            th.BooleanType,
            description="Indicates if sending time is localized",
        ),
        th.Property(
            "days_of_the_week_mask",
            th.StringType,
            description="Mask representing days of the week for sending",
        ),
        th.Property(
            "start_immediately",
            th.BooleanType,
            description="Indicates if the campaign starts immediately",
        ),
        th.Property(
            "double_optin",
            th.BooleanType,
            description="Indicates if double opt-in is enabled",
        ),
        th.Property(
            "send_to_confirmation_page",
            th.BooleanType,
            description="Indicates if subscribers are sent to a confirmation page",
        ),
        th.Property(
            "use_custom_confirmation_page",
            th.BooleanType,
            description="Indicates if a custom confirmation page is used",
        ),
        th.Property(
            "confirmation_url",
            th.StringType,
            description="URL of the custom confirmation page, if used",
        ),
        th.Property(
            "notify_subscribe_email",
            th.StringType,
            description="Email address to notify for subscriptions",
        ),
        th.Property(
            "notify_unsubscribe_email",
            th.StringType,
            description="Email address to notify for unsubscriptions",
        ),
        th.Property(
            "bcc",
            th.StringType,
            description="BCC email address, if any",
            nullable=True,
        ),
        th.Property(
            "email_count",
            th.IntegerType,
            description="Number of emails in the campaign",
        ),
        th.Property(
            "active_subscriber_count",
            th.IntegerType,
            description="Number of active subscribers",
        ),
        th.Property(
            "unsubscribed_subscriber_count",
            th.IntegerType,
            description="Number of unsubscribed subscribers",
        ),
        th.Property(
            "created_at",
            th.StringType,
            description="Timestamp of when the campaign was created",
        ),
        th.Property(
            "href",
            th.StringType,
            description="Link to the campaign resource",
        ),
        th.Property("links", th.ObjectType(additional_properties=True)),
        th.Property(
            "profile_id",
            th.StringType,
            description="Unique ID of the profile associated with the campaign",
        ),
    ).to_dict()
