from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_tribute_splits import NewTributeSplits


T = TypeVar("T", bound="NewTribute")


@_attrs_define
class NewTribute:
    """CreateTribute.

    Example:
        {'revenue_id': '', 'tribute_id': '', 'amount': 0, 'designation_id': '', 'splits': [{'id': '', 'designation_id':
            '', 'amount': 0, 'base_currency_id': ''}], 'apply_default_designation': False, 'revenue_posted': False,
            'revenue_designation_id': '', 'allow_default': False, 'base_currency_id': '', 'tribute_anonymous': False,
            'friends_asking_friends': False}

    Attributes:
        revenue_id (str): The revenue ID.
        tribute_id (str): The tribute.
        amount (float): The amount.
        designation_id (Union[Unset, str]): The default designation.
        splits (Union[Unset, List['NewTributeSplits']]): Splits.
        apply_default_designation (Union[Unset, bool]): Indicates whether apply default designation to revenue.
        revenue_posted (Union[Unset, bool]): Indicates whether isrevenueposted. Read-only in the SOAP API.
        revenue_designation_id (Union[Unset, str]): The revenuedesignationid. Read-only in the SOAP API.
        allow_default (Union[Unset, bool]): Indicates whether allowdefault. Read-only in the SOAP API.
        base_currency_id (Union[Unset, str]): The currency. Read-only in the SOAP API.
        tribute_anonymous (Union[Unset, bool]): Indicates whether do not display on website.
        friends_asking_friends (Union[Unset, bool]): Indicates whether friends asking friends. Read-only in the SOAP
            API.
    """

    revenue_id: str
    tribute_id: str
    amount: float
    designation_id: Union[Unset, str] = UNSET
    splits: Union[Unset, List["NewTributeSplits"]] = UNSET
    apply_default_designation: Union[Unset, bool] = UNSET
    revenue_posted: Union[Unset, bool] = UNSET
    revenue_designation_id: Union[Unset, str] = UNSET
    allow_default: Union[Unset, bool] = UNSET
    base_currency_id: Union[Unset, str] = UNSET
    tribute_anonymous: Union[Unset, bool] = UNSET
    friends_asking_friends: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        revenue_id = self.revenue_id

        tribute_id = self.tribute_id

        amount = self.amount

        designation_id = self.designation_id

        splits: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.splits, Unset):
            splits = []
            for splits_item_data in self.splits:
                splits_item = splits_item_data.to_dict()
                splits.append(splits_item)

        apply_default_designation = self.apply_default_designation

        revenue_posted = self.revenue_posted

        revenue_designation_id = self.revenue_designation_id

        allow_default = self.allow_default

        base_currency_id = self.base_currency_id

        tribute_anonymous = self.tribute_anonymous

        friends_asking_friends = self.friends_asking_friends

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "revenue_id": revenue_id,
                "tribute_id": tribute_id,
                "amount": amount,
            }
        )
        if designation_id is not UNSET:
            field_dict["designation_id"] = designation_id
        if splits is not UNSET:
            field_dict["splits"] = splits
        if apply_default_designation is not UNSET:
            field_dict["apply_default_designation"] = apply_default_designation
        if revenue_posted is not UNSET:
            field_dict["revenue_posted"] = revenue_posted
        if revenue_designation_id is not UNSET:
            field_dict["revenue_designation_id"] = revenue_designation_id
        if allow_default is not UNSET:
            field_dict["allow_default"] = allow_default
        if base_currency_id is not UNSET:
            field_dict["base_currency_id"] = base_currency_id
        if tribute_anonymous is not UNSET:
            field_dict["tribute_anonymous"] = tribute_anonymous
        if friends_asking_friends is not UNSET:
            field_dict["friends_asking_friends"] = friends_asking_friends

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_tribute_splits import NewTributeSplits

        d = src_dict.copy()
        revenue_id = d.pop("revenue_id")

        tribute_id = d.pop("tribute_id")

        amount = d.pop("amount")

        designation_id = d.pop("designation_id", UNSET)

        splits = []
        _splits = d.pop("splits", UNSET)
        for splits_item_data in _splits or []:
            splits_item = NewTributeSplits.from_dict(splits_item_data)

            splits.append(splits_item)

        apply_default_designation = d.pop("apply_default_designation", UNSET)

        revenue_posted = d.pop("revenue_posted", UNSET)

        revenue_designation_id = d.pop("revenue_designation_id", UNSET)

        allow_default = d.pop("allow_default", UNSET)

        base_currency_id = d.pop("base_currency_id", UNSET)

        tribute_anonymous = d.pop("tribute_anonymous", UNSET)

        friends_asking_friends = d.pop("friends_asking_friends", UNSET)

        new_tribute = cls(
            revenue_id=revenue_id,
            tribute_id=tribute_id,
            amount=amount,
            designation_id=designation_id,
            splits=splits,
            apply_default_designation=apply_default_designation,
            revenue_posted=revenue_posted,
            revenue_designation_id=revenue_designation_id,
            allow_default=allow_default,
            base_currency_id=base_currency_id,
            tribute_anonymous=tribute_anonymous,
            friends_asking_friends=friends_asking_friends,
        )

        return new_tribute
