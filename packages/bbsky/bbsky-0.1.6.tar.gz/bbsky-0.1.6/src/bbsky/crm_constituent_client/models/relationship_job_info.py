import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RelationshipJobInfo")


@_attrs_define
class RelationshipJobInfo:
    """GetRelationshipJobInfo.

    Attributes:
        job_title (Union[Unset, str]): The job title.
        career_level (Union[Unset, str]): The career level. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/careerlevelcode/entries
        job_category (Union[Unset, str]): The category. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/jobcategorycode/entries
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        job_department (Union[Unset, str]): The department.
        job_division (Union[Unset, str]): The division.
        job_schedule (Union[Unset, str]): The schedule. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/jobschedulecode/entries
        job_responsibility (Union[Unset, str]): The responsibilities.
        private_record (Union[Unset, bool]): Indicates whether is private.
        sync_end_date_to_relationship (Union[Unset, bool]): Indicates whether sync end date with organization
            relationship.
        last_job (Union[Unset, bool]): Indicates whether islastjob. Read-only in the SOAP API.
    """

    job_title: Union[Unset, str] = UNSET
    career_level: Union[Unset, str] = UNSET
    job_category: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    job_department: Union[Unset, str] = UNSET
    job_division: Union[Unset, str] = UNSET
    job_schedule: Union[Unset, str] = UNSET
    job_responsibility: Union[Unset, str] = UNSET
    private_record: Union[Unset, bool] = UNSET
    sync_end_date_to_relationship: Union[Unset, bool] = UNSET
    last_job: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        job_title = self.job_title

        career_level = self.career_level

        job_category = self.job_category

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        job_department = self.job_department

        job_division = self.job_division

        job_schedule = self.job_schedule

        job_responsibility = self.job_responsibility

        private_record = self.private_record

        sync_end_date_to_relationship = self.sync_end_date_to_relationship

        last_job = self.last_job

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if job_title is not UNSET:
            field_dict["job_title"] = job_title
        if career_level is not UNSET:
            field_dict["career_level"] = career_level
        if job_category is not UNSET:
            field_dict["job_category"] = job_category
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if job_department is not UNSET:
            field_dict["job_department"] = job_department
        if job_division is not UNSET:
            field_dict["job_division"] = job_division
        if job_schedule is not UNSET:
            field_dict["job_schedule"] = job_schedule
        if job_responsibility is not UNSET:
            field_dict["job_responsibility"] = job_responsibility
        if private_record is not UNSET:
            field_dict["private_record"] = private_record
        if sync_end_date_to_relationship is not UNSET:
            field_dict["sync_end_date_to_relationship"] = sync_end_date_to_relationship
        if last_job is not UNSET:
            field_dict["last_job"] = last_job

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_title = d.pop("job_title", UNSET)

        career_level = d.pop("career_level", UNSET)

        job_category = d.pop("job_category", UNSET)

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

        job_department = d.pop("job_department", UNSET)

        job_division = d.pop("job_division", UNSET)

        job_schedule = d.pop("job_schedule", UNSET)

        job_responsibility = d.pop("job_responsibility", UNSET)

        private_record = d.pop("private_record", UNSET)

        sync_end_date_to_relationship = d.pop("sync_end_date_to_relationship", UNSET)

        last_job = d.pop("last_job", UNSET)

        relationship_job_info = cls(
            job_title=job_title,
            career_level=career_level,
            job_category=job_category,
            start_date=start_date,
            end_date=end_date,
            job_department=job_department,
            job_division=job_division,
            job_schedule=job_schedule,
            job_responsibility=job_responsibility,
            private_record=private_record,
            sync_end_date_to_relationship=sync_end_date_to_relationship,
            last_job=last_job,
        )

        return relationship_job_info
