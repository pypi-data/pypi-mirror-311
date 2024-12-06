import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentNoteView")


@_attrs_define
class ConstituentNoteView:
    """ViewConstituentNote.

    Attributes:
        date_entered (Union[Unset, datetime.datetime]): The date. Uses the format YYYY-MM-DDThh:mm:ss. An example date:
            <i>1955-11-05T22:04:00</i>.
        title (Union[Unset, str]): The title.
        text_note (Union[Unset, str]): The note.
        author (Union[Unset, str]): The author.
        notetype (Union[Unset, str]): The type.
    """

    date_entered: Union[Unset, datetime.datetime] = UNSET
    title: Union[Unset, str] = UNSET
    text_note: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    notetype: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date_entered: Union[Unset, str] = UNSET
        if not isinstance(self.date_entered, Unset):
            date_entered = self.date_entered.isoformat()

        title = self.title

        text_note = self.text_note

        author = self.author

        notetype = self.notetype

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date_entered is not UNSET:
            field_dict["date_entered"] = date_entered
        if title is not UNSET:
            field_dict["title"] = title
        if text_note is not UNSET:
            field_dict["text_note"] = text_note
        if author is not UNSET:
            field_dict["author"] = author
        if notetype is not UNSET:
            field_dict["notetype"] = notetype

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _date_entered = d.pop("date_entered", UNSET)
        date_entered: Union[Unset, datetime.datetime]
        if isinstance(_date_entered, Unset):
            date_entered = UNSET
        else:
            date_entered = isoparse(_date_entered)

        title = d.pop("title", UNSET)

        text_note = d.pop("text_note", UNSET)

        author = d.pop("author", UNSET)

        notetype = d.pop("notetype", UNSET)

        constituent_note_view = cls(
            date_entered=date_entered,
            title=title,
            text_note=text_note,
            author=author,
            notetype=notetype,
        )

        return constituent_note_view
