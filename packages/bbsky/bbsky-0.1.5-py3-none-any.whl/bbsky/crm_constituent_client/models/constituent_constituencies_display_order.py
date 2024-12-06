from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentConstituenciesDisplayOrder")


@_attrs_define
class ConstituentConstituenciesDisplayOrder:
    """ConstituentConstituenciesDisplayOrder.

    Attributes:
        id (Union[Unset, str]): id
        description (Union[Unset, str]): description
        sequence (Union[Unset, int]): sequence
        system (Union[Unset, bool]): issystem
    """

    id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    sequence: Union[Unset, int] = UNSET
    system: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        description = self.description

        sequence = self.sequence

        system = self.system

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if sequence is not UNSET:
            field_dict["sequence"] = sequence
        if system is not UNSET:
            field_dict["system"] = system

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        sequence = d.pop("sequence", UNSET)

        system = d.pop("system", UNSET)

        constituent_constituencies_display_order = cls(
            id=id,
            description=description,
            sequence=sequence,
            system=system,
        )

        constituent_constituencies_display_order.additional_properties = d
        return constituent_constituencies_display_order

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
