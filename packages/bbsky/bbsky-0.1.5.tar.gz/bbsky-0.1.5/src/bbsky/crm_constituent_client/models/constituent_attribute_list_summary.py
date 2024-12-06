import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAttributeListSummary")


@_attrs_define
class ConstituentAttributeListSummary:
    """ListConstituentAttributes.

    Attributes:
        id (Union[Unset, str]): The ID.
        attribute_category_id (Union[Unset, str]): The attributecategoryid.
        category (Union[Unset, str]): The category.
        value (Union[Unset, str]): The value.
        attribute_key (Union[Unset, str]): The attributekey.
        comment (Union[Unset, str]): The comment.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        attribute_group (Union[Unset, str]): The attribute group.
    """

    id: Union[Unset, str] = UNSET
    attribute_category_id: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    attribute_key: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    attribute_group: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        attribute_category_id = self.attribute_category_id

        category = self.category

        value = self.value

        attribute_key = self.attribute_key

        comment = self.comment

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        attribute_group = self.attribute_group

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if attribute_category_id is not UNSET:
            field_dict["attribute_category_id"] = attribute_category_id
        if category is not UNSET:
            field_dict["category"] = category
        if value is not UNSET:
            field_dict["value"] = value
        if attribute_key is not UNSET:
            field_dict["attribute_key"] = attribute_key
        if comment is not UNSET:
            field_dict["comment"] = comment
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if attribute_group is not UNSET:
            field_dict["attribute_group"] = attribute_group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        attribute_category_id = d.pop("attribute_category_id", UNSET)

        category = d.pop("category", UNSET)

        value = d.pop("value", UNSET)

        attribute_key = d.pop("attribute_key", UNSET)

        comment = d.pop("comment", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        attribute_group = d.pop("attribute_group", UNSET)

        constituent_attribute_list_summary = cls(
            id=id,
            attribute_category_id=attribute_category_id,
            category=category,
            value=value,
            attribute_key=attribute_key,
            comment=comment,
            start_date=start_date,
            end_date=end_date,
            attribute_group=attribute_group,
        )

        return constituent_attribute_list_summary
