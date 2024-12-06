import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RelationshipJobInfoListSummary")


@_attrs_define
class RelationshipJobInfoListSummary:
    """ListRelationshipJobInfos.

    Attributes:
        relationship_set_id (Union[Unset, str]): The relationshipsetid.
        id (Union[Unset, str]): The ID.
        reciprocal_id (Union[Unset, str]): The reciprocalid.
        name (Union[Unset, str]): The name.
        job_title (Union[Unset, str]): The job title.
        job_category (Union[Unset, str]): The job category.
        career_level (Union[Unset, str]): The career level.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        job_schedule (Union[Unset, str]): The schedule.
        job_department (Union[Unset, str]): The department.
        job_division (Union[Unset, str]): The division.
        job_responsibility (Union[Unset, str]): The responsibilities.
        private_record (Union[Unset, bool]): Indicates whether is private.
    """

    relationship_set_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    reciprocal_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    job_title: Union[Unset, str] = UNSET
    job_category: Union[Unset, str] = UNSET
    career_level: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    job_schedule: Union[Unset, str] = UNSET
    job_department: Union[Unset, str] = UNSET
    job_division: Union[Unset, str] = UNSET
    job_responsibility: Union[Unset, str] = UNSET
    private_record: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        relationship_set_id = self.relationship_set_id

        id = self.id

        reciprocal_id = self.reciprocal_id

        name = self.name

        job_title = self.job_title

        job_category = self.job_category

        career_level = self.career_level

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        job_schedule = self.job_schedule

        job_department = self.job_department

        job_division = self.job_division

        job_responsibility = self.job_responsibility

        private_record = self.private_record

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if relationship_set_id is not UNSET:
            field_dict["relationship_set_id"] = relationship_set_id
        if id is not UNSET:
            field_dict["id"] = id
        if reciprocal_id is not UNSET:
            field_dict["reciprocal_id"] = reciprocal_id
        if name is not UNSET:
            field_dict["name"] = name
        if job_title is not UNSET:
            field_dict["job_title"] = job_title
        if job_category is not UNSET:
            field_dict["job_category"] = job_category
        if career_level is not UNSET:
            field_dict["career_level"] = career_level
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if job_schedule is not UNSET:
            field_dict["job_schedule"] = job_schedule
        if job_department is not UNSET:
            field_dict["job_department"] = job_department
        if job_division is not UNSET:
            field_dict["job_division"] = job_division
        if job_responsibility is not UNSET:
            field_dict["job_responsibility"] = job_responsibility
        if private_record is not UNSET:
            field_dict["private_record"] = private_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        relationship_set_id = d.pop("relationship_set_id", UNSET)

        id = d.pop("id", UNSET)

        reciprocal_id = d.pop("reciprocal_id", UNSET)

        name = d.pop("name", UNSET)

        job_title = d.pop("job_title", UNSET)

        job_category = d.pop("job_category", UNSET)

        career_level = d.pop("career_level", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        job_schedule = d.pop("job_schedule", UNSET)

        job_department = d.pop("job_department", UNSET)

        job_division = d.pop("job_division", UNSET)

        job_responsibility = d.pop("job_responsibility", UNSET)

        private_record = d.pop("private_record", UNSET)

        relationship_job_info_list_summary = cls(
            relationship_set_id=relationship_set_id,
            id=id,
            reciprocal_id=reciprocal_id,
            name=name,
            job_title=job_title,
            job_category=job_category,
            career_level=career_level,
            start_date=start_date,
            end_date=end_date,
            job_schedule=job_schedule,
            job_department=job_department,
            job_division=job_division,
            job_responsibility=job_responsibility,
            private_record=private_record,
        )

        return relationship_job_info_list_summary
