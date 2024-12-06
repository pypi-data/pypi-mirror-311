from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuzzy_date import FuzzyDate


T = TypeVar("T", bound="EducationListSummary")


@_attrs_define
class EducationListSummary:
    """ListEducations.

    Attributes:
        id (Union[Unset, str]): The ID.
        program (Union[Unset, str]): The program.
        name (Union[Unset, str]): The educational institution.
        degree (Union[Unset, str]): The degree.
        class_of (Union[Unset, int]): The class of.
        constituency_status (Union[Unset, str]): The status.
        primary_record (Union[Unset, bool]): Indicates whether primary education.
        start_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        end_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        end_date_string (Union[Unset, str]): The date to.
        education_history_status (Union[Unset, str]): The status.
        affiliated (Union[Unset, bool]): Indicates whether affiliated.
    """

    id: Union[Unset, str] = UNSET
    program: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    degree: Union[Unset, str] = UNSET
    class_of: Union[Unset, int] = UNSET
    constituency_status: Union[Unset, str] = UNSET
    primary_record: Union[Unset, bool] = UNSET
    start_date: Union[Unset, "FuzzyDate"] = UNSET
    end_date: Union[Unset, "FuzzyDate"] = UNSET
    end_date_string: Union[Unset, str] = UNSET
    education_history_status: Union[Unset, str] = UNSET
    affiliated: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        program = self.program

        name = self.name

        degree = self.degree

        class_of = self.class_of

        constituency_status = self.constituency_status

        primary_record = self.primary_record

        start_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.to_dict()

        end_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.to_dict()

        end_date_string = self.end_date_string

        education_history_status = self.education_history_status

        affiliated = self.affiliated

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if program is not UNSET:
            field_dict["program"] = program
        if name is not UNSET:
            field_dict["name"] = name
        if degree is not UNSET:
            field_dict["degree"] = degree
        if class_of is not UNSET:
            field_dict["class_of"] = class_of
        if constituency_status is not UNSET:
            field_dict["constituency_status"] = constituency_status
        if primary_record is not UNSET:
            field_dict["primary_record"] = primary_record
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if end_date_string is not UNSET:
            field_dict["end_date_string"] = end_date_string
        if education_history_status is not UNSET:
            field_dict["education_history_status"] = education_history_status
        if affiliated is not UNSET:
            field_dict["affiliated"] = affiliated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fuzzy_date import FuzzyDate

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        program = d.pop("program", UNSET)

        name = d.pop("name", UNSET)

        degree = d.pop("degree", UNSET)

        class_of = d.pop("class_of", UNSET)

        constituency_status = d.pop("constituency_status", UNSET)

        primary_record = d.pop("primary_record", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, FuzzyDate]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = FuzzyDate.from_dict(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, FuzzyDate]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = FuzzyDate.from_dict(_end_date)

        end_date_string = d.pop("end_date_string", UNSET)

        education_history_status = d.pop("education_history_status", UNSET)

        affiliated = d.pop("affiliated", UNSET)

        education_list_summary = cls(
            id=id,
            program=program,
            name=name,
            degree=degree,
            class_of=class_of,
            constituency_status=constituency_status,
            primary_record=primary_record,
            start_date=start_date,
            end_date=end_date,
            end_date_string=end_date_string,
            education_history_status=education_history_status,
            affiliated=affiliated,
        )

        return education_list_summary
