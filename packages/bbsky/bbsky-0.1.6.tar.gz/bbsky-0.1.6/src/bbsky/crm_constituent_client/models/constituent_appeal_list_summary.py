import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentAppealListSummary")


@_attrs_define
class ConstituentAppealListSummary:
    """ListConstituentAppeals.

    Attributes:
        id (Union[Unset, str]): The ID.
        appeal_id (Union[Unset, str]): The appeal ID.
        appeal (Union[Unset, str]): The appeal.
        description (Union[Unset, str]): The description.
        date_sent (Union[Unset, datetime.datetime]): The date sent. Uses the format YYYY-MM-DDThh:mm:ss. An example
            date: <i>1955-11-05T22:04:00</i>.
        source_code (Union[Unset, str]): The source code.
        finder_number (Union[Unset, int]): The finder number.
        comments (Union[Unset, str]): The comments.
        mkt_segmentation_id (Union[Unset, str]): The mailing ID.
        mkt_segmentation_segment_id (Union[Unset, str]): The segment ID.
        letter (Union[Unset, str]): The letter.
        package (Union[Unset, str]): The package.
        mailing (Union[Unset, str]): The mailing.
        segment (Union[Unset, str]): The segment.
        test_segment (Union[Unset, str]): The test segment.
        has_responses (Union[Unset, bool]): Indicates whether has responses.
        appeal_mailing (Union[Unset, bool]): Indicates whether appeal mailing.
        time_frame_text (Union[Unset, str]): The timeframe.
        time_frame_group_sort (Union[Unset, str]): The timeframeorder.
        site (Union[Unset, str]): The site.
        mailing_family_type_code (Union[Unset, int]): The mailing family type code.
    """

    id: Union[Unset, str] = UNSET
    appeal_id: Union[Unset, str] = UNSET
    appeal: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    date_sent: Union[Unset, datetime.datetime] = UNSET
    source_code: Union[Unset, str] = UNSET
    finder_number: Union[Unset, int] = UNSET
    comments: Union[Unset, str] = UNSET
    mkt_segmentation_id: Union[Unset, str] = UNSET
    mkt_segmentation_segment_id: Union[Unset, str] = UNSET
    letter: Union[Unset, str] = UNSET
    package: Union[Unset, str] = UNSET
    mailing: Union[Unset, str] = UNSET
    segment: Union[Unset, str] = UNSET
    test_segment: Union[Unset, str] = UNSET
    has_responses: Union[Unset, bool] = UNSET
    appeal_mailing: Union[Unset, bool] = UNSET
    time_frame_text: Union[Unset, str] = UNSET
    time_frame_group_sort: Union[Unset, str] = UNSET
    site: Union[Unset, str] = UNSET
    mailing_family_type_code: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        appeal_id = self.appeal_id

        appeal = self.appeal

        description = self.description

        date_sent: Union[Unset, str] = UNSET
        if not isinstance(self.date_sent, Unset):
            date_sent = self.date_sent.isoformat()

        source_code = self.source_code

        finder_number = self.finder_number

        comments = self.comments

        mkt_segmentation_id = self.mkt_segmentation_id

        mkt_segmentation_segment_id = self.mkt_segmentation_segment_id

        letter = self.letter

        package = self.package

        mailing = self.mailing

        segment = self.segment

        test_segment = self.test_segment

        has_responses = self.has_responses

        appeal_mailing = self.appeal_mailing

        time_frame_text = self.time_frame_text

        time_frame_group_sort = self.time_frame_group_sort

        site = self.site

        mailing_family_type_code = self.mailing_family_type_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if appeal_id is not UNSET:
            field_dict["appeal_id"] = appeal_id
        if appeal is not UNSET:
            field_dict["appeal"] = appeal
        if description is not UNSET:
            field_dict["description"] = description
        if date_sent is not UNSET:
            field_dict["date_sent"] = date_sent
        if source_code is not UNSET:
            field_dict["source_code"] = source_code
        if finder_number is not UNSET:
            field_dict["finder_number"] = finder_number
        if comments is not UNSET:
            field_dict["comments"] = comments
        if mkt_segmentation_id is not UNSET:
            field_dict["mkt_segmentation_id"] = mkt_segmentation_id
        if mkt_segmentation_segment_id is not UNSET:
            field_dict["mkt_segmentation_segment_id"] = mkt_segmentation_segment_id
        if letter is not UNSET:
            field_dict["letter"] = letter
        if package is not UNSET:
            field_dict["package"] = package
        if mailing is not UNSET:
            field_dict["mailing"] = mailing
        if segment is not UNSET:
            field_dict["segment"] = segment
        if test_segment is not UNSET:
            field_dict["test_segment"] = test_segment
        if has_responses is not UNSET:
            field_dict["has_responses"] = has_responses
        if appeal_mailing is not UNSET:
            field_dict["appeal_mailing"] = appeal_mailing
        if time_frame_text is not UNSET:
            field_dict["time_frame_text"] = time_frame_text
        if time_frame_group_sort is not UNSET:
            field_dict["time_frame_group_sort"] = time_frame_group_sort
        if site is not UNSET:
            field_dict["site"] = site
        if mailing_family_type_code is not UNSET:
            field_dict["mailing_family_type_code"] = mailing_family_type_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        appeal_id = d.pop("appeal_id", UNSET)

        appeal = d.pop("appeal", UNSET)

        description = d.pop("description", UNSET)

        _date_sent = d.pop("date_sent", UNSET)
        date_sent: Union[Unset, datetime.datetime]
        if isinstance(_date_sent, Unset):
            date_sent = UNSET
        else:
            date_sent = isoparse(_date_sent)

        source_code = d.pop("source_code", UNSET)

        finder_number = d.pop("finder_number", UNSET)

        comments = d.pop("comments", UNSET)

        mkt_segmentation_id = d.pop("mkt_segmentation_id", UNSET)

        mkt_segmentation_segment_id = d.pop("mkt_segmentation_segment_id", UNSET)

        letter = d.pop("letter", UNSET)

        package = d.pop("package", UNSET)

        mailing = d.pop("mailing", UNSET)

        segment = d.pop("segment", UNSET)

        test_segment = d.pop("test_segment", UNSET)

        has_responses = d.pop("has_responses", UNSET)

        appeal_mailing = d.pop("appeal_mailing", UNSET)

        time_frame_text = d.pop("time_frame_text", UNSET)

        time_frame_group_sort = d.pop("time_frame_group_sort", UNSET)

        site = d.pop("site", UNSET)

        mailing_family_type_code = d.pop("mailing_family_type_code", UNSET)

        constituent_appeal_list_summary = cls(
            id=id,
            appeal_id=appeal_id,
            appeal=appeal,
            description=description,
            date_sent=date_sent,
            source_code=source_code,
            finder_number=finder_number,
            comments=comments,
            mkt_segmentation_id=mkt_segmentation_id,
            mkt_segmentation_segment_id=mkt_segmentation_segment_id,
            letter=letter,
            package=package,
            mailing=mailing,
            segment=segment,
            test_segment=test_segment,
            has_responses=has_responses,
            appeal_mailing=appeal_mailing,
            time_frame_text=time_frame_text,
            time_frame_group_sort=time_frame_group_sort,
            site=site,
            mailing_family_type_code=mailing_family_type_code,
        )

        return constituent_appeal_list_summary
