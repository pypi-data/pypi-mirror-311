import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hour_minute import HourMinute
    from ..models.new_constituent_interaction_participants import NewConstituentInteractionParticipants
    from ..models.new_constituent_interaction_sites import NewConstituentInteractionSites


T = TypeVar("T", bound="NewConstituentInteraction")


@_attrs_define
class NewConstituentInteraction:
    """CreateConstituentInteraction.

    Example:
        {'constituent_id': '', 'interaction_type': '', 'objective': '', 'fundraiser_id': '', 'expected_date': '',
            'actual_date': '', 'status': 'Pending', 'comment': '', 'event_id': '', 'constituent_name': '', 'participants':
            [{'id': '', 'constituent_id': ''}], 'interaction_category': '', 'interaction_subcategory': '', 'sites': [{'id':
            '', 'siteid': ''}], 'site_required': False, 'selected_constituent_id': '', 'expected_start_time': '',
            'expected_end_time': '', 'is_all_day_event': False, 'time_zone_entry': '', 'actual_start_time': '',
            'actual_end_time': '', 'location': '', 'other_location': ''}

    Attributes:
        constituent_id (str): The constituent ID.
        interaction_type (str): The contact method. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/interactiontypecode/entries
        objective (str): The summary.
        expected_date (datetime.datetime): The expected date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        status (str): The status. Available values are <i>pending</i>, <i>completed</i>, <i>canceled</i>,
            <i>declined</i>
        fundraiser_id (Union[Unset, str]): The owner.
        actual_date (Union[Unset, datetime.datetime]): The actual date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        comment (Union[Unset, str]): The comment.
        event_id (Union[Unset, str]): The event.
        constituent_name (Union[Unset, str]): The constituent name. Read-only in the SOAP API.
        participants (Union[Unset, List['NewConstituentInteractionParticipants']]): Participants.
        interaction_category (Union[Unset, str]): The category. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/cbba7545-b66f-44ac-aa24-d9c2f8cbc4ec.
        interaction_subcategory (Union[Unset, str]): The subcategory. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/0eacc39b-07d1-4641-8774-e319559535a7?parameters=interactioncategoryid,{interactioncategoryid}.
        sites (Union[Unset, List['NewConstituentInteractionSites']]): Sites.
        site_required (Union[Unset, bool]): Indicates whether site required. Read-only in the SOAP API.
        selected_constituent_id (Union[Unset, str]): The constituent.
        expected_start_time (Union[Unset, HourMinute]): HourMinute
        expected_end_time (Union[Unset, HourMinute]): HourMinute
        is_all_day_event (Union[Unset, bool]): Indicates whether is all day event.
        time_zone_entry (Union[Unset, str]): The time zone. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/7fba76fa-b1ea-4c01-b841-edb18f03fe8c.
        actual_start_time (Union[Unset, HourMinute]): HourMinute
        actual_end_time (Union[Unset, HourMinute]): HourMinute
        location (Union[Unset, str]): The location. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/b0cb4058-4355-431a-abdb-3e9f2be8c918?parameters=constituent_id,{constituent_id}.
        other_location (Union[Unset, str]): The other location.
    """

    constituent_id: str
    interaction_type: str
    objective: str
    expected_date: datetime.datetime
    status: str
    fundraiser_id: Union[Unset, str] = UNSET
    actual_date: Union[Unset, datetime.datetime] = UNSET
    comment: Union[Unset, str] = UNSET
    event_id: Union[Unset, str] = UNSET
    constituent_name: Union[Unset, str] = UNSET
    participants: Union[Unset, List["NewConstituentInteractionParticipants"]] = UNSET
    interaction_category: Union[Unset, str] = UNSET
    interaction_subcategory: Union[Unset, str] = UNSET
    sites: Union[Unset, List["NewConstituentInteractionSites"]] = UNSET
    site_required: Union[Unset, bool] = UNSET
    selected_constituent_id: Union[Unset, str] = UNSET
    expected_start_time: Union[Unset, "HourMinute"] = UNSET
    expected_end_time: Union[Unset, "HourMinute"] = UNSET
    is_all_day_event: Union[Unset, bool] = UNSET
    time_zone_entry: Union[Unset, str] = UNSET
    actual_start_time: Union[Unset, "HourMinute"] = UNSET
    actual_end_time: Union[Unset, "HourMinute"] = UNSET
    location: Union[Unset, str] = UNSET
    other_location: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        interaction_type = self.interaction_type

        objective = self.objective

        expected_date = self.expected_date.isoformat()

        status = self.status

        fundraiser_id = self.fundraiser_id

        actual_date: Union[Unset, str] = UNSET
        if not isinstance(self.actual_date, Unset):
            actual_date = self.actual_date.isoformat()

        comment = self.comment

        event_id = self.event_id

        constituent_name = self.constituent_name

        participants: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.participants, Unset):
            participants = []
            for participants_item_data in self.participants:
                participants_item = participants_item_data.to_dict()
                participants.append(participants_item)

        interaction_category = self.interaction_category

        interaction_subcategory = self.interaction_subcategory

        sites: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sites, Unset):
            sites = []
            for sites_item_data in self.sites:
                sites_item = sites_item_data.to_dict()
                sites.append(sites_item)

        site_required = self.site_required

        selected_constituent_id = self.selected_constituent_id

        expected_start_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expected_start_time, Unset):
            expected_start_time = self.expected_start_time.to_dict()

        expected_end_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expected_end_time, Unset):
            expected_end_time = self.expected_end_time.to_dict()

        is_all_day_event = self.is_all_day_event

        time_zone_entry = self.time_zone_entry

        actual_start_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.actual_start_time, Unset):
            actual_start_time = self.actual_start_time.to_dict()

        actual_end_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.actual_end_time, Unset):
            actual_end_time = self.actual_end_time.to_dict()

        location = self.location

        other_location = self.other_location

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "constituent_id": constituent_id,
                "interaction_type": interaction_type,
                "objective": objective,
                "expected_date": expected_date,
                "status": status,
            }
        )
        if fundraiser_id is not UNSET:
            field_dict["fundraiser_id"] = fundraiser_id
        if actual_date is not UNSET:
            field_dict["actual_date"] = actual_date
        if comment is not UNSET:
            field_dict["comment"] = comment
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if constituent_name is not UNSET:
            field_dict["constituent_name"] = constituent_name
        if participants is not UNSET:
            field_dict["participants"] = participants
        if interaction_category is not UNSET:
            field_dict["interaction_category"] = interaction_category
        if interaction_subcategory is not UNSET:
            field_dict["interaction_subcategory"] = interaction_subcategory
        if sites is not UNSET:
            field_dict["sites"] = sites
        if site_required is not UNSET:
            field_dict["site_required"] = site_required
        if selected_constituent_id is not UNSET:
            field_dict["selected_constituent_id"] = selected_constituent_id
        if expected_start_time is not UNSET:
            field_dict["expected_start_time"] = expected_start_time
        if expected_end_time is not UNSET:
            field_dict["expected_end_time"] = expected_end_time
        if is_all_day_event is not UNSET:
            field_dict["is_all_day_event"] = is_all_day_event
        if time_zone_entry is not UNSET:
            field_dict["time_zone_entry"] = time_zone_entry
        if actual_start_time is not UNSET:
            field_dict["actual_start_time"] = actual_start_time
        if actual_end_time is not UNSET:
            field_dict["actual_end_time"] = actual_end_time
        if location is not UNSET:
            field_dict["location"] = location
        if other_location is not UNSET:
            field_dict["other_location"] = other_location

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.hour_minute import HourMinute
        from ..models.new_constituent_interaction_participants import NewConstituentInteractionParticipants
        from ..models.new_constituent_interaction_sites import NewConstituentInteractionSites

        d = src_dict.copy()
        constituent_id = d.pop("constituent_id")

        interaction_type = d.pop("interaction_type")

        objective = d.pop("objective")

        expected_date = isoparse(d.pop("expected_date"))

        status = d.pop("status")

        fundraiser_id = d.pop("fundraiser_id", UNSET)

        _actual_date = d.pop("actual_date", UNSET)
        actual_date: Union[Unset, datetime.datetime]
        if isinstance(_actual_date, Unset):
            actual_date = UNSET
        else:
            actual_date = isoparse(_actual_date)

        comment = d.pop("comment", UNSET)

        event_id = d.pop("event_id", UNSET)

        constituent_name = d.pop("constituent_name", UNSET)

        participants = []
        _participants = d.pop("participants", UNSET)
        for participants_item_data in _participants or []:
            participants_item = NewConstituentInteractionParticipants.from_dict(participants_item_data)

            participants.append(participants_item)

        interaction_category = d.pop("interaction_category", UNSET)

        interaction_subcategory = d.pop("interaction_subcategory", UNSET)

        sites = []
        _sites = d.pop("sites", UNSET)
        for sites_item_data in _sites or []:
            sites_item = NewConstituentInteractionSites.from_dict(sites_item_data)

            sites.append(sites_item)

        site_required = d.pop("site_required", UNSET)

        selected_constituent_id = d.pop("selected_constituent_id", UNSET)

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

        is_all_day_event = d.pop("is_all_day_event", UNSET)

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

        location = d.pop("location", UNSET)

        other_location = d.pop("other_location", UNSET)

        new_constituent_interaction = cls(
            constituent_id=constituent_id,
            interaction_type=interaction_type,
            objective=objective,
            expected_date=expected_date,
            status=status,
            fundraiser_id=fundraiser_id,
            actual_date=actual_date,
            comment=comment,
            event_id=event_id,
            constituent_name=constituent_name,
            participants=participants,
            interaction_category=interaction_category,
            interaction_subcategory=interaction_subcategory,
            sites=sites,
            site_required=site_required,
            selected_constituent_id=selected_constituent_id,
            expected_start_time=expected_start_time,
            expected_end_time=expected_end_time,
            is_all_day_event=is_all_day_event,
            time_zone_entry=time_zone_entry,
            actual_start_time=actual_start_time,
            actual_end_time=actual_end_time,
            location=location,
            other_location=other_location,
        )

        return new_constituent_interaction
