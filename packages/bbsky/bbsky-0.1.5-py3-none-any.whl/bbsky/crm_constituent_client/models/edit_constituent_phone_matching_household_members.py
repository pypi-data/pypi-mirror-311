from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditConstituentPhoneMatchingHouseholdMembers")


@_attrs_define
class EditConstituentPhoneMatchingHouseholdMembers:
    """EditConstituentPhoneMatchingHouseholdMembers.

    Attributes:
        constituent_id (Union[Unset, str]): constituent id
        name (Union[Unset, str]): household member
        relationship_to_primary (Union[Unset, str]): relationship to primary
    """

    constituent_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    relationship_to_primary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        name = self.name

        relationship_to_primary = self.relationship_to_primary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if constituent_id is not UNSET:
            field_dict["constituent_id"] = constituent_id
        if name is not UNSET:
            field_dict["name"] = name
        if relationship_to_primary is not UNSET:
            field_dict["relationship_to_primary"] = relationship_to_primary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        constituent_id = d.pop("constituent_id", UNSET)

        name = d.pop("name", UNSET)

        relationship_to_primary = d.pop("relationship_to_primary", UNSET)

        edit_constituent_phone_matching_household_members = cls(
            constituent_id=constituent_id,
            name=name,
            relationship_to_primary=relationship_to_primary,
        )

        edit_constituent_phone_matching_household_members.additional_properties = d
        return edit_constituent_phone_matching_household_members

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
