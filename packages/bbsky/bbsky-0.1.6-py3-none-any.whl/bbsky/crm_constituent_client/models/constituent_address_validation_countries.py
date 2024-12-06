from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAddressValidationCountries")


@_attrs_define
class ConstituentAddressValidationCountries:
    """ConstituentAddressValidationCountries.

    Attributes:
        country_id (Union[Unset, str]): countryid
        browsable (Union[Unset, bool]): browsable
    """

    country_id: Union[Unset, str] = UNSET
    browsable: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        country_id = self.country_id

        browsable = self.browsable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if country_id is not UNSET:
            field_dict["country_id"] = country_id
        if browsable is not UNSET:
            field_dict["browsable"] = browsable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        country_id = d.pop("country_id", UNSET)

        browsable = d.pop("browsable", UNSET)

        constituent_address_validation_countries = cls(
            country_id=country_id,
            browsable=browsable,
        )

        constituent_address_validation_countries.additional_properties = d
        return constituent_address_validation_countries

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
