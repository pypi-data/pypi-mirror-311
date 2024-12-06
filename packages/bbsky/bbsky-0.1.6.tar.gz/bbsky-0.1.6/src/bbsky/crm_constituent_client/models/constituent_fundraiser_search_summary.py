from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentFundraiserSearchSummary")


@_attrs_define
class ConstituentFundraiserSearchSummary:
    """SearchConstituentFundraisers.

    Attributes:
        id (Union[Unset, str]): The ID.
        sort_constituent_name (Union[Unset, str]): The name.
        city (Union[Unset, str]): The city.
        state (Union[Unset, str]): The state.
        post_code (Union[Unset, str]): The zip/postal code.
        phone (Union[Unset, str]): The phone.
        constituent_type (Union[Unset, str]): The constituent type.
        site (Union[Unset, str]): The site.
        name (Union[Unset, str]): The name.
    """

    id: Union[Unset, str] = UNSET
    sort_constituent_name: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    constituent_type: Union[Unset, str] = UNSET
    site: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        sort_constituent_name = self.sort_constituent_name

        city = self.city

        state = self.state

        post_code = self.post_code

        phone = self.phone

        constituent_type = self.constituent_type

        site = self.site

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if sort_constituent_name is not UNSET:
            field_dict["sort_constituent_name"] = sort_constituent_name
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if post_code is not UNSET:
            field_dict["post_code"] = post_code
        if phone is not UNSET:
            field_dict["phone"] = phone
        if constituent_type is not UNSET:
            field_dict["constituent_type"] = constituent_type
        if site is not UNSET:
            field_dict["site"] = site
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        sort_constituent_name = d.pop("sort_constituent_name", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        post_code = d.pop("post_code", UNSET)

        phone = d.pop("phone", UNSET)

        constituent_type = d.pop("constituent_type", UNSET)

        site = d.pop("site", UNSET)

        name = d.pop("name", UNSET)

        constituent_fundraiser_search_summary = cls(
            id=id,
            sort_constituent_name=sort_constituent_name,
            city=city,
            state=state,
            post_code=post_code,
            phone=phone,
            constituent_type=constituent_type,
            site=site,
            name=name,
        )

        return constituent_fundraiser_search_summary
