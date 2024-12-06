from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="IndividualRevenueSummaryView")


@_attrs_define
class IndividualRevenueSummaryView:
    """ViewIndividualRevenueSummary.

    Attributes:
        household_id (Union[Unset, str]): The household ID.
        total_giving (Union[Unset, float]): The total revenue.
        total_house_hold_and_member_giving (Union[Unset, float]): The total household revenue.
        membership_revenue (Union[Unset, float]): The membership revenue.
        event_revenue (Union[Unset, float]): The event revenue.
        is_registrant (Union[Unset, bool]): Indicates whether is registrant.
        is_volunteer (Union[Unset, bool]): Indicates whether is volunteer.
        revenue_id (Union[Unset, str]): The revenue ID.
        ticket_revenue (Union[Unset, float]): The ticket revenue.
        facility_revenue (Union[Unset, float]): The facility revenue.
        merchandise_revenue (Union[Unset, float]): The merchandise revenue.
        currency_id (Union[Unset, str]): The currency ID.
    """

    household_id: Union[Unset, str] = UNSET
    total_giving: Union[Unset, float] = UNSET
    total_house_hold_and_member_giving: Union[Unset, float] = UNSET
    membership_revenue: Union[Unset, float] = UNSET
    event_revenue: Union[Unset, float] = UNSET
    is_registrant: Union[Unset, bool] = UNSET
    is_volunteer: Union[Unset, bool] = UNSET
    revenue_id: Union[Unset, str] = UNSET
    ticket_revenue: Union[Unset, float] = UNSET
    facility_revenue: Union[Unset, float] = UNSET
    merchandise_revenue: Union[Unset, float] = UNSET
    currency_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        household_id = self.household_id

        total_giving = self.total_giving

        total_house_hold_and_member_giving = self.total_house_hold_and_member_giving

        membership_revenue = self.membership_revenue

        event_revenue = self.event_revenue

        is_registrant = self.is_registrant

        is_volunteer = self.is_volunteer

        revenue_id = self.revenue_id

        ticket_revenue = self.ticket_revenue

        facility_revenue = self.facility_revenue

        merchandise_revenue = self.merchandise_revenue

        currency_id = self.currency_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if household_id is not UNSET:
            field_dict["household_id"] = household_id
        if total_giving is not UNSET:
            field_dict["total_giving"] = total_giving
        if total_house_hold_and_member_giving is not UNSET:
            field_dict["total_house_hold_and_member_giving"] = total_house_hold_and_member_giving
        if membership_revenue is not UNSET:
            field_dict["membership_revenue"] = membership_revenue
        if event_revenue is not UNSET:
            field_dict["event_revenue"] = event_revenue
        if is_registrant is not UNSET:
            field_dict["is_registrant"] = is_registrant
        if is_volunteer is not UNSET:
            field_dict["is_volunteer"] = is_volunteer
        if revenue_id is not UNSET:
            field_dict["revenue_id"] = revenue_id
        if ticket_revenue is not UNSET:
            field_dict["ticket_revenue"] = ticket_revenue
        if facility_revenue is not UNSET:
            field_dict["facility_revenue"] = facility_revenue
        if merchandise_revenue is not UNSET:
            field_dict["merchandise_revenue"] = merchandise_revenue
        if currency_id is not UNSET:
            field_dict["currency_id"] = currency_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        household_id = d.pop("household_id", UNSET)

        total_giving = d.pop("total_giving", UNSET)

        total_house_hold_and_member_giving = d.pop("total_house_hold_and_member_giving", UNSET)

        membership_revenue = d.pop("membership_revenue", UNSET)

        event_revenue = d.pop("event_revenue", UNSET)

        is_registrant = d.pop("is_registrant", UNSET)

        is_volunteer = d.pop("is_volunteer", UNSET)

        revenue_id = d.pop("revenue_id", UNSET)

        ticket_revenue = d.pop("ticket_revenue", UNSET)

        facility_revenue = d.pop("facility_revenue", UNSET)

        merchandise_revenue = d.pop("merchandise_revenue", UNSET)

        currency_id = d.pop("currency_id", UNSET)

        individual_revenue_summary_view = cls(
            household_id=household_id,
            total_giving=total_giving,
            total_house_hold_and_member_giving=total_house_hold_and_member_giving,
            membership_revenue=membership_revenue,
            event_revenue=event_revenue,
            is_registrant=is_registrant,
            is_volunteer=is_volunteer,
            revenue_id=revenue_id,
            ticket_revenue=ticket_revenue,
            facility_revenue=facility_revenue,
            merchandise_revenue=merchandise_revenue,
            currency_id=currency_id,
        )

        return individual_revenue_summary_view
