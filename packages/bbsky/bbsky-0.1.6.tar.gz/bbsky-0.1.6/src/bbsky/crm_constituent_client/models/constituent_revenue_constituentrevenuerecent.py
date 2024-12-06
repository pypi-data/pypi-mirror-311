import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentRevenueConstituentrevenuerecent")


@_attrs_define
class ConstituentRevenueConstituentrevenuerecent:
    """ConstituentRevenueConstituentrevenuerecent.

    Attributes:
        id (Union[Unset, str]): revenue split id
        date (Union[Unset, datetime.date]): date
        type (Union[Unset, str]): type
        amount (Union[Unset, float]): amount
        currency_id (Union[Unset, str]): currency id
        given_anonymously (Union[Unset, bool]): given anonymously
    """

    id: Union[Unset, str] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    type: Union[Unset, str] = UNSET
    amount: Union[Unset, float] = UNSET
    currency_id: Union[Unset, str] = UNSET
    given_anonymously: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        type = self.type

        amount = self.amount

        currency_id = self.currency_id

        given_anonymously = self.given_anonymously

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if date is not UNSET:
            field_dict["date"] = date
        if type is not UNSET:
            field_dict["type"] = type
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency_id is not UNSET:
            field_dict["currency_id"] = currency_id
        if given_anonymously is not UNSET:
            field_dict["given_anonymously"] = given_anonymously

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        type = d.pop("type", UNSET)

        amount = d.pop("amount", UNSET)

        currency_id = d.pop("currency_id", UNSET)

        given_anonymously = d.pop("given_anonymously", UNSET)

        constituent_revenue_constituentrevenuerecent = cls(
            id=id,
            date=date,
            type=type,
            amount=amount,
            currency_id=currency_id,
            given_anonymously=given_anonymously,
        )

        constituent_revenue_constituentrevenuerecent.additional_properties = d
        return constituent_revenue_constituentrevenuerecent

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
