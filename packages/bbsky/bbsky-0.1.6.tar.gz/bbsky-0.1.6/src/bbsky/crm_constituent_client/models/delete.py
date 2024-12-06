from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Delete")


@_attrs_define
class Delete:
    """DeleteConstituent."""

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        delete = cls()

        return delete
