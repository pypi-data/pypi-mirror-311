from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentSearchSummary")


@_attrs_define
class ConstituentSearchSummary:
    """SearchConstituents.

    Attributes:
        id (Union[Unset, str]): The ID.
        lookup_id (Union[Unset, str]): The lookup ID.
        sort_constituent_name (Union[Unset, str]): The name.
        address (Union[Unset, str]): The address.
        city (Union[Unset, str]): The city.
        state (Union[Unset, str]): The state.
        post_code (Union[Unset, str]): The zip/postal code.
        country_id (Union[Unset, str]): The country.
        gives_anonymously (Union[Unset, bool]): Indicates whether gives anonymously.
        classof (Union[Unset, int]): The primary class year.
        organization (Union[Unset, bool]): Indicates whether is organization.
        name (Union[Unset, str]): The name.
        email_address (Union[Unset, str]): The email address.
        group (Union[Unset, bool]): Indicates whether is group.
        household (Union[Unset, bool]): Indicates whether is household.
        middle_name (Union[Unset, str]): The middle name.
        suffixcodeid (Union[Unset, str]): The suffix.
        phone (Union[Unset, str]): The phone.
        prospectmanager (Union[Unset, str]): The prospect manager.
    """

    id: Union[Unset, str] = UNSET
    lookup_id: Union[Unset, str] = UNSET
    sort_constituent_name: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    country_id: Union[Unset, str] = UNSET
    gives_anonymously: Union[Unset, bool] = UNSET
    classof: Union[Unset, int] = UNSET
    organization: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    group: Union[Unset, bool] = UNSET
    household: Union[Unset, bool] = UNSET
    middle_name: Union[Unset, str] = UNSET
    suffixcodeid: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    prospectmanager: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        lookup_id = self.lookup_id

        sort_constituent_name = self.sort_constituent_name

        address = self.address

        city = self.city

        state = self.state

        post_code = self.post_code

        country_id = self.country_id

        gives_anonymously = self.gives_anonymously

        classof = self.classof

        organization = self.organization

        name = self.name

        email_address = self.email_address

        group = self.group

        household = self.household

        middle_name = self.middle_name

        suffixcodeid = self.suffixcodeid

        phone = self.phone

        prospectmanager = self.prospectmanager

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if lookup_id is not UNSET:
            field_dict["lookup_id"] = lookup_id
        if sort_constituent_name is not UNSET:
            field_dict["sort_constituent_name"] = sort_constituent_name
        if address is not UNSET:
            field_dict["address"] = address
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if post_code is not UNSET:
            field_dict["post_code"] = post_code
        if country_id is not UNSET:
            field_dict["country_id"] = country_id
        if gives_anonymously is not UNSET:
            field_dict["gives_anonymously"] = gives_anonymously
        if classof is not UNSET:
            field_dict["classof"] = classof
        if organization is not UNSET:
            field_dict["organization"] = organization
        if name is not UNSET:
            field_dict["name"] = name
        if email_address is not UNSET:
            field_dict["email_address"] = email_address
        if group is not UNSET:
            field_dict["group"] = group
        if household is not UNSET:
            field_dict["household"] = household
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if suffixcodeid is not UNSET:
            field_dict["suffixcodeid"] = suffixcodeid
        if phone is not UNSET:
            field_dict["phone"] = phone
        if prospectmanager is not UNSET:
            field_dict["prospectmanager"] = prospectmanager

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        lookup_id = d.pop("lookup_id", UNSET)

        sort_constituent_name = d.pop("sort_constituent_name", UNSET)

        address = d.pop("address", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        post_code = d.pop("post_code", UNSET)

        country_id = d.pop("country_id", UNSET)

        gives_anonymously = d.pop("gives_anonymously", UNSET)

        classof = d.pop("classof", UNSET)

        organization = d.pop("organization", UNSET)

        name = d.pop("name", UNSET)

        email_address = d.pop("email_address", UNSET)

        group = d.pop("group", UNSET)

        household = d.pop("household", UNSET)

        middle_name = d.pop("middle_name", UNSET)

        suffixcodeid = d.pop("suffixcodeid", UNSET)

        phone = d.pop("phone", UNSET)

        prospectmanager = d.pop("prospectmanager", UNSET)

        constituent_search_summary = cls(
            id=id,
            lookup_id=lookup_id,
            sort_constituent_name=sort_constituent_name,
            address=address,
            city=city,
            state=state,
            post_code=post_code,
            country_id=country_id,
            gives_anonymously=gives_anonymously,
            classof=classof,
            organization=organization,
            name=name,
            email_address=email_address,
            group=group,
            household=household,
            middle_name=middle_name,
            suffixcodeid=suffixcodeid,
            phone=phone,
            prospectmanager=prospectmanager,
        )

        return constituent_search_summary
