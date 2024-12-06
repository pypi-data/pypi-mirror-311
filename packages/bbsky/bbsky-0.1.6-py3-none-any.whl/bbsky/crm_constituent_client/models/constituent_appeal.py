import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAppeal")


@_attrs_define
class ConstituentAppeal:
    """GetConstituentAppeal.

    Attributes:
        appeal_id (str): The appeal.
        mkt_segmentation (Union[Unset, str]): The mailing. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-
            adnmg/simplelists/664c0aa7-9f88-46f6-ba84-7b412e1131b5?parameters=appeal_id,{appeal_id}.
        date_sent (Union[Unset, datetime.datetime]): The date sent. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        mkt_package_id (Union[Unset, str]): The package.
        source_code (Union[Unset, str]): The source code.
        comments (Union[Unset, str]): The comments.
        read_only (Union[Unset, bool]): Indicates whether read only. Read-only in the SOAP API.
    """

    appeal_id: str
    mkt_segmentation: Union[Unset, str] = UNSET
    date_sent: Union[Unset, datetime.datetime] = UNSET
    mkt_package_id: Union[Unset, str] = UNSET
    source_code: Union[Unset, str] = UNSET
    comments: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        appeal_id = self.appeal_id

        mkt_segmentation = self.mkt_segmentation

        date_sent: Union[Unset, str] = UNSET
        if not isinstance(self.date_sent, Unset):
            date_sent = self.date_sent.isoformat()

        mkt_package_id = self.mkt_package_id

        source_code = self.source_code

        comments = self.comments

        read_only = self.read_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "appeal_id": appeal_id,
            }
        )
        if mkt_segmentation is not UNSET:
            field_dict["mkt_segmentation"] = mkt_segmentation
        if date_sent is not UNSET:
            field_dict["date_sent"] = date_sent
        if mkt_package_id is not UNSET:
            field_dict["mkt_package_id"] = mkt_package_id
        if source_code is not UNSET:
            field_dict["source_code"] = source_code
        if comments is not UNSET:
            field_dict["comments"] = comments
        if read_only is not UNSET:
            field_dict["read_only"] = read_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        appeal_id = d.pop("appeal_id")

        mkt_segmentation = d.pop("mkt_segmentation", UNSET)

        _date_sent = d.pop("date_sent", UNSET)
        date_sent: Union[Unset, datetime.datetime]
        if isinstance(_date_sent, Unset):
            date_sent = UNSET
        else:
            date_sent = isoparse(_date_sent)

        mkt_package_id = d.pop("mkt_package_id", UNSET)

        source_code = d.pop("source_code", UNSET)

        comments = d.pop("comments", UNSET)

        read_only = d.pop("read_only", UNSET)

        constituent_appeal = cls(
            appeal_id=appeal_id,
            mkt_segmentation=mkt_segmentation,
            date_sent=date_sent,
            mkt_package_id=mkt_package_id,
            source_code=source_code,
            comments=comments,
            read_only=read_only,
        )

        return constituent_appeal
