import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_organization_validation_countries import NewOrganizationValidationCountries
    from ..models.new_organization_zip_lookup_countries import NewOrganizationZipLookupCountries


T = TypeVar("T", bound="NewOrganization")


@_attrs_define
class NewOrganization:
    """CreateOrganization.

    Example:
        {'name': '', 'web_address': '', 'picture': '', 'picture_thumbnail': '', 'industry': '', 'num_employees': 0,
        'num_subsidiaries': 0, 'parent_corp_id': '', 'address_type': '', 'address_block': '', 'address_city': '',
        'address_state': '', 'address_postcode': '', 'address_country': '', 'address_do_not_mail': False,
        'address_do_not_mail_reason': '', 'phone_type': '', 'phone_number': '', 'email_address_type': '',
        'email_address': '', 'skip_adding_security_groups': False, 'zip_lookup_countries': [{'country_id': '',
        'country_name': ''}], 'omit_from_validation': False, 'dpc': '', 'cart': '', 'lot': '', 'county': '',
        'congressional_district': '', 'last_validation_attempt_date': '', 'validation_message': '',
        'certification_data': 0, 'validation_countries': [{'country_id': '', 'browsable': False}], 'is_primary': False,
        'skip_adding_sites': False, 'info_source': ''}

    Attributes:
        name (str): The name.
        web_address (Union[Unset, str]): The website.
        picture (Union[Unset, str]): The image.
        picture_thumbnail (Union[Unset, str]): The picture thumbnail.
        industry (Union[Unset, str]): The industry. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/industrycode/entries
        num_employees (Union[Unset, int]): The no. of employees.
        num_subsidiaries (Union[Unset, int]): The no. of subsidiary orgs.
        parent_corp_id (Union[Unset, str]): The parent org.
        address_type (Union[Unset, str]): The address type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/addresstypecode/entries
        address_block (Union[Unset, str]): The address.
        address_city (Union[Unset, str]): The city.
        address_state (Union[Unset, str]): The state. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/7fa91401-596c-4f7c-936d-6e41683121d7?parameters=country_id,{address_countryid}.
        address_postcode (Union[Unset, str]): The zip.
        address_country (Union[Unset, str]): The country. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/c9649672-353d-42e8-8c25-4d34bbabfbba.
        address_do_not_mail (Union[Unset, bool]): Indicates whether do not send mail to this address.
        address_do_not_mail_reason (Union[Unset, str]): The reason. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/donotmailreasoncode/entries
        phone_type (Union[Unset, str]): The phone type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/phonetypecode/entries
        phone_number (Union[Unset, str]): The phone number.
        email_address_type (Union[Unset, str]): The email type. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/emailaddresstypecode/entries
        email_address (Union[Unset, str]): The email address.
        skip_adding_security_groups (Union[Unset, bool]): Indicates whether skip adding security groups.
        zip_lookup_countries (Union[Unset, List['NewOrganizationZipLookupCountries']]): Zip lookup countries.
        omit_from_validation (Union[Unset, bool]): Indicates whether omit from validation.
        dpc (Union[Unset, str]): The dpc.
        cart (Union[Unset, str]): The cart.
        lot (Union[Unset, str]): The lot.
        county (Union[Unset, str]): The county. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/countycode/entries
        congressional_district (Union[Unset, str]): The congressional district. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/congressionaldistrictcode/entries
        last_validation_attempt_date (Union[Unset, datetime.datetime]): The last validation attempt date. Uses the
            format YYYY-MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        validation_message (Union[Unset, str]): The validation message.
        certification_data (Union[Unset, int]): The certification data.
        validation_countries (Union[Unset, List['NewOrganizationValidationCountries']]): Validation countries.
        is_primary (Union[Unset, bool]): Indicates whether this is a primary organization.
        skip_adding_sites (Union[Unset, bool]): Indicates whether skip adding sites.
        info_source (Union[Unset, str]): The information source. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/infosourcecode/entries
    """

    name: str
    web_address: Union[Unset, str] = UNSET
    picture: Union[Unset, str] = UNSET
    picture_thumbnail: Union[Unset, str] = UNSET
    industry: Union[Unset, str] = UNSET
    num_employees: Union[Unset, int] = UNSET
    num_subsidiaries: Union[Unset, int] = UNSET
    parent_corp_id: Union[Unset, str] = UNSET
    address_type: Union[Unset, str] = UNSET
    address_block: Union[Unset, str] = UNSET
    address_city: Union[Unset, str] = UNSET
    address_state: Union[Unset, str] = UNSET
    address_postcode: Union[Unset, str] = UNSET
    address_country: Union[Unset, str] = UNSET
    address_do_not_mail: Union[Unset, bool] = UNSET
    address_do_not_mail_reason: Union[Unset, str] = UNSET
    phone_type: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    email_address_type: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    skip_adding_security_groups: Union[Unset, bool] = UNSET
    zip_lookup_countries: Union[Unset, List["NewOrganizationZipLookupCountries"]] = UNSET
    omit_from_validation: Union[Unset, bool] = UNSET
    dpc: Union[Unset, str] = UNSET
    cart: Union[Unset, str] = UNSET
    lot: Union[Unset, str] = UNSET
    county: Union[Unset, str] = UNSET
    congressional_district: Union[Unset, str] = UNSET
    last_validation_attempt_date: Union[Unset, datetime.datetime] = UNSET
    validation_message: Union[Unset, str] = UNSET
    certification_data: Union[Unset, int] = UNSET
    validation_countries: Union[Unset, List["NewOrganizationValidationCountries"]] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    skip_adding_sites: Union[Unset, bool] = UNSET
    info_source: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        web_address = self.web_address

        picture = self.picture

        picture_thumbnail = self.picture_thumbnail

        industry = self.industry

        num_employees = self.num_employees

        num_subsidiaries = self.num_subsidiaries

        parent_corp_id = self.parent_corp_id

        address_type = self.address_type

        address_block = self.address_block

        address_city = self.address_city

        address_state = self.address_state

        address_postcode = self.address_postcode

        address_country = self.address_country

        address_do_not_mail = self.address_do_not_mail

        address_do_not_mail_reason = self.address_do_not_mail_reason

        phone_type = self.phone_type

        phone_number = self.phone_number

        email_address_type = self.email_address_type

        email_address = self.email_address

        skip_adding_security_groups = self.skip_adding_security_groups

        zip_lookup_countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.zip_lookup_countries, Unset):
            zip_lookup_countries = []
            for zip_lookup_countries_item_data in self.zip_lookup_countries:
                zip_lookup_countries_item = zip_lookup_countries_item_data.to_dict()
                zip_lookup_countries.append(zip_lookup_countries_item)

        omit_from_validation = self.omit_from_validation

        dpc = self.dpc

        cart = self.cart

        lot = self.lot

        county = self.county

        congressional_district = self.congressional_district

        last_validation_attempt_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_validation_attempt_date, Unset):
            last_validation_attempt_date = self.last_validation_attempt_date.isoformat()

        validation_message = self.validation_message

        certification_data = self.certification_data

        validation_countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.validation_countries, Unset):
            validation_countries = []
            for validation_countries_item_data in self.validation_countries:
                validation_countries_item = validation_countries_item_data.to_dict()
                validation_countries.append(validation_countries_item)

        is_primary = self.is_primary

        skip_adding_sites = self.skip_adding_sites

        info_source = self.info_source

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if web_address is not UNSET:
            field_dict["web_address"] = web_address
        if picture is not UNSET:
            field_dict["picture"] = picture
        if picture_thumbnail is not UNSET:
            field_dict["picture_thumbnail"] = picture_thumbnail
        if industry is not UNSET:
            field_dict["industry"] = industry
        if num_employees is not UNSET:
            field_dict["num_employees"] = num_employees
        if num_subsidiaries is not UNSET:
            field_dict["num_subsidiaries"] = num_subsidiaries
        if parent_corp_id is not UNSET:
            field_dict["parent_corp_id"] = parent_corp_id
        if address_type is not UNSET:
            field_dict["address_type"] = address_type
        if address_block is not UNSET:
            field_dict["address_block"] = address_block
        if address_city is not UNSET:
            field_dict["address_city"] = address_city
        if address_state is not UNSET:
            field_dict["address_state"] = address_state
        if address_postcode is not UNSET:
            field_dict["address_postcode"] = address_postcode
        if address_country is not UNSET:
            field_dict["address_country"] = address_country
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
        if zip_lookup_countries is not UNSET:
            field_dict["zip_lookup_countries"] = zip_lookup_countries
        if omit_from_validation is not UNSET:
            field_dict["omit_from_validation"] = omit_from_validation
        if dpc is not UNSET:
            field_dict["dpc"] = dpc
        if cart is not UNSET:
            field_dict["cart"] = cart
        if lot is not UNSET:
            field_dict["lot"] = lot
        if county is not UNSET:
            field_dict["county"] = county
        if congressional_district is not UNSET:
            field_dict["congressional_district"] = congressional_district
        if last_validation_attempt_date is not UNSET:
            field_dict["last_validation_attempt_date"] = last_validation_attempt_date
        if validation_message is not UNSET:
            field_dict["validation_message"] = validation_message
        if certification_data is not UNSET:
            field_dict["certification_data"] = certification_data
        if validation_countries is not UNSET:
            field_dict["validation_countries"] = validation_countries
        if is_primary is not UNSET:
            field_dict["is_primary"] = is_primary
        if skip_adding_sites is not UNSET:
            field_dict["skip_adding_sites"] = skip_adding_sites
        if info_source is not UNSET:
            field_dict["info_source"] = info_source

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_organization_validation_countries import NewOrganizationValidationCountries
        from ..models.new_organization_zip_lookup_countries import NewOrganizationZipLookupCountries

        d = src_dict.copy()
        name = d.pop("name")

        web_address = d.pop("web_address", UNSET)

        picture = d.pop("picture", UNSET)

        picture_thumbnail = d.pop("picture_thumbnail", UNSET)

        industry = d.pop("industry", UNSET)

        num_employees = d.pop("num_employees", UNSET)

        num_subsidiaries = d.pop("num_subsidiaries", UNSET)

        parent_corp_id = d.pop("parent_corp_id", UNSET)

        address_type = d.pop("address_type", UNSET)

        address_block = d.pop("address_block", UNSET)

        address_city = d.pop("address_city", UNSET)

        address_state = d.pop("address_state", UNSET)

        address_postcode = d.pop("address_postcode", UNSET)

        address_country = d.pop("address_country", UNSET)

        address_do_not_mail = d.pop("address_do_not_mail", UNSET)

        address_do_not_mail_reason = d.pop("address_do_not_mail_reason", UNSET)

        phone_type = d.pop("phone_type", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        email_address_type = d.pop("email_address_type", UNSET)

        email_address = d.pop("email_address", UNSET)

        skip_adding_security_groups = d.pop("skip_adding_security_groups", UNSET)

        zip_lookup_countries = []
        _zip_lookup_countries = d.pop("zip_lookup_countries", UNSET)
        for zip_lookup_countries_item_data in _zip_lookup_countries or []:
            zip_lookup_countries_item = NewOrganizationZipLookupCountries.from_dict(zip_lookup_countries_item_data)

            zip_lookup_countries.append(zip_lookup_countries_item)

        omit_from_validation = d.pop("omit_from_validation", UNSET)

        dpc = d.pop("dpc", UNSET)

        cart = d.pop("cart", UNSET)

        lot = d.pop("lot", UNSET)

        county = d.pop("county", UNSET)

        congressional_district = d.pop("congressional_district", UNSET)

        _last_validation_attempt_date = d.pop("last_validation_attempt_date", UNSET)
        last_validation_attempt_date: Union[Unset, datetime.datetime]
        if isinstance(_last_validation_attempt_date, Unset):
            last_validation_attempt_date = UNSET
        else:
            last_validation_attempt_date = isoparse(_last_validation_attempt_date)

        validation_message = d.pop("validation_message", UNSET)

        certification_data = d.pop("certification_data", UNSET)

        validation_countries = []
        _validation_countries = d.pop("validation_countries", UNSET)
        for validation_countries_item_data in _validation_countries or []:
            validation_countries_item = NewOrganizationValidationCountries.from_dict(validation_countries_item_data)

            validation_countries.append(validation_countries_item)

        is_primary = d.pop("is_primary", UNSET)

        skip_adding_sites = d.pop("skip_adding_sites", UNSET)

        info_source = d.pop("info_source", UNSET)

        new_organization = cls(
            name=name,
            web_address=web_address,
            picture=picture,
            picture_thumbnail=picture_thumbnail,
            industry=industry,
            num_employees=num_employees,
            num_subsidiaries=num_subsidiaries,
            parent_corp_id=parent_corp_id,
            address_type=address_type,
            address_block=address_block,
            address_city=address_city,
            address_state=address_state,
            address_postcode=address_postcode,
            address_country=address_country,
            address_do_not_mail=address_do_not_mail,
            address_do_not_mail_reason=address_do_not_mail_reason,
            phone_type=phone_type,
            phone_number=phone_number,
            email_address_type=email_address_type,
            email_address=email_address,
            skip_adding_security_groups=skip_adding_security_groups,
            zip_lookup_countries=zip_lookup_countries,
            omit_from_validation=omit_from_validation,
            dpc=dpc,
            cart=cart,
            lot=lot,
            county=county,
            congressional_district=congressional_district,
            last_validation_attempt_date=last_validation_attempt_date,
            validation_message=validation_message,
            certification_data=certification_data,
            validation_countries=validation_countries,
            is_primary=is_primary,
            skip_adding_sites=skip_adding_sites,
            info_source=info_source,
        )

        return new_organization
