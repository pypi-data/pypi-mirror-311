from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentProfilePictureView")


@_attrs_define
class ConstituentProfilePictureView:
    """ViewConstituentProfilePicture.

    Attributes:
        picture (Union[Unset, str]): The picture.
        title (Union[Unset, str]): The title.
        first_name (Union[Unset, str]): The first name.
        middle_name (Union[Unset, str]): The middle name.
        key_name (Union[Unset, str]): The last name.
        suffix (Union[Unset, str]): The suffix.
        nick_name (Union[Unset, str]): The nickname.
        maiden_name (Union[Unset, str]): The maiden.
        gives_anonymously (Union[Unset, bool]): Indicates whether gives anonymously.
    """

    picture: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    key_name: Union[Unset, str] = UNSET
    suffix: Union[Unset, str] = UNSET
    nick_name: Union[Unset, str] = UNSET
    maiden_name: Union[Unset, str] = UNSET
    gives_anonymously: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        picture = self.picture

        title = self.title

        first_name = self.first_name

        middle_name = self.middle_name

        key_name = self.key_name

        suffix = self.suffix

        nick_name = self.nick_name

        maiden_name = self.maiden_name

        gives_anonymously = self.gives_anonymously

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if picture is not UNSET:
            field_dict["picture"] = picture
        if title is not UNSET:
            field_dict["title"] = title
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if key_name is not UNSET:
            field_dict["key_name"] = key_name
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if nick_name is not UNSET:
            field_dict["nick_name"] = nick_name
        if maiden_name is not UNSET:
            field_dict["maiden_name"] = maiden_name
        if gives_anonymously is not UNSET:
            field_dict["gives_anonymously"] = gives_anonymously

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        picture = d.pop("picture", UNSET)

        title = d.pop("title", UNSET)

        first_name = d.pop("first_name", UNSET)

        middle_name = d.pop("middle_name", UNSET)

        key_name = d.pop("key_name", UNSET)

        suffix = d.pop("suffix", UNSET)

        nick_name = d.pop("nick_name", UNSET)

        maiden_name = d.pop("maiden_name", UNSET)

        gives_anonymously = d.pop("gives_anonymously", UNSET)

        constituent_profile_picture_view = cls(
            picture=picture,
            title=title,
            first_name=first_name,
            middle_name=middle_name,
            key_name=key_name,
            suffix=suffix,
            nick_name=nick_name,
            maiden_name=maiden_name,
            gives_anonymously=gives_anonymously,
        )

        return constituent_profile_picture_view
