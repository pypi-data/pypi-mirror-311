from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentUserDefinedConstituencies")


@_attrs_define
class ConstituentUserDefinedConstituencies:
    """ConstituentUserDefinedConstituencies.

    Attributes:
        description (Union[Unset, str]): description
        sequence (Union[Unset, int]): sequence
    """

    description: Union[Unset, str] = UNSET
    sequence: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        sequence = self.sequence

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if sequence is not UNSET:
            field_dict["sequence"] = sequence

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        sequence = d.pop("sequence", UNSET)

        constituent_user_defined_constituencies = cls(
            description=description,
            sequence=sequence,
        )

        constituent_user_defined_constituencies.additional_properties = d
        return constituent_user_defined_constituencies

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
