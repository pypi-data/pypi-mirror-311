from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FuzzyDate")


@_attrs_define
class FuzzyDate:
    """FuzzyDate.

    Example:
        {'year': 2024, 'month': 4, 'day': 13}

    Attributes:
        year (Union[Unset, int]): The year.
        month (Union[Unset, int]): The month.
        day (Union[Unset, int]): The day.
    """

    year: Union[Unset, int] = UNSET
    month: Union[Unset, int] = UNSET
    day: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        year = self.year

        month = self.month

        day = self.day

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if year is not UNSET:
            field_dict["year"] = year
        if month is not UNSET:
            field_dict["month"] = month
        if day is not UNSET:
            field_dict["day"] = day

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        year = d.pop("year", UNSET)

        month = d.pop("month", UNSET)

        day = d.pop("day", UNSET)

        fuzzy_date = cls(
            year=year,
            month=month,
            day=day,
        )

        fuzzy_date.additional_properties = d
        return fuzzy_date

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
