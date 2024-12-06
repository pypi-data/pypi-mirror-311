import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_constituent_email_address_matching_household_members import (
        EditConstituentEmailAddressMatchingHouseholdMembers,
    )


T = TypeVar("T", bound="EditConstituentEmailAddress")


@_attrs_define
class EditConstituentEmailAddress:
    """EditConstituentEmailAddress.

    Example:
        {'email_address_type': 'Email', 'email_address': 'jules@att.com', 'primary': False, 'do_not_email': False,
            'spouse_name': '', 'spouse_has_matching_email_address': False, 'update_matching_spouse_email_address': False,
            'household': False, 'household_member': False, 'update_matching_household_email_address': False,
            'matching_household_members': [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}],
            'info_source': '', 'info_source_comments': '', 'constituent_data_review_rollback_reason': '', 'forced_primary':
            False, 'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User', 'start_date':
            '2016-02-18T12:00:00.0000000+00:00', 'end_date': '2017-06-12T12:00:00.0000000+00:00', 'invalid_email': False,
            'email_bounced_date': '2018-01-03T12:00:00.0000000+00:00'}

    Attributes:
        email_address_type (Union[Unset, str]): The type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/emailaddresstypecode/entries
        email_address (Union[Unset, str]): The email address.
        primary (Union[Unset, bool]): Indicates whether set as primary email address.
        do_not_email (Union[Unset, bool]): Indicates whether do not send email to this address.
        spouse_name (Union[Unset, str]): The spouse name. Read-only in the SOAP API.
        spouse_has_matching_email_address (Union[Unset, bool]): Indicates whether spouse has matching email address.
            Read-only in the SOAP API.
        update_matching_spouse_email_address (Union[Unset, bool]): Indicates whether update matching email information
            for spouse.
        household (Union[Unset, bool]): Indicates whether household. Read-only in the SOAP API.
        household_member (Union[Unset, bool]): Indicates whether household member. Read-only in the SOAP API.
        update_matching_household_email_address (Union[Unset, bool]): Indicates whether update matching email addresses
            in household.
        matching_household_members (Union[Unset, List['EditConstituentEmailAddressMatchingHouseholdMembers']]): Matching
            household members.
        info_source (Union[Unset, str]): The information source. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/infosourcecode/entries
        info_source_comments (Union[Unset, str]): The comments.
        constituent_data_review_rollback_reason (Union[Unset, str]): The reason. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/484441bc-f0e6-4f5f-a6bf-49f02881dd13.
        forced_primary (Union[Unset, bool]): Indicates whether forced primary. Read-only in the SOAP API.
        can_edit_primary (Union[Unset, bool]): Indicates whether can edit primary. Read-only in the SOAP API.
        invalid_fields (Union[Unset, str]): The invalid fields. Read-only in the SOAP API.
        origin (Union[Unset, str]): The origin. Read-only in the SOAP API. Available values are <i>user</i>, <i>web
            forms</i>
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        invalid_email (Union[Unset, bool]): Indicates whether invalid email. Read-only in the SOAP API.
        email_bounced_date (Union[Unset, datetime.datetime]): The email bounced date. Read-only in the SOAP API. Uses
            the format YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        emailisconfidential (Union[Unset, bool]): Indicates whether this email is confidential.
        donotemailreason (Union[Unset, str]): The reason. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/donotemailreasoncode/entries
    """

    email_address_type: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    do_not_email: Union[Unset, bool] = UNSET
    spouse_name: Union[Unset, str] = UNSET
    spouse_has_matching_email_address: Union[Unset, bool] = UNSET
    update_matching_spouse_email_address: Union[Unset, bool] = UNSET
    household: Union[Unset, bool] = UNSET
    household_member: Union[Unset, bool] = UNSET
    update_matching_household_email_address: Union[Unset, bool] = UNSET
    matching_household_members: Union[Unset, List["EditConstituentEmailAddressMatchingHouseholdMembers"]] = UNSET
    info_source: Union[Unset, str] = UNSET
    info_source_comments: Union[Unset, str] = UNSET
    constituent_data_review_rollback_reason: Union[Unset, str] = UNSET
    forced_primary: Union[Unset, bool] = UNSET
    can_edit_primary: Union[Unset, bool] = UNSET
    invalid_fields: Union[Unset, str] = UNSET
    origin: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    invalid_email: Union[Unset, bool] = UNSET
    email_bounced_date: Union[Unset, datetime.datetime] = UNSET
    emailisconfidential: Union[Unset, bool] = UNSET
    donotemailreason: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        email_address_type = self.email_address_type

        email_address = self.email_address

        primary = self.primary

        do_not_email = self.do_not_email

        spouse_name = self.spouse_name

        spouse_has_matching_email_address = self.spouse_has_matching_email_address

        update_matching_spouse_email_address = self.update_matching_spouse_email_address

        household = self.household

        household_member = self.household_member

        update_matching_household_email_address = self.update_matching_household_email_address

        matching_household_members: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.matching_household_members, Unset):
            matching_household_members = []
            for matching_household_members_item_data in self.matching_household_members:
                matching_household_members_item = matching_household_members_item_data.to_dict()
                matching_household_members.append(matching_household_members_item)

        info_source = self.info_source

        info_source_comments = self.info_source_comments

        constituent_data_review_rollback_reason = self.constituent_data_review_rollback_reason

        forced_primary = self.forced_primary

        can_edit_primary = self.can_edit_primary

        invalid_fields = self.invalid_fields

        origin = self.origin

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        invalid_email = self.invalid_email

        email_bounced_date: Union[Unset, str] = UNSET
        if not isinstance(self.email_bounced_date, Unset):
            email_bounced_date = self.email_bounced_date.isoformat()

        emailisconfidential = self.emailisconfidential

        donotemailreason = self.donotemailreason

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if email_address_type is not UNSET:
            field_dict["email_address_type"] = email_address_type
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if primary is not UNSET:
            field_dict["primary"] = primary
        if do_not_email is not UNSET:
            field_dict["do_not_email"] = do_not_email
        if spouse_name is not UNSET:
            field_dict["spouse_name"] = spouse_name
        if spouse_has_matching_email_address is not UNSET:
            field_dict["spouse_has_matching_email_address"] = spouse_has_matching_email_address
        if update_matching_spouse_email_address is not UNSET:
            field_dict["update_matching_spouse_email_address"] = update_matching_spouse_email_address
        if household is not UNSET:
            field_dict["household"] = household
        if household_member is not UNSET:
            field_dict["household_member"] = household_member
        if update_matching_household_email_address is not UNSET:
            field_dict["update_matching_household_email_address"] = update_matching_household_email_address
        if matching_household_members is not UNSET:
            field_dict["matching_household_members"] = matching_household_members
        if info_source is not UNSET:
            field_dict["info_source"] = info_source
        if info_source_comments is not UNSET:
            field_dict["info_source_comments"] = info_source_comments
        if constituent_data_review_rollback_reason is not UNSET:
            field_dict["constituent_data_review_rollback_reason"] = constituent_data_review_rollback_reason
        if forced_primary is not UNSET:
            field_dict["forced_primary"] = forced_primary
        if can_edit_primary is not UNSET:
            field_dict["can_edit_primary"] = can_edit_primary
        if invalid_fields is not UNSET:
            field_dict["invalid_fields"] = invalid_fields
        if origin is not UNSET:
            field_dict["origin"] = origin
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if invalid_email is not UNSET:
            field_dict["invalid_email"] = invalid_email
        if email_bounced_date is not UNSET:
            field_dict["email_bounced_date"] = email_bounced_date
        if emailisconfidential is not UNSET:
            field_dict["emailisconfidential"] = emailisconfidential
        if donotemailreason is not UNSET:
            field_dict["donotemailreason"] = donotemailreason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_constituent_email_address_matching_household_members import (
            EditConstituentEmailAddressMatchingHouseholdMembers,
        )

        d = src_dict.copy()
        email_address_type = d.pop("email_address_type", UNSET)

        email_address = d.pop("email_address", UNSET)

        primary = d.pop("primary", UNSET)

        do_not_email = d.pop("do_not_email", UNSET)

        spouse_name = d.pop("spouse_name", UNSET)

        spouse_has_matching_email_address = d.pop("spouse_has_matching_email_address", UNSET)

        update_matching_spouse_email_address = d.pop("update_matching_spouse_email_address", UNSET)

        household = d.pop("household", UNSET)

        household_member = d.pop("household_member", UNSET)

        update_matching_household_email_address = d.pop("update_matching_household_email_address", UNSET)

        matching_household_members = []
        _matching_household_members = d.pop("matching_household_members", UNSET)
        for matching_household_members_item_data in _matching_household_members or []:
            matching_household_members_item = EditConstituentEmailAddressMatchingHouseholdMembers.from_dict(
                matching_household_members_item_data
            )

            matching_household_members.append(matching_household_members_item)

        info_source = d.pop("info_source", UNSET)

        info_source_comments = d.pop("info_source_comments", UNSET)

        constituent_data_review_rollback_reason = d.pop("constituent_data_review_rollback_reason", UNSET)

        forced_primary = d.pop("forced_primary", UNSET)

        can_edit_primary = d.pop("can_edit_primary", UNSET)

        invalid_fields = d.pop("invalid_fields", UNSET)

        origin = d.pop("origin", UNSET)

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

        invalid_email = d.pop("invalid_email", UNSET)

        _email_bounced_date = d.pop("email_bounced_date", UNSET)
        email_bounced_date: Union[Unset, datetime.datetime]
        if isinstance(_email_bounced_date, Unset):
            email_bounced_date = UNSET
        else:
            email_bounced_date = isoparse(_email_bounced_date)

        emailisconfidential = d.pop("emailisconfidential", UNSET)

        donotemailreason = d.pop("donotemailreason", UNSET)

        edit_constituent_email_address = cls(
            email_address_type=email_address_type,
            email_address=email_address,
            primary=primary,
            do_not_email=do_not_email,
            spouse_name=spouse_name,
            spouse_has_matching_email_address=spouse_has_matching_email_address,
            update_matching_spouse_email_address=update_matching_spouse_email_address,
            household=household,
            household_member=household_member,
            update_matching_household_email_address=update_matching_household_email_address,
            matching_household_members=matching_household_members,
            info_source=info_source,
            info_source_comments=info_source_comments,
            constituent_data_review_rollback_reason=constituent_data_review_rollback_reason,
            forced_primary=forced_primary,
            can_edit_primary=can_edit_primary,
            invalid_fields=invalid_fields,
            origin=origin,
            start_date=start_date,
            end_date=end_date,
            invalid_email=invalid_email,
            email_bounced_date=email_bounced_date,
            emailisconfidential=emailisconfidential,
            donotemailreason=donotemailreason,
        )

        return edit_constituent_email_address
