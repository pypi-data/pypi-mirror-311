import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentEmailAddressListSummary")


@_attrs_define
class ConstituentEmailAddressListSummary:
    """ListConstituentEmailAddresses.

    Attributes:
        id (Union[Unset, str]): The ID.
        email_address (Union[Unset, str]): The email address.
        type (Union[Unset, str]): The type.
        primary (Union[Unset, bool]): Indicates whether primary.
        info_source (Union[Unset, str]): The information source.
        info_source_comments (Union[Unset, str]): The information source comments.
        email_address_type_code_id (Union[Unset, str]): The email address type code ID.
        start_date (Union[Unset, datetime.datetime]): The startdate. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The enddate. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
    """

    id: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    info_source: Union[Unset, str] = UNSET
    info_source_comments: Union[Unset, str] = UNSET
    email_address_type_code_id: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        email_address = self.email_address

        type = self.type

        primary = self.primary

        info_source = self.info_source

        info_source_comments = self.info_source_comments

        email_address_type_code_id = self.email_address_type_code_id

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
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if type is not UNSET:
            field_dict["type"] = type
        if primary is not UNSET:
            field_dict["primary"] = primary
        if info_source is not UNSET:
            field_dict["info_source"] = info_source
        if info_source_comments is not UNSET:
            field_dict["info_source_comments"] = info_source_comments
        if email_address_type_code_id is not UNSET:
            field_dict["email_address_type_code_id"] = email_address_type_code_id
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        email_address = d.pop("email_address", UNSET)

        type = d.pop("type", UNSET)

        primary = d.pop("primary", UNSET)

        info_source = d.pop("info_source", UNSET)

        info_source_comments = d.pop("info_source_comments", UNSET)

        email_address_type_code_id = d.pop("email_address_type_code_id", UNSET)

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

        constituent_email_address_list_summary = cls(
            id=id,
            email_address=email_address,
            type=type,
            primary=primary,
            info_source=info_source,
            info_source_comments=info_source_comments,
            email_address_type_code_id=email_address_type_code_id,
            start_date=start_date,
            end_date=end_date,
        )

        return constituent_email_address_list_summary
