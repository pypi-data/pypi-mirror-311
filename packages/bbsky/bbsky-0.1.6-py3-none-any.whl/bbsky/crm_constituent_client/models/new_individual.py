import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuzzy_date import FuzzyDate
    from ..models.new_individual_validation_countries import NewIndividualValidationCountries
    from ..models.new_individual_zip_lookup_countries import NewIndividualZipLookupCountries

T = TypeVar("T", bound="NewIndividual")


@_attrs_define
class NewIndividual:
    """CreateIndividual.

    Example:
        {'last_name': '', 'first_name': '', 'middle_name': '', 'title': '', 'suffix': '', 'nickname': '', 'maiden_name':
            '', 'birth_date': '', 'gender': 'Unknown', 'marital_status': '', 'address_type': '', 'address_country': '',
            'address_block': '', 'address_city': '', 'address_state': '', 'address_post_code': '', 'address_do_not_mail':
            False, 'address_do_not_mail_reason': '', 'phone_type': '', 'phone_number': '', 'email_address_type': '',
            'email_address': '', 'skip_adding_security_groups': False, 'existing_spouse': False, 'spouse_id': '',
            'spouse_last_name': '', 'spouse_first_name': '', 'spouse_middle_name': '', 'spouse_title': '', 'spouse_suffix':
            '', 'spouse_nick_name': '', 'spouse_maiden_name': '', 'spouse_birth_date': '', 'spouse_gender': 'Unknown',
            'spouse_relationship_type_code': '', 'spouse_reciprocal_type_code': '', 'spouse_start_date': '',
            'copy_primary_information': False, 'primary_soft_credit_relationship_exists': False,
            'primary_soft_credit_match_factor': 0, 'reciprocal_soft_credit_relationship_exists': False,
            'reciprocal_soft_credit_match_factor': 0, 'existing_organization': False, 'organization_id': '',
            'organization_name': '', 'organization_address_type': '', 'organization_country': '',
            'organization_address_block': '', 'organization_city': '', 'organization_state': '', 'organization_post_code':
            '', 'organization_do_not_mail': False, 'organization_do_not_mail_reason': '', 'organization_phone_type': '',
            'organization_number': '', 'organization_relationship_type_code': '', 'organization_reciprocal_type_code': '',
            'organization_start_date': '', 'organization_end_date': '', 'contact': False, 'contact_type': '',
            'primary_contact': False, 'position': '', 'matching_gift_relationship': False, 'reciprocal_recognition_type':
            '', 'primary_recognition_type': '', 'address_omit_from_validation': False, 'address_dpc': '', 'address_cart':
            '', 'address_lot': '', 'address_county': '', 'address_congressional_district': '',
            'address_last_validation_attempt_date': '', 'address_validation_message': '', 'address_certification_data': 0,
            'organization_omit_from_validation': False, 'organization_dpc': '', 'organization_cart': '', 'organization_lot':
            '', 'organization_county': '', 'organization_congressional_district': '',
            'organization_last_validation_attempt_date': '', 'organization_validation_message': '',
            'organization_certification_data': 0, 'validation_countries': [{'country_id': '', 'browsable': False}],
            'zip_lookup_countries': [{'country_id': '', 'country_name': ''}], 'spouse_relationship': False,
            'house_hold_copy_primary_contact_info': False, 'job_category': '', 'career_level': '', 'address_info_source':
            '', 'organization_info_source': '', 'title_2': '', 'suffix_2': '', 'spouse_title_2': '', 'spouse_suffix_2': '',
            'skip_adding_sites': False, 'constituent_type': 0, 'organization_primary_soft_credit_relationship_exists':
            False, 'organization_primary_soft_credit_match_factor': 0,
            'organization_reciprocal_soft_credit_relationship_exists': False,
            'organization_reciprocal_soft_credit_match_factor': 0, 'organization_primary_recognition_type': '',
            'organization_reciprocal_recognition_type': '', 'gender_code': '', 'spouse_gender_code': ''}

    Attributes:
        last_name (str): The the constituent's last name. character limit: 100..
        gender (str): The the constituent's gender.. Available values are <i>unknown</i>, <i>male</i>, <i>female</i>,
            <i>other</i>
        first_name (Union[Unset, str]): The the constituent's first name. character limit: 50..
        middle_name (Union[Unset, str]): The the constituent's middle name. character limit: 50..
        title (Union[Unset, str]): The the constituent's primary title. for individuals only.. This code table can be
            queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/titlecode/entries
        suffix (Union[Unset, str]): The the constituent's suffix.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/suffixcode/entries
        nickname (Union[Unset, str]): The the constituent's nickname. character limit: 50..
        maiden_name (Union[Unset, str]): The the constituent's maiden name. character limit: 100..
        birth_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        marital_status (Union[Unset, str]): The the constituent's marital status.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/maritalstatuscode/entries
        address_type (Union[Unset, str]): The the address type of the constituent's address.. This code table can be
            queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/addresstypecode/entries
        address_country (Union[Unset, str]): The the country of the constituent's address.. This simple list can be
            queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/c9649672-353d-42e8-8c25-4d34bbabfbba.
        address_block (Union[Unset, str]): The the constituent's address. character limit: 150..
        address_city (Union[Unset, str]): The the city of the constituent's address. character limit: 50..
        address_state (Union[Unset, str]): The the state of the constituent's address.. This simple list can be queried
            at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/7fa91401-596c-4f7c-936d-6e41683121d7?parameters=country_id,{address_countryid}.
        address_post_code (Union[Unset, str]): The the postal code of the constituent's address. character limit: 12..
        address_do_not_mail (Union[Unset, bool]): Indicates whether indicates whether the constituent should not be
            contacted at this address..
        address_do_not_mail_reason (Union[Unset, str]): The indicates the reason the constituent should not be contacted
            at this address.. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/donotmailreasoncode/entries
        phone_type (Union[Unset, str]): The the phone type of the constituent's phone.. This code table can be queried
            at https://api.sky.blackbaud.com/crm-adnmg/codetables/phonetypecode/entries
        phone_number (Union[Unset, str]): The the constituent's phone number..
        email_address_type (Union[Unset, str]): The the email address type of the constituent's email.. This code table
            can be queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/emailaddresstypecode/entries
        email_address (Union[Unset, str]): The the constituent's email address..
        skip_adding_security_groups (Union[Unset, bool]): Indicates whether skip adding security groups.
        existing_spouse (Union[Unset, bool]): Indicates whether search existing individuals.
        spouse_id (Union[Unset, str]): The an individual related to the constituent. this individual will be added to
            the same household as the constituent..
        spouse_last_name (Union[Unset, str]): The the related individual's last name. character limit: 100..
        spouse_first_name (Union[Unset, str]): The the related individual's first name. character limit: 50..
        spouse_middle_name (Union[Unset, str]): The the related individual's middle name. character limit: 50..
        spouse_title (Union[Unset, str]): The the related individual's title. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/titlecode/entries
        spouse_suffix (Union[Unset, str]): The the related individual's suffix. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/suffixcode/entries
        spouse_nick_name (Union[Unset, str]): The the related individual's nickname. character limit: 50..
        spouse_maiden_name (Union[Unset, str]): The the related individual's maiden name. character limit: 100..
        spouse_birth_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        spouse_gender (Union[Unset, str]): The the related individual's gender.. Available values are <i>unknown</i>,
            <i>male</i>, <i>female</i>, <i>other</i>
        spouse_relationship_type_code (Union[Unset, str]): The the type of relationship between the constituent and
            related individual. can be expressed as, "the individual is the constituent's _______".. This simple list can be
            queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/4e869c5a-9b9d-4e84-b6e0-
            1fc66bafbafc?parameters=gender,{gendercode}&parameters=appliestoconstituenttype,{constituent_type}&parameters=re
            latestoconstituenttype,{0}.
        spouse_reciprocal_type_code (Union[Unset, str]): The the type of relationship between the related individual and
            the constituent. can be expressed as, "the constituent is the individual's _______".. This simple list can be
            queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/c3018803-2ea5-4f62-91cf-
            412e88d15f9b?parameters=appliestoconstituenttype,{constituent_type}&parameters=constituentid,{spouse_id}&paramet
            ers=appliestorelationshiptypeid,{spouse_relationshiptypecodeid}&parameters=gender,{spouse_gendercode}&parameters
            =relatestoconstituenttype,{0}.
        spouse_start_date (Union[Unset, datetime.datetime]): The the start date of the relationship.. Uses the format
            YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        copy_primary_information (Union[Unset, bool]): Indicates whether indicates whether to copy the constituent's
            primary information to the related constituent's record..
        primary_soft_credit_relationship_exists (Union[Unset, bool]): Indicates whether soft credit individual for
            constituent's payments.
        primary_soft_credit_match_factor (Union[Unset, float]): The recognition match percent.
        reciprocal_soft_credit_relationship_exists (Union[Unset, bool]): Indicates whether soft credit constituent for
            individual's payments.
        reciprocal_soft_credit_match_factor (Union[Unset, float]): The recognition match percent.
        existing_organization (Union[Unset, bool]): Indicates whether search existing organizations.
        organization_id (Union[Unset, str]): The the related organization's id..
        organization_name (Union[Unset, str]): The the related organization's name. character limit: 100..
        organization_address_type (Union[Unset, str]): The address type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/addresstypecode/entries
        organization_country (Union[Unset, str]): The the country of the related organization's address.. This simple
            list can be queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/c9649672-353d-42e8-8c25-4d34bbabfbba.
        organization_address_block (Union[Unset, str]): The the related organization's address. character limit: 150..
        organization_city (Union[Unset, str]): The the city of the related organization's address. character limit: 50..
        organization_state (Union[Unset, str]): The the state of the related organization's address.. This simple list
            can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/7fa91401-596c-4f7c-936d-6e41683121d7?parameters=country_id,{organization_countryid}.
        organization_post_code (Union[Unset, str]): The the postal code of the related organization's address. character
            limit: 50..
        organization_do_not_mail (Union[Unset, bool]): Indicates whether indicates whether the organization should not
            be contacted at this address..
        organization_do_not_mail_reason (Union[Unset, str]): The indicates the reason the organization should not be
            contacted at this address.. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/donotmailreasoncode/entries
        organization_phone_type (Union[Unset, str]): The the phone type of the related organization's phone.. This code
            table can be queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/phonetypecode/entries
        organization_number (Union[Unset, str]): The the related organization's phone number. character limit: 100..
        organization_relationship_type_code (Union[Unset, str]): The the type of relationship between the constituent
            and related organization. can be expressed as, "the organization is the constituent's _______".. This simple
            list can be queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/4e869c5a-9b9d-4e84-b6e0-
            1fc66bafbafc?parameters=gender,{gendercode}&parameters=appliestoconstituenttype,{constituent_type}&parameters=re
            latestoconstituenttype,{1}.
        organization_reciprocal_type_code (Union[Unset, str]): The the type of relationship between the related
            organization and the constituent. can be expressed as, "the constituent is the organization's _______".. This
            simple list can be queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/c3018803-2ea5-4f62-91cf-
            412e88d15f9b?parameters=appliestoconstituenttype,{constituent_type}&parameters=constituentid,{organization_id}&p
            arameters=appliestorelationshiptypeid,{organization_relationshiptypecodeid}&parameters=relatestoconstituenttype,
            {1}.
        organization_start_date (Union[Unset, datetime.datetime]): The the related organization's start date.. Uses the
            format YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        organization_end_date (Union[Unset, datetime.datetime]): The the related organization's end date.. Uses the
            format YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        contact (Union[Unset, bool]): Indicates whether contact.
        contact_type (Union[Unset, str]): The the related organization's contact type.. This code table can be queried
            at https://api.sky.blackbaud.com/crm-adnmg/codetables/contacttypecode/entries
        primary_contact (Union[Unset, bool]): Indicates whether indicates whether this is the constituent's primary
            contact..
        position (Union[Unset, str]): The the constituent's job title. character limit: 100..
        matching_gift_relationship (Union[Unset, bool]): Indicates whether indicates whether this organization will
            match an individual's contributions..
        reciprocal_recognition_type (Union[Unset, str]): The recognition credit type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/revenuerecognitiontypecode/entries
        primary_recognition_type (Union[Unset, str]): The recognition credit type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/revenuerecognitiontypecode/entries
        address_omit_from_validation (Union[Unset, bool]): Indicates whether indicates the constituent's address is
            omitted from validation..
        address_dpc (Union[Unset, str]): The address dpc.
        address_cart (Union[Unset, str]): The address cart.
        address_lot (Union[Unset, str]): The address lot.
        address_county (Union[Unset, str]): The address county. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/countycode/entries
        address_congressional_district (Union[Unset, str]): The address congressional district. This code table can be
            queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/congressionaldistrictcode/entries
        address_last_validation_attempt_date (Union[Unset, datetime.datetime]): The address last validation attempt
            date. Uses the format YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        address_validation_message (Union[Unset, str]): The address validation message.
        address_certification_data (Union[Unset, int]): The address certification data.
        organization_omit_from_validation (Union[Unset, bool]): Indicates whether omit from validation.
        organization_dpc (Union[Unset, str]): The organization dpc.
        organization_cart (Union[Unset, str]): The organization cart.
        organization_lot (Union[Unset, str]): The organization lot.
        organization_county (Union[Unset, str]): The organization county. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/countycode/entries
        organization_congressional_district (Union[Unset, str]): The organization congressional district. This code
            table can be queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/congressionaldistrictcode/entries
        organization_last_validation_attempt_date (Union[Unset, datetime.datetime]): The organization last validation
            attempt date. Uses the format YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        organization_validation_message (Union[Unset, str]): The organization validation message.
        organization_certification_data (Union[Unset, int]): The organization certification data.
        validation_countries (Union[Unset, List['NewIndividualValidationCountries']]): Validation countries.
        zip_lookup_countries (Union[Unset, List['NewIndividualZipLookupCountries']]): Zip lookup countries.
        spouse_relationship (Union[Unset, bool]): Indicates whether indicates whether this is a spouse relationship with
            the constituent..
        house_hold_copy_primary_contact_info (Union[Unset, bool]): Indicates whether indicates whether to copy the
            individual's primary contact information to the household..
        job_category (Union[Unset, str]): The the constituent's job category.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/jobcategorycode/entries
        career_level (Union[Unset, str]): The the constituent's career level.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/careerlevelcode/entries
        address_info_source (Union[Unset, str]): The the infomation source of the constituent's address .. This code
            table can be queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/infosourcecode/entries
        organization_info_source (Union[Unset, str]): The the infomation source of the related organization.. This code
            table can be queried at https://api.sky.blackbaud.com/crm-adnmg/codetables/infosourcecode/entries
        title_2 (Union[Unset, str]): The the constituent's second title.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/titlecode/entries
        suffix_2 (Union[Unset, str]): The the related individual's second suffix.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/suffixcode/entries
        spouse_title_2 (Union[Unset, str]): The the related individual's second title.. This code table can be queried
            at https://api.sky.blackbaud.com/crm-adnmg/codetables/titlecode/entries
        spouse_suffix_2 (Union[Unset, str]): The the constituent's second suffix.. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/suffixcode/entries
        skip_adding_sites (Union[Unset, bool]): Indicates whether skip adding sites.
        constituent_type (Union[Unset, int]): The the constituent's type.. Read-only in the SOAP API.
        organization_primary_soft_credit_relationship_exists (Union[Unset, bool]): Indicates whether indicates whether
            to apply recognition credits from gifts made by the organization to the individual..
        organization_primary_soft_credit_match_factor (Union[Unset, float]): The the match percentage for recognition
            credits applied to the individual from gifts made by the organization..
        organization_reciprocal_soft_credit_relationship_exists (Union[Unset, bool]): Indicates whether apply
            recognition credits from gifts by the individual to the organization..
        organization_reciprocal_soft_credit_match_factor (Union[Unset, float]): The the match percentage for recognition
            credits applied to the organization from gifts made by the individual..
        organization_primary_recognition_type (Union[Unset, str]): The the recognition type of credits applied to the
            individual from the organization.. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/revenuerecognitiontypecode/entries
        organization_reciprocal_recognition_type (Union[Unset, str]): The the recognition type of credits applied to the
            organization from the individual.. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/revenuerecognitiontypecode/entries
        gender_code (Union[Unset, str]): The gender. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/gendercode/entries
        spouse_gender_code (Union[Unset, str]): The gender. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/gendercode/entries
    """

    last_name: str
    gender: str
    first_name: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    suffix: Union[Unset, str] = UNSET
    nickname: Union[Unset, str] = UNSET
    maiden_name: Union[Unset, str] = UNSET
    birth_date: Union[Unset, "FuzzyDate"] = UNSET
    marital_status: Union[Unset, str] = UNSET
    address_type: Union[Unset, str] = UNSET
    address_country: Union[Unset, str] = UNSET
    address_block: Union[Unset, str] = UNSET
    address_city: Union[Unset, str] = UNSET
    address_state: Union[Unset, str] = UNSET
    address_post_code: Union[Unset, str] = UNSET
    address_do_not_mail: Union[Unset, bool] = UNSET
    address_do_not_mail_reason: Union[Unset, str] = UNSET
    phone_type: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    email_address_type: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    skip_adding_security_groups: Union[Unset, bool] = UNSET
    existing_spouse: Union[Unset, bool] = UNSET
    spouse_id: Union[Unset, str] = UNSET
    spouse_last_name: Union[Unset, str] = UNSET
    spouse_first_name: Union[Unset, str] = UNSET
    spouse_middle_name: Union[Unset, str] = UNSET
    spouse_title: Union[Unset, str] = UNSET
    spouse_suffix: Union[Unset, str] = UNSET
    spouse_nick_name: Union[Unset, str] = UNSET
    spouse_maiden_name: Union[Unset, str] = UNSET
    spouse_birth_date: Union[Unset, "FuzzyDate"] = UNSET
    spouse_gender: Union[Unset, str] = UNSET
    spouse_relationship_type_code: Union[Unset, str] = UNSET
    spouse_reciprocal_type_code: Union[Unset, str] = UNSET
    spouse_start_date: Union[Unset, datetime.datetime] = UNSET
    copy_primary_information: Union[Unset, bool] = UNSET
    primary_soft_credit_relationship_exists: Union[Unset, bool] = UNSET
    primary_soft_credit_match_factor: Union[Unset, float] = UNSET
    reciprocal_soft_credit_relationship_exists: Union[Unset, bool] = UNSET
    reciprocal_soft_credit_match_factor: Union[Unset, float] = UNSET
    existing_organization: Union[Unset, bool] = UNSET
    organization_id: Union[Unset, str] = UNSET
    organization_name: Union[Unset, str] = UNSET
    organization_address_type: Union[Unset, str] = UNSET
    organization_country: Union[Unset, str] = UNSET
    organization_address_block: Union[Unset, str] = UNSET
    organization_city: Union[Unset, str] = UNSET
    organization_state: Union[Unset, str] = UNSET
    organization_post_code: Union[Unset, str] = UNSET
    organization_do_not_mail: Union[Unset, bool] = UNSET
    organization_do_not_mail_reason: Union[Unset, str] = UNSET
    organization_phone_type: Union[Unset, str] = UNSET
    organization_number: Union[Unset, str] = UNSET
    organization_relationship_type_code: Union[Unset, str] = UNSET
    organization_reciprocal_type_code: Union[Unset, str] = UNSET
    organization_start_date: Union[Unset, datetime.datetime] = UNSET
    organization_end_date: Union[Unset, datetime.datetime] = UNSET
    contact: Union[Unset, bool] = UNSET
    contact_type: Union[Unset, str] = UNSET
    primary_contact: Union[Unset, bool] = UNSET
    position: Union[Unset, str] = UNSET
    matching_gift_relationship: Union[Unset, bool] = UNSET
    reciprocal_recognition_type: Union[Unset, str] = UNSET
    primary_recognition_type: Union[Unset, str] = UNSET
    address_omit_from_validation: Union[Unset, bool] = UNSET
    address_dpc: Union[Unset, str] = UNSET
    address_cart: Union[Unset, str] = UNSET
    address_lot: Union[Unset, str] = UNSET
    address_county: Union[Unset, str] = UNSET
    address_congressional_district: Union[Unset, str] = UNSET
    address_last_validation_attempt_date: Union[Unset, datetime.datetime] = UNSET
    address_validation_message: Union[Unset, str] = UNSET
    address_certification_data: Union[Unset, int] = UNSET
    organization_omit_from_validation: Union[Unset, bool] = UNSET
    organization_dpc: Union[Unset, str] = UNSET
    organization_cart: Union[Unset, str] = UNSET
    organization_lot: Union[Unset, str] = UNSET
    organization_county: Union[Unset, str] = UNSET
    organization_congressional_district: Union[Unset, str] = UNSET
    organization_last_validation_attempt_date: Union[Unset, datetime.datetime] = UNSET
    organization_validation_message: Union[Unset, str] = UNSET
    organization_certification_data: Union[Unset, int] = UNSET
    validation_countries: Union[Unset, List["NewIndividualValidationCountries"]] = UNSET
    zip_lookup_countries: Union[Unset, List["NewIndividualZipLookupCountries"]] = UNSET
    spouse_relationship: Union[Unset, bool] = UNSET
    house_hold_copy_primary_contact_info: Union[Unset, bool] = UNSET
    job_category: Union[Unset, str] = UNSET
    career_level: Union[Unset, str] = UNSET
    address_info_source: Union[Unset, str] = UNSET
    organization_info_source: Union[Unset, str] = UNSET
    title_2: Union[Unset, str] = UNSET
    suffix_2: Union[Unset, str] = UNSET
    spouse_title_2: Union[Unset, str] = UNSET
    spouse_suffix_2: Union[Unset, str] = UNSET
    skip_adding_sites: Union[Unset, bool] = UNSET
    constituent_type: Union[Unset, int] = UNSET
    organization_primary_soft_credit_relationship_exists: Union[Unset, bool] = UNSET
    organization_primary_soft_credit_match_factor: Union[Unset, float] = UNSET
    organization_reciprocal_soft_credit_relationship_exists: Union[Unset, bool] = UNSET
    organization_reciprocal_soft_credit_match_factor: Union[Unset, float] = UNSET
    organization_primary_recognition_type: Union[Unset, str] = UNSET
    organization_reciprocal_recognition_type: Union[Unset, str] = UNSET
    gender_code: Union[Unset, str] = UNSET
    spouse_gender_code: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        last_name = self.last_name

        gender = self.gender

        first_name = self.first_name

        middle_name = self.middle_name

        title = self.title

        suffix = self.suffix

        nickname = self.nickname

        maiden_name = self.maiden_name

        birth_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.birth_date, Unset):
            birth_date = self.birth_date.to_dict()

        marital_status = self.marital_status

        address_type = self.address_type

        address_country = self.address_country

        address_block = self.address_block

        address_city = self.address_city

        address_state = self.address_state

        address_post_code = self.address_post_code

        address_do_not_mail = self.address_do_not_mail

        address_do_not_mail_reason = self.address_do_not_mail_reason

        phone_type = self.phone_type

        phone_number = self.phone_number

        email_address_type = self.email_address_type

        email_address = self.email_address

        skip_adding_security_groups = self.skip_adding_security_groups

        existing_spouse = self.existing_spouse

        spouse_id = self.spouse_id

        spouse_last_name = self.spouse_last_name

        spouse_first_name = self.spouse_first_name

        spouse_middle_name = self.spouse_middle_name

        spouse_title = self.spouse_title

        spouse_suffix = self.spouse_suffix

        spouse_nick_name = self.spouse_nick_name

        spouse_maiden_name = self.spouse_maiden_name

        spouse_birth_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.spouse_birth_date, Unset):
            spouse_birth_date = self.spouse_birth_date.to_dict()

        spouse_gender = self.spouse_gender

        spouse_relationship_type_code = self.spouse_relationship_type_code

        spouse_reciprocal_type_code = self.spouse_reciprocal_type_code

        spouse_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.spouse_start_date, Unset):
            spouse_start_date = self.spouse_start_date.isoformat()

        copy_primary_information = self.copy_primary_information

        primary_soft_credit_relationship_exists = self.primary_soft_credit_relationship_exists

        primary_soft_credit_match_factor = self.primary_soft_credit_match_factor

        reciprocal_soft_credit_relationship_exists = self.reciprocal_soft_credit_relationship_exists

        reciprocal_soft_credit_match_factor = self.reciprocal_soft_credit_match_factor

        existing_organization = self.existing_organization

        organization_id = self.organization_id

        organization_name = self.organization_name

        organization_address_type = self.organization_address_type

        organization_country = self.organization_country

        organization_address_block = self.organization_address_block

        organization_city = self.organization_city

        organization_state = self.organization_state

        organization_post_code = self.organization_post_code

        organization_do_not_mail = self.organization_do_not_mail

        organization_do_not_mail_reason = self.organization_do_not_mail_reason

        organization_phone_type = self.organization_phone_type

        organization_number = self.organization_number

        organization_relationship_type_code = self.organization_relationship_type_code

        organization_reciprocal_type_code = self.organization_reciprocal_type_code

        organization_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.organization_start_date, Unset):
            organization_start_date = self.organization_start_date.isoformat()

        organization_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.organization_end_date, Unset):
            organization_end_date = self.organization_end_date.isoformat()

        contact = self.contact

        contact_type = self.contact_type

        primary_contact = self.primary_contact

        position = self.position

        matching_gift_relationship = self.matching_gift_relationship

        reciprocal_recognition_type = self.reciprocal_recognition_type

        primary_recognition_type = self.primary_recognition_type

        address_omit_from_validation = self.address_omit_from_validation

        address_dpc = self.address_dpc

        address_cart = self.address_cart

        address_lot = self.address_lot

        address_county = self.address_county

        address_congressional_district = self.address_congressional_district

        address_last_validation_attempt_date: Union[Unset, str] = UNSET
        if not isinstance(self.address_last_validation_attempt_date, Unset):
            address_last_validation_attempt_date = self.address_last_validation_attempt_date.isoformat()

        address_validation_message = self.address_validation_message

        address_certification_data = self.address_certification_data

        organization_omit_from_validation = self.organization_omit_from_validation

        organization_dpc = self.organization_dpc

        organization_cart = self.organization_cart

        organization_lot = self.organization_lot

        organization_county = self.organization_county

        organization_congressional_district = self.organization_congressional_district

        organization_last_validation_attempt_date: Union[Unset, str] = UNSET
        if not isinstance(self.organization_last_validation_attempt_date, Unset):
            organization_last_validation_attempt_date = self.organization_last_validation_attempt_date.isoformat()

        organization_validation_message = self.organization_validation_message

        organization_certification_data = self.organization_certification_data

        validation_countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.validation_countries, Unset):
            validation_countries = []
            for validation_countries_item_data in self.validation_countries:
                validation_countries_item = validation_countries_item_data.to_dict()
                validation_countries.append(validation_countries_item)

        zip_lookup_countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.zip_lookup_countries, Unset):
            zip_lookup_countries = []
            for zip_lookup_countries_item_data in self.zip_lookup_countries:
                zip_lookup_countries_item = zip_lookup_countries_item_data.to_dict()
                zip_lookup_countries.append(zip_lookup_countries_item)

        spouse_relationship = self.spouse_relationship

        house_hold_copy_primary_contact_info = self.house_hold_copy_primary_contact_info

        job_category = self.job_category

        career_level = self.career_level

        address_info_source = self.address_info_source

        organization_info_source = self.organization_info_source

        title_2 = self.title_2

        suffix_2 = self.suffix_2

        spouse_title_2 = self.spouse_title_2

        spouse_suffix_2 = self.spouse_suffix_2

        skip_adding_sites = self.skip_adding_sites

        constituent_type = self.constituent_type

        organization_primary_soft_credit_relationship_exists = self.organization_primary_soft_credit_relationship_exists

        organization_primary_soft_credit_match_factor = self.organization_primary_soft_credit_match_factor

        organization_reciprocal_soft_credit_relationship_exists = (
            self.organization_reciprocal_soft_credit_relationship_exists
        )

        organization_reciprocal_soft_credit_match_factor = self.organization_reciprocal_soft_credit_match_factor

        organization_primary_recognition_type = self.organization_primary_recognition_type

        organization_reciprocal_recognition_type = self.organization_reciprocal_recognition_type

        gender_code = self.gender_code

        spouse_gender_code = self.spouse_gender_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "last_name": last_name,
                "gender": gender,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if title is not UNSET:
            field_dict["title"] = title
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if nickname is not UNSET:
            field_dict["nickname"] = nickname
        if maiden_name is not UNSET:
            field_dict["maiden_name"] = maiden_name
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if marital_status is not UNSET:
            field_dict["marital_status"] = marital_status
        if address_type is not UNSET:
            field_dict["address_type"] = address_type
        if address_country is not UNSET:
            field_dict["address_country"] = address_country
        if address_block is not UNSET:
            field_dict["address_block"] = address_block
        if address_city is not UNSET:
            field_dict["address_city"] = address_city
        if address_state is not UNSET:
            field_dict["address_state"] = address_state
        if address_post_code is not UNSET:
            field_dict["address_post_code"] = address_post_code
        if address_do_not_mail is not UNSET:
            field_dict["address_do_not_mail"] = address_do_not_mail
        if address_do_not_mail_reason is not UNSET:
            field_dict["address_do_not_mail_reason"] = address_do_not_mail_reason
        if phone_type is not UNSET:
            field_dict["phone_type"] = phone_type
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if email_address_type is not UNSET:
            field_dict["email_address_type"] = email_address_type
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if skip_adding_security_groups is not UNSET:
            field_dict["skip_adding_security_groups"] = skip_adding_security_groups
        if existing_spouse is not UNSET:
            field_dict["existing_spouse"] = existing_spouse
        if spouse_id is not UNSET:
            field_dict["spouse_id"] = spouse_id
        if spouse_last_name is not UNSET:
            field_dict["spouse_last_name"] = spouse_last_name
        if spouse_first_name is not UNSET:
            field_dict["spouse_first_name"] = spouse_first_name
        if spouse_middle_name is not UNSET:
            field_dict["spouse_middle_name"] = spouse_middle_name
        if spouse_title is not UNSET:
            field_dict["spouse_title"] = spouse_title
        if spouse_suffix is not UNSET:
            field_dict["spouse_suffix"] = spouse_suffix
        if spouse_nick_name is not UNSET:
            field_dict["spouse_nick_name"] = spouse_nick_name
        if spouse_maiden_name is not UNSET:
            field_dict["spouse_maiden_name"] = spouse_maiden_name
        if spouse_birth_date is not UNSET:
            field_dict["spouse_birth_date"] = spouse_birth_date
        if spouse_gender is not UNSET:
            field_dict["spouse_gender"] = spouse_gender
        if spouse_relationship_type_code is not UNSET:
            field_dict["spouse_relationship_type_code"] = spouse_relationship_type_code
        if spouse_reciprocal_type_code is not UNSET:
            field_dict["spouse_reciprocal_type_code"] = spouse_reciprocal_type_code
        if spouse_start_date is not UNSET:
            field_dict["spouse_start_date"] = spouse_start_date
        if copy_primary_information is not UNSET:
            field_dict["copy_primary_information"] = copy_primary_information
        if primary_soft_credit_relationship_exists is not UNSET:
            field_dict["primary_soft_credit_relationship_exists"] = primary_soft_credit_relationship_exists
        if primary_soft_credit_match_factor is not UNSET:
            field_dict["primary_soft_credit_match_factor"] = primary_soft_credit_match_factor
        if reciprocal_soft_credit_relationship_exists is not UNSET:
            field_dict["reciprocal_soft_credit_relationship_exists"] = reciprocal_soft_credit_relationship_exists
        if reciprocal_soft_credit_match_factor is not UNSET:
            field_dict["reciprocal_soft_credit_match_factor"] = reciprocal_soft_credit_match_factor
        if existing_organization is not UNSET:
            field_dict["existing_organization"] = existing_organization
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if organization_address_type is not UNSET:
            field_dict["organization_address_type"] = organization_address_type
        if organization_country is not UNSET:
            field_dict["organization_country"] = organization_country
        if organization_address_block is not UNSET:
            field_dict["organization_address_block"] = organization_address_block
        if organization_city is not UNSET:
            field_dict["organization_city"] = organization_city
        if organization_state is not UNSET:
            field_dict["organization_state"] = organization_state
        if organization_post_code is not UNSET:
            field_dict["organization_post_code"] = organization_post_code
        if organization_do_not_mail is not UNSET:
            field_dict["organization_do_not_mail"] = organization_do_not_mail
        if organization_do_not_mail_reason is not UNSET:
            field_dict["organization_do_not_mail_reason"] = organization_do_not_mail_reason
        if organization_phone_type is not UNSET:
            field_dict["organization_phone_type"] = organization_phone_type
        if organization_number is not UNSET:
            field_dict["organization_number"] = organization_number
        if organization_relationship_type_code is not UNSET:
            field_dict["organization_relationship_type_code"] = organization_relationship_type_code
        if organization_reciprocal_type_code is not UNSET:
            field_dict["organization_reciprocal_type_code"] = organization_reciprocal_type_code
        if organization_start_date is not UNSET:
            field_dict["organization_start_date"] = organization_start_date
        if organization_end_date is not UNSET:
            field_dict["organization_end_date"] = organization_end_date
        if contact is not UNSET:
            field_dict["contact"] = contact
        if contact_type is not UNSET:
            field_dict["contact_type"] = contact_type
        if primary_contact is not UNSET:
            field_dict["primary_contact"] = primary_contact
        if position is not UNSET:
            field_dict["position"] = position
        if matching_gift_relationship is not UNSET:
            field_dict["matching_gift_relationship"] = matching_gift_relationship
        if reciprocal_recognition_type is not UNSET:
            field_dict["reciprocal_recognition_type"] = reciprocal_recognition_type
        if primary_recognition_type is not UNSET:
            field_dict["primary_recognition_type"] = primary_recognition_type
        if address_omit_from_validation is not UNSET:
            field_dict["address_omit_from_validation"] = address_omit_from_validation
        if address_dpc is not UNSET:
            field_dict["address_dpc"] = address_dpc
        if address_cart is not UNSET:
            field_dict["address_cart"] = address_cart
        if address_lot is not UNSET:
            field_dict["address_lot"] = address_lot
        if address_county is not UNSET:
            field_dict["address_county"] = address_county
        if address_congressional_district is not UNSET:
            field_dict["address_congressional_district"] = address_congressional_district
        if address_last_validation_attempt_date is not UNSET:
            field_dict["address_last_validation_attempt_date"] = address_last_validation_attempt_date
        if address_validation_message is not UNSET:
            field_dict["address_validation_message"] = address_validation_message
        if address_certification_data is not UNSET:
            field_dict["address_certification_data"] = address_certification_data
        if organization_omit_from_validation is not UNSET:
            field_dict["organization_omit_from_validation"] = organization_omit_from_validation
        if organization_dpc is not UNSET:
            field_dict["organization_dpc"] = organization_dpc
        if organization_cart is not UNSET:
            field_dict["organization_cart"] = organization_cart
        if organization_lot is not UNSET:
            field_dict["organization_lot"] = organization_lot
        if organization_county is not UNSET:
            field_dict["organization_county"] = organization_county
        if organization_congressional_district is not UNSET:
            field_dict["organization_congressional_district"] = organization_congressional_district
        if organization_last_validation_attempt_date is not UNSET:
            field_dict["organization_last_validation_attempt_date"] = organization_last_validation_attempt_date
        if organization_validation_message is not UNSET:
            field_dict["organization_validation_message"] = organization_validation_message
        if organization_certification_data is not UNSET:
            field_dict["organization_certification_data"] = organization_certification_data
        if validation_countries is not UNSET:
            field_dict["validation_countries"] = validation_countries
        if zip_lookup_countries is not UNSET:
            field_dict["zip_lookup_countries"] = zip_lookup_countries
        if spouse_relationship is not UNSET:
            field_dict["spouse_relationship"] = spouse_relationship
        if house_hold_copy_primary_contact_info is not UNSET:
            field_dict["house_hold_copy_primary_contact_info"] = house_hold_copy_primary_contact_info
        if job_category is not UNSET:
            field_dict["job_category"] = job_category
        if career_level is not UNSET:
            field_dict["career_level"] = career_level
        if address_info_source is not UNSET:
            field_dict["address_info_source"] = address_info_source
        if organization_info_source is not UNSET:
            field_dict["organization_info_source"] = organization_info_source
        if title_2 is not UNSET:
            field_dict["title_2"] = title_2
        if suffix_2 is not UNSET:
            field_dict["suffix_2"] = suffix_2
        if spouse_title_2 is not UNSET:
            field_dict["spouse_title_2"] = spouse_title_2
        if spouse_suffix_2 is not UNSET:
            field_dict["spouse_suffix_2"] = spouse_suffix_2
        if skip_adding_sites is not UNSET:
            field_dict["skip_adding_sites"] = skip_adding_sites
        if constituent_type is not UNSET:
            field_dict["constituent_type"] = constituent_type
        if organization_primary_soft_credit_relationship_exists is not UNSET:
            field_dict["organization_primary_soft_credit_relationship_exists"] = (
                organization_primary_soft_credit_relationship_exists
            )
        if organization_primary_soft_credit_match_factor is not UNSET:
            field_dict["organization_primary_soft_credit_match_factor"] = organization_primary_soft_credit_match_factor
        if organization_reciprocal_soft_credit_relationship_exists is not UNSET:
            field_dict["organization_reciprocal_soft_credit_relationship_exists"] = (
                organization_reciprocal_soft_credit_relationship_exists
            )
        if organization_reciprocal_soft_credit_match_factor is not UNSET:
            field_dict["organization_reciprocal_soft_credit_match_factor"] = (
                organization_reciprocal_soft_credit_match_factor
            )
        if organization_primary_recognition_type is not UNSET:
            field_dict["organization_primary_recognition_type"] = organization_primary_recognition_type
        if organization_reciprocal_recognition_type is not UNSET:
            field_dict["organization_reciprocal_recognition_type"] = organization_reciprocal_recognition_type
        if gender_code is not UNSET:
            field_dict["gender_code"] = gender_code
        if spouse_gender_code is not UNSET:
            field_dict["spouse_gender_code"] = spouse_gender_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fuzzy_date import FuzzyDate
        from ..models.new_individual_validation_countries import NewIndividualValidationCountries
        from ..models.new_individual_zip_lookup_countries import NewIndividualZipLookupCountries

        d = src_dict.copy()
        last_name = d.pop("last_name")

        gender = d.pop("gender")

        first_name = d.pop("first_name", UNSET)

        middle_name = d.pop("middle_name", UNSET)

        title = d.pop("title", UNSET)

        suffix = d.pop("suffix", UNSET)

        nickname = d.pop("nickname", UNSET)

        maiden_name = d.pop("maiden_name", UNSET)

        _birth_date = d.pop("birth_date", UNSET)
        birth_date: Union[Unset, FuzzyDate]
        if isinstance(_birth_date, Unset):
            birth_date = UNSET
        else:
            birth_date = FuzzyDate.from_dict(_birth_date)

        marital_status = d.pop("marital_status", UNSET)

        address_type = d.pop("address_type", UNSET)

        address_country = d.pop("address_country", UNSET)

        address_block = d.pop("address_block", UNSET)

        address_city = d.pop("address_city", UNSET)

        address_state = d.pop("address_state", UNSET)

        address_post_code = d.pop("address_post_code", UNSET)

        address_do_not_mail = d.pop("address_do_not_mail", UNSET)

        address_do_not_mail_reason = d.pop("address_do_not_mail_reason", UNSET)

        phone_type = d.pop("phone_type", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        email_address_type = d.pop("email_address_type", UNSET)

        email_address = d.pop("email_address", UNSET)

        skip_adding_security_groups = d.pop("skip_adding_security_groups", UNSET)

        existing_spouse = d.pop("existing_spouse", UNSET)

        spouse_id = d.pop("spouse_id", UNSET)

        spouse_last_name = d.pop("spouse_last_name", UNSET)

        spouse_first_name = d.pop("spouse_first_name", UNSET)

        spouse_middle_name = d.pop("spouse_middle_name", UNSET)

        spouse_title = d.pop("spouse_title", UNSET)

        spouse_suffix = d.pop("spouse_suffix", UNSET)

        spouse_nick_name = d.pop("spouse_nick_name", UNSET)

        spouse_maiden_name = d.pop("spouse_maiden_name", UNSET)

        _spouse_birth_date = d.pop("spouse_birth_date", UNSET)
        spouse_birth_date: Union[Unset, FuzzyDate]
        if isinstance(_spouse_birth_date, Unset):
            spouse_birth_date = UNSET
        else:
            spouse_birth_date = FuzzyDate.from_dict(_spouse_birth_date)

        spouse_gender = d.pop("spouse_gender", UNSET)

        spouse_relationship_type_code = d.pop("spouse_relationship_type_code", UNSET)

        spouse_reciprocal_type_code = d.pop("spouse_reciprocal_type_code", UNSET)

        _spouse_start_date = d.pop("spouse_start_date", UNSET)
        spouse_start_date: Union[Unset, datetime.datetime]
        if isinstance(_spouse_start_date, Unset):
            spouse_start_date = UNSET
        else:
            spouse_start_date = isoparse(_spouse_start_date)

        copy_primary_information = d.pop("copy_primary_information", UNSET)

        primary_soft_credit_relationship_exists = d.pop("primary_soft_credit_relationship_exists", UNSET)

        primary_soft_credit_match_factor = d.pop("primary_soft_credit_match_factor", UNSET)

        reciprocal_soft_credit_relationship_exists = d.pop("reciprocal_soft_credit_relationship_exists", UNSET)

        reciprocal_soft_credit_match_factor = d.pop("reciprocal_soft_credit_match_factor", UNSET)

        existing_organization = d.pop("existing_organization", UNSET)

        organization_id = d.pop("organization_id", UNSET)

        organization_name = d.pop("organization_name", UNSET)

        organization_address_type = d.pop("organization_address_type", UNSET)

        organization_country = d.pop("organization_country", UNSET)

        organization_address_block = d.pop("organization_address_block", UNSET)

        organization_city = d.pop("organization_city", UNSET)

        organization_state = d.pop("organization_state", UNSET)

        organization_post_code = d.pop("organization_post_code", UNSET)

        organization_do_not_mail = d.pop("organization_do_not_mail", UNSET)

        organization_do_not_mail_reason = d.pop("organization_do_not_mail_reason", UNSET)

        organization_phone_type = d.pop("organization_phone_type", UNSET)

        organization_number = d.pop("organization_number", UNSET)

        organization_relationship_type_code = d.pop("organization_relationship_type_code", UNSET)

        organization_reciprocal_type_code = d.pop("organization_reciprocal_type_code", UNSET)

        _organization_start_date = d.pop("organization_start_date", UNSET)
        organization_start_date: Union[Unset, datetime.datetime]
        if isinstance(_organization_start_date, Unset):
            organization_start_date = UNSET
        else:
            organization_start_date = isoparse(_organization_start_date)

        _organization_end_date = d.pop("organization_end_date", UNSET)
        organization_end_date: Union[Unset, datetime.datetime]
        if isinstance(_organization_end_date, Unset):
            organization_end_date = UNSET
        else:
            organization_end_date = isoparse(_organization_end_date)

        contact = d.pop("contact", UNSET)

        contact_type = d.pop("contact_type", UNSET)

        primary_contact = d.pop("primary_contact", UNSET)

        position = d.pop("position", UNSET)

        matching_gift_relationship = d.pop("matching_gift_relationship", UNSET)

        reciprocal_recognition_type = d.pop("reciprocal_recognition_type", UNSET)

        primary_recognition_type = d.pop("primary_recognition_type", UNSET)

        address_omit_from_validation = d.pop("address_omit_from_validation", UNSET)

        address_dpc = d.pop("address_dpc", UNSET)

        address_cart = d.pop("address_cart", UNSET)

        address_lot = d.pop("address_lot", UNSET)

        address_county = d.pop("address_county", UNSET)

        address_congressional_district = d.pop("address_congressional_district", UNSET)

        _address_last_validation_attempt_date = d.pop("address_last_validation_attempt_date", UNSET)
        address_last_validation_attempt_date: Union[Unset, datetime.datetime]
        if isinstance(_address_last_validation_attempt_date, Unset):
            address_last_validation_attempt_date = UNSET
        else:
            address_last_validation_attempt_date = isoparse(_address_last_validation_attempt_date)

        address_validation_message = d.pop("address_validation_message", UNSET)

        address_certification_data = d.pop("address_certification_data", UNSET)

        organization_omit_from_validation = d.pop("organization_omit_from_validation", UNSET)

        organization_dpc = d.pop("organization_dpc", UNSET)

        organization_cart = d.pop("organization_cart", UNSET)

        organization_lot = d.pop("organization_lot", UNSET)

        organization_county = d.pop("organization_county", UNSET)

        organization_congressional_district = d.pop("organization_congressional_district", UNSET)

        _organization_last_validation_attempt_date = d.pop("organization_last_validation_attempt_date", UNSET)
        organization_last_validation_attempt_date: Union[Unset, datetime.datetime]
        if isinstance(_organization_last_validation_attempt_date, Unset):
            organization_last_validation_attempt_date = UNSET
        else:
            organization_last_validation_attempt_date = isoparse(_organization_last_validation_attempt_date)

        organization_validation_message = d.pop("organization_validation_message", UNSET)

        organization_certification_data = d.pop("organization_certification_data", UNSET)

        validation_countries = []
        _validation_countries = d.pop("validation_countries", UNSET)
        for validation_countries_item_data in _validation_countries or []:
            validation_countries_item = NewIndividualValidationCountries.from_dict(validation_countries_item_data)

            validation_countries.append(validation_countries_item)

        zip_lookup_countries = []
        _zip_lookup_countries = d.pop("zip_lookup_countries", UNSET)
        for zip_lookup_countries_item_data in _zip_lookup_countries or []:
            zip_lookup_countries_item = NewIndividualZipLookupCountries.from_dict(zip_lookup_countries_item_data)

            zip_lookup_countries.append(zip_lookup_countries_item)

        spouse_relationship = d.pop("spouse_relationship", UNSET)

        house_hold_copy_primary_contact_info = d.pop("house_hold_copy_primary_contact_info", UNSET)

        job_category = d.pop("job_category", UNSET)

        career_level = d.pop("career_level", UNSET)

        address_info_source = d.pop("address_info_source", UNSET)

        organization_info_source = d.pop("organization_info_source", UNSET)

        title_2 = d.pop("title_2", UNSET)

        suffix_2 = d.pop("suffix_2", UNSET)

        spouse_title_2 = d.pop("spouse_title_2", UNSET)

        spouse_suffix_2 = d.pop("spouse_suffix_2", UNSET)

        skip_adding_sites = d.pop("skip_adding_sites", UNSET)

        constituent_type = d.pop("constituent_type", UNSET)

        organization_primary_soft_credit_relationship_exists = d.pop(
            "organization_primary_soft_credit_relationship_exists", UNSET
        )

        organization_primary_soft_credit_match_factor = d.pop("organization_primary_soft_credit_match_factor", UNSET)

        organization_reciprocal_soft_credit_relationship_exists = d.pop(
            "organization_reciprocal_soft_credit_relationship_exists", UNSET
        )

        organization_reciprocal_soft_credit_match_factor = d.pop(
            "organization_reciprocal_soft_credit_match_factor", UNSET
        )

        organization_primary_recognition_type = d.pop("organization_primary_recognition_type", UNSET)

        organization_reciprocal_recognition_type = d.pop("organization_reciprocal_recognition_type", UNSET)

        gender_code = d.pop("gender_code", UNSET)

        spouse_gender_code = d.pop("spouse_gender_code", UNSET)

        new_individual = cls(
            last_name=last_name,
            gender=gender,
            first_name=first_name,
            middle_name=middle_name,
            title=title,
            suffix=suffix,
            nickname=nickname,
            maiden_name=maiden_name,
            birth_date=birth_date,
            marital_status=marital_status,
            address_type=address_type,
            address_country=address_country,
            address_block=address_block,
            address_city=address_city,
            address_state=address_state,
            address_post_code=address_post_code,
            address_do_not_mail=address_do_not_mail,
            address_do_not_mail_reason=address_do_not_mail_reason,
            phone_type=phone_type,
            phone_number=phone_number,
            email_address_type=email_address_type,
            email_address=email_address,
            skip_adding_security_groups=skip_adding_security_groups,
            existing_spouse=existing_spouse,
            spouse_id=spouse_id,
            spouse_last_name=spouse_last_name,
            spouse_first_name=spouse_first_name,
            spouse_middle_name=spouse_middle_name,
            spouse_title=spouse_title,
            spouse_suffix=spouse_suffix,
            spouse_nick_name=spouse_nick_name,
            spouse_maiden_name=spouse_maiden_name,
            spouse_birth_date=spouse_birth_date,
            spouse_gender=spouse_gender,
            spouse_relationship_type_code=spouse_relationship_type_code,
            spouse_reciprocal_type_code=spouse_reciprocal_type_code,
            spouse_start_date=spouse_start_date,
            copy_primary_information=copy_primary_information,
            primary_soft_credit_relationship_exists=primary_soft_credit_relationship_exists,
            primary_soft_credit_match_factor=primary_soft_credit_match_factor,
            reciprocal_soft_credit_relationship_exists=reciprocal_soft_credit_relationship_exists,
            reciprocal_soft_credit_match_factor=reciprocal_soft_credit_match_factor,
            existing_organization=existing_organization,
            organization_id=organization_id,
            organization_name=organization_name,
            organization_address_type=organization_address_type,
            organization_country=organization_country,
            organization_address_block=organization_address_block,
            organization_city=organization_city,
            organization_state=organization_state,
            organization_post_code=organization_post_code,
            organization_do_not_mail=organization_do_not_mail,
            organization_do_not_mail_reason=organization_do_not_mail_reason,
            organization_phone_type=organization_phone_type,
            organization_number=organization_number,
            organization_relationship_type_code=organization_relationship_type_code,
            organization_reciprocal_type_code=organization_reciprocal_type_code,
            organization_start_date=organization_start_date,
            organization_end_date=organization_end_date,
            contact=contact,
            contact_type=contact_type,
            primary_contact=primary_contact,
            position=position,
            matching_gift_relationship=matching_gift_relationship,
            reciprocal_recognition_type=reciprocal_recognition_type,
            primary_recognition_type=primary_recognition_type,
            address_omit_from_validation=address_omit_from_validation,
            address_dpc=address_dpc,
            address_cart=address_cart,
            address_lot=address_lot,
            address_county=address_county,
            address_congressional_district=address_congressional_district,
            address_last_validation_attempt_date=address_last_validation_attempt_date,
            address_validation_message=address_validation_message,
            address_certification_data=address_certification_data,
            organization_omit_from_validation=organization_omit_from_validation,
            organization_dpc=organization_dpc,
            organization_cart=organization_cart,
            organization_lot=organization_lot,
            organization_county=organization_county,
            organization_congressional_district=organization_congressional_district,
            organization_last_validation_attempt_date=organization_last_validation_attempt_date,
            organization_validation_message=organization_validation_message,
            organization_certification_data=organization_certification_data,
            validation_countries=validation_countries,
            zip_lookup_countries=zip_lookup_countries,
            spouse_relationship=spouse_relationship,
            house_hold_copy_primary_contact_info=house_hold_copy_primary_contact_info,
            job_category=job_category,
            career_level=career_level,
            address_info_source=address_info_source,
            organization_info_source=organization_info_source,
            title_2=title_2,
            suffix_2=suffix_2,
            spouse_title_2=spouse_title_2,
            spouse_suffix_2=spouse_suffix_2,
            skip_adding_sites=skip_adding_sites,
            constituent_type=constituent_type,
            organization_primary_soft_credit_relationship_exists=organization_primary_soft_credit_relationship_exists,
            organization_primary_soft_credit_match_factor=organization_primary_soft_credit_match_factor,
            organization_reciprocal_soft_credit_relationship_exists=organization_reciprocal_soft_credit_relationship_exists,
            organization_reciprocal_soft_credit_match_factor=organization_reciprocal_soft_credit_match_factor,
            organization_primary_recognition_type=organization_primary_recognition_type,
            organization_reciprocal_recognition_type=organization_reciprocal_recognition_type,
            gender_code=gender_code,
            spouse_gender_code=spouse_gender_code,
        )

        return new_individual
