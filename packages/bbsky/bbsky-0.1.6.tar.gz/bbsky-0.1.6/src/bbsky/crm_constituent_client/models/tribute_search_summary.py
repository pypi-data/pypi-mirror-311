import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TributeSearchSummary")


@_attrs_define
class TributeSearchSummary:
    """SearchTributes.

    Attributes:
        id (Union[Unset, str]): The ID.
        tribute_text (Union[Unset, str]): The tribute text.
        tributee_name (Union[Unset, str]): The tributee.
        tribute_type (Union[Unset, str]): The tribute type.
        date_created (Union[Unset, datetime.datetime]): The date created. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        active (Union[Unset, bool]): Indicates whether is active.
        designation_id (Union[Unset, str]): The default designation ID.
        designation (Union[Unset, str]): The default designation.
        site_id (Union[Unset, str]): The site.
    """

    id: Union[Unset, str] = UNSET
    tribute_text: Union[Unset, str] = UNSET
    tributee_name: Union[Unset, str] = UNSET
    tribute_type: Union[Unset, str] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    active: Union[Unset, bool] = UNSET
    designation_id: Union[Unset, str] = UNSET
    designation: Union[Unset, str] = UNSET
    site_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tribute_text = self.tribute_text

        tributee_name = self.tributee_name

        tribute_type = self.tribute_type

        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        active = self.active

        designation_id = self.designation_id

        designation = self.designation

        site_id = self.site_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tribute_text is not UNSET:
            field_dict["tribute_text"] = tribute_text
        if tributee_name is not UNSET:
            field_dict["tributee_name"] = tributee_name
        if tribute_type is not UNSET:
            field_dict["tribute_type"] = tribute_type
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if active is not UNSET:
            field_dict["active"] = active
        if designation_id is not UNSET:
            field_dict["designation_id"] = designation_id
        if designation is not UNSET:
            field_dict["designation"] = designation
        if site_id is not UNSET:
            field_dict["site_id"] = site_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        tribute_text = d.pop("tribute_text", UNSET)

        tributee_name = d.pop("tributee_name", UNSET)

        tribute_type = d.pop("tribute_type", UNSET)

        _date_created = d.pop("date_created", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        active = d.pop("active", UNSET)

        designation_id = d.pop("designation_id", UNSET)

        designation = d.pop("designation", UNSET)

        site_id = d.pop("site_id", UNSET)

        tribute_search_summary = cls(
            id=id,
            tribute_text=tribute_text,
            tributee_name=tributee_name,
            tribute_type=tribute_type,
            date_created=date_created,
            active=active,
            designation_id=designation_id,
            designation=designation,
            site_id=site_id,
        )

        return tribute_search_summary
