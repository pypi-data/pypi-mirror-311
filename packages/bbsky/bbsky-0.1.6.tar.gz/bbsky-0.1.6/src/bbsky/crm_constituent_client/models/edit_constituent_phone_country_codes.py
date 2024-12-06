from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditConstituentPhoneCountryCodes")


@_attrs_define
class EditConstituentPhoneCountryCodes:
    """EditConstituentPhoneCountryCodes.

    Attributes:
        country_id (Union[Unset, str]): countryid
        country_code (Union[Unset, str]): country code
    """

    country_id: Union[Unset, str] = UNSET
    country_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        country_id = self.country_id

        country_code = self.country_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if country_id is not UNSET:
            field_dict["country_id"] = country_id
        if country_code is not UNSET:
            field_dict["country_code"] = country_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        country_id = d.pop("country_id", UNSET)

        country_code = d.pop("country_code", UNSET)

        edit_constituent_phone_country_codes = cls(
            country_id=country_id,
            country_code=country_code,
        )

        edit_constituent_phone_country_codes.additional_properties = d
        return edit_constituent_phone_country_codes

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
