import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewConstituentAppealResponse")


@_attrs_define
class NewConstituentAppealResponse:
    """CreateConstituentAppealResponse.

    Example:
        {'constituent_appeal_id': '7D2E2D1B-AEAD-4D92-9219-65E9C84E139C', 'date': '2022-10-21T12:00:00.0000000+00:00',
            'response_category': 'Test', 'response': 'Do Not Email'}

    Attributes:
        constituent_appeal_id (str): The constituent appeal ID.
        response_category (str): The the response category. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/fa5c3e42-aea6-450c-a66f-e79919df98d8. Read-only in the SOAP
            API.
        response (str): The the response. This simple list can be queried at https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/e48745a4-b8cd-4e31-885a-3173d7374ea6?parameters=responsecategoryid,{responsecategoryid}.
        date (Union[Unset, datetime.datetime]): The the date of the response. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
    """

    constituent_appeal_id: str
    response_category: str
    response: str
    date: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_appeal_id = self.constituent_appeal_id

        response_category = self.response_category

        response = self.response

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "constituent_appeal_id": constituent_appeal_id,
                "response_category": response_category,
                "response": response,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        constituent_appeal_id = d.pop("constituent_appeal_id")

        response_category = d.pop("response_category")

        response = d.pop("response")

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        new_constituent_appeal_response = cls(
            constituent_appeal_id=constituent_appeal_id,
            response_category=response_category,
            response=response,
            date=date,
        )

        return new_constituent_appeal_response
