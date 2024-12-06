from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewIndividualZipLookupCountries")


@_attrs_define
class NewIndividualZipLookupCountries:
    """NewIndividualZipLookupCountries.

    Attributes:
        country_id (Union[Unset, str]): countryid
        country_name (Union[Unset, str]): name
    """

    country_id: Union[Unset, str] = UNSET
    country_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        country_id = self.country_id

        country_name = self.country_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if country_id is not UNSET:
            field_dict["country_id"] = country_id
        if country_name is not UNSET:
            field_dict["country_name"] = country_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        country_id = d.pop("country_id", UNSET)

        country_name = d.pop("country_name", UNSET)

        new_individual_zip_lookup_countries = cls(
            country_id=country_id,
            country_name=country_name,
        )

        new_individual_zip_lookup_countries.additional_properties = d
        return new_individual_zip_lookup_countries

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
