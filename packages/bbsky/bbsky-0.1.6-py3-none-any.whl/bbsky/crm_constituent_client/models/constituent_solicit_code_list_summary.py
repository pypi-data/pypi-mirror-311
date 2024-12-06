import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentSolicitCodeListSummary")


@_attrs_define
class ConstituentSolicitCodeListSummary:
    """ListConstituentSolicitCodes.

    Attributes:
        id (Union[Unset, str]): The ID.
        description (Union[Unset, str]): The code.
        site (Union[Unset, str]): The site.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        comments (Union[Unset, str]): The comments.
        expired (Union[Unset, bool]): Indicates whether expired.
        editable (Union[Unset, bool]): Indicates whether editable.
        solicit_code_id (Union[Unset, str]): The solicit code ID.
        consent_preference (Union[Unset, str]): The preference. Available values are <i>no response</i>, <i>opt-out</i>,
            <i>opt-in</i>, <i></i>
        source (Union[Unset, str]): The source.
        source_file_path (Union[Unset, bool]): Indicates whether source file.
        privacy_policy_file_path (Union[Unset, bool]): Indicates whether privacy policy.
        supporting_information (Union[Unset, bool]): Indicates whether supporting information.
        consent_statement (Union[Unset, bool]): Indicates whether consent statement.
        consent_code (Union[Unset, int]): The consent code.
    """

    id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    site: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    comments: Union[Unset, str] = UNSET
    expired: Union[Unset, bool] = UNSET
    editable: Union[Unset, bool] = UNSET
    solicit_code_id: Union[Unset, str] = UNSET
    consent_preference: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    source_file_path: Union[Unset, bool] = UNSET
    privacy_policy_file_path: Union[Unset, bool] = UNSET
    supporting_information: Union[Unset, bool] = UNSET
    consent_statement: Union[Unset, bool] = UNSET
    consent_code: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        description = self.description

        site = self.site

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        comments = self.comments

        expired = self.expired

        editable = self.editable

        solicit_code_id = self.solicit_code_id

        consent_preference = self.consent_preference

        source = self.source

        source_file_path = self.source_file_path

        privacy_policy_file_path = self.privacy_policy_file_path

        supporting_information = self.supporting_information

        consent_statement = self.consent_statement

        consent_code = self.consent_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if site is not UNSET:
            field_dict["site"] = site
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if comments is not UNSET:
            field_dict["comments"] = comments
        if expired is not UNSET:
            field_dict["expired"] = expired
        if editable is not UNSET:
            field_dict["editable"] = editable
        if solicit_code_id is not UNSET:
            field_dict["solicit_code_id"] = solicit_code_id
        if consent_preference is not UNSET:
            field_dict["consent_preference"] = consent_preference
        if source is not UNSET:
            field_dict["source"] = source
        if source_file_path is not UNSET:
            field_dict["source_file_path"] = source_file_path
        if privacy_policy_file_path is not UNSET:
            field_dict["privacy_policy_file_path"] = privacy_policy_file_path
        if supporting_information is not UNSET:
            field_dict["supporting_information"] = supporting_information
        if consent_statement is not UNSET:
            field_dict["consent_statement"] = consent_statement
        if consent_code is not UNSET:
            field_dict["consent_code"] = consent_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        site = d.pop("site", UNSET)

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

        comments = d.pop("comments", UNSET)

        expired = d.pop("expired", UNSET)

        editable = d.pop("editable", UNSET)

        solicit_code_id = d.pop("solicit_code_id", UNSET)

        consent_preference = d.pop("consent_preference", UNSET)

        source = d.pop("source", UNSET)

        source_file_path = d.pop("source_file_path", UNSET)

        privacy_policy_file_path = d.pop("privacy_policy_file_path", UNSET)

        supporting_information = d.pop("supporting_information", UNSET)

        consent_statement = d.pop("consent_statement", UNSET)

        consent_code = d.pop("consent_code", UNSET)

        constituent_solicit_code_list_summary = cls(
            id=id,
            description=description,
            site=site,
            start_date=start_date,
            end_date=end_date,
            comments=comments,
            expired=expired,
            editable=editable,
            solicit_code_id=solicit_code_id,
            consent_preference=consent_preference,
            source=source,
            source_file_path=source_file_path,
            privacy_policy_file_path=privacy_policy_file_path,
            supporting_information=supporting_information,
            consent_statement=consent_statement,
            consent_code=consent_code,
        )

        return constituent_solicit_code_list_summary
