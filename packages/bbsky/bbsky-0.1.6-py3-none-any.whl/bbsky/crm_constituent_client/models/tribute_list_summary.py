import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TributeListSummary")


@_attrs_define
class TributeListSummary:
    """ListTributes.

    Attributes:
        id (Union[Unset, str]): The ID.
        tribute_text (Union[Unset, str]): The tribute text.
        tribute_type (Union[Unset, str]): The tribute type.
        active (Union[Unset, bool]): Indicates whether is active.
        date_created (Union[Unset, datetime.datetime]): The date created. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        tributee (Union[Unset, bool]): Indicates whether is tributee.
        acknowledgee (Union[Unset, bool]): Indicates whether is acknowledgee.
        sites (Union[Unset, str]): The sites.
    """

    id: Union[Unset, str] = UNSET
    tribute_text: Union[Unset, str] = UNSET
    tribute_type: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    tributee: Union[Unset, bool] = UNSET
    acknowledgee: Union[Unset, bool] = UNSET
    sites: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tribute_text = self.tribute_text

        tribute_type = self.tribute_type

        active = self.active

        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        tributee = self.tributee

        acknowledgee = self.acknowledgee

        sites = self.sites

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tribute_text is not UNSET:
            field_dict["tribute_text"] = tribute_text
        if tribute_type is not UNSET:
            field_dict["tribute_type"] = tribute_type
        if active is not UNSET:
            field_dict["active"] = active
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if tributee is not UNSET:
            field_dict["tributee"] = tributee
        if acknowledgee is not UNSET:
            field_dict["acknowledgee"] = acknowledgee
        if sites is not UNSET:
            field_dict["sites"] = sites

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        tribute_text = d.pop("tribute_text", UNSET)

        tribute_type = d.pop("tribute_type", UNSET)

        active = d.pop("active", UNSET)

        _date_created = d.pop("date_created", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        tributee = d.pop("tributee", UNSET)

        acknowledgee = d.pop("acknowledgee", UNSET)

        sites = d.pop("sites", UNSET)

        tribute_list_summary = cls(
            id=id,
            tribute_text=tribute_text,
            tribute_type=tribute_type,
            active=active,
            date_created=date_created,
            tributee=tributee,
            acknowledgee=acknowledgee,
            sites=sites,
        )

        return tribute_list_summary
