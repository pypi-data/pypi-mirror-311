from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentInactivityReasonCodesListSummary")


@_attrs_define
class ConstituentInactivityReasonCodesListSummary:
    """ListConstituentInactivityReasonCodes.

    Attributes:
        id (Union[Unset, str]): The ID.
        code (Union[Unset, str]): The reason code.
        description (Union[Unset, str]): The description.
        active (Union[Unset, bool]): Indicates whether active.
    """

    id: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        code = self.code

        description = self.description

        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if code is not UNSET:
            field_dict["code"] = code
        if description is not UNSET:
            field_dict["description"] = description
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        code = d.pop("code", UNSET)

        description = d.pop("description", UNSET)

        active = d.pop("active", UNSET)

        constituent_inactivity_reason_codes_list_summary = cls(
            id=id,
            code=code,
            description=description,
            active=active,
        )

        return constituent_inactivity_reason_codes_list_summary
