from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuzzy_date import FuzzyDate
    from ..models.new_education_affiliate_dadditional_information import (
        NewEducationAffiliateDadditionalInformation,
    )
    from ..models.new_education_unaffiliated_additional_information import (
        NewEducationUnaffiliatedAdditionalInformation,
    )


T = TypeVar("T", bound="NewEducation")


@_attrs_define
class NewEducation:
    """CreateEducation.

    Example:
        {'constituent_id': '', 'primary_record': False, 'educational_institution_id': '', 'academic_catalog_program':
            '', 'educational_program': '', 'constituency_status': 'Unknown', 'date_graduated': '', 'date_left': '',
            'educational_history_level': '', 'educational_history_reason': '', 'academic_catalog_degree': '',
            'educational_degree': '', 'educational_award': '', 'start_date': '', 'class_year': 0, 'preferred_class_year': 0,
            'educational_source': '', 'educational_source_date': '', 'comment': '', 'affiliate_dadditional_information':
            [{'id': '', 'academiccatalogcollege': '', 'academiccatalogdivision': '', 'academiccatalogdepartment': '',
            'academiccatalogsubdepartment': '', 'academiccatalogdegreetype': ''}], 'unaffiliated_additional_information':
            [{'id': '', 'educational_college': '', 'educational_division': '', 'educational_department': '',
            'educational_sub_department': '', 'educational_degree_type': ''}], 'affiliated': False, 'use_academic_catalog':
            False, 'educational_history_status': ''}

    Attributes:
        constituent_id (str): The constituent ID.
        educational_institution_id (str): The educational institution.
        educational_history_status (str): The status. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/086c5bfb-1a80-46cf-a2f5-05ef51120891.
        primary_record (Union[Unset, bool]): Indicates whether primary education information.
        academic_catalog_program (Union[Unset, str]): The program. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/d411c16b-8bcf-4fc8-a747-
            754e1e89e9bc?parameters=educational_institution_id,{educational_institution_id}.
        educational_program (Union[Unset, str]): The program. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalprogramcode/entries
        constituency_status (Union[Unset, str]): The status. Available values are <i>unknown</i>, <i>currently
            attending</i>, <i>incomplete</i>, <i>graduated</i>
        date_graduated (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        date_left (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        educational_history_level (Union[Unset, str]): The level. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalhistorylevelcode/entries
        educational_history_reason (Union[Unset, str]): The reason. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalhistoryreasoncode/entries
        academic_catalog_degree (Union[Unset, str]): The degree. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/73c67942-07ad-412e-8596-
            a042e5e68002?parameters=academiccatalogprogramid,{academiccatalogprogramid}.
        educational_degree (Union[Unset, str]): The degree. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationaldegreecode/entries
        educational_award (Union[Unset, str]): The honor awarded. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalawardcode/entries
        start_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        class_year (Union[Unset, int]): The class of.
        preferred_class_year (Union[Unset, int]): The preferred class of.
        educational_source (Union[Unset, str]): The information source. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/educationalsourcecode/entries
        educational_source_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        comment (Union[Unset, str]): The comments.
        affiliate_dadditional_information (Union[Unset, List['NewEducationAffiliateDadditionalInformation']]): Affiliate
            dadditional information.
        unaffiliated_additional_information (Union[Unset, List['NewEducationUnaffiliatedAdditionalInformation']]):
            Unaffiliated additional information.
        affiliated (Union[Unset, bool]): Indicates whether affiliated.
        use_academic_catalog (Union[Unset, bool]): Indicates whether use academic catalog. Read-only in the SOAP API.
    """

    constituent_id: str
    educational_institution_id: str
    educational_history_status: str
    primary_record: Union[Unset, bool] = UNSET
    academic_catalog_program: Union[Unset, str] = UNSET
    educational_program: Union[Unset, str] = UNSET
    constituency_status: Union[Unset, str] = UNSET
    date_graduated: Union[Unset, "FuzzyDate"] = UNSET
    date_left: Union[Unset, "FuzzyDate"] = UNSET
    educational_history_level: Union[Unset, str] = UNSET
    educational_history_reason: Union[Unset, str] = UNSET
    academic_catalog_degree: Union[Unset, str] = UNSET
    educational_degree: Union[Unset, str] = UNSET
    educational_award: Union[Unset, str] = UNSET
    start_date: Union[Unset, "FuzzyDate"] = UNSET
    class_year: Union[Unset, int] = UNSET
    preferred_class_year: Union[Unset, int] = UNSET
    educational_source: Union[Unset, str] = UNSET
    educational_source_date: Union[Unset, "FuzzyDate"] = UNSET
    comment: Union[Unset, str] = UNSET
    affiliate_dadditional_information: Union[Unset, List["NewEducationAffiliateDadditionalInformation"]] = UNSET
    unaffiliated_additional_information: Union[Unset, List["NewEducationUnaffiliatedAdditionalInformation"]] = UNSET
    affiliated: Union[Unset, bool] = UNSET
    use_academic_catalog: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        educational_institution_id = self.educational_institution_id

        educational_history_status = self.educational_history_status

        primary_record = self.primary_record

        academic_catalog_program = self.academic_catalog_program

        educational_program = self.educational_program

        constituency_status = self.constituency_status

        date_graduated: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.date_graduated, Unset):
            date_graduated = self.date_graduated.to_dict()

        date_left: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.date_left, Unset):
            date_left = self.date_left.to_dict()

        educational_history_level = self.educational_history_level

        educational_history_reason = self.educational_history_reason

        academic_catalog_degree = self.academic_catalog_degree

        educational_degree = self.educational_degree

        educational_award = self.educational_award

        start_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.to_dict()

        class_year = self.class_year

        preferred_class_year = self.preferred_class_year

        educational_source = self.educational_source

        educational_source_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.educational_source_date, Unset):
            educational_source_date = self.educational_source_date.to_dict()

        comment = self.comment

        affiliate_dadditional_information: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.affiliate_dadditional_information, Unset):
            affiliate_dadditional_information = []
            for affiliate_dadditional_information_item_data in self.affiliate_dadditional_information:
                affiliate_dadditional_information_item = affiliate_dadditional_information_item_data.to_dict()
                affiliate_dadditional_information.append(affiliate_dadditional_information_item)

        unaffiliated_additional_information: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.unaffiliated_additional_information, Unset):
            unaffiliated_additional_information = []
            for unaffiliated_additional_information_item_data in self.unaffiliated_additional_information:
                unaffiliated_additional_information_item = unaffiliated_additional_information_item_data.to_dict()
                unaffiliated_additional_information.append(unaffiliated_additional_information_item)

        affiliated = self.affiliated

        use_academic_catalog = self.use_academic_catalog

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "constituent_id": constituent_id,
                "educational_institution_id": educational_institution_id,
                "educational_history_status": educational_history_status,
            }
        )
        if primary_record is not UNSET:
            field_dict["primary_record"] = primary_record
        if academic_catalog_program is not UNSET:
            field_dict["academic_catalog_program"] = academic_catalog_program
        if educational_program is not UNSET:
            field_dict["educational_program"] = educational_program
        if constituency_status is not UNSET:
            field_dict["constituency_status"] = constituency_status
        if date_graduated is not UNSET:
            field_dict["date_graduated"] = date_graduated
        if date_left is not UNSET:
            field_dict["date_left"] = date_left
        if educational_history_level is not UNSET:
            field_dict["educational_history_level"] = educational_history_level
        if educational_history_reason is not UNSET:
            field_dict["educational_history_reason"] = educational_history_reason
        if academic_catalog_degree is not UNSET:
            field_dict["academic_catalog_degree"] = academic_catalog_degree
        if educational_degree is not UNSET:
            field_dict["educational_degree"] = educational_degree
        if educational_award is not UNSET:
            field_dict["educational_award"] = educational_award
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if class_year is not UNSET:
            field_dict["class_year"] = class_year
        if preferred_class_year is not UNSET:
            field_dict["preferred_class_year"] = preferred_class_year
        if educational_source is not UNSET:
            field_dict["educational_source"] = educational_source
        if educational_source_date is not UNSET:
            field_dict["educational_source_date"] = educational_source_date
        if comment is not UNSET:
            field_dict["comment"] = comment
        if affiliate_dadditional_information is not UNSET:
            field_dict["affiliate_dadditional_information"] = affiliate_dadditional_information
        if unaffiliated_additional_information is not UNSET:
            field_dict["unaffiliated_additional_information"] = unaffiliated_additional_information
        if affiliated is not UNSET:
            field_dict["affiliated"] = affiliated
        if use_academic_catalog is not UNSET:
            field_dict["use_academic_catalog"] = use_academic_catalog

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fuzzy_date import FuzzyDate
        from ..models.new_education_affiliate_dadditional_information import (
            NewEducationAffiliateDadditionalInformation,
        )
        from ..models.new_education_unaffiliated_additional_information import (
            NewEducationUnaffiliatedAdditionalInformation,
        )

        d = src_dict.copy()
        constituent_id = d.pop("constituent_id")

        educational_institution_id = d.pop("educational_institution_id")

        educational_history_status = d.pop("educational_history_status")

        primary_record = d.pop("primary_record", UNSET)

        academic_catalog_program = d.pop("academic_catalog_program", UNSET)

        educational_program = d.pop("educational_program", UNSET)

        constituency_status = d.pop("constituency_status", UNSET)

        _date_graduated = d.pop("date_graduated", UNSET)
        date_graduated: Union[Unset, FuzzyDate]
        if isinstance(_date_graduated, Unset):
            date_graduated = UNSET
        else:
            date_graduated = FuzzyDate.from_dict(_date_graduated)

        _date_left = d.pop("date_left", UNSET)
        date_left: Union[Unset, FuzzyDate]
        if isinstance(_date_left, Unset):
            date_left = UNSET
        else:
            date_left = FuzzyDate.from_dict(_date_left)

        educational_history_level = d.pop("educational_history_level", UNSET)

        educational_history_reason = d.pop("educational_history_reason", UNSET)

        academic_catalog_degree = d.pop("academic_catalog_degree", UNSET)

        educational_degree = d.pop("educational_degree", UNSET)

        educational_award = d.pop("educational_award", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, FuzzyDate]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = FuzzyDate.from_dict(_start_date)

        class_year = d.pop("class_year", UNSET)

        preferred_class_year = d.pop("preferred_class_year", UNSET)

        educational_source = d.pop("educational_source", UNSET)

        _educational_source_date = d.pop("educational_source_date", UNSET)
        educational_source_date: Union[Unset, FuzzyDate]
        if isinstance(_educational_source_date, Unset):
            educational_source_date = UNSET
        else:
            educational_source_date = FuzzyDate.from_dict(_educational_source_date)

        comment = d.pop("comment", UNSET)

        affiliate_dadditional_information = []
        _affiliate_dadditional_information = d.pop("affiliate_dadditional_information", UNSET)
        for affiliate_dadditional_information_item_data in _affiliate_dadditional_information or []:
            affiliate_dadditional_information_item = NewEducationAffiliateDadditionalInformation.from_dict(
                affiliate_dadditional_information_item_data
            )

            affiliate_dadditional_information.append(affiliate_dadditional_information_item)

        unaffiliated_additional_information = []
        _unaffiliated_additional_information = d.pop("unaffiliated_additional_information", UNSET)
        for unaffiliated_additional_information_item_data in _unaffiliated_additional_information or []:
            unaffiliated_additional_information_item = NewEducationUnaffiliatedAdditionalInformation.from_dict(
                unaffiliated_additional_information_item_data
            )

            unaffiliated_additional_information.append(unaffiliated_additional_information_item)

        affiliated = d.pop("affiliated", UNSET)

        use_academic_catalog = d.pop("use_academic_catalog", UNSET)

        new_education = cls(
            constituent_id=constituent_id,
            educational_institution_id=educational_institution_id,
            educational_history_status=educational_history_status,
            primary_record=primary_record,
            academic_catalog_program=academic_catalog_program,
            educational_program=educational_program,
            constituency_status=constituency_status,
            date_graduated=date_graduated,
            date_left=date_left,
            educational_history_level=educational_history_level,
            educational_history_reason=educational_history_reason,
            academic_catalog_degree=academic_catalog_degree,
            educational_degree=educational_degree,
            educational_award=educational_award,
            start_date=start_date,
            class_year=class_year,
            preferred_class_year=preferred_class_year,
            educational_source=educational_source,
            educational_source_date=educational_source_date,
            comment=comment,
            affiliate_dadditional_information=affiliate_dadditional_information,
            unaffiliated_additional_information=unaffiliated_additional_information,
            affiliated=affiliated,
            use_academic_catalog=use_academic_catalog,
        )

        return new_education
