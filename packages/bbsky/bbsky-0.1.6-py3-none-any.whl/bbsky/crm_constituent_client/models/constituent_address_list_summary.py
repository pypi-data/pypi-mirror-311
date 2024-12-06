import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAddressListSummary")


@_attrs_define
class ConstituentAddressListSummary:
    """ListConstituentAddresses.

    Attributes:
        id (Union[Unset, str]): The ID.
        contact_info (Union[Unset, str]): The contact information.
        type (Union[Unset, str]): The type.
        primary (Union[Unset, str]): The primary.
        do_not_contact (Union[Unset, str]): The do not contact.
        confidential (Union[Unset, bool]): Indicates whether confidential.
        former (Union[Unset, bool]): Indicates whether isformer.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        geocoded (Union[Unset, bool]): Indicates whether isgeocoded.
        pending_geocode (Union[Unset, bool]): Indicates whether pendinggeocode.
        invalid_geocode (Union[Unset, bool]): Indicates whether invalidgeocode.
        map_context_id (Union[Unset, str]): The mapcontextid.
        image_key (Union[Unset, str]): The imagekey.
    """

    id: Union[Unset, str] = UNSET
    contact_info: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    primary: Union[Unset, str] = UNSET
    do_not_contact: Union[Unset, str] = UNSET
    confidential: Union[Unset, bool] = UNSET
    former: Union[Unset, bool] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    geocoded: Union[Unset, bool] = UNSET
    pending_geocode: Union[Unset, bool] = UNSET
    invalid_geocode: Union[Unset, bool] = UNSET
    map_context_id: Union[Unset, str] = UNSET
    image_key: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        contact_info = self.contact_info

        type = self.type

        primary = self.primary

        do_not_contact = self.do_not_contact

        confidential = self.confidential

        former = self.former

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        geocoded = self.geocoded

        pending_geocode = self.pending_geocode

        invalid_geocode = self.invalid_geocode

        map_context_id = self.map_context_id

        image_key = self.image_key

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if contact_info is not UNSET:
            field_dict["contact_info"] = contact_info
        if type is not UNSET:
            field_dict["type"] = type
        if primary is not UNSET:
            field_dict["primary"] = primary
        if do_not_contact is not UNSET:
            field_dict["do_not_contact"] = do_not_contact
        if confidential is not UNSET:
            field_dict["confidential"] = confidential
        if former is not UNSET:
            field_dict["former"] = former
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if geocoded is not UNSET:
            field_dict["geocoded"] = geocoded
        if pending_geocode is not UNSET:
            field_dict["pending_geocode"] = pending_geocode
        if invalid_geocode is not UNSET:
            field_dict["invalid_geocode"] = invalid_geocode
        if map_context_id is not UNSET:
            field_dict["map_context_id"] = map_context_id
        if image_key is not UNSET:
            field_dict["image_key"] = image_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        contact_info = d.pop("contact_info", UNSET)

        type = d.pop("type", UNSET)

        primary = d.pop("primary", UNSET)

        do_not_contact = d.pop("do_not_contact", UNSET)

        confidential = d.pop("confidential", UNSET)

        former = d.pop("former", UNSET)

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

        geocoded = d.pop("geocoded", UNSET)

        pending_geocode = d.pop("pending_geocode", UNSET)

        invalid_geocode = d.pop("invalid_geocode", UNSET)

        map_context_id = d.pop("map_context_id", UNSET)

        image_key = d.pop("image_key", UNSET)

        constituent_address_list_summary = cls(
            id=id,
            contact_info=contact_info,
            type=type,
            primary=primary,
            do_not_contact=do_not_contact,
            confidential=confidential,
            former=former,
            start_date=start_date,
            end_date=end_date,
            geocoded=geocoded,
            pending_geocode=pending_geocode,
            invalid_geocode=invalid_geocode,
            map_context_id=map_context_id,
            image_key=image_key,
        )

        return constituent_address_list_summary
