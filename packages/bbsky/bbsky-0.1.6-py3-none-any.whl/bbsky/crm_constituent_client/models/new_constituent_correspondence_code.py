import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewConstituentCorrespondenceCode")


@_attrs_define
class NewConstituentCorrespondenceCode:
    """CreateConstituentCorrespondenceCode.

    Example:
        {'constituent_id': 'FE204CAB-0E67-4F28-990C-3E1B3B5C40A5', 'correspondence_code': 'Newsletter', 'date_sent':
            '2018-05-22T12:00:00.0000000+00:00', 'comments': 'Newsletter discussing the volunteer drive.'}

    Attributes:
        constituent_id (str): The constituent ID.
        correspondence_code (str): The the code associated with this correspondence.. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/63305295-220e-43a1-b744-359c7ffb77f5.
        date_sent (datetime.datetime): The date when this correspondence was sent.. Uses the format YYYY-MM-DDThh:mm:ss.
            An example date: <i>1955-11-05T22:04:00</i>.
        comments (Union[Unset, str]): The comments regarding this correspondence..
    """

    constituent_id: str
    correspondence_code: str
    date_sent: datetime.datetime
    comments: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        correspondence_code = self.correspondence_code

        date_sent = self.date_sent.isoformat()

        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "constituent_id": constituent_id,
                "correspondence_code": correspondence_code,
                "date_sent": date_sent,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        constituent_id = d.pop("constituent_id")

        correspondence_code = d.pop("correspondence_code")

        date_sent = isoparse(d.pop("date_sent"))

        comments = d.pop("comments", UNSET)

        new_constituent_correspondence_code = cls(
            constituent_id=constituent_id,
            correspondence_code=correspondence_code,
            date_sent=date_sent,
            comments=comments,
        )

        return new_constituent_correspondence_code
