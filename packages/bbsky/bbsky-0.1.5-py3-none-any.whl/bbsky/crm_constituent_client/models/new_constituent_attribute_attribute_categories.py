from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewConstituentAttributeAttributeCategories")


@_attrs_define
class NewConstituentAttributeAttributeCategories:
    """NewConstituentAttributeAttributeCategories.

    Attributes:
        id (Union[Unset, str]): id
        data_type_code (Union[Unset, int]): datatypecode
        constituent_search_list_catalog_id (Union[Unset, str]): constituentsearchlistcatalogid
        code_table_name (Union[Unset, str]): codetablename
    """

    id: Union[Unset, str] = UNSET
    data_type_code: Union[Unset, int] = UNSET
    constituent_search_list_catalog_id: Union[Unset, str] = UNSET
    code_table_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        data_type_code = self.data_type_code

        constituent_search_list_catalog_id = self.constituent_search_list_catalog_id

        code_table_name = self.code_table_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if data_type_code is not UNSET:
            field_dict["data_type_code"] = data_type_code
        if constituent_search_list_catalog_id is not UNSET:
            field_dict["constituent_search_list_catalog_id"] = constituent_search_list_catalog_id
        if code_table_name is not UNSET:
            field_dict["code_table_name"] = code_table_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        data_type_code = d.pop("data_type_code", UNSET)

        constituent_search_list_catalog_id = d.pop("constituent_search_list_catalog_id", UNSET)

        code_table_name = d.pop("code_table_name", UNSET)

        new_constituent_attribute_attribute_categories = cls(
            id=id,
            data_type_code=data_type_code,
            constituent_search_list_catalog_id=constituent_search_list_catalog_id,
            code_table_name=code_table_name,
        )

        new_constituent_attribute_attribute_categories.additional_properties = d
        return new_constituent_attribute_attribute_categories

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
