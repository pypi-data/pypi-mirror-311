import datetime
from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.month_day import MonthDay


T = TypeVar("T", bound="ConstituentAddressView")


@_attrs_define
class ConstituentAddressView:
    """ViewConstituentAddress.

    Attributes:
        address_type (Union[Unset, str]): The type.
        country_id (Union[Unset, str]): The country ID.
        country (Union[Unset, str]): The country.
        address_block (Union[Unset, str]): The address.
        city (Union[Unset, str]): The city.
        state (Union[Unset, str]): The state.
        post_code (Union[Unset, str]): The post code.
        primary (Union[Unset, bool]): Indicates whether is primary.
        do_not_mail (Union[Unset, bool]): Indicates whether do not mail.
        do_not_mail_reason_code (Union[Unset, str]): The do not mail reason code.
        confidential (Union[Unset, bool]): Indicates whether is confidential.
        start_date (Union[Unset, datetime.datetime]): The start date. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        end_date (Union[Unset, datetime.datetime]): The end date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        date_added (Union[Unset, datetime.datetime]): The date added. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        seasonal_start_date (Union[Unset, MonthDay]): MonthDay Example: {'month': 4, 'day': 13}.
        seasonal_end_date (Union[Unset, MonthDay]): MonthDay Example: {'month': 4, 'day': 13}.
        info_source_code (Union[Unset, str]): The information source.
        info_source_comments (Union[Unset, str]): The comments.
        state_abbreviation (Union[Unset, str]): The state abbreviation.
    """

    address_type: Union[Unset, str] = UNSET
    country_id: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    address_block: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    post_code: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    do_not_mail: Union[Unset, bool] = UNSET
    do_not_mail_reason_code: Union[Unset, str] = UNSET
    confidential: Union[Unset, bool] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    date_added: Union[Unset, datetime.datetime] = UNSET
    seasonal_start_date: Union[Unset, "MonthDay"] = UNSET
    seasonal_end_date: Union[Unset, "MonthDay"] = UNSET
    info_source_code: Union[Unset, str] = UNSET
    info_source_comments: Union[Unset, str] = UNSET
    state_abbreviation: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        address_type = self.address_type

        country_id = self.country_id

        country = self.country

        address_block = self.address_block

        city = self.city

        state = self.state

        post_code = self.post_code

        primary = self.primary

        do_not_mail = self.do_not_mail

        do_not_mail_reason_code = self.do_not_mail_reason_code

        confidential = self.confidential

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        date_added: Union[Unset, str] = UNSET
        if not isinstance(self.date_added, Unset):
            date_added = self.date_added.isoformat()

        seasonal_start_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.seasonal_start_date, Unset):
            seasonal_start_date = self.seasonal_start_date.to_dict()

        seasonal_end_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.seasonal_end_date, Unset):
            seasonal_end_date = self.seasonal_end_date.to_dict()

        info_source_code = self.info_source_code

        info_source_comments = self.info_source_comments

        state_abbreviation = self.state_abbreviation

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if address_type is not UNSET:
            field_dict["address_type"] = address_type
        if country_id is not UNSET:
            field_dict["country_id"] = country_id
        if country is not UNSET:
            field_dict["country"] = country
        if address_block is not UNSET:
            field_dict["address_block"] = address_block
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if post_code is not UNSET:
            field_dict["post_code"] = post_code
        if primary is not UNSET:
            field_dict["primary"] = primary
        if do_not_mail is not UNSET:
            field_dict["do_not_mail"] = do_not_mail
        if do_not_mail_reason_code is not UNSET:
            field_dict["do_not_mail_reason_code"] = do_not_mail_reason_code
        if confidential is not UNSET:
            field_dict["confidential"] = confidential
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if date_added is not UNSET:
            field_dict["date_added"] = date_added
        if seasonal_start_date is not UNSET:
            field_dict["seasonal_start_date"] = seasonal_start_date
        if seasonal_end_date is not UNSET:
            field_dict["seasonal_end_date"] = seasonal_end_date
        if info_source_code is not UNSET:
            field_dict["info_source_code"] = info_source_code
        if info_source_comments is not UNSET:
            field_dict["info_source_comments"] = info_source_comments
        if state_abbreviation is not UNSET:
            field_dict["state_abbreviation"] = state_abbreviation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.month_day import MonthDay

        d = src_dict.copy()
        address_type = d.pop("address_type", UNSET)

        country_id = d.pop("country_id", UNSET)

        country = d.pop("country", UNSET)

        address_block = d.pop("address_block", UNSET)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        post_code = d.pop("post_code", UNSET)

        primary = d.pop("primary", UNSET)

        do_not_mail = d.pop("do_not_mail", UNSET)

        do_not_mail_reason_code = d.pop("do_not_mail_reason_code", UNSET)

        confidential = d.pop("confidential", UNSET)

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

        _date_added = d.pop("date_added", UNSET)
        date_added: Union[Unset, datetime.datetime]
        if isinstance(_date_added, Unset):
            date_added = UNSET
        else:
            date_added = isoparse(_date_added)

        _seasonal_start_date = d.pop("seasonal_start_date", UNSET)
        seasonal_start_date: Union[Unset, MonthDay]
        if isinstance(_seasonal_start_date, Unset):
            seasonal_start_date = UNSET
        else:
            seasonal_start_date = MonthDay.from_dict(_seasonal_start_date)

        _seasonal_end_date = d.pop("seasonal_end_date", UNSET)
        seasonal_end_date: Union[Unset, MonthDay]
        if isinstance(_seasonal_end_date, Unset):
            seasonal_end_date = UNSET
        else:
            seasonal_end_date = MonthDay.from_dict(_seasonal_end_date)

        info_source_code = d.pop("info_source_code", UNSET)

        info_source_comments = d.pop("info_source_comments", UNSET)

        state_abbreviation = d.pop("state_abbreviation", UNSET)

        constituent_address_view = cls(
            address_type=address_type,
            country_id=country_id,
            country=country,
            address_block=address_block,
            city=city,
            state=state,
            post_code=post_code,
            primary=primary,
            do_not_mail=do_not_mail,
            do_not_mail_reason_code=do_not_mail_reason_code,
            confidential=confidential,
            start_date=start_date,
            end_date=end_date,
            date_added=date_added,
            seasonal_start_date=seasonal_start_date,
            seasonal_end_date=seasonal_end_date,
            info_source_code=info_source_code,
            info_source_comments=info_source_comments,
            state_abbreviation=state_abbreviation,
        )

        return constituent_address_view
