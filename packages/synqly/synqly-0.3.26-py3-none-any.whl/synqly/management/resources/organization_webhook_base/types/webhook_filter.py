# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class WebhookFilter(str, enum.Enum):
    ALL = "all"
    ACCOUNT_CREATE = "account_create"
    ACCOUNT_DELETE = "account_delete"
    ACCOUNT_UPDATE = "account_update"
    INTEGRATION_CREATE = "integration_create"
    INTEGRATION_DELETE = "integration_delete"
    INTEGRATION_UPDATE = "integration_update"

    def visit(
        self,
        all_: typing.Callable[[], T_Result],
        account_create: typing.Callable[[], T_Result],
        account_delete: typing.Callable[[], T_Result],
        account_update: typing.Callable[[], T_Result],
        integration_create: typing.Callable[[], T_Result],
        integration_delete: typing.Callable[[], T_Result],
        integration_update: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is WebhookFilter.ALL:
            return all_()
        if self is WebhookFilter.ACCOUNT_CREATE:
            return account_create()
        if self is WebhookFilter.ACCOUNT_DELETE:
            return account_delete()
        if self is WebhookFilter.ACCOUNT_UPDATE:
            return account_update()
        if self is WebhookFilter.INTEGRATION_CREATE:
            return integration_create()
        if self is WebhookFilter.INTEGRATION_DELETE:
            return integration_delete()
        if self is WebhookFilter.INTEGRATION_UPDATE:
            return integration_update()
