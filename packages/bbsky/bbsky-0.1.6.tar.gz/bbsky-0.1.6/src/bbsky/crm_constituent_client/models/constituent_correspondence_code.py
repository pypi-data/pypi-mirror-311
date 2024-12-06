import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentCorrespondenceCode")


@_attrs_define
class ConstituentCorrespondenceCode:
    """GetConstituentCorrespondenceCode.

    Attributes:
        date_sent (datetime.datetime): The date when this correspondence was sent.. Uses the format YYYY-MM-DDThh:mm:ss.
            An example date: <i>1955-11-05T22:04:00</i>.
        correspondence_code (Union[Unset, str]): The the code associated with this correspondence.. This simple list can
            be queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/63305295-220e-43a1-b744-359c7ffb77f5.
        comments (Union[Unset, str]): The comments regarding this correspondence..
        require_code (Union[Unset, bool]): Indicates whether require code. Read-only in the SOAP API.
    """

    date_sent: datetime.datetime
    correspondence_code: Union[Unset, str] = UNSET
    comments: Union[Unset, str] = UNSET
    require_code: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date_sent = self.date_sent.isoformat()

        correspondence_code = self.correspondence_code

        comments = self.comments

        require_code = self.require_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "date_sent": date_sent,
            }
        )
        if correspondence_code is not UNSET:
            field_dict["correspondence_code"] = correspondence_code
        if comments is not UNSET:
            field_dict["comments"] = comments
        if require_code is not UNSET:
            field_dict["require_code"] = require_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        date_sent = isoparse(d.pop("date_sent"))

        correspondence_code = d.pop("correspondence_code", UNSET)

        comments = d.pop("comments", UNSET)

        require_code = d.pop("require_code", UNSET)

        constituent_correspondence_code = cls(
            date_sent=date_sent,
            correspondence_code=correspondence_code,
            comments=comments,
            require_code=require_code,
        )

        return constituent_correspondence_code
