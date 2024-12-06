from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constituent_revenue_constituentrevenuerecent import (
        ConstituentRevenueConstituentrevenuerecent,
    )


T = TypeVar("T", bound="IndividualRecentRevenueView")


@_attrs_define
class IndividualRecentRevenueView:
    """ViewIndividualRecentRevenue.

    Attributes:
        constituentrevenuerecent (Union[Unset, List['ConstituentRevenueConstituentrevenuerecent']]):
            Constituentrevenuerecent.
    """

    constituentrevenuerecent: Union[Unset, List["ConstituentRevenueConstituentrevenuerecent"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituentrevenuerecent: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.constituentrevenuerecent, Unset):
            constituentrevenuerecent = []
            for constituentrevenuerecent_item_data in self.constituentrevenuerecent:
                constituentrevenuerecent_item = constituentrevenuerecent_item_data.to_dict()
                constituentrevenuerecent.append(constituentrevenuerecent_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if constituentrevenuerecent is not UNSET:
            field_dict["constituentrevenuerecent"] = constituentrevenuerecent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constituent_revenue_constituentrevenuerecent import (
            ConstituentRevenueConstituentrevenuerecent,
        )

        d = src_dict.copy()
        constituentrevenuerecent = []
        _constituentrevenuerecent = d.pop("constituentrevenuerecent", UNSET)
        for constituentrevenuerecent_item_data in _constituentrevenuerecent or []:
            constituentrevenuerecent_item = ConstituentRevenueConstituentrevenuerecent.from_dict(
                constituentrevenuerecent_item_data
            )

            constituentrevenuerecent.append(constituentrevenuerecent_item)

        individual_recent_revenue_view = cls(
            constituentrevenuerecent=constituentrevenuerecent,
        )

        return individual_recent_revenue_view
