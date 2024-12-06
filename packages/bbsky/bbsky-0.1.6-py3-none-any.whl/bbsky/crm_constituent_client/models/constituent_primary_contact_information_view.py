from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentPrimaryContactInformationView")


@_attrs_define
class ConstituentPrimaryContactInformationView:
    """ViewConstituentPrimaryContactInformation.

    Attributes:
        address_type_label (Union[Unset, str]): The addresstypelabel.
        address_type_id (Union[Unset, str]): The addresstypeid.
        address (Union[Unset, str]): The address.
        city (Union[Unset, str]): The city.
        state_id (Union[Unset, str]): The stateid.
        post_code (Union[Unset, str]): The postcode.
        country_id (Union[Unset, str]): The countryid.
        phone_type_label (Union[Unset, str]): The phonetypelabel.
        phone_type_id (Union[Unset, str]): The phonetypeid.
        phone (Union[Unset, str]): The phone.
        email_type_label (Union[Unset, str]): The emailtypelabel.
        email_type_id (Union[Unset, str]): The emailtypeid.
        email (Union[Unset, str]): The email.
        web_address (Union[Unset, str]): The webaddress.
        do_not_mail (Union[Unset, bool]): Indicates whether donotmail.
        do_not_mail_reason_code_id (Union[Unset, str]): The donotmailreasoncodeid.
        do_not_call (Union[Unset, bool]): Indicates whether donotcall.
        do_not_email (Union[Unset, bool]): Indicates whether donotemail.
        confidential (Union[Unset, bool]): Indicates whether isconfidential.
        do_not_call_reason_code_id (Union[Unset, str]): The donotcallreasoncodeid.
        phone_is_confidential (Union[Unset, bool]): Indicates whether phoneisconfidential.
    """

    address_type_label: Union[Unset, str] = UNSET
    address_type_id: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    state_id: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    country_id: Union[Unset, str] = UNSET
    phone_type_label: Union[Unset, str] = UNSET
    phone_type_id: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    email_type_label: Union[Unset, str] = UNSET
    email_type_id: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    web_address: Union[Unset, str] = UNSET
    do_not_mail: Union[Unset, bool] = UNSET
    do_not_mail_reason_code_id: Union[Unset, str] = UNSET
    do_not_call: Union[Unset, bool] = UNSET
    do_not_email: Union[Unset, bool] = UNSET
    confidential: Union[Unset, bool] = UNSET
    do_not_call_reason_code_id: Union[Unset, str] = UNSET
    phone_is_confidential: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        address_type_label = self.address_type_label

        address_type_id = self.address_type_id

        address = self.address

        city = self.city

        state_id = self.state_id

        post_code = self.post_code

        country_id = self.country_id

        phone_type_label = self.phone_type_label

        phone_type_id = self.phone_type_id

        phone = self.phone

        email_type_label = self.email_type_label

        email_type_id = self.email_type_id

        email = self.email

        web_address = self.web_address

        do_not_mail = self.do_not_mail

        do_not_mail_reason_code_id = self.do_not_mail_reason_code_id

        do_not_call = self.do_not_call

        do_not_email = self.do_not_email

        confidential = self.confidential

        do_not_call_reason_code_id = self.do_not_call_reason_code_id

        phone_is_confidential = self.phone_is_confidential

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if address_type_label is not UNSET:
            field_dict["address_type_label"] = address_type_label
        if address_type_id is not UNSET:
            field_dict["address_type_id"] = address_type_id
        if address is not UNSET:
            field_dict["address"] = address
        if city is not UNSET:
            field_dict["city"] = city
        if state_id is not UNSET:
            field_dict["state_id"] = state_id
        if post_code is not UNSET:
            field_dict["post_code"] = post_code
        if country_id is not UNSET:
            field_dict["country_id"] = country_id
        if phone_type_label is not UNSET:
            field_dict["phone_type_label"] = phone_type_label
        if phone_type_id is not UNSET:
            field_dict["phone_type_id"] = phone_type_id
        if phone is not UNSET:
            field_dict["phone"] = phone
        if email_type_label is not UNSET:
            field_dict["email_type_label"] = email_type_label
        if email_type_id is not UNSET:
            field_dict["email_type_id"] = email_type_id
        if email is not UNSET:
            field_dict["email"] = email
        if web_address is not UNSET:
            field_dict["web_address"] = web_address
        if do_not_mail is not UNSET:
            field_dict["do_not_mail"] = do_not_mail
        if do_not_mail_reason_code_id is not UNSET:
            field_dict["do_not_mail_reason_code_id"] = do_not_mail_reason_code_id
        if do_not_call is not UNSET:
            field_dict["do_not_call"] = do_not_call
        if do_not_email is not UNSET:
            field_dict["do_not_email"] = do_not_email
        if confidential is not UNSET:
            field_dict["confidential"] = confidential
        if do_not_call_reason_code_id is not UNSET:
            field_dict["do_not_call_reason_code_id"] = do_not_call_reason_code_id
        if phone_is_confidential is not UNSET:
            field_dict["phone_is_confidential"] = phone_is_confidential

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address_type_label = d.pop("address_type_label", UNSET)

        address_type_id = d.pop("address_type_id", UNSET)

        address = d.pop("address", UNSET)

        city = d.pop("city", UNSET)

        state_id = d.pop("state_id", UNSET)

        post_code = d.pop("post_code", UNSET)

        country_id = d.pop("country_id", UNSET)

        phone_type_label = d.pop("phone_type_label", UNSET)

        phone_type_id = d.pop("phone_type_id", UNSET)

        phone = d.pop("phone", UNSET)

        email_type_label = d.pop("email_type_label", UNSET)

        email_type_id = d.pop("email_type_id", UNSET)

        email = d.pop("email", UNSET)

        web_address = d.pop("web_address", UNSET)

        do_not_mail = d.pop("do_not_mail", UNSET)

        do_not_mail_reason_code_id = d.pop("do_not_mail_reason_code_id", UNSET)

        do_not_call = d.pop("do_not_call", UNSET)

        do_not_email = d.pop("do_not_email", UNSET)

        confidential = d.pop("confidential", UNSET)

        do_not_call_reason_code_id = d.pop("do_not_call_reason_code_id", UNSET)

        phone_is_confidential = d.pop("phone_is_confidential", UNSET)

        constituent_primary_contact_information_view = cls(
            address_type_label=address_type_label,
            address_type_id=address_type_id,
            address=address,
            city=city,
            state_id=state_id,
            post_code=post_code,
            country_id=country_id,
            phone_type_label=phone_type_label,
            phone_type_id=phone_type_id,
            phone=phone,
            email_type_label=email_type_label,
            email_type_id=email_type_id,
            email=email,
            web_address=web_address,
            do_not_mail=do_not_mail,
            do_not_mail_reason_code_id=do_not_mail_reason_code_id,
            do_not_call=do_not_call,
            do_not_email=do_not_email,
            confidential=confidential,
            do_not_call_reason_code_id=do_not_call_reason_code_id,
            phone_is_confidential=phone_is_confidential,
        )

        return constituent_primary_contact_information_view
