import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_constituent_interaction_participants import EditConstituentInteractionParticipants
    from ..models.edit_constituent_interaction_sites import EditConstituentInteractionSites
    from ..models.hour_minute import HourMinute


T = TypeVar("T", bound="EditConstituentInteraction")


@_attrs_define
class EditConstituentInteraction:
    """EditConstituentInteraction.

    Example:
        {'interaction_type': 'Phone call', 'objective': 'Introductory call', 'fundraiser_id':
            '0DE9D2A3-82EE-4979-AA40-AF9C9DF2C0A2', 'expected_date': '2015-02-17T12:00:00.0000000+00:00', 'actual_date':
            '2015-02-17T12:00:00.0000000+00:00', 'status': 'Completed', 'comment': '', 'step': False, 'event_id': '',
            'participants': [{'id': 'd4873d67-c341-442c-bdc4-2cdb47bff7e2', 'constituent_id':
            '83ED6E63-4687-447A-B94F-35611ADF47B3'}], 'constituent_id': '', 'constituent_name': '', 'interaction_category':
            '', 'interaction_subcategory': '', 'sites': [{'id': 'a62483d4-cb71-46ae-9f06-da0644d0629f', 'site_id':
            'D0AD4D30-800D-4F81-A5BA-DDA2A60C85A9'}], 'expected_start_time': {'hour': 1, 'minute': 26}, 'expected_end_time':
            {'hour': 3, 'minute': 33}, 'all_day_event': False, 'time_zone_entry': '', 'actual_start_time': {'hour': 2,
            'minute': 19}, 'actual_end_time': {'hour': 6, 'minute': 40}}

    Attributes:
        interaction_type (Union[Unset, str]): The contact method. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/interactiontypecode/entries
        objective (Union[Unset, str]): The summary.
        fundraiser_id (Union[Unset, str]): The owner.
        expected_date (Union[Unset, datetime.datetime]): The expected date. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        actual_date (Union[Unset, datetime.datetime]): The actual date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        status (Union[Unset, str]): The status. Available values are <i>pending</i>, <i>completed</i>, <i>canceled</i>,
            <i>declined</i>
        comment (Union[Unset, str]): The comment.
        step (Union[Unset, bool]): Indicates whether is step. Read-only in the SOAP API.
        event_id (Union[Unset, str]): The event.
        participants (Union[Unset, List['EditConstituentInteractionParticipants']]): Participants.
        constituent_id (Union[Unset, str]): The constituent ID. Read-only in the SOAP API.
        constituent_name (Union[Unset, str]): The constituent name. Read-only in the SOAP API.
        interaction_category (Union[Unset, str]): The category. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/cbba7545-b66f-44ac-aa24-d9c2f8cbc4ec.
        interaction_subcategory (Union[Unset, str]): The subcategory. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/0eacc39b-07d1-4641-8774-e319559535a7?parameters=interactioncategoryid,{interactioncategoryid}.
        sites (Union[Unset, List['EditConstituentInteractionSites']]): Sites.
        expected_start_time (Union[Unset, HourMinute]): HourMinute
        expected_end_time (Union[Unset, HourMinute]): HourMinute
        all_day_event (Union[Unset, bool]): Indicates whether all day event.
        time_zone_entry (Union[Unset, str]): The time zone. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/7fba76fa-b1ea-4c01-b841-edb18f03fe8c.
        actual_start_time (Union[Unset, HourMinute]): HourMinute
        actual_end_time (Union[Unset, HourMinute]): HourMinute
    """

    interaction_type: Union[Unset, str] = UNSET
    objective: Union[Unset, str] = UNSET
    fundraiser_id: Union[Unset, str] = UNSET
    expected_date: Union[Unset, datetime.datetime] = UNSET
    actual_date: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    step: Union[Unset, bool] = UNSET
    event_id: Union[Unset, str] = UNSET
    participants: Union[Unset, List["EditConstituentInteractionParticipants"]] = UNSET
    constituent_id: Union[Unset, str] = UNSET
    constituent_name: Union[Unset, str] = UNSET
    interaction_category: Union[Unset, str] = UNSET
    interaction_subcategory: Union[Unset, str] = UNSET
    sites: Union[Unset, List["EditConstituentInteractionSites"]] = UNSET
    expected_start_time: Union[Unset, "HourMinute"] = UNSET
    expected_end_time: Union[Unset, "HourMinute"] = UNSET
    all_day_event: Union[Unset, bool] = UNSET
    time_zone_entry: Union[Unset, str] = UNSET
    actual_start_time: Union[Unset, "HourMinute"] = UNSET
    actual_end_time: Union[Unset, "HourMinute"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        interaction_type = self.interaction_type

        objective = self.objective

        fundraiser_id = self.fundraiser_id

        expected_date: Union[Unset, str] = UNSET
        if not isinstance(self.expected_date, Unset):
            expected_date = self.expected_date.isoformat()

        actual_date: Union[Unset, str] = UNSET
        if not isinstance(self.actual_date, Unset):
            actual_date = self.actual_date.isoformat()

        status = self.status

        comment = self.comment

        step = self.step

        event_id = self.event_id

        participants: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.participants, Unset):
            participants = []
            for participants_item_data in self.participants:
                participants_item = participants_item_data.to_dict()
                participants.append(participants_item)

        constituent_id = self.constituent_id

        constituent_name = self.constituent_name

        interaction_category = self.interaction_category

        interaction_subcategory = self.interaction_subcategory

        sites: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sites, Unset):
            sites = []
            for sites_item_data in self.sites:
                sites_item = sites_item_data.to_dict()
                sites.append(sites_item)

        expected_start_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expected_start_time, Unset):
            expected_start_time = self.expected_start_time.to_dict()

        expected_end_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expected_end_time, Unset):
            expected_end_time = self.expected_end_time.to_dict()

        all_day_event = self.all_day_event

        time_zone_entry = self.time_zone_entry

        actual_start_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.actual_start_time, Unset):
            actual_start_time = self.actual_start_time.to_dict()

        actual_end_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.actual_end_time, Unset):
            actual_end_time = self.actual_end_time.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if interaction_type is not UNSET:
            field_dict["interaction_type"] = interaction_type
        if objective is not UNSET:
            field_dict["objective"] = objective
        if fundraiser_id is not UNSET:
            field_dict["fundraiser_id"] = fundraiser_id
        if expected_date is not UNSET:
            field_dict["expected_date"] = expected_date
        if actual_date is not UNSET:
            field_dict["actual_date"] = actual_date
        if status is not UNSET:
            field_dict["status"] = status
        if comment is not UNSET:
            field_dict["comment"] = comment
        if step is not UNSET:
            field_dict["step"] = step
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if participants is not UNSET:
            field_dict["participants"] = participants
        if constituent_id is not UNSET:
            field_dict["constituent_id"] = constituent_id
        if constituent_name is not UNSET:
            field_dict["constituent_name"] = constituent_name
        if interaction_category is not UNSET:
            field_dict["interaction_category"] = interaction_category
        if interaction_subcategory is not UNSET:
            field_dict["interaction_subcategory"] = interaction_subcategory
        if sites is not UNSET:
            field_dict["sites"] = sites
        if expected_start_time is not UNSET:
            field_dict["expected_start_time"] = expected_start_time
        if expected_end_time is not UNSET:
            field_dict["expected_end_time"] = expected_end_time
        if all_day_event is not UNSET:
            field_dict["all_day_event"] = all_day_event
        if time_zone_entry is not UNSET:
            field_dict["time_zone_entry"] = time_zone_entry
        if actual_start_time is not UNSET:
            field_dict["actual_start_time"] = actual_start_time
        if actual_end_time is not UNSET:
            field_dict["actual_end_time"] = actual_end_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_constituent_interaction_participants import EditConstituentInteractionParticipants
        from ..models.edit_constituent_interaction_sites import EditConstituentInteractionSites
        from ..models.hour_minute import HourMinute

        d = src_dict.copy()
        interaction_type = d.pop("interaction_type", UNSET)

        objective = d.pop("objective", UNSET)

        fundraiser_id = d.pop("fundraiser_id", UNSET)

        _expected_date = d.pop("expected_date", UNSET)
        expected_date: Union[Unset, datetime.datetime]
        if isinstance(_expected_date, Unset):
            expected_date = UNSET
        else:
            expected_date = isoparse(_expected_date)

        _actual_date = d.pop("actual_date", UNSET)
        actual_date: Union[Unset, datetime.datetime]
        if isinstance(_actual_date, Unset):
            actual_date = UNSET
        else:
            actual_date = isoparse(_actual_date)

        status = d.pop("status", UNSET)

        comment = d.pop("comment", UNSET)

        step = d.pop("step", UNSET)

        event_id = d.pop("event_id", UNSET)

        participants = []
        _participants = d.pop("participants", UNSET)
        for participants_item_data in _participants or []:
            participants_item = EditConstituentInteractionParticipants.from_dict(participants_item_data)

            participants.append(participants_item)

        constituent_id = d.pop("constituent_id", UNSET)

        constituent_name = d.pop("constituent_name", UNSET)

        interaction_category = d.pop("interaction_category", UNSET)

        interaction_subcategory = d.pop("interaction_subcategory", UNSET)

        sites = []
        _sites = d.pop("sites", UNSET)
        for sites_item_data in _sites or []:
            sites_item = EditConstituentInteractionSites.from_dict(sites_item_data)

            sites.append(sites_item)

        _expected_start_time = d.pop("expected_start_time", UNSET)
        expected_start_time: Union[Unset, HourMinute]
        if isinstance(_expected_start_time, Unset):
            expected_start_time = UNSET
        else:
            expected_start_time = HourMinute.from_dict(_expected_start_time)

        _expected_end_time = d.pop("expected_end_time", UNSET)
        expected_end_time: Union[Unset, HourMinute]
        if isinstance(_expected_end_time, Unset):
            expected_end_time = UNSET
        else:
            expected_end_time = HourMinute.from_dict(_expected_end_time)

        all_day_event = d.pop("all_day_event", UNSET)

        time_zone_entry = d.pop("time_zone_entry", UNSET)

        _actual_start_time = d.pop("actual_start_time", UNSET)
        actual_start_time: Union[Unset, HourMinute]
        if isinstance(_actual_start_time, Unset):
            actual_start_time = UNSET
        else:
            actual_start_time = HourMinute.from_dict(_actual_start_time)

        _actual_end_time = d.pop("actual_end_time", UNSET)
        actual_end_time: Union[Unset, HourMinute]
        if isinstance(_actual_end_time, Unset):
            actual_end_time = UNSET
        else:
            actual_end_time = HourMinute.from_dict(_actual_end_time)

        edit_constituent_interaction = cls(
            interaction_type=interaction_type,
            objective=objective,
            fundraiser_id=fundraiser_id,
            expected_date=expected_date,
            actual_date=actual_date,
            status=status,
            comment=comment,
            step=step,
            event_id=event_id,
            participants=participants,
            constituent_id=constituent_id,
            constituent_name=constituent_name,
            interaction_category=interaction_category,
            interaction_subcategory=interaction_subcategory,
            sites=sites,
            expected_start_time=expected_start_time,
            expected_end_time=expected_end_time,
            all_day_event=all_day_event,
            time_zone_entry=time_zone_entry,
            actual_start_time=actual_start_time,
            actual_end_time=actual_end_time,
        )

        return edit_constituent_interaction
