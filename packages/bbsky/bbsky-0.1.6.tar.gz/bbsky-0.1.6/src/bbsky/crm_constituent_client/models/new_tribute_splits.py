from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewTributeSplits")


@_attrs_define
class NewTributeSplits:
    """NewTributeSplits.

    Attributes:
        id (Union[Unset, str]): id
        designation_id (Union[Unset, str]): designation
        amount (Union[Unset, float]): amount
        base_currency_id (Union[Unset, str]): currency
    """

    id: Union[Unset, str] = UNSET
    designation_id: Union[Unset, str] = UNSET
    amount: Union[Unset, float] = UNSET
    base_currency_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        designation_id = self.designation_id

        amount = self.amount

        base_currency_id = self.base_currency_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if designation_id is not UNSET:
            field_dict["designation_id"] = designation_id
        if amount is not UNSET:
            field_dict["amount"] = amount
        if base_currency_id is not UNSET:
            field_dict["base_currency_id"] = base_currency_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        designation_id = d.pop("designation_id", UNSET)

        amount = d.pop("amount", UNSET)

        base_currency_id = d.pop("base_currency_id", UNSET)

        new_tribute_splits = cls(
            id=id,
            designation_id=designation_id,
            amount=amount,
            base_currency_id=base_currency_id,
        )

        new_tribute_splits.additional_properties = d
        return new_tribute_splits

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
