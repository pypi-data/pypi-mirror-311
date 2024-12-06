from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAlternateLookupIdListSummary")


@_attrs_define
class ConstituentAlternateLookupIdListSummary:
    """ListConstituentAlternateLookupIds.

    Attributes:
        id (Union[Unset, str]): The ID.
        type (Union[Unset, str]): The type.
        alternate_lookup_id (Union[Unset, str]): The lookup ID.
    """

    id: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    alternate_lookup_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        type = self.type

        alternate_lookup_id = self.alternate_lookup_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if alternate_lookup_id is not UNSET:
            field_dict["alternate_lookup_id"] = alternate_lookup_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        type = d.pop("type", UNSET)

        alternate_lookup_id = d.pop("alternate_lookup_id", UNSET)

        constituent_alternate_lookup_id_list_summary = cls(
            id=id,
            type=type,
            alternate_lookup_id=alternate_lookup_id,
        )

        return constituent_alternate_lookup_id_list_summary
