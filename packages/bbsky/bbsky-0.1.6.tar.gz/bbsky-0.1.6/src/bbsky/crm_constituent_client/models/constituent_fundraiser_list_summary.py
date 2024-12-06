from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentFundraiserListSummary")


@_attrs_define
class ConstituentFundraiserListSummary:
    """ListConstituentFundraisers.

    Attributes:
        id (Union[Unset, str]): The ID.
        name (Union[Unset, str]): The name.
        prospect_plans_as_primary_manager (Union[Unset, int]): The prospect plans (as primary manager).
        prospect_plans_relative_to_average (Union[Unset, str]): The prospect plans (relative to average).
        planned_steps_next_7_days (Union[Unset, int]): The planned steps (next 7 days).
        planned_steps_next_30_days (Union[Unset, int]): The planned steps (next 30 days).
        completed_steps_last_7_days (Union[Unset, int]): The completed steps (last 7 days).
        completed_steps_last_30_days (Union[Unset, int]): The completed steps (last 30 days).
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    prospect_plans_as_primary_manager: Union[Unset, int] = UNSET
    prospect_plans_relative_to_average: Union[Unset, str] = UNSET
    planned_steps_next_7_days: Union[Unset, int] = UNSET
    planned_steps_next_30_days: Union[Unset, int] = UNSET
    completed_steps_last_7_days: Union[Unset, int] = UNSET
    completed_steps_last_30_days: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        prospect_plans_as_primary_manager = self.prospect_plans_as_primary_manager

        prospect_plans_relative_to_average = self.prospect_plans_relative_to_average

        planned_steps_next_7_days = self.planned_steps_next_7_days

        planned_steps_next_30_days = self.planned_steps_next_30_days

        completed_steps_last_7_days = self.completed_steps_last_7_days

        completed_steps_last_30_days = self.completed_steps_last_30_days

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if prospect_plans_as_primary_manager is not UNSET:
            field_dict["prospect_plans_as_primary_manager"] = prospect_plans_as_primary_manager
        if prospect_plans_relative_to_average is not UNSET:
            field_dict["prospect_plans_relative_to_average"] = prospect_plans_relative_to_average
        if planned_steps_next_7_days is not UNSET:
            field_dict["planned_steps_next_7_days"] = planned_steps_next_7_days
        if planned_steps_next_30_days is not UNSET:
            field_dict["planned_steps_next_30_days"] = planned_steps_next_30_days
        if completed_steps_last_7_days is not UNSET:
            field_dict["completed_steps_last_7_days"] = completed_steps_last_7_days
        if completed_steps_last_30_days is not UNSET:
            field_dict["completed_steps_last_30_days"] = completed_steps_last_30_days

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        prospect_plans_as_primary_manager = d.pop("prospect_plans_as_primary_manager", UNSET)

        prospect_plans_relative_to_average = d.pop("prospect_plans_relative_to_average", UNSET)

        planned_steps_next_7_days = d.pop("planned_steps_next_7_days", UNSET)

        planned_steps_next_30_days = d.pop("planned_steps_next_30_days", UNSET)

        completed_steps_last_7_days = d.pop("completed_steps_last_7_days", UNSET)

        completed_steps_last_30_days = d.pop("completed_steps_last_30_days", UNSET)

        constituent_fundraiser_list_summary = cls(
            id=id,
            name=name,
            prospect_plans_as_primary_manager=prospect_plans_as_primary_manager,
            prospect_plans_relative_to_average=prospect_plans_relative_to_average,
            planned_steps_next_7_days=planned_steps_next_7_days,
            planned_steps_next_30_days=planned_steps_next_30_days,
            completed_steps_last_7_days=completed_steps_last_7_days,
            completed_steps_last_30_days=completed_steps_last_30_days,
        )

        return constituent_fundraiser_list_summary
