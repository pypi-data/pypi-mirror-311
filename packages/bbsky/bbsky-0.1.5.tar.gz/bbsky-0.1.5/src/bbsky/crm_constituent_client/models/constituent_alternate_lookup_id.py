from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ConstituentAlternateLookupId")


@_attrs_define
class ConstituentAlternateLookupId:
    """GetConstituentAlternateLookupId.

    Attributes:
        alternate_lookup_id_type (str): The type. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/alternatelookupidtypecode/entries
        alternate_lookup_id (str): The lookup ID.
    """

    alternate_lookup_id_type: str
    alternate_lookup_id: str

    def to_dict(self) -> Dict[str, Any]:
        alternate_lookup_id_type = self.alternate_lookup_id_type

        alternate_lookup_id = self.alternate_lookup_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "alternate_lookup_id_type": alternate_lookup_id_type,
                "alternate_lookup_id": alternate_lookup_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        alternate_lookup_id_type = d.pop("alternate_lookup_id_type")

        alternate_lookup_id = d.pop("alternate_lookup_id")

        constituent_alternate_lookup_id = cls(
            alternate_lookup_id_type=alternate_lookup_id_type,
            alternate_lookup_id=alternate_lookup_id,
        )

        return constituent_alternate_lookup_id
