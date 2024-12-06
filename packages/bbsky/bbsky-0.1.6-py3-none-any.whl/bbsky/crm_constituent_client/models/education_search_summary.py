from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="EducationSearchSummary")


@_attrs_define
class EducationSearchSummary:
    r"""SearchEducations.

    Attributes:
        id (Union[Unset, str]): The ID.
        full_name_educational_institution (Union[Unset, str]): The full name\educational institution.
        constituent_name (Union[Unset, str]): The constituent name.
        constituent_lookup_id (Union[Unset, str]): The constituent lookup ID.
        constituent_address (Union[Unset, str]): The constituent address.
        constituent_city (Union[Unset, str]): The constituent city.
        constituent_state (Union[Unset, str]): The constituent state.
        constituent_post_code (Union[Unset, str]): The constituent zip/postal code.
        educational_institution (Union[Unset, str]): The educational institution.
        program (Union[Unset, str]): The program.
        degree (Union[Unset, str]): The degree.
        status (Union[Unset, str]): The status.
        class_year (Union[Unset, str]): The class year.
        educational_history_status (Union[Unset, str]): The status.
    """

    id: Union[Unset, str] = UNSET
    full_name_educational_institution: Union[Unset, str] = UNSET
    constituent_name: Union[Unset, str] = UNSET
    constituent_lookup_id: Union[Unset, str] = UNSET
    constituent_address: Union[Unset, str] = UNSET
    constituent_city: Union[Unset, str] = UNSET
    constituent_state: Union[Unset, str] = UNSET
    constituent_post_code: Union[Unset, str] = UNSET
    educational_institution: Union[Unset, str] = UNSET
    program: Union[Unset, str] = UNSET
    degree: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    class_year: Union[Unset, str] = UNSET
    educational_history_status: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        full_name_educational_institution = self.full_name_educational_institution

        constituent_name = self.constituent_name

        constituent_lookup_id = self.constituent_lookup_id

        constituent_address = self.constituent_address

        constituent_city = self.constituent_city

        constituent_state = self.constituent_state

        constituent_post_code = self.constituent_post_code

        educational_institution = self.educational_institution

        program = self.program

        degree = self.degree

        status = self.status

        class_year = self.class_year

        educational_history_status = self.educational_history_status

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if full_name_educational_institution is not UNSET:
            field_dict["full_name_educational_institution"] = full_name_educational_institution
        if constituent_name is not UNSET:
            field_dict["constituent_name"] = constituent_name
        if constituent_lookup_id is not UNSET:
            field_dict["constituent_lookup_id"] = constituent_lookup_id
        if constituent_address is not UNSET:
            field_dict["constituent_address"] = constituent_address
        if constituent_city is not UNSET:
            field_dict["constituent_city"] = constituent_city
        if constituent_state is not UNSET:
            field_dict["constituent_state"] = constituent_state
        if constituent_post_code is not UNSET:
            field_dict["constituent_post_code"] = constituent_post_code
        if educational_institution is not UNSET:
            field_dict["educational_institution"] = educational_institution
        if program is not UNSET:
            field_dict["program"] = program
        if degree is not UNSET:
            field_dict["degree"] = degree
        if status is not UNSET:
            field_dict["status"] = status
        if class_year is not UNSET:
            field_dict["class_year"] = class_year
        if educational_history_status is not UNSET:
            field_dict["educational_history_status"] = educational_history_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        full_name_educational_institution = d.pop("full_name_educational_institution", UNSET)

        constituent_name = d.pop("constituent_name", UNSET)

        constituent_lookup_id = d.pop("constituent_lookup_id", UNSET)

        constituent_address = d.pop("constituent_address", UNSET)

        constituent_city = d.pop("constituent_city", UNSET)

        constituent_state = d.pop("constituent_state", UNSET)

        constituent_post_code = d.pop("constituent_post_code", UNSET)

        educational_institution = d.pop("educational_institution", UNSET)

        program = d.pop("program", UNSET)

        degree = d.pop("degree", UNSET)

        status = d.pop("status", UNSET)

        class_year = d.pop("class_year", UNSET)

        educational_history_status = d.pop("educational_history_status", UNSET)

        education_search_summary = cls(
            id=id,
            full_name_educational_institution=full_name_educational_institution,
            constituent_name=constituent_name,
            constituent_lookup_id=constituent_lookup_id,
            constituent_address=constituent_address,
            constituent_city=constituent_city,
            constituent_state=constituent_state,
            constituent_post_code=constituent_post_code,
            educational_institution=educational_institution,
            program=program,
            degree=degree,
            status=status,
            class_year=class_year,
            educational_history_status=educational_history_status,
        )

        return education_search_summary
