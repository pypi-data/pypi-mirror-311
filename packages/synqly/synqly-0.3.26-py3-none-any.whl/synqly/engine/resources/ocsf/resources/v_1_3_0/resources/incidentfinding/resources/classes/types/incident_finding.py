# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..........core.datetime_utils import serialize_datetime
from ...base.types.timestamp import Timestamp
from ...base.types.url_string import UrlString
from ...objects.types.api import Api
from ...objects.types.attack import Attack
from ...objects.types.cloud import Cloud
from ...objects.types.enrichment import Enrichment
from ...objects.types.finding_info import FindingInfo
from ...objects.types.group import Group
from ...objects.types.metadata import Metadata
from ...objects.types.object import Object
from ...objects.types.observable import Observable
from ...objects.types.osint import Osint
from ...objects.types.ticket import Ticket
from ...objects.types.user import User
from .activity_id import ActivityId
from .category_uid import CategoryUid
from .class_uid import ClassUid
from .confidence_id import ConfidenceId
from .impact_id import ImpactId
from .priority_id import PriorityId
from .severity_id import SeverityId
from .status_id import StatusId
from .type_uid import TypeUid
from .verdict_id import VerdictId

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class IncidentFinding(pydantic.BaseModel):
    """
    An Incident Finding reports the creation, update, or closure of security incidents as a result of detections and/or analytics.
    """

    activity_id: ActivityId = pydantic.Field()
    """
    The normalized identifier of the Incident activity.
    """

    activity_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The Incident activity name, as defined by the <code>activity_id</code>.
    """

    api: typing.Optional[Api] = pydantic.Field(default=None)
    """
    Describes details about a typical API (Application Programming Interface) call.
    """

    assignee: typing.Optional[User] = pydantic.Field(default=None)
    """
    The details of the user assigned to an Incident.
    """

    assignee_group: typing.Optional[Group] = pydantic.Field(default=None)
    """
    The details of the group assigned to an Incident.
    """

    attacks: typing.Optional[typing.List[Attack]] = pydantic.Field(default=None)
    """
    An array of <a target='_blank' href='https://attack.mitre.org'>MITRE ATT&CK®</a> objects describing the tactics, techniques & sub-techniques associated to the Incident.
    """

    category_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event category name, as defined by category_uid value: <code>Findings</code>.
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

    comment: typing.Optional[str] = pydantic.Field(default=None)
    """
    Additional user supplied details for updating or closing the incident.
    """

    confidence: typing.Optional[str] = pydantic.Field(default=None)
    """
    The confidence, normalized to the caption of the confidence_id value. In the case of 'Other', it is defined by the event source.
    """

    confidence_id: typing.Optional[ConfidenceId] = pydantic.Field(default=None)
    """
    The normalized confidence refers to the accuracy of the rule that created the finding. A rule with a low confidence means that the finding scope is wide and may create finding reports that may not be malicious in nature.
    """

    confidence_score: typing.Optional[int] = pydantic.Field(default=None)
    """
    The confidence score as reported by the event source.
    """

    count: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.
    """

    desc: typing.Optional[str] = pydantic.Field(default=None)
    """
    The short description of the Incident.
    """

    duration: typing.Optional[int] = pydantic.Field(default=None)
    """
    The event duration or aggregate time, the amount of time the event covers from <code>start_time</code> to <code>end_time</code> in milliseconds.
    """

    end_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The time of the most recent event included in the incident.
    """

    end_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The time of the most recent event included in the incident.
    """

    enrichments: typing.Optional[typing.List[Enrichment]] = pydantic.Field(default=None)
    """
    The additional information from an external data source, which is associated with the event or a finding. For example add location information for the IP address in the DNS answers:</p><code>[{"name": "answers.ip", "value": "92.24.47.250", "type": "location", "data": {"city": "Socotra", "continent": "Asia", "coordinates": [-25.4153, 17.0743], "country": "YE", "desc": "Yemen"}}]</code>
    """

    finding_info_list: typing.List[FindingInfo] = pydantic.Field()
    """
    A list of <code>finding_info</code> objects associated to an incident.
    """

    impact: typing.Optional[str] = pydantic.Field(default=None)
    """
    The impact , normalized to the caption of the impact_id value. In the case of 'Other', it is defined by the event source.
    """

    impact_id: typing.Optional[ImpactId] = pydantic.Field(default=None)
    """
    The normalized impact of the finding.
    """

    impact_score: typing.Optional[int] = pydantic.Field(default=None)
    """
    The impact of the finding, valid range 0-100.
    """

    is_suspected_breach: typing.Optional[bool] = pydantic.Field(default=None)
    """
    A determination based on analytics as to whether a potential breach was found.
    """

    message: typing.Optional[str] = pydantic.Field(default=None)
    """
    The description of the event/finding, as defined by the source.
    """

    metadata: Metadata = pydantic.Field()
    """
    The metadata associated with the event or a finding.
    """

    observables: typing.Optional[typing.List[Observable]] = pydantic.Field(default=None)
    """
    The observables associated with the event or a finding.
    """

    osint: typing.List[Osint] = pydantic.Field()
    """
    The OSINT (Open Source Intelligence) object contains details related to an indicator such as the indicator itself, related indicators, geolocation, registrar information, subdomains, analyst commentary, and other contextual information. This information can be used to further enrich a detection or finding by providing decisioning support to other analysts and engineers.
    """

    priority: typing.Optional[str] = pydantic.Field(default=None)
    """
    The priority, normalized to the caption of the priority_id value. In the case of 'Other', it is defined by the event source.
    """

    priority_id: typing.Optional[PriorityId] = pydantic.Field(default=None)
    """
    The normalized priority. Priority identifies the relative importance of the finding. It is a measurement of urgency.
    """

    raw_data: typing.Optional[str] = pydantic.Field(default=None)
    """
    The raw event/finding data as received from the source.
    """

    severity: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event/finding severity, normalized to the caption of the severity_id value. In the case of 'Other', it is defined by the source.
    """

    severity_id: SeverityId = pydantic.Field()
    """
    <p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.
    """

    src_url: typing.Optional[UrlString] = pydantic.Field(default=None)
    """
    A Url link used to access the original incident.
    """

    start_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The time of the least recent event included in the incident.
    """

    start_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The time of the least recent event included in the incident.
    """

    status: typing.Optional[str] = pydantic.Field(default=None)
    """
    The normalized status of the Incident normalized to the caption of the status_id value. In the case of 'Other', it is defined by the source.
    """

    status_code: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event status code, as reported by the event source.<br /><br />For example, in a Windows Failed Authentication event, this would be the value of 'Failure Code', e.g. 0x18.
    """

    status_detail: typing.Optional[str] = pydantic.Field(default=None)
    """
    The status detail contains additional information about the event/finding outcome.
    """

    status_id: StatusId = pydantic.Field()
    """
    The normalized status identifier of the Incident.
    """

    ticket: typing.Optional[Ticket] = pydantic.Field(default=None)
    """
    The linked ticket in the ticketing system.
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

    verdict: typing.Optional[str] = pydantic.Field(default=None)
    """
    The verdict assigned to an Incident finding.
    """

    verdict_id: typing.Optional[VerdictId] = pydantic.Field(default=None)
    """
    The normalized verdict of an Incident.
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
