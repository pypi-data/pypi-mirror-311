import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuzzy_date import FuzzyDate
    from ..models.hour_minute import HourMinute
    from ..models.new_constituent_attribute_attribute_categories import (
        NewConstituentAttributeAttributeCategories,
    )


T = TypeVar("T", bound="NewConstituentAttribute")


@_attrs_define
class NewConstituentAttribute:
    """CreateConstituentAttribute.

    Example:
        {'attribute_context_id': '', 'header_caption': '', 'attribute_category': '', 'string_value': '', 'number_value':
            0, 'money_value': 0, 'date_value': '', 'boolean_value': 'No', 'code_table_value': '', 'fuzzy_date_value': '',
            'constituent_id_value': '', 'hour_minute_value': '', 'memo_value': '', 'attribute_categories': [{'id': '',
            'data_type_code': 0, 'constituent_search_list_catalog_id': '', 'code_table_name': ''}], 'comment': '',
            'start_date': '', 'end_date': '', 'record_type_string': '', 'currency': '', 'transaction_currency_id': '',
            'base_currency_id': ''}

    Attributes:
        attribute_context_id (str): The attribute context ID.
        attribute_category (str): The category. This simple list can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/958132a3-762a-4844-b7a1-f3a3098da95a?parameters=record_type,{record_type_string}.
        header_caption (Union[Unset, str]): The headercaption. Read-only in the SOAP API.
        string_value (Union[Unset, str]): The value.
        number_value (Union[Unset, int]): The value.
        money_value (Union[Unset, float]): The value.
        date_value (Union[Unset, datetime.datetime]): The value. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        boolean_value (Union[Unset, str]): The value. Available values are <i>no</i>, <i>yes</i>
        code_table_value (Union[Unset, str]): The value. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/addresstypecode/entries
        fuzzy_date_value (Union[Unset, FuzzyDate]): FuzzyDate Example: {'year': 2024, 'month': 4, 'day': 13}.
        constituent_id_value (Union[Unset, str]): The value.
        hour_minute_value (Union[Unset, HourMinute]): HourMinute
        memo_value (Union[Unset, str]): The value.
        attribute_categories (Union[Unset, List['NewConstituentAttributeAttributeCategories']]): Attribute categories.
        comment (Union[Unset, str]): The comment.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        record_type_string (Union[Unset, str]): The record type. Read-only in the SOAP API.
        currency (Union[Unset, str]): The currency. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/13612288-b37e-409d-ba52-
            6ab31637ddd6?parameters=transaction_currency_id,{transaction_currency_id}&parameters=base_currency_id,{base_curr
            ency_id}.
        transaction_currency_id (Union[Unset, str]): The transaction currency. Read-only in the SOAP API.
        base_currency_id (Union[Unset, str]): The base currency. Read-only in the SOAP API.
    """

    attribute_context_id: str
    attribute_category: str
    header_caption: Union[Unset, str] = UNSET
    string_value: Union[Unset, str] = UNSET
    number_value: Union[Unset, int] = UNSET
    money_value: Union[Unset, float] = UNSET
    date_value: Union[Unset, datetime.datetime] = UNSET
    boolean_value: Union[Unset, str] = UNSET
    code_table_value: Union[Unset, str] = UNSET
    fuzzy_date_value: Union[Unset, "FuzzyDate"] = UNSET
    constituent_id_value: Union[Unset, str] = UNSET
    hour_minute_value: Union[Unset, "HourMinute"] = UNSET
    memo_value: Union[Unset, str] = UNSET
    attribute_categories: Union[Unset, List["NewConstituentAttributeAttributeCategories"]] = UNSET
    comment: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    record_type_string: Union[Unset, str] = UNSET
    currency: Union[Unset, str] = UNSET
    transaction_currency_id: Union[Unset, str] = UNSET
    base_currency_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        attribute_context_id = self.attribute_context_id

        attribute_category = self.attribute_category

        header_caption = self.header_caption

        string_value = self.string_value

        number_value = self.number_value

        money_value = self.money_value

        date_value: Union[Unset, str] = UNSET
        if not isinstance(self.date_value, Unset):
            date_value = self.date_value.isoformat()

        boolean_value = self.boolean_value

        code_table_value = self.code_table_value

        fuzzy_date_value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fuzzy_date_value, Unset):
            fuzzy_date_value = self.fuzzy_date_value.to_dict()

        constituent_id_value = self.constituent_id_value

        hour_minute_value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hour_minute_value, Unset):
            hour_minute_value = self.hour_minute_value.to_dict()

        memo_value = self.memo_value

        attribute_categories: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.attribute_categories, Unset):
            attribute_categories = []
            for attribute_categories_item_data in self.attribute_categories:
                attribute_categories_item = attribute_categories_item_data.to_dict()
                attribute_categories.append(attribute_categories_item)

        comment = self.comment

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        record_type_string = self.record_type_string

        currency = self.currency

        transaction_currency_id = self.transaction_currency_id

        base_currency_id = self.base_currency_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "attribute_context_id": attribute_context_id,
                "attribute_category": attribute_category,
            }
        )
        if header_caption is not UNSET:
            field_dict["header_caption"] = header_caption
        if string_value is not UNSET:
            field_dict["string_value"] = string_value
        if number_value is not UNSET:
            field_dict["number_value"] = number_value
        if money_value is not UNSET:
            field_dict["money_value"] = money_value
        if date_value is not UNSET:
            field_dict["date_value"] = date_value
        if boolean_value is not UNSET:
            field_dict["boolean_value"] = boolean_value
        if code_table_value is not UNSET:
            field_dict["code_table_value"] = code_table_value
        if fuzzy_date_value is not UNSET:
            field_dict["fuzzy_date_value"] = fuzzy_date_value
        if constituent_id_value is not UNSET:
            field_dict["constituent_id_value"] = constituent_id_value
        if hour_minute_value is not UNSET:
            field_dict["hour_minute_value"] = hour_minute_value
        if memo_value is not UNSET:
            field_dict["memo_value"] = memo_value
        if attribute_categories is not UNSET:
            field_dict["attribute_categories"] = attribute_categories
        if comment is not UNSET:
            field_dict["comment"] = comment
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if record_type_string is not UNSET:
            field_dict["record_type_string"] = record_type_string
        if currency is not UNSET:
            field_dict["currency"] = currency
        if transaction_currency_id is not UNSET:
            field_dict["transaction_currency_id"] = transaction_currency_id
        if base_currency_id is not UNSET:
            field_dict["base_currency_id"] = base_currency_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fuzzy_date import FuzzyDate
        from ..models.hour_minute import HourMinute
        from ..models.new_constituent_attribute_attribute_categories import (
            NewConstituentAttributeAttributeCategories,
        )

        d = src_dict.copy()
        attribute_context_id = d.pop("attribute_context_id")

        attribute_category = d.pop("attribute_category")

        header_caption = d.pop("header_caption", UNSET)

        string_value = d.pop("string_value", UNSET)

        number_value = d.pop("number_value", UNSET)

        money_value = d.pop("money_value", UNSET)

        _date_value = d.pop("date_value", UNSET)
        date_value: Union[Unset, datetime.datetime]
        if isinstance(_date_value, Unset):
            date_value = UNSET
        else:
            date_value = isoparse(_date_value)

        boolean_value = d.pop("boolean_value", UNSET)

        code_table_value = d.pop("code_table_value", UNSET)

        _fuzzy_date_value = d.pop("fuzzy_date_value", UNSET)
        fuzzy_date_value: Union[Unset, FuzzyDate]
        if isinstance(_fuzzy_date_value, Unset):
            fuzzy_date_value = UNSET
        else:
            fuzzy_date_value = FuzzyDate.from_dict(_fuzzy_date_value)

        constituent_id_value = d.pop("constituent_id_value", UNSET)

        _hour_minute_value = d.pop("hour_minute_value", UNSET)
        hour_minute_value: Union[Unset, HourMinute]
        if isinstance(_hour_minute_value, Unset):
            hour_minute_value = UNSET
        else:
            hour_minute_value = HourMinute.from_dict(_hour_minute_value)

        memo_value = d.pop("memo_value", UNSET)

        attribute_categories = []
        _attribute_categories = d.pop("attribute_categories", UNSET)
        for attribute_categories_item_data in _attribute_categories or []:
            attribute_categories_item = NewConstituentAttributeAttributeCategories.from_dict(
                attribute_categories_item_data
            )

            attribute_categories.append(attribute_categories_item)

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

        record_type_string = d.pop("record_type_string", UNSET)

        currency = d.pop("currency", UNSET)

        transaction_currency_id = d.pop("transaction_currency_id", UNSET)

        base_currency_id = d.pop("base_currency_id", UNSET)

        new_constituent_attribute = cls(
            attribute_context_id=attribute_context_id,
            attribute_category=attribute_category,
            header_caption=header_caption,
            string_value=string_value,
            number_value=number_value,
            money_value=money_value,
            date_value=date_value,
            boolean_value=boolean_value,
            code_table_value=code_table_value,
            fuzzy_date_value=fuzzy_date_value,
            constituent_id_value=constituent_id_value,
            hour_minute_value=hour_minute_value,
            memo_value=memo_value,
            attribute_categories=attribute_categories,
            comment=comment,
            start_date=start_date,
            end_date=end_date,
            record_type_string=record_type_string,
            currency=currency,
            transaction_currency_id=transaction_currency_id,
            base_currency_id=base_currency_id,
        )

        return new_constituent_attribute
