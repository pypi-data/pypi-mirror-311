import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditConstituentSolicitCode")


@_attrs_define
class EditConstituentSolicitCode:
    """EditConstituentSolicitCode.

    Example:
        {'solicit_code': 'Do not phone', 'start_date': '', 'end_date': '', 'comments': '', 'consent_preference': 'No
            response', 'source_evidence': '', 'source_file': '', 'privacy_policy': '', 'supporting_information': '',
            'consent_statement': ''}

    Attributes:
        solicit_code (Union[Unset, str]): The solicit code. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/ea7286bd-d27b-4028-b507-
            4bdb92580499?parameters=feature_id,{c5b90f15-b76b-48e3-bf4f-b55c8717d36e}&parameters=feature_type,{1}.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        comments (Union[Unset, str]): The comments.
        consent_preference (Union[Unset, str]): The preference. Available values are <i>no response</i>, <i>opt-out</i>,
            <i>opt-in</i>
        source_evidence (Union[Unset, str]): The source. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/dataprotectionevidencesourcecode/entries
        source_file (Union[Unset, str]): The source file.
        privacy_policy (Union[Unset, str]): The privacy policy.
        supporting_information (Union[Unset, str]): The supporting information.
        consent_statement (Union[Unset, str]): The consent statement.
    """

    solicit_code: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    comments: Union[Unset, str] = UNSET
    consent_preference: Union[Unset, str] = UNSET
    source_evidence: Union[Unset, str] = UNSET
    source_file: Union[Unset, str] = UNSET
    privacy_policy: Union[Unset, str] = UNSET
    supporting_information: Union[Unset, str] = UNSET
    consent_statement: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        solicit_code = self.solicit_code

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        comments = self.comments

        consent_preference = self.consent_preference

        source_evidence = self.source_evidence

        source_file = self.source_file

        privacy_policy = self.privacy_policy

        supporting_information = self.supporting_information

        consent_statement = self.consent_statement

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if solicit_code is not UNSET:
            field_dict["solicit_code"] = solicit_code
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if comments is not UNSET:
            field_dict["comments"] = comments
        if consent_preference is not UNSET:
            field_dict["consent_preference"] = consent_preference
        if source_evidence is not UNSET:
            field_dict["source_evidence"] = source_evidence
        if source_file is not UNSET:
            field_dict["source_file"] = source_file
        if privacy_policy is not UNSET:
            field_dict["privacy_policy"] = privacy_policy
        if supporting_information is not UNSET:
            field_dict["supporting_information"] = supporting_information
        if consent_statement is not UNSET:
            field_dict["consent_statement"] = consent_statement

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        solicit_code = d.pop("solicit_code", UNSET)

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

        consent_preference = d.pop("consent_preference", UNSET)

        source_evidence = d.pop("source_evidence", UNSET)

        source_file = d.pop("source_file", UNSET)

        privacy_policy = d.pop("privacy_policy", UNSET)

        supporting_information = d.pop("supporting_information", UNSET)

        consent_statement = d.pop("consent_statement", UNSET)

        edit_constituent_solicit_code = cls(
            solicit_code=solicit_code,
            start_date=start_date,
            end_date=end_date,
            comments=comments,
            consent_preference=consent_preference,
            source_evidence=source_evidence,
            source_file=source_file,
            privacy_policy=privacy_policy,
            supporting_information=supporting_information,
            consent_statement=consent_statement,
        )

        return edit_constituent_solicit_code
