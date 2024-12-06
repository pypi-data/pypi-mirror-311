import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditConstituentCorrespondenceCode")


@_attrs_define
class EditConstituentCorrespondenceCode:
    """EditConstituentCorrespondenceCode.

    Example:
        {'correspondence_code': 'Phone', 'date_sent': '2018-10-21T12:00:00.0000000+00:00', 'comments': 'Follow up phone
            call.', 'require_code': False}

    Attributes:
        correspondence_code (Union[Unset, str]): The the code associated with this correspondence.. This simple list can
            be queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/63305295-220e-43a1-b744-359c7ffb77f5.
        date_sent (Union[Unset, datetime.datetime]): The date when this correspondence was sent.. Uses the format YYYY-
            MM-DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        comments (Union[Unset, str]): The comments regarding this correspondence..
        require_code (Union[Unset, bool]): Indicates whether require code. Read-only in the SOAP API.
    """

    correspondence_code: Union[Unset, str] = UNSET
    date_sent: Union[Unset, datetime.datetime] = UNSET
    comments: Union[Unset, str] = UNSET
    require_code: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        correspondence_code = self.correspondence_code

        date_sent: Union[Unset, str] = UNSET
        if not isinstance(self.date_sent, Unset):
            date_sent = self.date_sent.isoformat()

        comments = self.comments

        require_code = self.require_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if correspondence_code is not UNSET:
            field_dict["correspondence_code"] = correspondence_code
        if date_sent is not UNSET:
            field_dict["date_sent"] = date_sent
        if comments is not UNSET:
            field_dict["comments"] = comments
        if require_code is not UNSET:
            field_dict["require_code"] = require_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        correspondence_code = d.pop("correspondence_code", UNSET)

        _date_sent = d.pop("date_sent", UNSET)
        date_sent: Union[Unset, datetime.datetime]
        if isinstance(_date_sent, Unset):
            date_sent = UNSET
        else:
            date_sent = isoparse(_date_sent)

        comments = d.pop("comments", UNSET)

        require_code = d.pop("require_code", UNSET)

        edit_constituent_correspondence_code = cls(
            correspondence_code=correspondence_code,
            date_sent=date_sent,
            comments=comments,
            require_code=require_code,
        )

        return edit_constituent_correspondence_code
