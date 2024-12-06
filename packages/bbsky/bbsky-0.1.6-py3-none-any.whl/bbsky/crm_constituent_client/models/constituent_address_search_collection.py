from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constituent_address_search_summary import ConstituentAddressSearchSummary


T = TypeVar("T", bound="ConstituentAddressSearchCollection")


@_attrs_define
class ConstituentAddressSearchCollection:
    """A collection of items. Data lists can contain paginated results.

    Attributes:
        count (Union[Unset, int]): The number of items available for retrieval into the collection after applying any
            request parameters.
        value (Union[Unset, List['ConstituentAddressSearchSummary']]): The set of items included in the response. This
            may be a subset of the items in the collection.
    """

    count: Union[Unset, int] = UNSET
    value: Union[Unset, List["ConstituentAddressSearchSummary"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        count = self.count

        value: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.value, Unset):
            value = []
            for value_item_data in self.value:
                value_item = value_item_data.to_dict()
                value.append(value_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constituent_address_search_summary import ConstituentAddressSearchSummary

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        value = []
        _value = d.pop("value", UNSET)
        for value_item_data in _value or []:
            value_item = ConstituentAddressSearchSummary.from_dict(value_item_data)

            value.append(value_item)

        constituent_address_search_collection = cls(
            count=count,
            value=value,
        )

        return constituent_address_search_collection
