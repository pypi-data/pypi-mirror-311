import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.month_day import MonthDay
    from ..models.new_constituent_address_validation_countries import NewConstituentAddressValidationCountries
    from ..models.new_constituent_address_zip_lookup_countries import NewConstituentAddressZipLookupCountries


T = TypeVar("T", bound="NewConstituentAddress")


@_attrs_define
class NewConstituentAddress:
    """CreateConstituentAddress.

    Example:
        {'constituent_id': '4B358EDA-9374-4DED-BE55-7C404BB5E4AB', 'address_type': '', 'address_block': '', 'city': '',
            'state': '', 'postcode': '', 'country': '', 'do_not_mail': False, 'cart': '', 'lot': '', 'dpc': '',
            'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date': {'year': 2024, 'month': 4, 'day': 13},
            'primary': False, 'historical_start_date': '2014-11-04T10:04:00.0000000+00:00', 'recent_move': False,
            'old_address': '', 'spouse_name': '', 'update_matching_spouse_addresses': False, 'omit_from_validation': False,
            'county': '', 'congressional_district': '', 'state_house_district': '', 'state_senate_district': '',
            'local_precinct': '', 'info_source': '', 'region': '', 'last_validation_attempt_date':
            '2019-11-04T10:04:00.0000000+00:00', 'validation_message': '', 'certification_data': 0, 'zip_lookup_countries':
            [{'country_id': '4B358EDA-9374-4DED-BE55-7C404BB5E3AB', 'country_name': 'us'}], 'household': False,
            'household_member': False, 'update_matching_household_addresses': False, 'validation_countries': [{'country_id':
            '', 'browsable': False}], 'do_not_mail_reason': '', 'info_source_comments': '', 'confidential': False,
            'constituent_data_review_rollback_reason': '', 'forced_primary': False, 'can_edit_primary': False,
            'invalid_fields': '', 'origin': 'User'}

    Attributes:
        constituent_id (str): The constituent ID.
        country (str): The country. This simple list can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/c9649672-353d-42e8-8c25-4d34bbabfbba.
        address_type (Union[Unset, str]): The type. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/addresstypecode/entries
        address_block (Union[Unset, str]): The address.
        city (Union[Unset, str]): The city.
        state (Union[Unset, str]): The state. This simple list can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/7fa91401-596c-4f7c-936d-6e41683121d7?parameters=countryid,{countryid}.
        postcode (Union[Unset, str]): The zip.
        do_not_mail (Union[Unset, bool]): Indicates whether do not send mail to this address.
        cart (Union[Unset, str]): The cart.
        lot (Union[Unset, str]): The lot.
        dpc (Union[Unset, str]): The dpc.
        start_date (Union[Unset, MonthDay]): MonthDay Example: {'month': 4, 'day': 13}.
        end_date (Union[Unset, MonthDay]): MonthDay Example: {'month': 4, 'day': 13}.
        primary (Union[Unset, bool]): Indicates whether set as primary address.
        historical_start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        recent_move (Union[Unset, bool]): Indicates whether recently moved/changed from this address?.
        old_address (Union[Unset, str]): The old address. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/bc075172-8103-4ccb-8285-658180e603a1?parameters=constituent_id,{constituent_id}.
        spouse_name (Union[Unset, str]): The spouse name. Read-only in the SOAP API.
        update_matching_spouse_addresses (Union[Unset, bool]): Indicates whether update matching address information for
            spouse.
        omit_from_validation (Union[Unset, bool]): Indicates whether omit this address from validation.
        county (Union[Unset, str]): The county. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/countycode/entries
        congressional_district (Union[Unset, str]): The congressional district. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/congressionaldistrictcode/entries
        state_house_district (Union[Unset, str]): The state house district. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/statehousedistrictcode/entries
        state_senate_district (Union[Unset, str]): The state senate district. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/statesenatedistrictcode/entries
        local_precinct (Union[Unset, str]): The local precinct. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/localprecinctcode/entries
        info_source (Union[Unset, str]): The information source. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/infosourcecode/entries
        region (Union[Unset, str]): The region. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/regioncode/entries
        last_validation_attempt_date (Union[Unset, datetime.datetime]): The last attempt. Uses the format YYYY-MM-
            DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        validation_message (Union[Unset, str]): The validation message.
        certification_data (Union[Unset, int]): The certification data.
        zip_lookup_countries (Union[Unset, List['NewConstituentAddressZipLookupCountries']]): Zip lookup countries.
        household (Union[Unset, bool]): Indicates whether household. Read-only in the SOAP API.
        household_member (Union[Unset, bool]): Indicates whether household member. Read-only in the SOAP API.
        update_matching_household_addresses (Union[Unset, bool]): Indicates whether copy address information to
            household members.
        validation_countries (Union[Unset, List['NewConstituentAddressValidationCountries']]): Validation countries.
        do_not_mail_reason (Union[Unset, str]): The reason. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/donotmailreasoncode/entries
        info_source_comments (Union[Unset, str]): The comments.
        confidential (Union[Unset, bool]): Indicates whether this address is confidential.
        constituent_data_review_rollback_reason (Union[Unset, str]): The reason. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/484441bc-f0e6-4f5f-a6bf-49f02881dd13.
        forced_primary (Union[Unset, bool]): Indicates whether forced primary. Read-only in the SOAP API.
        can_edit_primary (Union[Unset, bool]): Indicates whether can edit primary. Read-only in the SOAP API.
        invalid_fields (Union[Unset, str]): The invalid fields. Read-only in the SOAP API.
        origin (Union[Unset, str]): The origin. Available values are <i>user</i>, <i>web forms</i>
    """

    constituent_id: str
    country: str
    address_type: Union[Unset, str] = UNSET
    address_block: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    postcode: Union[Unset, str] = UNSET
    do_not_mail: Union[Unset, bool] = UNSET
    cart: Union[Unset, str] = UNSET
    lot: Union[Unset, str] = UNSET
    dpc: Union[Unset, str] = UNSET
    start_date: Union[Unset, "MonthDay"] = UNSET
    end_date: Union[Unset, "MonthDay"] = UNSET
    primary: Union[Unset, bool] = UNSET
    historical_start_date: Union[Unset, datetime.datetime] = UNSET
    recent_move: Union[Unset, bool] = UNSET
    old_address: Union[Unset, str] = UNSET
    spouse_name: Union[Unset, str] = UNSET
    update_matching_spouse_addresses: Union[Unset, bool] = UNSET
    omit_from_validation: Union[Unset, bool] = UNSET
    county: Union[Unset, str] = UNSET
    congressional_district: Union[Unset, str] = UNSET
    state_house_district: Union[Unset, str] = UNSET
    state_senate_district: Union[Unset, str] = UNSET
    local_precinct: Union[Unset, str] = UNSET
    info_source: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    last_validation_attempt_date: Union[Unset, datetime.datetime] = UNSET
    validation_message: Union[Unset, str] = UNSET
    certification_data: Union[Unset, int] = UNSET
    zip_lookup_countries: Union[Unset, List["NewConstituentAddressZipLookupCountries"]] = UNSET
    household: Union[Unset, bool] = UNSET
    household_member: Union[Unset, bool] = UNSET
    update_matching_household_addresses: Union[Unset, bool] = UNSET
    validation_countries: Union[Unset, List["NewConstituentAddressValidationCountries"]] = UNSET
    do_not_mail_reason: Union[Unset, str] = UNSET
    info_source_comments: Union[Unset, str] = UNSET
    confidential: Union[Unset, bool] = UNSET
    constituent_data_review_rollback_reason: Union[Unset, str] = UNSET
    forced_primary: Union[Unset, bool] = UNSET
    can_edit_primary: Union[Unset, bool] = UNSET
    invalid_fields: Union[Unset, str] = UNSET
    origin: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        country = self.country

        address_type = self.address_type

        address_block = self.address_block

        city = self.city

        state = self.state

        postcode = self.postcode

        do_not_mail = self.do_not_mail

        cart = self.cart

        lot = self.lot

        dpc = self.dpc

        start_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.to_dict()

        end_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.to_dict()

        primary = self.primary

        historical_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.historical_start_date, Unset):
            historical_start_date = self.historical_start_date.isoformat()

        recent_move = self.recent_move

        old_address = self.old_address

        spouse_name = self.spouse_name

        update_matching_spouse_addresses = self.update_matching_spouse_addresses

        omit_from_validation = self.omit_from_validation

        county = self.county

        congressional_district = self.congressional_district

        state_house_district = self.state_house_district

        state_senate_district = self.state_senate_district

        local_precinct = self.local_precinct

        info_source = self.info_source

        region = self.region

        last_validation_attempt_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_validation_attempt_date, Unset):
            last_validation_attempt_date = self.last_validation_attempt_date.isoformat()

        validation_message = self.validation_message

        certification_data = self.certification_data

        zip_lookup_countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.zip_lookup_countries, Unset):
            zip_lookup_countries = []
            for zip_lookup_countries_item_data in self.zip_lookup_countries:
                zip_lookup_countries_item = zip_lookup_countries_item_data.to_dict()
                zip_lookup_countries.append(zip_lookup_countries_item)

        household = self.household

        household_member = self.household_member

        update_matching_household_addresses = self.update_matching_household_addresses

        validation_countries: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.validation_countries, Unset):
            validation_countries = []
            for validation_countries_item_data in self.validation_countries:
                validation_countries_item = validation_countries_item_data.to_dict()
                validation_countries.append(validation_countries_item)

        do_not_mail_reason = self.do_not_mail_reason

        info_source_comments = self.info_source_comments

        confidential = self.confidential

        constituent_data_review_rollback_reason = self.constituent_data_review_rollback_reason

        forced_primary = self.forced_primary

        can_edit_primary = self.can_edit_primary

        invalid_fields = self.invalid_fields

        origin = self.origin

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "constituent_id": constituent_id,
                "country": country,
            }
        )
        if address_type is not UNSET:
            field_dict["address_type"] = address_type
        if address_block is not UNSET:
            field_dict["address_block"] = address_block
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if postcode is not UNSET:
            field_dict["postcode"] = postcode
        if do_not_mail is not UNSET:
            field_dict["do_not_mail"] = do_not_mail
        if cart is not UNSET:
            field_dict["cart"] = cart
        if lot is not UNSET:
            field_dict["lot"] = lot
        if dpc is not UNSET:
            field_dict["dpc"] = dpc
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if primary is not UNSET:
            field_dict["primary"] = primary
        if historical_start_date is not UNSET:
            field_dict["historical_start_date"] = historical_start_date
        if recent_move is not UNSET:
            field_dict["recent_move"] = recent_move
        if old_address is not UNSET:
            field_dict["old_address"] = old_address
        if spouse_name is not UNSET:
            field_dict["spouse_name"] = spouse_name
        if update_matching_spouse_addresses is not UNSET:
            field_dict["update_matching_spouse_addresses"] = update_matching_spouse_addresses
        if omit_from_validation is not UNSET:
            field_dict["omit_from_validation"] = omit_from_validation
        if county is not UNSET:
            field_dict["county"] = county
        if congressional_district is not UNSET:
            field_dict["congressional_district"] = congressional_district
        if state_house_district is not UNSET:
            field_dict["state_house_district"] = state_house_district
        if state_senate_district is not UNSET:
            field_dict["state_senate_district"] = state_senate_district
        if local_precinct is not UNSET:
            field_dict["local_precinct"] = local_precinct
        if info_source is not UNSET:
            field_dict["info_source"] = info_source
        if region is not UNSET:
            field_dict["region"] = region
        if last_validation_attempt_date is not UNSET:
            field_dict["last_validation_attempt_date"] = last_validation_attempt_date
        if validation_message is not UNSET:
            field_dict["validation_message"] = validation_message
        if certification_data is not UNSET:
            field_dict["certification_data"] = certification_data
        if zip_lookup_countries is not UNSET:
            field_dict["zip_lookup_countries"] = zip_lookup_countries
        if household is not UNSET:
            field_dict["household"] = household
        if household_member is not UNSET:
            field_dict["household_member"] = household_member
        if update_matching_household_addresses is not UNSET:
            field_dict["update_matching_household_addresses"] = update_matching_household_addresses
        if validation_countries is not UNSET:
            field_dict["validation_countries"] = validation_countries
        if do_not_mail_reason is not UNSET:
            field_dict["do_not_mail_reason"] = do_not_mail_reason
        if info_source_comments is not UNSET:
            field_dict["info_source_comments"] = info_source_comments
        if confidential is not UNSET:
            field_dict["confidential"] = confidential
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.month_day import MonthDay
        from ..models.new_constituent_address_validation_countries import (
            NewConstituentAddressValidationCountries,
        )
        from ..models.new_constituent_address_zip_lookup_countries import (
            NewConstituentAddressZipLookupCountries,
        )

        d = src_dict.copy()
        constituent_id = d.pop("constituent_id")

        country = d.pop("country")

        address_type = d.pop("address_type", UNSET)

        address_block = d.pop("address_block", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        postcode = d.pop("postcode", UNSET)

        do_not_mail = d.pop("do_not_mail", UNSET)

        cart = d.pop("cart", UNSET)

        lot = d.pop("lot", UNSET)

        dpc = d.pop("dpc", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, MonthDay]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = MonthDay.from_dict(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, MonthDay]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = MonthDay.from_dict(_end_date)

        primary = d.pop("primary", UNSET)

        _historical_start_date = d.pop("historical_start_date", UNSET)
        historical_start_date: Union[Unset, datetime.datetime]
        if isinstance(_historical_start_date, Unset):
            historical_start_date = UNSET
        else:
            historical_start_date = isoparse(_historical_start_date)

        recent_move = d.pop("recent_move", UNSET)

        old_address = d.pop("old_address", UNSET)

        spouse_name = d.pop("spouse_name", UNSET)

        update_matching_spouse_addresses = d.pop("update_matching_spouse_addresses", UNSET)

        omit_from_validation = d.pop("omit_from_validation", UNSET)

        county = d.pop("county", UNSET)

        congressional_district = d.pop("congressional_district", UNSET)

        state_house_district = d.pop("state_house_district", UNSET)

        state_senate_district = d.pop("state_senate_district", UNSET)

        local_precinct = d.pop("local_precinct", UNSET)

        info_source = d.pop("info_source", UNSET)

        region = d.pop("region", UNSET)

        _last_validation_attempt_date = d.pop("last_validation_attempt_date", UNSET)
        last_validation_attempt_date: Union[Unset, datetime.datetime]
        if isinstance(_last_validation_attempt_date, Unset):
            last_validation_attempt_date = UNSET
        else:
            last_validation_attempt_date = isoparse(_last_validation_attempt_date)

        validation_message = d.pop("validation_message", UNSET)

        certification_data = d.pop("certification_data", UNSET)

        zip_lookup_countries = []
        _zip_lookup_countries = d.pop("zip_lookup_countries", UNSET)
        for zip_lookup_countries_item_data in _zip_lookup_countries or []:
            zip_lookup_countries_item = NewConstituentAddressZipLookupCountries.from_dict(
                zip_lookup_countries_item_data
            )

            zip_lookup_countries.append(zip_lookup_countries_item)

        household = d.pop("household", UNSET)

        household_member = d.pop("household_member", UNSET)

        update_matching_household_addresses = d.pop("update_matching_household_addresses", UNSET)

        validation_countries = []
        _validation_countries = d.pop("validation_countries", UNSET)
        for validation_countries_item_data in _validation_countries or []:
            validation_countries_item = NewConstituentAddressValidationCountries.from_dict(
                validation_countries_item_data
            )

            validation_countries.append(validation_countries_item)

        do_not_mail_reason = d.pop("do_not_mail_reason", UNSET)

        info_source_comments = d.pop("info_source_comments", UNSET)

        confidential = d.pop("confidential", UNSET)

        constituent_data_review_rollback_reason = d.pop("constituent_data_review_rollback_reason", UNSET)

        forced_primary = d.pop("forced_primary", UNSET)

        can_edit_primary = d.pop("can_edit_primary", UNSET)

        invalid_fields = d.pop("invalid_fields", UNSET)

        origin = d.pop("origin", UNSET)

        new_constituent_address = cls(
            constituent_id=constituent_id,
            country=country,
            address_type=address_type,
            address_block=address_block,
            city=city,
            state=state,
            postcode=postcode,
            do_not_mail=do_not_mail,
            cart=cart,
            lot=lot,
            dpc=dpc,
            start_date=start_date,
            end_date=end_date,
            primary=primary,
            historical_start_date=historical_start_date,
            recent_move=recent_move,
            old_address=old_address,
            spouse_name=spouse_name,
            update_matching_spouse_addresses=update_matching_spouse_addresses,
            omit_from_validation=omit_from_validation,
            county=county,
            congressional_district=congressional_district,
            state_house_district=state_house_district,
            state_senate_district=state_senate_district,
            local_precinct=local_precinct,
            info_source=info_source,
            region=region,
            last_validation_attempt_date=last_validation_attempt_date,
            validation_message=validation_message,
            certification_data=certification_data,
            zip_lookup_countries=zip_lookup_countries,
            household=household,
            household_member=household_member,
            update_matching_household_addresses=update_matching_household_addresses,
            validation_countries=validation_countries,
            do_not_mail_reason=do_not_mail_reason,
            info_source_comments=info_source_comments,
            confidential=confidential,
            constituent_data_review_rollback_reason=constituent_data_review_rollback_reason,
            forced_primary=forced_primary,
            can_edit_primary=can_edit_primary,
            invalid_fields=invalid_fields,
            origin=origin,
        )

        return new_constituent_address
