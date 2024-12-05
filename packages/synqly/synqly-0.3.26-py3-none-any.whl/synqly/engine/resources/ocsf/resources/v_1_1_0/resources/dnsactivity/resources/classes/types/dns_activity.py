# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..........core.datetime_utils import serialize_datetime
from ...base.types.timestamp import Timestamp
from ...objects.types.actor import Actor
from ...objects.types.api import Api
from ...objects.types.attack import Attack
from ...objects.types.authorization import Authorization
from ...objects.types.cloud import Cloud
from ...objects.types.device import Device
from ...objects.types.dns_answer import DnsAnswer
from ...objects.types.dns_query import DnsQuery
from ...objects.types.enrichment import Enrichment
from ...objects.types.firewall_rule import FirewallRule
from ...objects.types.http_request import HttpRequest
from ...objects.types.http_response import HttpResponse
from ...objects.types.load_balancer import LoadBalancer
from ...objects.types.malware import Malware
from ...objects.types.metadata import Metadata
from ...objects.types.network_connection_info import NetworkConnectionInfo
from ...objects.types.network_endpoint import NetworkEndpoint
from ...objects.types.network_proxy import NetworkProxy
from ...objects.types.network_traffic import NetworkTraffic
from ...objects.types.object import Object
from ...objects.types.observable import Observable
from ...objects.types.tls import Tls
from .action_id import ActionId
from .activity_id import ActivityId
from .category_uid import CategoryUid
from .class_uid import ClassUid
from .disposition_id import DispositionId
from .rcode_id import RcodeId
from .severity_id import SeverityId
from .status_id import StatusId
from .type_uid import TypeUid

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class DnsActivity(pydantic.BaseModel):
    """
    DNS Activity events report DNS queries and answers as seen on the network.
    """

    action: typing.Optional[str] = pydantic.Field(default=None)
    """
    The normalized caption of <code>action_id</code>.
    """

    action_id: ActionId = pydantic.Field()
    """
    The action taken by a control or other policy-based system leading to an outcome or disposition. Dispositions conform to an action of <code>1</code> 'Allowed' or <code>2</code> 'Denied' in most cases. Note that <code>99</code> 'Other' is not an option. No action would equate to <code>1</code> 'Allowed'. An unknown action may still correspond to a known disposition. Refer to <code>disposition_id</code> for the outcome of the action.
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

    answers: typing.Optional[typing.List[DnsAnswer]] = pydantic.Field(default=None)
    """
    The Domain Name System (DNS) answers.
    """

    api: typing.Optional[Api] = pydantic.Field(default=None)
    """
    Describes details about a typical API (Application Programming Interface) call.
    """

    app_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The name of the application that is associated with the event or object.
    """

    attacks: typing.Optional[typing.List[Attack]] = pydantic.Field(default=None)
    """
    An array of <a target='_blank' href='https://attack.mitre.org'>MITRE ATT&CK®</a> objects describing the tactics, techniques & sub-techniques identified by a security control or finding.
    """

    authorizations: typing.Optional[typing.List[Authorization]] = pydantic.Field(default=None)
    """
    Provides details about an authorization, such as authorization outcome, and any associated policies related to the activity/event.
    """

    category_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event category name, as defined by category_uid value: <code>Network Activity</code>.
    """

    category_uid: CategoryUid = pydantic.Field()
    """
    The category unique identifier of the event.
    """

    class_uid: ClassUid = pydantic.Field()
    """
    The unique identifier of a class. A Class describes the attributes available in an event.
    """

    cloud: typing.Optional[Cloud] = pydantic.Field(default=None)
    """
    Describes details about the Cloud environment where the event was originally created or logged.
    """

    connection_info: typing.Optional[NetworkConnectionInfo] = pydantic.Field(default=None)
    """
    The network connection information.
    """

    count: typing.Optional[int] = pydantic.Field(default=None)
    """
    The number of times that events in the same logical group occurred during the event <strong>Start Time</strong> to <strong>End Time</strong> period.
    """

    device: typing.Optional[Device] = pydantic.Field(default=None)
    """
    An addressable device, computer system or host.
    """

    disposition: typing.Optional[str] = pydantic.Field(default=None)
    """
    The disposition name, normalized to the caption of the disposition_id value. In the case of 'Other', it is defined by the event source.
    """

    disposition_id: typing.Optional[DispositionId] = pydantic.Field(default=None)
    """
    Describes the outcome or action taken by a security control, such as access control checks, malware detections or various types of policy violations.
    """

    dst_endpoint: typing.Optional[NetworkEndpoint] = pydantic.Field(default=None)
    """
    The responder (server) in a network connection.
    """

    duration: typing.Optional[int] = pydantic.Field(default=None)
    """
    The event duration or aggregate time, the amount of time the event covers from <code>start_time</code> to <code>end_time</code> in milliseconds.
    """

    end_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The end time of a time period, or the time of the most recent event included in the aggregate event.
    """

    end_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The end time of a time period, or the time of the most recent event included in the aggregate event.
    """

    enrichments: typing.Optional[typing.List[Enrichment]] = pydantic.Field(default=None)
    """
    The additional information from an external data source, which is associated with the event or a finding. For example add location information for the IP address in the DNS answers:</p><code>[{"name": "answers.ip", "value": "92.24.47.250", "type": "location", "data": {"city": "Socotra", "continent": "Asia", "coordinates": [-25.4153, 17.0743], "country": "YE", "desc": "Yemen"}}]</code>
    """

    firewall_rule: typing.Optional[FirewallRule] = pydantic.Field(default=None)
    """
    The firewall rule that triggered the event.
    """

    load_balancer: typing.Optional[LoadBalancer] = pydantic.Field(default=None)
    """
    The Load Balancer object contains information related to the device that is distributing incoming traffic to specified destinations.
    """

    malware: typing.Optional[typing.List[Malware]] = pydantic.Field(default=None)
    """
    A list of Malware objects, describing details about the identified malware.
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

    proxy: typing.Optional[NetworkProxy] = pydantic.Field(default=None)
    """
    The proxy (server) in a network connection.
    """

    proxy_connection_info: typing.Optional[NetworkConnectionInfo] = pydantic.Field(default=None)
    """
    The connection information from the proxy server to the remote server.
    """

    proxy_endpoint: typing.Optional[NetworkProxy] = pydantic.Field(default=None)
    """
    The proxy (server) in a network connection.
    """

    proxy_http_request: typing.Optional[HttpRequest] = pydantic.Field(default=None)
    """
    The HTTP Request from the proxy server to the remote server.
    """

    proxy_http_response: typing.Optional[HttpResponse] = pydantic.Field(default=None)
    """
    The HTTP Response from the remote server to the proxy server.
    """

    proxy_tls: typing.Optional[Tls] = pydantic.Field(default=None)
    """
    The TLS protocol negotiated between the proxy server and the remote server.
    """

    proxy_traffic: typing.Optional[NetworkTraffic] = pydantic.Field(default=None)
    """
    The network traffic refers to the amount of data moving across a network, from proxy to remote server at a given point of time.
    """

    query: typing.Optional[DnsQuery] = pydantic.Field(default=None)
    """
    The Domain Name System (DNS) query.
    """

    query_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The Domain Name System (DNS) query time.
    """

    query_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The Domain Name System (DNS) query time.
    """

    raw_data: typing.Optional[str] = pydantic.Field(default=None)
    """
    The raw event/finding data as received from the source.
    """

    rcode: typing.Optional[str] = pydantic.Field(default=None)
    """
    The DNS server response code, normalized to the caption of the rcode_id value. In the case of 'Other', it is defined by the event source.
    """

    rcode_id: typing.Optional[RcodeId] = pydantic.Field(default=None)
    """
    The normalized identifier of the DNS server response code. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc6895'>RFC-6895</a>.
    """

    response_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The Domain Name System (DNS) response time.
    """

    response_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The Domain Name System (DNS) response time.
    """

    severity: typing.Optional[str] = pydantic.Field(default=None)
    """
    The event/finding severity, normalized to the caption of the severity_id value. In the case of 'Other', it is defined by the source.
    """

    severity_id: SeverityId = pydantic.Field()
    """
    <p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.
    """

    src_endpoint: NetworkEndpoint = pydantic.Field()
    """
    The initiator (client) of the network connection.
    """

    start_time: typing.Optional[Timestamp] = pydantic.Field(default=None)
    """
    The start time of a time period, or the time of the least recent event included in the aggregate event.
    """

    start_time_dt: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The start time of a time period, or the time of the least recent event included in the aggregate event.
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
    The status details contains additional information about the event/finding outcome.
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

    tls: typing.Optional[Tls] = pydantic.Field(default=None)
    """
    The Transport Layer Security (TLS) attributes.
    """

    traffic: typing.Optional[NetworkTraffic] = pydantic.Field(default=None)
    """
    The network traffic refers to the amount of data moving across a network at a given point of time. Intended to be used alongside Network Connection.
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
