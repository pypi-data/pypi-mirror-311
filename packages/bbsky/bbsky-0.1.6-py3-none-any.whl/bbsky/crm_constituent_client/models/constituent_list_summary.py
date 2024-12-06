import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentListSummary")


@_attrs_define
class ConstituentListSummary:
    """ListPatronData.

    Attributes:
        id (Union[Unset, str]): The ID.
        sales_order_id (Union[Unset, str]): The salesorderid.
        refund_date (Union[Unset, datetime.datetime]): The refund date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        refund_total (Union[Unset, float]): The refund amount.
        refund_items (Union[Unset, str]): The refund items.
        transaction_date (Union[Unset, datetime.datetime]): The order date. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        order_number (Union[Unset, str]): The order number.
        order_total (Union[Unset, float]): The order total.
    """

    id: Union[Unset, str] = UNSET
    sales_order_id: Union[Unset, str] = UNSET
    refund_date: Union[Unset, datetime.datetime] = UNSET
    refund_total: Union[Unset, float] = UNSET
    refund_items: Union[Unset, str] = UNSET
    transaction_date: Union[Unset, datetime.datetime] = UNSET
    order_number: Union[Unset, str] = UNSET
    order_total: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        sales_order_id = self.sales_order_id

        refund_date: Union[Unset, str] = UNSET
        if not isinstance(self.refund_date, Unset):
            refund_date = self.refund_date.isoformat()

        refund_total = self.refund_total

        refund_items = self.refund_items

        transaction_date: Union[Unset, str] = UNSET
        if not isinstance(self.transaction_date, Unset):
            transaction_date = self.transaction_date.isoformat()

        order_number = self.order_number

        order_total = self.order_total

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if sales_order_id is not UNSET:
            field_dict["sales_order_id"] = sales_order_id
        if refund_date is not UNSET:
            field_dict["refund_date"] = refund_date
        if refund_total is not UNSET:
            field_dict["refund_total"] = refund_total
        if refund_items is not UNSET:
            field_dict["refund_items"] = refund_items
        if transaction_date is not UNSET:
            field_dict["transaction_date"] = transaction_date
        if order_number is not UNSET:
            field_dict["order_number"] = order_number
        if order_total is not UNSET:
            field_dict["order_total"] = order_total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        sales_order_id = d.pop("sales_order_id", UNSET)

        _refund_date = d.pop("refund_date", UNSET)
        refund_date: Union[Unset, datetime.datetime]
        if isinstance(_refund_date, Unset):
            refund_date = UNSET
        else:
            refund_date = isoparse(_refund_date)

        refund_total = d.pop("refund_total", UNSET)

        refund_items = d.pop("refund_items", UNSET)

        _transaction_date = d.pop("transaction_date", UNSET)
        transaction_date: Union[Unset, datetime.datetime]
        if isinstance(_transaction_date, Unset):
            transaction_date = UNSET
        else:
            transaction_date = isoparse(_transaction_date)

        order_number = d.pop("order_number", UNSET)

        order_total = d.pop("order_total", UNSET)

        constituent_list_summary = cls(
            id=id,
            sales_order_id=sales_order_id,
            refund_date=refund_date,
            refund_total=refund_total,
            refund_items=refund_items,
            transaction_date=transaction_date,
            order_number=order_number,
            order_total=order_total,
        )

        return constituent_list_summary
