from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentMembershipsListSummary")


@_attrs_define
class ConstituentMembershipsListSummary:
    """ListConstituentMemberships.

    Attributes:
        id (Union[Unset, str]): The ID.
        membership_name (Union[Unset, str]): The membership.
        primary_member_name (Union[Unset, str]): The primary member.
        combo_id (Union[Unset, str]): The combo ID.
        status_code (Union[Unset, int]): The status code.
    """

    id: Union[Unset, str] = UNSET
    membership_name: Union[Unset, str] = UNSET
    primary_member_name: Union[Unset, str] = UNSET
    combo_id: Union[Unset, str] = UNSET
    status_code: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        membership_name = self.membership_name

        primary_member_name = self.primary_member_name

        combo_id = self.combo_id

        status_code = self.status_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if membership_name is not UNSET:
            field_dict["membership_name"] = membership_name
        if primary_member_name is not UNSET:
            field_dict["primary_member_name"] = primary_member_name
        if combo_id is not UNSET:
            field_dict["combo_id"] = combo_id
        if status_code is not UNSET:
            field_dict["status_code"] = status_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        membership_name = d.pop("membership_name", UNSET)

        primary_member_name = d.pop("primary_member_name", UNSET)

        combo_id = d.pop("combo_id", UNSET)

        status_code = d.pop("status_code", UNSET)

        constituent_memberships_list_summary = cls(
            id=id,
            membership_name=membership_name,
            primary_member_name=primary_member_name,
            combo_id=combo_id,
            status_code=status_code,
        )

        return constituent_memberships_list_summary
