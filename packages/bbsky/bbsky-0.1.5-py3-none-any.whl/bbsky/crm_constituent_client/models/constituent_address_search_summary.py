from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAddressSearchSummary")


@_attrs_define
class ConstituentAddressSearchSummary:
    """SearchConstituentAddresses.

    Attributes:
        id (Union[Unset, str]): The ID.
        name (Union[Unset, str]): The name.
        address (Union[Unset, str]): The address.
        city (Union[Unset, str]): The city.
        state (Union[Unset, str]): The state.
        post_code (Union[Unset, str]): The post code.
        full_address (Union[Unset, str]): The full address.
        key_name (Union[Unset, str]): The last name.
        first_name (Union[Unset, str]): The first name.
        primary (Union[Unset, bool]): Indicates whether is primary address.
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    full_address: Union[Unset, str] = UNSET
    key_name: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        address = self.address

        city = self.city

        state = self.state

        post_code = self.post_code

        full_address = self.full_address

        key_name = self.key_name

        first_name = self.first_name

        primary = self.primary

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if address is not UNSET:
            field_dict["address"] = address
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if post_code is not UNSET:
            field_dict["post_code"] = post_code
        if full_address is not UNSET:
            field_dict["full_address"] = full_address
        if key_name is not UNSET:
            field_dict["key_name"] = key_name
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if primary is not UNSET:
            field_dict["primary"] = primary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        address = d.pop("address", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        post_code = d.pop("post_code", UNSET)

        full_address = d.pop("full_address", UNSET)

        key_name = d.pop("key_name", UNSET)

        first_name = d.pop("first_name", UNSET)

        primary = d.pop("primary", UNSET)

        constituent_address_search_summary = cls(
            id=id,
            name=name,
            address=address,
            city=city,
            state=state,
            post_code=post_code,
            full_address=full_address,
            key_name=key_name,
            first_name=first_name,
            primary=primary,
        )

        return constituent_address_search_summary
