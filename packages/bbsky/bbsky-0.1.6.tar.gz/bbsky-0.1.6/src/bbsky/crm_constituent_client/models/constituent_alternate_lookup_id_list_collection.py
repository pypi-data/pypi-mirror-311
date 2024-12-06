from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constituent_alternate_lookup_id_list_summary import ConstituentAlternateLookupIdListSummary


T = TypeVar("T", bound="ConstituentAlternateLookupIdListCollection")


@_attrs_define
class ConstituentAlternateLookupIdListCollection:
    """A collection of items. Data lists can contain paginated results.

    Attributes:
        count (Union[Unset, int]): The number of items available for retrieval into the collection after applying any
            request parameters.
        value (Union[Unset, List['ConstituentAlternateLookupIdListSummary']]): The set of items included in the
            response. This may be a subset of the items in the collection.
        infinity_session (Union[Unset, str]): Values for cookies related to the Infinity load balancer session.
        session_key (Union[Unset, str]): Session key for paging provided by user in request query parameter.
        total_available_rows (Union[Unset, int]): The number of total rows available.
        more_rows_range_key (Union[Unset, str]): Key for accessing cached results on subsequent calls to this data list.
        data_no_longer_available (Union[Unset, bool]): Indicates data is no longer available in the context of this
            session.
    """

    count: Union[Unset, int] = UNSET
    value: Union[Unset, List["ConstituentAlternateLookupIdListSummary"]] = UNSET
    infinity_session: Union[Unset, str] = UNSET
    session_key: Union[Unset, str] = UNSET
    total_available_rows: Union[Unset, int] = UNSET
    more_rows_range_key: Union[Unset, str] = UNSET
    data_no_longer_available: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        count = self.count

        value: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.value, Unset):
            value = []
            for value_item_data in self.value:
                value_item = value_item_data.to_dict()
                value.append(value_item)

        infinity_session = self.infinity_session

        session_key = self.session_key

        total_available_rows = self.total_available_rows

        more_rows_range_key = self.more_rows_range_key

        data_no_longer_available = self.data_no_longer_available

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if value is not UNSET:
            field_dict["value"] = value
        if infinity_session is not UNSET:
            field_dict["infinity_session"] = infinity_session
        if session_key is not UNSET:
            field_dict["session_key"] = session_key
        if total_available_rows is not UNSET:
            field_dict["total_available_rows"] = total_available_rows
        if more_rows_range_key is not UNSET:
            field_dict["more_rows_range_key"] = more_rows_range_key
        if data_no_longer_available is not UNSET:
            field_dict["data_no_longer_available"] = data_no_longer_available

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constituent_alternate_lookup_id_list_summary import (
            ConstituentAlternateLookupIdListSummary,
        )

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        value = []
        _value = d.pop("value", UNSET)
        for value_item_data in _value or []:
            value_item = ConstituentAlternateLookupIdListSummary.from_dict(value_item_data)

            value.append(value_item)

        infinity_session = d.pop("infinity_session", UNSET)

        session_key = d.pop("session_key", UNSET)

        total_available_rows = d.pop("total_available_rows", UNSET)

        more_rows_range_key = d.pop("more_rows_range_key", UNSET)

        data_no_longer_available = d.pop("data_no_longer_available", UNSET)

        constituent_alternate_lookup_id_list_collection = cls(
            count=count,
            value=value,
            infinity_session=infinity_session,
            session_key=session_key,
            total_available_rows=total_available_rows,
            more_rows_range_key=more_rows_range_key,
            data_no_longer_available=data_no_longer_available,
        )

        return constituent_alternate_lookup_id_list_collection
