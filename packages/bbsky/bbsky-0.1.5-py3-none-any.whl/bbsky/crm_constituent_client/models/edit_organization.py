from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditOrganization")


@_attrs_define
class EditOrganization:
    """EditOrganization.

    Example:
        {'organization_name': 'ABC Learning Center', 'industry': 'Education', 'num_employees': 20, 'num_subsidiaries':
            2, 'parent_corp_id': '', 'picture': '', 'picture_thumbnail': '', 'picture_changed': False, 'web_address': '',
            'is_primary': False, 'primary_address_id': '4811c284-31b1-4ba1-a94b-424687975bda', 'address_type': 'Business',
            'address_country': 'United States', 'address_block': '29 Hitch Avenue', 'address_city': 'Morgan',
            'address_state': 'UT', 'address_postcode': '84050', 'address_do_not_mail': False, 'address_do_not_mail_reason':
            '', 'primary_phone_id': '88f5c331-b465-413c-b955-976ec018beb5', 'phone_type': 'Business', 'phone_number':
            '801-557-2819', 'primary_email_address_id': '', 'email_address_type': '', 'email_address': ''}

    Attributes:
        organization_name (Union[Unset, str]): The name.
        industry (Union[Unset, str]): The industry. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/industrycode/entries
        num_employees (Union[Unset, int]): The no. of employees.
        num_subsidiaries (Union[Unset, int]): The no. of subsidiary orgs.
        parent_corp_id (Union[Unset, str]): The parent org.
        picture (Union[Unset, str]): The image.
        picture_thumbnail (Union[Unset, str]): The image thumbnail.
        picture_changed (Union[Unset, bool]): Indicates whether picture changed?.
        web_address (Union[Unset, str]): The website.
        is_primary (Union[Unset, bool]): Indicates whether this is a primary organization.
        primary_address_id (Union[Unset, str]): The primary address ID.
        address_type (Union[Unset, str]): The address type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/addresstypecode/entries
        address_country (Union[Unset, str]): The country. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/c9649672-353d-42e8-8c25-4d34bbabfbba.
        address_block (Union[Unset, str]): The address.
        address_city (Union[Unset, str]): The city.
        address_state (Union[Unset, str]): The state. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/7fa91401-596c-4f7c-936d-6e41683121d7?parameters=country_id,{address_countryid}.
        address_postcode (Union[Unset, str]): The zip.
        address_do_not_mail (Union[Unset, bool]): Indicates whether do not send mail to this address.
        address_do_not_mail_reason (Union[Unset, str]): The reason. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/donotmailreasoncode/entries
        primary_phone_id (Union[Unset, str]): The primary phone ID.
        phone_type (Union[Unset, str]): The phone type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/phonetypecode/entries
        phone_number (Union[Unset, str]): The phone number.
        primary_email_address_id (Union[Unset, str]): The primary email address ID.
        email_address_type (Union[Unset, str]): The email type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/emailaddresstypecode/entries
        email_address (Union[Unset, str]): The email address.
    """

    organization_name: Union[Unset, str] = UNSET
    industry: Union[Unset, str] = UNSET
    num_employees: Union[Unset, int] = UNSET
    num_subsidiaries: Union[Unset, int] = UNSET
    parent_corp_id: Union[Unset, str] = UNSET
    picture: Union[Unset, str] = UNSET
    picture_thumbnail: Union[Unset, str] = UNSET
    picture_changed: Union[Unset, bool] = UNSET
    web_address: Union[Unset, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    primary_address_id: Union[Unset, str] = UNSET
    address_type: Union[Unset, str] = UNSET
    address_country: Union[Unset, str] = UNSET
    address_block: Union[Unset, str] = UNSET
    address_city: Union[Unset, str] = UNSET
    address_state: Union[Unset, str] = UNSET
    address_postcode: Union[Unset, str] = UNSET
    address_do_not_mail: Union[Unset, bool] = UNSET
    address_do_not_mail_reason: Union[Unset, str] = UNSET
    primary_phone_id: Union[Unset, str] = UNSET
    phone_type: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    primary_email_address_id: Union[Unset, str] = UNSET
    email_address_type: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        organization_name = self.organization_name

        industry = self.industry

        num_employees = self.num_employees

        num_subsidiaries = self.num_subsidiaries

        parent_corp_id = self.parent_corp_id

        picture = self.picture

        picture_thumbnail = self.picture_thumbnail

        picture_changed = self.picture_changed

        web_address = self.web_address

        is_primary = self.is_primary

        primary_address_id = self.primary_address_id

        address_type = self.address_type

        address_country = self.address_country

        address_block = self.address_block

        address_city = self.address_city

        address_state = self.address_state

        address_postcode = self.address_postcode

        address_do_not_mail = self.address_do_not_mail

        address_do_not_mail_reason = self.address_do_not_mail_reason

        primary_phone_id = self.primary_phone_id

        phone_type = self.phone_type

        phone_number = self.phone_number

        primary_email_address_id = self.primary_email_address_id

        email_address_type = self.email_address_type

        email_address = self.email_address

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if industry is not UNSET:
            field_dict["industry"] = industry
        if num_employees is not UNSET:
            field_dict["num_employees"] = num_employees
        if num_subsidiaries is not UNSET:
            field_dict["num_subsidiaries"] = num_subsidiaries
        if parent_corp_id is not UNSET:
            field_dict["parent_corp_id"] = parent_corp_id
        if picture is not UNSET:
            field_dict["picture"] = picture
        if picture_thumbnail is not UNSET:
            field_dict["picture_thumbnail"] = picture_thumbnail
        if picture_changed is not UNSET:
            field_dict["picture_changed"] = picture_changed
        if web_address is not UNSET:
            field_dict["web_address"] = web_address
        if is_primary is not UNSET:
            field_dict["is_primary"] = is_primary
        if primary_address_id is not UNSET:
            field_dict["primary_address_id"] = primary_address_id
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
        if address_postcode is not UNSET:
            field_dict["address_postcode"] = address_postcode
        if address_do_not_mail is not UNSET:
            field_dict["address_do_not_mail"] = address_do_not_mail
        if address_do_not_mail_reason is not UNSET:
            field_dict["address_do_not_mail_reason"] = address_do_not_mail_reason
        if primary_phone_id is not UNSET:
            field_dict["primary_phone_id"] = primary_phone_id
        if phone_type is not UNSET:
            field_dict["phone_type"] = phone_type
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if primary_email_address_id is not UNSET:
            field_dict["primary_email_address_id"] = primary_email_address_id
        if email_address_type is not UNSET:
            field_dict["email_address_type"] = email_address_type
        if email_address is not UNSET:
            field_dict["email_address"] = email_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        organization_name = d.pop("organization_name", UNSET)

        industry = d.pop("industry", UNSET)

        num_employees = d.pop("num_employees", UNSET)

        num_subsidiaries = d.pop("num_subsidiaries", UNSET)

        parent_corp_id = d.pop("parent_corp_id", UNSET)

        picture = d.pop("picture", UNSET)

        picture_thumbnail = d.pop("picture_thumbnail", UNSET)

        picture_changed = d.pop("picture_changed", UNSET)

        web_address = d.pop("web_address", UNSET)

        is_primary = d.pop("is_primary", UNSET)

        primary_address_id = d.pop("primary_address_id", UNSET)

        address_type = d.pop("address_type", UNSET)

        address_country = d.pop("address_country", UNSET)

        address_block = d.pop("address_block", UNSET)

        address_city = d.pop("address_city", UNSET)

        address_state = d.pop("address_state", UNSET)

        address_postcode = d.pop("address_postcode", UNSET)

        address_do_not_mail = d.pop("address_do_not_mail", UNSET)

        address_do_not_mail_reason = d.pop("address_do_not_mail_reason", UNSET)

        primary_phone_id = d.pop("primary_phone_id", UNSET)

        phone_type = d.pop("phone_type", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        primary_email_address_id = d.pop("primary_email_address_id", UNSET)

        email_address_type = d.pop("email_address_type", UNSET)

        email_address = d.pop("email_address", UNSET)

        edit_organization = cls(
            organization_name=organization_name,
            industry=industry,
            num_employees=num_employees,
            num_subsidiaries=num_subsidiaries,
            parent_corp_id=parent_corp_id,
            picture=picture,
            picture_thumbnail=picture_thumbnail,
            picture_changed=picture_changed,
            web_address=web_address,
            is_primary=is_primary,
            primary_address_id=primary_address_id,
            address_type=address_type,
            address_country=address_country,
            address_block=address_block,
            address_city=address_city,
            address_state=address_state,
            address_postcode=address_postcode,
            address_do_not_mail=address_do_not_mail,
            address_do_not_mail_reason=address_do_not_mail_reason,
            primary_phone_id=primary_phone_id,
            phone_type=phone_type,
            phone_number=phone_number,
            primary_email_address_id=primary_email_address_id,
            email_address_type=email_address_type,
            email_address=email_address,
        )

        return edit_organization
