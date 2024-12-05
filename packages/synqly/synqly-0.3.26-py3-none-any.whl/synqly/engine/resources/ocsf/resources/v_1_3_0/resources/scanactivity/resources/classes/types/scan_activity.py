# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..........core.datetime_utils import serialize_datetime
from ...base.types.timestamp import Timestamp
from ...objects.types.actor import Actor
from ...objects.types.agent import Agent
from ...objects.types.api import Api
from ...objects.types.cloud import Cloud
from ...objects.types.device import Device
from ...objects.types.enrichment import Enrichment
from ...objects.types.metadata import Metadata
from ...objects.types.object import Object
from ...objects.types.observable import Observable
from ...objects.types.osint import Osint
from ...objects.types.policy import Policy
from ...objects.types.scan import Scan
from .activity_id import ActivityId
from .category_uid import CategoryUid
from .class_uid import ClassUid
from .severity_id import SeverityId
from .status_id import StatusId
from .type_uid import TypeUid

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class ScanActivity(pydantic.BaseModel):
    """
    Scan events report the start, completion, and results of a scan job. The scan event includes the number of items that were scanned and the number of detections that were resolved.
    """

    activity_id: ActivityId = pydantic.Field()
    """
    The normalized identifier of the activity that triggered the event.
    """

    activity_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event activity name, as defined by the activity_id.
    """

    actor: typing.Optional[Actor] = pydantic.Field(default=None)
    """
    The actor object describes details about the user/role/process that was the source of the activity.
    """

    agent_list: typing.Optional[typing.List[Agent]] = pydantic.Field(default=None)
    """
    The agents that were used to scan the devices.
    """

    api: typing.Optional[Api] = pydantic.Field(default=None)
    """
    Describes details about a typical API (Application Programming Interface) call.
    """

    category_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event category name, as defined by category_uid value: <code>Application Activity</code>.
    """

    category_uid: CategoryUid = pydantic.Field()
    """
    The category unique identifier of the event.
    """

    class_uid: ClassUid = pydantic.Field()
    """
    The unique identifier of a class. A class describes the attributes available in an event.
    """

    cloud: typing.Optional[Cloud] = pydantic.Field(default=None)
    """
    Describes details about the Cloud environment where the event was originally created or logged.
    """

    command_uid: typing.Optional[str] = pydantic.Field(default=None)
    """
    The command identifier that is associated with this scan event. This ID uniquely identifies the proactive scan command, e.g., if remotely initiated.
    """

    count: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.
    """

    device: typing.Optional[Device] = pydantic.Field(default=None)
    """
    An addressable device, computer system or host.
    """

    duration: typing.Optional[int] = pydantic.Field(default=None)
    """
    The duration of the scan
    """

    end_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The end time of the scan job.
    """

    end_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The end time of the scan job.
    """

    enrichments: typing.Optional[typing.List[Enrichment]] = pydantic.Field(default=None)
    """
    The additional information from an external data source, which is associated with the event or a finding. For example add location information for the IP address in the DNS answers:</p><code>[{"name": "answers.ip", "value": "92.24.47.250", "type": "location", "data": {"city": "Socotra", "continent": "Asia", "coordinates": [-25.4153, 17.0743], "country": "YE", "desc": "Yemen"}}]</code>
    """

    message: typing.Optional[str] = pydantic.Field(default=None)
    """
    The description of the event/finding, as defined by the source.
    """

    metadata: Metadata = pydantic.Field()
    """
    The metadata associated with the event or a finding.
    """

    num_detections: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of detections.
    """

    num_files: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of files scanned.
    """

    num_folders: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of folders scanned.
    """

    num_hosts: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of hosts that were scanned.
    """

    num_network_items: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of network items scanned.
    """

    num_processes: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of processes scanned.
    """

    num_registry_items: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of registry items scanned.
    """

    num_resolutions: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of items that were resolved.
    """

    num_skipped_items: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of skipped items.
    """

    num_trusted_items: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of trusted items.
    """

    observables: typing.Optional[typing.List[Observable]] = pydantic.Field(default=None)
    """
    The observables associated with the event or a finding.
    """

    osint: typing.List[Osint] = pydantic.Field()
    """
    The OSINT (Open Source Intelligence) object contains details related to an indicator such as the indicator itself, related indicators, geolocation, registrar information, subdomains, analyst commentary, and other contextual information. This information can be used to further enrich a detection or finding by providing decisioning support to other analysts and engineers.
    """

    policy: typing.Optional[Policy] = pydantic.Field(default=None)
    """
    The policy associated with this Scan event; required if the scan was initiated by a policy.
    """

    raw_data: typing.Optional[str] = pydantic.Field(default=None)
    """
    The raw event/finding data as received from the source.
    """

    scan: Scan = pydantic.Field()
    """
    The Scan object describes characteristics of the scan job.
    """

    schedule_uid: typing.Optional[str] = pydantic.Field(default=None)
    """
    The unique identifier of the schedule associated with a scan job.
    """

    severity: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event/finding severity, normalized to the caption of the severity_id value. In the case of 'Other', it is defined by the source.
    """

    severity_id: SeverityId = pydantic.Field()
    """
    <p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.
    """

    start_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The start time of the scan job.
    """

    start_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The start time of the scan job.
    """

    status: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event status, normalized to the caption of the status_id value. In the case of 'Other', it is defined by the event source.
    """

    status_code: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event status code, as reported by the event source.<br /><br />For example, in a Windows Failed Authentication event, this would be the value of 'Failure Code', e.g. 0x18.
    """

    status_detail: typing.Optional[str] = pydantic.Field(default=None)
    """
    The status detail contains additional information about the event/finding outcome.
    """

    status_id: typing.Optional[StatusId] = pydantic.Field(default=None)
    """
    The normalized identifier of the event status.
    """

    time: Timestamp = pydantic.Field()
    """
    The normalized event occurrence time or the finding creation time.
    """

    time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The normalized event occurrence time or the finding creation time.
    """

    timezone_offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of minutes that the reported event <code>time</code> is ahead or behind UTC, in the range -1,080 to +1,080.
    """

    total: typing.Optional[int] = pydantic.Field(default=None)
    """
    The total number of items that were scanned; zero if no items were scanned.
    """

    type_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event/finding type name, as defined by the type_uid.
    """

    type_uid: TypeUid = pydantic.Field()
    """
    The event/finding type ID. It identifies the event's semantics and structure. The value is calculated by the logging system as: <code>class_uid \* 100 + activity_id</code>.
    """

    unmapped: typing.Optional[Object] = pydantic.Field(default=None)
    """
    The attributes that are not mapped to the event schema. The names and values of those attributes are specific to the event source.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
