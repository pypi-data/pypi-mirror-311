from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EducationAffiliatedAdditionalInformation")


@_attrs_define
class EducationAffiliatedAdditionalInformation:
    """EducationAffiliatedAdditionalInformation.

    Attributes:
        id (Union[Unset, str]): id
        academiccatalogcollege (Union[Unset, str]): The college/school. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/70f445a9-9efd-436e-a724-
            4be727219dd5?parameters=academiccatalogdegreeid,{academiccatalogdegreeid}.
        academiccatalogdivision (Union[Unset, str]): The division. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/6d688d29-3846-4285-8bf7-
            2e24c29acef1?parameters=academiccatalogcollegeid,{academiccatalogcollegeid}.
        academiccatalogdepartment (Union[Unset, str]): The department. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/1093fae2-baf1-4488-9332-
            74d9193741ca?parameters=academiccatalogcollegeid,{academiccatalogcollegeid}&parameters=academiccatalogdivisionid
            ,{academiccatalogdivisionid}.
        academiccatalogsubdepartment (Union[Unset, str]): The sub department. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/b1da0663-f912-4533-abc2-
            de27bcbe8b10?parameters=academiccatalogdepartmentid,{academiccatalogdepartmentid}.
        academiccatalogdegreetype (Union[Unset, str]): The degree type. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/02026401-2351-4e56-832c-
            299c9426c649?parameters=academiccatalogdepartmentid,{academiccatalogdepartmentid}&parameters=academiccatalogsubd
            epartmentid,{academiccatalogsubdepartmentid}.
    """

    id: Union[Unset, str] = UNSET
    academiccatalogcollege: Union[Unset, str] = UNSET
    academiccatalogdivision: Union[Unset, str] = UNSET
    academiccatalogdepartment: Union[Unset, str] = UNSET
    academiccatalogsubdepartment: Union[Unset, str] = UNSET
    academiccatalogdegreetype: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        academiccatalogcollege = self.academiccatalogcollege

        academiccatalogdivision = self.academiccatalogdivision

        academiccatalogdepartment = self.academiccatalogdepartment

        academiccatalogsubdepartment = self.academiccatalogsubdepartment

        academiccatalogdegreetype = self.academiccatalogdegreetype

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if academiccatalogcollege is not UNSET:
            field_dict["academiccatalogcollege"] = academiccatalogcollege
        if academiccatalogdivision is not UNSET:
            field_dict["academiccatalogdivision"] = academiccatalogdivision
        if academiccatalogdepartment is not UNSET:
            field_dict["academiccatalogdepartment"] = academiccatalogdepartment
        if academiccatalogsubdepartment is not UNSET:
            field_dict["academiccatalogsubdepartment"] = academiccatalogsubdepartment
        if academiccatalogdegreetype is not UNSET:
            field_dict["academiccatalogdegreetype"] = academiccatalogdegreetype

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        academiccatalogcollege = d.pop("academiccatalogcollege", UNSET)

        academiccatalogdivision = d.pop("academiccatalogdivision", UNSET)

        academiccatalogdepartment = d.pop("academiccatalogdepartment", UNSET)

        academiccatalogsubdepartment = d.pop("academiccatalogsubdepartment", UNSET)

        academiccatalogdegreetype = d.pop("academiccatalogdegreetype", UNSET)

        education_affiliated_additional_information = cls(
            id=id,
            academiccatalogcollege=academiccatalogcollege,
            academiccatalogdivision=academiccatalogdivision,
            academiccatalogdepartment=academiccatalogdepartment,
            academiccatalogsubdepartment=academiccatalogsubdepartment,
            academiccatalogdegreetype=academiccatalogdegreetype,
        )

        education_affiliated_additional_information.additional_properties = d
        return education_affiliated_additional_information

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
