import datetime
from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hour_minute import HourMinute


T = TypeVar("T", bound="ConstituentPhoneListSummary")


@_attrs_define
class ConstituentPhoneListSummary:
    """ListConstituentPhones.

    Attributes:
        id (Union[Unset, str]): The ID.
        phone_number (Union[Unset, str]): The phone number.
        type (Union[Unset, str]): The type.
        primary (Union[Unset, bool]): Indicates whether primary.
        do_not_call (Union[Unset, str]): The do not call.
        start_time (Union[Unset, HourMinute]): HourMinute
        end_time (Union[Unset, HourMinute]): HourMinute
        info_source (Union[Unset, str]): The information source.
        info_source_comments (Union[Unset, str]): The information source comments.
        country (Union[Unset, str]): The country.
        phone_type_code_id (Union[Unset, str]): The phone type code ID.
        donotcall (Union[Unset, bool]): Indicates whether donotcall.
        start_date (Union[Unset, datetime.datetime]): The startdate. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The enddate. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
    """

    id: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    do_not_call: Union[Unset, str] = UNSET
    start_time: Union[Unset, "HourMinute"] = UNSET
    end_time: Union[Unset, "HourMinute"] = UNSET
    info_source: Union[Unset, str] = UNSET
    info_source_comments: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    phone_type_code_id: Union[Unset, str] = UNSET
    donotcall: Union[Unset, bool] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        phone_number = self.phone_number

        type = self.type

        primary = self.primary

        do_not_call = self.do_not_call

        start_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.to_dict()

        end_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.to_dict()

        info_source = self.info_source

        info_source_comments = self.info_source_comments

        country = self.country

        phone_type_code_id = self.phone_type_code_id

        donotcall = self.donotcall

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if type is not UNSET:
            field_dict["type"] = type
        if primary is not UNSET:
            field_dict["primary"] = primary
        if do_not_call is not UNSET:
            field_dict["do_not_call"] = do_not_call
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if info_source is not UNSET:
            field_dict["info_source"] = info_source
        if info_source_comments is not UNSET:
            field_dict["info_source_comments"] = info_source_comments
        if country is not UNSET:
            field_dict["country"] = country
        if phone_type_code_id is not UNSET:
            field_dict["phone_type_code_id"] = phone_type_code_id
        if donotcall is not UNSET:
            field_dict["donotcall"] = donotcall
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.hour_minute import HourMinute

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        type = d.pop("type", UNSET)

        primary = d.pop("primary", UNSET)

        do_not_call = d.pop("do_not_call", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, HourMinute]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = HourMinute.from_dict(_start_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, HourMinute]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = HourMinute.from_dict(_end_time)

        info_source = d.pop("info_source", UNSET)

        info_source_comments = d.pop("info_source_comments", UNSET)

        country = d.pop("country", UNSET)

        phone_type_code_id = d.pop("phone_type_code_id", UNSET)

        donotcall = d.pop("donotcall", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        constituent_phone_list_summary = cls(
            id=id,
            phone_number=phone_number,
            type=type,
            primary=primary,
            do_not_call=do_not_call,
            start_time=start_time,
            end_time=end_time,
            info_source=info_source,
            info_source_comments=info_source_comments,
            country=country,
            phone_type_code_id=phone_type_code_id,
            donotcall=donotcall,
            start_date=start_date,
            end_date=end_date,
        )

        return constituent_phone_list_summary
