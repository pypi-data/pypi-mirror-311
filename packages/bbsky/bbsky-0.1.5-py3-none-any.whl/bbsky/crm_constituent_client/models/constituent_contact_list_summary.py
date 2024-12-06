import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentContactListSummary")


@_attrs_define
class ConstituentContactListSummary:
    """ListContactEmailAddresses.

    Attributes:
        id (Union[Unset, str]): The ID.
        contact_info (Union[Unset, str]): The contact information.
        type (Union[Unset, str]): The type.
        is_primary (Union[Unset, str]): The primary.
        do_not_contact (Union[Unset, str]): The do not contact.
        is_former (Union[Unset, bool]): Indicates whether isformer.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        invalid_email (Union[Unset, bool]): Indicates whether invalid email.
        isconfidential (Union[Unset, bool]): Indicates whether confidential.
    """

    id: Union[Unset, str] = UNSET
    contact_info: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    is_primary: Union[Unset, str] = UNSET
    do_not_contact: Union[Unset, str] = UNSET
    is_former: Union[Unset, bool] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    invalid_email: Union[Unset, bool] = UNSET
    isconfidential: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        contact_info = self.contact_info

        type = self.type

        is_primary = self.is_primary

        do_not_contact = self.do_not_contact

        is_former = self.is_former

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        invalid_email = self.invalid_email

        isconfidential = self.isconfidential

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if contact_info is not UNSET:
            field_dict["contact_info"] = contact_info
        if type is not UNSET:
            field_dict["type"] = type
        if is_primary is not UNSET:
            field_dict["is_primary"] = is_primary
        if do_not_contact is not UNSET:
            field_dict["do_not_contact"] = do_not_contact
        if is_former is not UNSET:
            field_dict["is_former"] = is_former
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if invalid_email is not UNSET:
            field_dict["invalid_email"] = invalid_email
        if isconfidential is not UNSET:
            field_dict["isconfidential"] = isconfidential

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        contact_info = d.pop("contact_info", UNSET)

        type = d.pop("type", UNSET)

        is_primary = d.pop("is_primary", UNSET)

        do_not_contact = d.pop("do_not_contact", UNSET)

        is_former = d.pop("is_former", UNSET)

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

        invalid_email = d.pop("invalid_email", UNSET)

        isconfidential = d.pop("isconfidential", UNSET)

        constituent_contact_list_summary = cls(
            id=id,
            contact_info=contact_info,
            type=type,
            is_primary=is_primary,
            do_not_contact=do_not_contact,
            is_former=is_former,
            start_date=start_date,
            end_date=end_date,
            invalid_email=invalid_email,
            isconfidential=isconfidential,
        )

        return constituent_contact_list_summary
