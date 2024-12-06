import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constituent_phone_country_codes import ConstituentPhoneCountryCodes
    from ..models.constituent_phone_matching_household_members import ConstituentPhoneMatchingHouseholdMembers
    from ..models.hour_minute import HourMinute
    from ..models.month_day import MonthDay


T = TypeVar("T", bound="ConstituentPhone")


@_attrs_define
class ConstituentPhone:
    """GetConstituentPhone.

    Attributes:
        number (str): The number.
        phone_type (Union[Unset, str]): The type. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/phonetypecode/entries
        primary (Union[Unset, bool]): Indicates whether set as primary phone number.
        do_not_call (Union[Unset, bool]): Indicates whether do not call this phone number.
        spouse_name (Union[Unset, str]): The spouse name. Read-only in the SOAP API.
        spouse_has_matching_phone (Union[Unset, bool]): Indicates whether spouse has matching phone. Read-only in the
            SOAP API.
        update_matching_spouse_phone (Union[Unset, bool]): Indicates whether update matching phone information for
            household.
        household (Union[Unset, bool]): Indicates whether household. Read-only in the SOAP API.
        household_member (Union[Unset, bool]): Indicates whether household member. Read-only in the SOAP API.
        update_matching_household_phone (Union[Unset, bool]): Indicates whether update matching phone numbers in
            household.
        matching_household_members (Union[Unset, List['ConstituentPhoneMatchingHouseholdMembers']]): Matching household
            members.
        start_time (Union[Unset, HourMinute]): HourMinute
        end_time (Union[Unset, HourMinute]): HourMinute
        info_source (Union[Unset, str]): The information source. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/infosourcecode/entries
        info_source_comments (Union[Unset, str]): The comments.
        country (Union[Unset, str]): The country. This simple list can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/c9649672-353d-42e8-8c25-4d34bbabfbba.
        seasonal_start_date (Union[Unset, MonthDay]): MonthDay Example: {'month': 4, 'day': 13}.
        seasonal_end_date (Union[Unset, MonthDay]): MonthDay Example: {'month': 4, 'day': 13}.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        do_not_call_reason (Union[Unset, str]): The reason. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/donotcallreasoncode/entries
        confidential (Union[Unset, bool]): Indicates whether this phone number is confidential.
        country_codes (Union[Unset, List['ConstituentPhoneCountryCodes']]): Country codes.
        constituent_data_review_rollback_reason (Union[Unset, str]): The reason. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/484441bc-f0e6-4f5f-a6bf-49f02881dd13.
        forced_primary (Union[Unset, bool]): Indicates whether forced primary. Read-only in the SOAP API.
        can_edit_primary (Union[Unset, bool]): Indicates whether can edit primary. Read-only in the SOAP API.
        invalid_fields (Union[Unset, str]): The invalid fields. Read-only in the SOAP API.
        origin (Union[Unset, str]): The origin. Read-only in the SOAP API. Available values are <i>user</i>, <i>web
            forms</i>
        donottext (Union[Unset, bool]): Indicates whether do not text message this phone number.
    """

    number: str
    phone_type: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    do_not_call: Union[Unset, bool] = UNSET
    spouse_name: Union[Unset, str] = UNSET
    spouse_has_matching_phone: Union[Unset, bool] = UNSET
    update_matching_spouse_phone: Union[Unset, bool] = UNSET
    household: Union[Unset, bool] = UNSET
    household_member: Union[Unset, bool] = UNSET
    update_matching_household_phone: Union[Unset, bool] = UNSET
    matching_household_members: Union[Unset, List["ConstituentPhoneMatchingHouseholdMembers"]] = UNSET
    start_time: Union[Unset, "HourMinute"] = UNSET
    end_time: Union[Unset, "HourMinute"] = UNSET
    info_source: Union[Unset, str] = UNSET
    info_source_comments: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    seasonal_start_date: Union[Unset, "MonthDay"] = UNSET
    seasonal_end_date: Union[Unset, "MonthDay"] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    do_not_call_reason: Union[Unset, str] = UNSET
    confidential: Union[Unset, bool] = UNSET
    country_codes: Union[Unset, List["ConstituentPhoneCountryCodes"]] = UNSET
    constituent_data_review_rollback_reason: Union[Unset, str] = UNSET
    forced_primary: Union[Unset, bool] = UNSET
    can_edit_primary: Union[Unset, bool] = UNSET
    invalid_fields: Union[Unset, str] = UNSET
    origin: Union[Unset, str] = UNSET
    donottext: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        number = self.number

        phone_type = self.phone_type

        primary = self.primary

        do_not_call = self.do_not_call

        spouse_name = self.spouse_name

        spouse_has_matching_phone = self.spouse_has_matching_phone

        update_matching_spouse_phone = self.update_matching_spouse_phone

        household = self.household

        household_member = self.household_member

        update_matching_household_phone = self.update_matching_household_phone

        matching_household_members: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.matching_household_members, Unset):
            matching_household_members = []
            for matching_household_members_item_data in self.matching_household_members:
                matching_household_members_item = matching_household_members_item_data.to_dict()
                matching_household_members.append(matching_household_members_item)

        start_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.to_dict()

        end_time: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.to_dict()

        info_source = self.info_source

        info_source_comments = self.info_source_comments

        country = self.country

        seasonal_start_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.seasonal_start_date, Unset):
            seasonal_start_date = self.seasonal_start_date.to_dict()

        seasonal_end_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.seasonal_end_date, Unset):
            seasonal_end_date = self.seasonal_end_date.to_dict()

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        do_not_call_reason = self.do_not_call_reason

        confidential = self.confidential

        country_codes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.country_codes, Unset):
            country_codes = []
            for country_codes_item_data in self.country_codes:
                country_codes_item = country_codes_item_data.to_dict()
                country_codes.append(country_codes_item)

        constituent_data_review_rollback_reason = self.constituent_data_review_rollback_reason

        forced_primary = self.forced_primary

        can_edit_primary = self.can_edit_primary

        invalid_fields = self.invalid_fields

        origin = self.origin

        donottext = self.donottext

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "number": number,
            }
        )
        if phone_type is not UNSET:
            field_dict["phone_type"] = phone_type
        if primary is not UNSET:
            field_dict["primary"] = primary
        if do_not_call is not UNSET:
            field_dict["do_not_call"] = do_not_call
        if spouse_name is not UNSET:
            field_dict["spouse_name"] = spouse_name
        if spouse_has_matching_phone is not UNSET:
            field_dict["spouse_has_matching_phone"] = spouse_has_matching_phone
        if update_matching_spouse_phone is not UNSET:
            field_dict["update_matching_spouse_phone"] = update_matching_spouse_phone
        if household is not UNSET:
            field_dict["household"] = household
        if household_member is not UNSET:
            field_dict["household_member"] = household_member
        if update_matching_household_phone is not UNSET:
            field_dict["update_matching_household_phone"] = update_matching_household_phone
        if matching_household_members is not UNSET:
            field_dict["matching_household_members"] = matching_household_members
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if info_source is not UNSET:
            field_dict["info_source"] = info_source
        if info_source_comments is not UNSET:
            field_dict["info_source_comments"] = info_source_comments
        if country is not UNSET:
            field_dict["country"] = country
        if seasonal_start_date is not UNSET:
            field_dict["seasonal_start_date"] = seasonal_start_date
        if seasonal_end_date is not UNSET:
            field_dict["seasonal_end_date"] = seasonal_end_date
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if do_not_call_reason is not UNSET:
            field_dict["do_not_call_reason"] = do_not_call_reason
        if confidential is not UNSET:
            field_dict["confidential"] = confidential
        if country_codes is not UNSET:
            field_dict["country_codes"] = country_codes
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
        if donottext is not UNSET:
            field_dict["donottext"] = donottext

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constituent_phone_country_codes import ConstituentPhoneCountryCodes
        from ..models.constituent_phone_matching_household_members import (
            ConstituentPhoneMatchingHouseholdMembers,
        )
        from ..models.hour_minute import HourMinute
        from ..models.month_day import MonthDay

        d = src_dict.copy()
        number = d.pop("number")

        phone_type = d.pop("phone_type", UNSET)

        primary = d.pop("primary", UNSET)

        do_not_call = d.pop("do_not_call", UNSET)

        spouse_name = d.pop("spouse_name", UNSET)

        spouse_has_matching_phone = d.pop("spouse_has_matching_phone", UNSET)

        update_matching_spouse_phone = d.pop("update_matching_spouse_phone", UNSET)

        household = d.pop("household", UNSET)

        household_member = d.pop("household_member", UNSET)

        update_matching_household_phone = d.pop("update_matching_household_phone", UNSET)

        matching_household_members = []
        _matching_household_members = d.pop("matching_household_members", UNSET)
        for matching_household_members_item_data in _matching_household_members or []:
            matching_household_members_item = ConstituentPhoneMatchingHouseholdMembers.from_dict(
                matching_household_members_item_data
            )

            matching_household_members.append(matching_household_members_item)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, HourMinute]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = HourMinute.from_dict(_start_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, HourMinute]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = HourMinute.from_dict(_end_time)

        info_source = d.pop("info_source", UNSET)

        info_source_comments = d.pop("info_source_comments", UNSET)

        country = d.pop("country", UNSET)

        _seasonal_start_date = d.pop("seasonal_start_date", UNSET)
        seasonal_start_date: Union[Unset, MonthDay]
        if isinstance(_seasonal_start_date, Unset):
            seasonal_start_date = UNSET
        else:
            seasonal_start_date = MonthDay.from_dict(_seasonal_start_date)

        _seasonal_end_date = d.pop("seasonal_end_date", UNSET)
        seasonal_end_date: Union[Unset, MonthDay]
        if isinstance(_seasonal_end_date, Unset):
            seasonal_end_date = UNSET
        else:
            seasonal_end_date = MonthDay.from_dict(_seasonal_end_date)

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

        do_not_call_reason = d.pop("do_not_call_reason", UNSET)

        confidential = d.pop("confidential", UNSET)

        country_codes = []
        _country_codes = d.pop("country_codes", UNSET)
        for country_codes_item_data in _country_codes or []:
            country_codes_item = ConstituentPhoneCountryCodes.from_dict(country_codes_item_data)

            country_codes.append(country_codes_item)

        constituent_data_review_rollback_reason = d.pop("constituent_data_review_rollback_reason", UNSET)

        forced_primary = d.pop("forced_primary", UNSET)

        can_edit_primary = d.pop("can_edit_primary", UNSET)

        invalid_fields = d.pop("invalid_fields", UNSET)

        origin = d.pop("origin", UNSET)

        donottext = d.pop("donottext", UNSET)

        constituent_phone = cls(
            number=number,
            phone_type=phone_type,
            primary=primary,
            do_not_call=do_not_call,
            spouse_name=spouse_name,
            spouse_has_matching_phone=spouse_has_matching_phone,
            update_matching_spouse_phone=update_matching_spouse_phone,
            household=household,
            household_member=household_member,
            update_matching_household_phone=update_matching_household_phone,
            matching_household_members=matching_household_members,
            start_time=start_time,
            end_time=end_time,
            info_source=info_source,
            info_source_comments=info_source_comments,
            country=country,
            seasonal_start_date=seasonal_start_date,
            seasonal_end_date=seasonal_end_date,
            start_date=start_date,
            end_date=end_date,
            do_not_call_reason=do_not_call_reason,
            confidential=confidential,
            country_codes=country_codes,
            constituent_data_review_rollback_reason=constituent_data_review_rollback_reason,
            forced_primary=forced_primary,
            can_edit_primary=can_edit_primary,
            invalid_fields=invalid_fields,
            origin=origin,
            donottext=donottext,
        )

        return constituent_phone
