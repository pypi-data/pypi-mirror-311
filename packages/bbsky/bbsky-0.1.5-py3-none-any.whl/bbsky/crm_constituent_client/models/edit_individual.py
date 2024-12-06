from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuzzy_date import FuzzyDate


T = TypeVar("T", bound="EditIndividual")


@_attrs_define
class EditIndividual:
    """EditIndividual.

    Example:
        {'last_name': 'Adamson', 'first_name': 'Eric', 'middle_name': 'Arnold', 'maiden_name': '', 'nickname': '',
            'title': 'Mr.', 'suffix': '', 'gender': 'Male', 'birth_date': {'year': 1990, 'month': 8, 'day': 16}, 'age': 29,
            'gives_anonymously': False, 'picture': '', 'picture_thumbnail': '', 'picture_changed': False, 'web_address': '',
            'marital_status': '', 'title_2': '', 'suffix_2': '', 'deceased': False}

    Attributes:
        last_name (Union[Unset, str]): The last name.
        first_name (Union[Unset, str]): The first name.
        middle_name (Union[Unset, str]): The middle name.
        maiden_name (Union[Unset, str]): The maiden name.
        nickname (Union[Unset, str]): The nickname.
        title (Union[Unset, str]): The title. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/titlecode/entries
        suffix (Union[Unset, str]): The suffix. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/suffixcode/entries
        gender (Union[Unset, str]): The gender. Available values are <i>unknown</i>, <i>male</i>, <i>female</i>,
            <i>other</i>
        gender_code (Union[Unset, str]): The gender. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/gendercode/entries
        birth_date (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        age (Union[Unset, int]): The age. Read-only in the SOAP API.
        gives_anonymously (Union[Unset, bool]): Indicates whether gives anonymously.
        picture (Union[Unset, str]): The image.
        picture_thumbnail (Union[Unset, str]): The image.
        picture_changed (Union[Unset, bool]): Indicates whether picture changed.
        web_address (Union[Unset, str]): The website.
        marital_status (Union[Unset, str]): The marital status. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/maritalstatuscode/entries
        title_2 (Union[Unset, str]): The title 2. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/titlecode/entries
        suffix_2 (Union[Unset, str]): The suffix 2. This code table can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/codetables/suffixcode/entries
        deceased (Union[Unset, bool]): Indicates whether is deceased. Read-only in the SOAP API.
    """

    last_name: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    maiden_name: Union[Unset, str] = UNSET
    nickname: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    suffix: Union[Unset, str] = UNSET
    gender: Union[Unset, str] = UNSET
    gender_code: Union[Unset, str] = UNSET
    birth_date: Union[Unset, "FuzzyDate"] = UNSET
    age: Union[Unset, int] = UNSET
    gives_anonymously: Union[Unset, bool] = UNSET
    picture: Union[Unset, str] = UNSET
    picture_thumbnail: Union[Unset, str] = UNSET
    picture_changed: Union[Unset, bool] = UNSET
    web_address: Union[Unset, str] = UNSET
    marital_status: Union[Unset, str] = UNSET
    title_2: Union[Unset, str] = UNSET
    suffix_2: Union[Unset, str] = UNSET
    deceased: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        last_name = self.last_name

        first_name = self.first_name

        middle_name = self.middle_name

        maiden_name = self.maiden_name

        nickname = self.nickname

        title = self.title

        suffix = self.suffix

        gender = self.gender

        gender_code = self.gender_code

        birth_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.birth_date, Unset):
            birth_date = self.birth_date.to_dict()

        age = self.age

        gives_anonymously = self.gives_anonymously

        picture = self.picture

        picture_thumbnail = self.picture_thumbnail

        picture_changed = self.picture_changed

        web_address = self.web_address

        marital_status = self.marital_status

        title_2 = self.title_2

        suffix_2 = self.suffix_2

        deceased = self.deceased

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if maiden_name is not UNSET:
            field_dict["maiden_name"] = maiden_name
        if nickname is not UNSET:
            field_dict["nickname"] = nickname
        if title is not UNSET:
            field_dict["title"] = title
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if gender is not UNSET:
            field_dict["gender"] = gender
        if gender_code is not UNSET:
            field_dict["gender_code"] = gender_code
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if age is not UNSET:
            field_dict["age"] = age
        if gives_anonymously is not UNSET:
            field_dict["gives_anonymously"] = gives_anonymously
        if picture is not UNSET:
            field_dict["picture"] = picture
        if picture_thumbnail is not UNSET:
            field_dict["picture_thumbnail"] = picture_thumbnail
        if picture_changed is not UNSET:
            field_dict["picture_changed"] = picture_changed
        if web_address is not UNSET:
            field_dict["web_address"] = web_address
        if marital_status is not UNSET:
            field_dict["marital_status"] = marital_status
        if title_2 is not UNSET:
            field_dict["title_2"] = title_2
        if suffix_2 is not UNSET:
            field_dict["suffix_2"] = suffix_2
        if deceased is not UNSET:
            field_dict["deceased"] = deceased

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fuzzy_date import FuzzyDate

        d = src_dict.copy()
        last_name = d.pop("last_name", UNSET)

        first_name = d.pop("first_name", UNSET)

        middle_name = d.pop("middle_name", UNSET)

        maiden_name = d.pop("maiden_name", UNSET)

        nickname = d.pop("nickname", UNSET)

        title = d.pop("title", UNSET)

        suffix = d.pop("suffix", UNSET)

        gender = d.pop("gender", UNSET)

        gender_code = d.pop("gender_code", UNSET)

        _birth_date = d.pop("birth_date", UNSET)
        birth_date: Union[Unset, FuzzyDate]
        if isinstance(_birth_date, Unset):
            birth_date = UNSET
        else:
            birth_date = FuzzyDate.from_dict(_birth_date)

        age = d.pop("age", UNSET)

        gives_anonymously = d.pop("gives_anonymously", UNSET)

        picture = d.pop("picture", UNSET)

        picture_thumbnail = d.pop("picture_thumbnail", UNSET)

        picture_changed = d.pop("picture_changed", UNSET)

        web_address = d.pop("web_address", UNSET)

        marital_status = d.pop("marital_status", UNSET)

        title_2 = d.pop("title_2", UNSET)

        suffix_2 = d.pop("suffix_2", UNSET)

        deceased = d.pop("deceased", UNSET)

        edit_individual = cls(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            maiden_name=maiden_name,
            nickname=nickname,
            title=title,
            suffix=suffix,
            gender=gender,
            gender_code=gender_code,
            birth_date=birth_date,
            age=age,
            gives_anonymously=gives_anonymously,
            picture=picture,
            picture_thumbnail=picture_thumbnail,
            picture_changed=picture_changed,
            web_address=web_address,
            marital_status=marital_status,
            title_2=title_2,
            suffix_2=suffix_2,
            deceased=deceased,
        )

        return edit_individual
