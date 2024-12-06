"""Stream type classes for tap-mailchimp."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_mailchimp.client import MailchimpStream


class CampaignsStream(MailchimpStream):
    """Define custom stream."""

    name = "mailchimp_campaigns"
    path = "/reports"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.campaigns[*]"
    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="Unique ID of the campaign"),
        th.Property("web_id", th.IntegerType, description="Web ID of the campaign"),
        th.Property(
            "parent_campaign_id",
            th.StringType,
            description="Parent campaign ID if applicable",
            nullable=True,
        ),
        th.Property(
            "type", th.StringType, description="Type of campaign (e.g., regular)"
        ),
        th.Property(
            "create_time",
            th.StringType,
            description="Timestamp of when the campaign was created",
        ),
        th.Property(
            "archive_url",
            th.StringType,
            description="URL to the campaign archive",
        ),
        th.Property(
            "long_archive_url",
            th.StringType,
            description="Long URL to the campaign archive",
        ),
        th.Property("status", th.StringType, description="Status of the campaign"),
        th.Property("emails_sent", th.IntegerType, description="Number of emails sent"),
        th.Property(
            "send_time",
            th.StringType,
            description="Timestamp of when the campaign was sent",
            nullable=True,
        ),
        th.Property(
            "content_type",
            th.StringType,
            description="Content type of the campaign",
        ),
        th.Property(
            "needs_block_refresh",
            th.BooleanType,
            description="Indicates if blocks need refreshing",
        ),
        th.Property(
            "resendable",
            th.BooleanType,
            description="Indicates if the campaign is resendable",
        ),
        th.Property(
            "recipients",
            th.ObjectType(
                th.Property("list_id", th.StringType, description="List ID"),
                th.Property(
                    "list_is_active",
                    th.BooleanType,
                    description="Indicates if the list is active",
                ),
                th.Property("list_name", th.StringType, description="Name of the list"),
                th.Property(
                    "segment_text",
                    th.StringType,
                    description="Description of the segment",
                    nullable=True,
                ),
                th.Property(
                    "recipient_count",
                    th.IntegerType,
                    description="Count of recipients",
                ),
                th.Property(
                    "segment_opts",
                    th.ObjectType(
                        th.Property(
                            "saved_segment_id",
                            th.IntegerType,
                            description="ID of the saved segment",
                            nullable=True,
                        ),
                        th.Property(
                            "prebuilt_segment_id",
                            th.StringType,
                            description="ID of the prebuilt segment",
                            nullable=True,
                        ),
                        th.Property(
                            "match",
                            th.StringType,
                            description="Match type for the segment",
                            nullable=True,
                        ),
                        th.Property(
                            "conditions",
                            th.ArrayType(th.StringType),
                            description="Conditions for the segment",
                            nullable=True,
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "settings",
            th.ObjectType(
                th.Property("subject_line", th.StringType, description="Subject line"),
                th.Property("preview_text", th.StringType, description="Preview text"),
                th.Property(
                    "title", th.StringType, description="Title of the campaign"
                ),
                th.Property("from_name", th.StringType, description="Sender name"),
                th.Property("reply_to", th.StringType, description="Reply-to email"),
                th.Property(
                    "use_conversation",
                    th.BooleanType,
                    description="Use conversation mode",
                ),
                th.Property("to_name", th.StringType, description="Recipient name"),
                th.Property("folder_id", th.StringType, description="Folder ID"),
                th.Property(
                    "authenticate", th.BooleanType, description="Authenticate emails"
                ),
                th.Property(
                    "auto_footer", th.BooleanType, description="Auto footer enabled"
                ),
                th.Property(
                    "inline_css", th.BooleanType, description="Inline CSS enabled"
                ),
                th.Property(
                    "auto_tweet", th.BooleanType, description="Auto tweet enabled"
                ),
                th.Property(
                    "auto_fb_post",
                    th.ArrayType(th.StringType),
                    description="Facebook post configuration",
                    nullable=True,
                ),
                th.Property(
                    "fb_comments",
                    th.BooleanType,
                    description="Facebook comments enabled",
                ),
                th.Property("timewarp", th.BooleanType, description="Timewarp enabled"),
                th.Property("template_id", th.IntegerType, description="Template ID"),
                th.Property(
                    "drag_and_drop", th.BooleanType, description="Drag-and-drop enabled"
                ),
            ),
        ),
        th.Property(
            "tracking",
            th.ObjectType(
                th.Property("opens", th.BooleanType, description="Track opens"),
                th.Property(
                    "html_clicks", th.BooleanType, description="Track HTML clicks"
                ),
                th.Property(
                    "text_clicks", th.BooleanType, description="Track text clicks"
                ),
                th.Property(
                    "goal_tracking", th.BooleanType, description="Goal tracking enabled"
                ),
                th.Property(
                    "ecomm360", th.BooleanType, description="eCommerce tracking enabled"
                ),
                th.Property(
                    "google_analytics",
                    th.StringType,
                    description="Google Analytics tracking ID",
                    nullable=True,
                ),
                th.Property(
                    "clicktale",
                    th.StringType,
                    description="ClickTale tracking ID",
                    nullable=True,
                ),
                th.Property(
                    "salesforce",
                    th.ObjectType(
                        th.Property("campaign", th.BooleanType),
                        th.Property("notes", th.BooleanType),
                    ),
                ),
                th.Property(
                    "capsule",
                    th.ObjectType(
                        th.Property("notes", th.BooleanType),
                    ),
                ),
            ),
        ),
        th.Property(
            "rss_opts",
            th.ObjectType(
                th.Property("feed_url", th.StringType),
                th.Property("frequency", th.StringType),
                th.Property(
                    "schedule",
                    th.ObjectType(
                        th.Property("hour", th.IntegerType),
                        th.Property(
                            "daily_send",
                            th.ObjectType(
                                th.Property("sunday", th.BooleanType),
                                th.Property("monday", th.BooleanType),
                                th.Property("tuesday", th.BooleanType),
                                th.Property("wednesday", th.BooleanType),
                                th.Property("thursday", th.BooleanType),
                                th.Property("friday", th.BooleanType),
                                th.Property("saturday", th.BooleanType),
                            ),
                        ),
                        th.Property("weekly_send_day", th.StringType),
                        th.Property("monthly_send_date", th.IntegerType),
                    ),
                ),
                th.Property("last_sent", th.StringType),
                th.Property("constrain_rss_img", th.BooleanType),
            ),
        ),
        th.Property(
            "report_summary",
            th.ObjectType(
                th.Property("opens", th.IntegerType),
                th.Property("unique_opens", th.IntegerType),
                th.Property("open_rate", th.NumberType),
                th.Property("clicks", th.IntegerType),
                th.Property("subscriber_clicks", th.IntegerType),
                th.Property("click_rate", th.NumberType),
                th.Property(
                    "ecommerce",
                    th.ObjectType(
                        th.Property("total_orders", th.IntegerType),
                        th.Property("total_spent", th.NumberType),
                        th.Property("total_revenue", th.NumberType),
                    ),
                ),
            ),
        ),
        th.Property(
            "delivery_status",
            th.ObjectType(
                th.Property("enabled", th.BooleanType),
                th.Property("can_cancel", th.BooleanType),
                th.Property("status", th.StringType),
                th.Property("emails_sent", th.IntegerType),
                th.Property("emails_canceled", th.IntegerType),
            ),
        ),
        th.Property("_links", th.ArrayType(th.ObjectType(additional_properties=True))),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class AudiencesStream(MailchimpStream):
    """Define custom stream."""

    name = "mailchimp_lists"
    path = "/lists"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.lists[*]"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique ID for the list",
        ),
        th.Property(
            "web_id",
            th.IntegerType,
            description="Web ID for the list",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Name of the list",
        ),
        th.Property(
            "contact",
            th.ObjectType(
                th.Property("company", th.StringType, description="Company name"),
                th.Property("address1", th.StringType, description="Address line 1"),
                th.Property("address2", th.StringType, description="Address line 2"),
                th.Property("city", th.StringType, description="City"),
                th.Property("state", th.StringType, description="State"),
                th.Property("zip", th.StringType, description="Postal code"),
                th.Property("country", th.StringType, description="Country"),
                th.Property("phone", th.StringType, description="Phone number"),
            ),
        ),
        th.Property(
            "permission_reminder",
            th.StringType,
            description="Permission reminder text for the list",
        ),
        th.Property(
            "use_archive_bar",
            th.BooleanType,
            description="Whether the archive bar is used",
        ),
        th.Property(
            "campaign_defaults",
            th.ObjectType(
                th.Property(
                    "from_name", th.StringType, description="Default sender name"
                ),
                th.Property(
                    "from_email", th.StringType, description="Default sender email"
                ),
                th.Property(
                    "subject", th.StringType, description="Default subject line"
                ),
                th.Property("language", th.StringType, description="Default language"),
            ),
        ),
        th.Property(
            "notify_on_subscribe",
            th.BooleanType,
            description="Whether notifications are sent on subscription",
        ),
        th.Property(
            "notify_on_unsubscribe",
            th.BooleanType,
            description="Whether notifications are sent on unsubscription",
        ),
        th.Property(
            "date_created",
            th.StringType,
            description="Date and time when the list was created",
        ),
        th.Property(
            "list_rating",
            th.IntegerType,
            description="The list rating",
        ),
        th.Property(
            "email_type_option",
            th.BooleanType,
            description="Whether the list supports email type options",
        ),
        th.Property(
            "subscribe_url_short",
            th.StringType,
            description="Short URL for subscription",
        ),
        th.Property(
            "subscribe_url_long",
            th.StringType,
            description="Long URL for subscription",
        ),
        th.Property(
            "beamer_address",
            th.StringType,
            description="Beamer address for the list",
        ),
        th.Property(
            "visibility",
            th.StringType,
            description="Visibility of the list (e.g., pub)",
        ),
        th.Property(
            "double_optin",
            th.BooleanType,
            description="Whether double opt-in is enabled",
        ),
        th.Property(
            "has_welcome",
            th.BooleanType,
            description="Whether the list has a welcome email",
        ),
        th.Property(
            "marketing_permissions",
            th.BooleanType,
            description="Whether the list uses marketing permissions",
        ),
        th.Property(
            "modules",
            th.ArrayType(th.StringType),
            description="Modules associated with the list",
        ),
        th.Property(
            "stats",
            th.ObjectType(
                th.Property(
                    "member_count", th.IntegerType, description="Total members"
                ),
                th.Property(
                    "total_contacts", th.IntegerType, description="Total contacts"
                ),
                th.Property(
                    "unsubscribe_count",
                    th.IntegerType,
                    description="Total unsubscribed contacts",
                ),
                th.Property(
                    "cleaned_count",
                    th.IntegerType,
                    description="Total cleaned contacts",
                ),
                th.Property(
                    "member_count_since_send",
                    th.IntegerType,
                    description="Members added since last campaign",
                ),
                th.Property(
                    "unsubscribe_count_since_send",
                    th.IntegerType,
                    description="Unsubscribes since last campaign",
                ),
                th.Property(
                    "cleaned_count_since_send",
                    th.IntegerType,
                    description="Cleaned contacts since last campaign",
                ),
                th.Property(
                    "campaign_count",
                    th.IntegerType,
                    description="Number of campaigns sent to this list",
                ),
                th.Property(
                    "campaign_last_sent",
                    th.StringType,
                    description="Date of the last campaign sent",
                    nullable=True,
                ),
                th.Property(
                    "merge_field_count",
                    th.IntegerType,
                    description="Number of merge fields for the list",
                ),
                th.Property(
                    "avg_sub_rate",
                    th.NumberType,
                    description="Average subscription rate",
                ),
                th.Property(
                    "avg_unsub_rate",
                    th.NumberType,
                    description="Average unsubscription rate",
                ),
                th.Property(
                    "target_sub_rate",
                    th.NumberType,
                    description="Target subscription rate",
                ),
                th.Property("open_rate", th.NumberType, description="Open rate"),
                th.Property("click_rate", th.NumberType, description="Click rate"),
                th.Property(
                    "last_sub_date",
                    th.StringType,
                    description="Last subscription date",
                    nullable=True,
                ),
                th.Property(
                    "last_unsub_date",
                    th.StringType,
                    description="Last unsubscription date",
                    nullable=True,
                ),
            ),
        ),
        th.Property(
            "_links",
            th.ArrayType(
                th.ObjectType(
                    th.Property("rel", th.StringType, description="Relation type"),
                    th.Property("href", th.StringType, description="Link URL"),
                    th.Property("method", th.StringType, description="HTTP method"),
                    th.Property("targetSchema", th.StringType, nullable=True),
                    th.Property("schema", th.StringType, nullable=True),
                ),
            ),
        ),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class AutomationsStream(MailchimpStream):
    """Define custom stream."""

    name = "mailchimp_automations"
    path = "/automations"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.lists[*]"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique ID of the automation",
        ),
        th.Property(
            "create_time",
            th.StringType,
            description="Timestamp when the automation was created",
        ),
        th.Property(
            "start_time",
            th.StringType,
            description="Timestamp when the automation started",
        ),
        th.Property(
            "status",
            th.StringType,
            description="Status of the automation",
        ),
        th.Property(
            "emails_sent",
            th.IntegerType,
            description="Number of emails sent by this automation",
        ),
        th.Property(
            "recipients",
            th.ObjectType(
                th.Property("list_id", th.StringType, description="List ID"),
                th.Property(
                    "list_is_active",
                    th.BooleanType,
                    description="Indicates if the list is active",
                ),
                th.Property("list_name", th.StringType, description="Name of the list"),
                th.Property(
                    "segment_opts",
                    th.ObjectType(
                        th.Property(
                            "saved_segment_id",
                            th.IntegerType,
                            description="ID of the saved segment",
                        ),
                        th.Property(
                            "match",
                            th.StringType,
                            description="Match type for segment options",
                        ),
                        th.Property(
                            "conditions",
                            th.ArrayType(th.StringType, nullable=True),
                            description="Conditions for segment options",
                        ),
                    ),
                ),
                th.Property("store_id", th.StringType, description="Store ID"),
            ),
        ),
        th.Property(
            "settings",
            th.ObjectType(
                th.Property(
                    "title", th.StringType, description="Title of the automation"
                ),
                th.Property("from_name", th.StringType, description="Sender's name"),
                th.Property(
                    "reply_to", th.StringType, description="Reply-to email address"
                ),
                th.Property(
                    "use_conversation",
                    th.BooleanType,
                    description="Indicates if conversations are enabled",
                ),
                th.Property("to_name", th.StringType, description="Recipient's name"),
                th.Property(
                    "authenticate",
                    th.BooleanType,
                    description="Indicates if the sender's email is authenticated",
                ),
                th.Property(
                    "auto_footer",
                    th.BooleanType,
                    description="Indicates if auto footers are added",
                ),
                th.Property(
                    "inline_css",
                    th.BooleanType,
                    description="Indicates if inline CSS is applied",
                ),
            ),
        ),
        th.Property(
            "tracking",
            th.ObjectType(
                th.Property(
                    "opens",
                    th.BooleanType,
                    description="Indicates if opens are tracked",
                ),
                th.Property(
                    "html_clicks",
                    th.BooleanType,
                    description="Indicates if HTML clicks are tracked",
                ),
                th.Property(
                    "text_clicks",
                    th.BooleanType,
                    description="Indicates if text clicks are tracked",
                ),
                th.Property(
                    "goal_tracking",
                    th.BooleanType,
                    description="Indicates if goal tracking is enabled",
                ),
                th.Property(
                    "ecomm360",
                    th.BooleanType,
                    description="Indicates if eCommerce360 is enabled",
                ),
                th.Property(
                    "google_analytics",
                    th.StringType,
                    description="Google Analytics tracking ID",
                ),
                th.Property(
                    "clicktale", th.StringType, description="Clicktale tracking ID"
                ),
                th.Property(
                    "salesforce",
                    th.ObjectType(
                        th.Property(
                            "campaign", th.BooleanType, description="Campaign tracking"
                        ),
                        th.Property(
                            "notes", th.BooleanType, description="Notes tracking"
                        ),
                    ),
                ),
                th.Property(
                    "capsule",
                    th.ObjectType(
                        th.Property(
                            "notes",
                            th.BooleanType,
                            description="Capsule notes tracking",
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "trigger_settings",
            th.ObjectType(
                th.Property(
                    "workflow_type",
                    th.StringType,
                    description="Type of the workflow trigger",
                ),
                th.Property(
                    "workflow_title",
                    th.StringType,
                    description="Title of the workflow",
                ),
                th.Property(
                    "runtime",
                    th.ObjectType(
                        th.Property(
                            "days",
                            th.ArrayType(th.StringType),
                            description="Days of the week the workflow runs",
                        ),
                        th.Property(
                            "hours",
                            th.ObjectType(
                                th.Property(
                                    "type",
                                    th.StringType,
                                    description="Type of runtime scheduling",
                                )
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "workflow_emails_count",
                    th.IntegerType,
                    description="Count of emails in the workflow",
                ),
            ),
        ),
        th.Property(
            "report_summary",
            th.ObjectType(
                th.Property(
                    "opens", th.IntegerType, description="Total number of opens"
                ),
                th.Property(
                    "unique_opens",
                    th.IntegerType,
                    description="Number of unique opens",
                ),
                th.Property(
                    "open_rate", th.NumberType, description="Open rate percentage"
                ),
                th.Property(
                    "clicks", th.IntegerType, description="Total number of clicks"
                ),
                th.Property(
                    "subscriber_clicks",
                    th.IntegerType,
                    description="Number of clicks from subscribers",
                ),
                th.Property(
                    "click_rate",
                    th.NumberType,
                    description="Click rate percentage",
                ),
            ),
        ),
        th.Property(
            "_links",
            th.ArrayType(
                th.ObjectType(
                    th.Property("rel", th.StringType, description="Relation type"),
                    th.Property("href", th.StringType, description="Link URL"),
                    th.Property("method", th.StringType, description="HTTP method"),
                    th.Property("targetSchema", th.StringType, nullable=True),
                    th.Property("schema", th.StringType, nullable=True),
                ),
            ),
        ),
        th.Property("profile_id", th.StringType),
    ).to_dict()
