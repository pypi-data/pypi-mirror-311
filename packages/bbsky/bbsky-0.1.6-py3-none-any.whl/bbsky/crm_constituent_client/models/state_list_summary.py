from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="StateListSummary")


@_attrs_define
class StateListSummary:
    """ListStates.

    Attributes:
        id (Union[Unset, str]): The ID.
        state (Union[Unset, str]): The state.
        abbreviation (Union[Unset, str]): The abbreviation.
        active (Union[Unset, bool]): Indicates whether active.
    """

    id: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    abbreviation: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        state = self.state

        abbreviation = self.abbreviation

        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if state is not UNSET:
            field_dict["state"] = state
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        state = d.pop("state", UNSET)

        abbreviation = d.pop("abbreviation", UNSET)

        active = d.pop("active", UNSET)

        state_list_summary = cls(
            id=id,
            state=state,
            abbreviation=abbreviation,
            active=active,
        )

        return state_list_summary
