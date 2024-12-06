from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditConstituentAlternateLookupId")


@_attrs_define
class EditConstituentAlternateLookupId:
    """EditConstituentAlternateLookupId.

    Example:
        {'alternate_lookup_id_type': '', 'alternate_lookup_id': ''}

    Attributes:
        alternate_lookup_id_type (Union[Unset, str]): The type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/alternatelookupidtypecode/entries
        alternate_lookup_id (Union[Unset, str]): The lookup ID.
    """

    alternate_lookup_id_type: Union[Unset, str] = UNSET
    alternate_lookup_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        alternate_lookup_id_type = self.alternate_lookup_id_type

        alternate_lookup_id = self.alternate_lookup_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if alternate_lookup_id_type is not UNSET:
            field_dict["alternate_lookup_id_type"] = alternate_lookup_id_type
        if alternate_lookup_id is not UNSET:
            field_dict["alternate_lookup_id"] = alternate_lookup_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        alternate_lookup_id_type = d.pop("alternate_lookup_id_type", UNSET)

        alternate_lookup_id = d.pop("alternate_lookup_id", UNSET)

        edit_constituent_alternate_lookup_id = cls(
            alternate_lookup_id_type=alternate_lookup_id_type,
            alternate_lookup_id=alternate_lookup_id,
        )

        return edit_constituent_alternate_lookup_id
