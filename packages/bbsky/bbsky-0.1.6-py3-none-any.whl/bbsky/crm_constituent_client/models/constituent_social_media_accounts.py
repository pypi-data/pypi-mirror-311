from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentSocialMediaAccounts")


@_attrs_define
class ConstituentSocialMediaAccounts:
    """ConstituentSocialMediaAccounts.

    Attributes:
        id (Union[Unset, str]): id
        social_media_service_id (Union[Unset, str]): socialmediaserviceid
        social_media_service_name (Union[Unset, str]): socialmediaservicename
        social_media_service_icon (Union[Unset, str]): socialmediaserviceicon
        user_id (Union[Unset, str]): userid
        url (Union[Unset, str]): url
        social_media_account_type_code_id (Union[Unset, str]): socialmediaaccounttypecodeid
        social_media_account_type (Union[Unset, str]): socialmediaaccounttype
        info_source_code_id (Union[Unset, str]): infosourcecodeid
        info_source (Union[Unset, str]): infosource
        do_not_contact (Union[Unset, bool]): donotcontact
        sequence (Union[Unset, int]): sequence
    """

    id: Union[Unset, str] = UNSET
    social_media_service_id: Union[Unset, str] = UNSET
    social_media_service_name: Union[Unset, str] = UNSET
    social_media_service_icon: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    social_media_account_type_code_id: Union[Unset, str] = UNSET
    social_media_account_type: Union[Unset, str] = UNSET
    info_source_code_id: Union[Unset, str] = UNSET
    info_source: Union[Unset, str] = UNSET
    do_not_contact: Union[Unset, bool] = UNSET
    sequence: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        social_media_service_id = self.social_media_service_id

        social_media_service_name = self.social_media_service_name

        social_media_service_icon = self.social_media_service_icon

        user_id = self.user_id

        url = self.url

        social_media_account_type_code_id = self.social_media_account_type_code_id

        social_media_account_type = self.social_media_account_type

        info_source_code_id = self.info_source_code_id

        info_source = self.info_source

        do_not_contact = self.do_not_contact

        sequence = self.sequence

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if social_media_service_id is not UNSET:
            field_dict["social_media_service_id"] = social_media_service_id
        if social_media_service_name is not UNSET:
            field_dict["social_media_service_name"] = social_media_service_name
        if social_media_service_icon is not UNSET:
            field_dict["social_media_service_icon"] = social_media_service_icon
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if url is not UNSET:
            field_dict["url"] = url
        if social_media_account_type_code_id is not UNSET:
            field_dict["social_media_account_type_code_id"] = social_media_account_type_code_id
        if social_media_account_type is not UNSET:
            field_dict["social_media_account_type"] = social_media_account_type
        if info_source_code_id is not UNSET:
            field_dict["info_source_code_id"] = info_source_code_id
        if info_source is not UNSET:
            field_dict["info_source"] = info_source
        if do_not_contact is not UNSET:
            field_dict["do_not_contact"] = do_not_contact
        if sequence is not UNSET:
            field_dict["sequence"] = sequence

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        social_media_service_id = d.pop("social_media_service_id", UNSET)

        social_media_service_name = d.pop("social_media_service_name", UNSET)

        social_media_service_icon = d.pop("social_media_service_icon", UNSET)

        user_id = d.pop("user_id", UNSET)

        url = d.pop("url", UNSET)

        social_media_account_type_code_id = d.pop("social_media_account_type_code_id", UNSET)

        social_media_account_type = d.pop("social_media_account_type", UNSET)

        info_source_code_id = d.pop("info_source_code_id", UNSET)

        info_source = d.pop("info_source", UNSET)

        do_not_contact = d.pop("do_not_contact", UNSET)

        sequence = d.pop("sequence", UNSET)

        constituent_social_media_accounts = cls(
            id=id,
            social_media_service_id=social_media_service_id,
            social_media_service_name=social_media_service_name,
            social_media_service_icon=social_media_service_icon,
            user_id=user_id,
            url=url,
            social_media_account_type_code_id=social_media_account_type_code_id,
            social_media_account_type=social_media_account_type,
            info_source_code_id=info_source_code_id,
            info_source=info_source,
            do_not_contact=do_not_contact,
            sequence=sequence,
        )

        constituent_social_media_accounts.additional_properties = d
        return constituent_social_media_accounts

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
