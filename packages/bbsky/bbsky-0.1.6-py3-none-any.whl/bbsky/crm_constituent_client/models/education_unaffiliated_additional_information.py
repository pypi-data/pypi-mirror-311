from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EducationUnaffiliatedAdditionalInformation")


@_attrs_define
class EducationUnaffiliatedAdditionalInformation:
    """EducationUnaffiliatedAdditionalInformation.

    Attributes:
        id (Union[Unset, str]): id
        educational_college (Union[Unset, str]): The college/school. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalcollegecode/entries
        educational_division (Union[Unset, str]): The division. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationaldivisioncode/entries
        educational_department (Union[Unset, str]): The department. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationaldepartmentcode/entries
        educational_sub_department (Union[Unset, str]): The sub department. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalsubdepartmentcode/entries
        educational_degree_type (Union[Unset, str]): The degree type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationaldegreetypecode/entries
    """

    id: Union[Unset, str] = UNSET
    educational_college: Union[Unset, str] = UNSET
    educational_division: Union[Unset, str] = UNSET
    educational_department: Union[Unset, str] = UNSET
    educational_sub_department: Union[Unset, str] = UNSET
    educational_degree_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        educational_college = self.educational_college

        educational_division = self.educational_division

        educational_department = self.educational_department

        educational_sub_department = self.educational_sub_department

        educational_degree_type = self.educational_degree_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if educational_college is not UNSET:
            field_dict["educational_college"] = educational_college
        if educational_division is not UNSET:
            field_dict["educational_division"] = educational_division
        if educational_department is not UNSET:
            field_dict["educational_department"] = educational_department
        if educational_sub_department is not UNSET:
            field_dict["educational_sub_department"] = educational_sub_department
        if educational_degree_type is not UNSET:
            field_dict["educational_degree_type"] = educational_degree_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        educational_college = d.pop("educational_college", UNSET)

        educational_division = d.pop("educational_division", UNSET)

        educational_department = d.pop("educational_department", UNSET)

        educational_sub_department = d.pop("educational_sub_department", UNSET)

        educational_degree_type = d.pop("educational_degree_type", UNSET)

        education_unaffiliated_additional_information = cls(
            id=id,
            educational_college=educational_college,
            educational_division=educational_division,
            educational_department=educational_department,
            educational_sub_department=educational_sub_department,
            educational_degree_type=educational_degree_type,
        )

        education_unaffiliated_additional_information.additional_properties = d
        return education_unaffiliated_additional_information

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
