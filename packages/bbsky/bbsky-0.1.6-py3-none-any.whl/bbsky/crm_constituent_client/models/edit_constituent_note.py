import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditConstituentNote")


@_attrs_define
class EditConstituentNote:
    """EditConstituentNote.

    Example:
        {'context_type': 0, 'title': 'Merge note', 'date_entered': '2022-08-24T01:02:47.0000000+00:00', 'author_id':
            'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE', 'note_type': 'Merge', 'text_note': 'Constituent merged 10/12/20',
            'html_note': '<!DOCTYPE html><html><head></head><body><p>Constituent merged 10/12/20</p></body></html>'}

    Attributes:
        context_type (Union[Unset, int]): The context type. Read-only in the SOAP API.
        title (Union[Unset, str]): The the title of this note.
        date_entered (Union[Unset, datetime.datetime]): The the date this note was entered. Uses the format YYYY-MM-
            DDThh:mm:ss. An example date: <i>1955-11-05T22:04:00</i>.
        author_id (Union[Unset, str]): The the author of this note.
        note_type (Union[Unset, str]): The the user-defined type of this note. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/constituentnotetypecode/entries
        text_note (Union[Unset, str]): The the plain text that comprises this note.
        html_note (Union[Unset, str]): The the html that comprises this note.
    """

    context_type: Union[Unset, int] = UNSET
    title: Union[Unset, str] = UNSET
    date_entered: Union[Unset, datetime.datetime] = UNSET
    author_id: Union[Unset, str] = UNSET
    note_type: Union[Unset, str] = UNSET
    text_note: Union[Unset, str] = UNSET
    html_note: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        context_type = self.context_type

        title = self.title

        date_entered: Union[Unset, str] = UNSET
        if not isinstance(self.date_entered, Unset):
            date_entered = self.date_entered.isoformat()

        author_id = self.author_id

        note_type = self.note_type

        text_note = self.text_note

        html_note = self.html_note

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if context_type is not UNSET:
            field_dict["context_type"] = context_type
        if title is not UNSET:
            field_dict["title"] = title
        if date_entered is not UNSET:
            field_dict["date_entered"] = date_entered
        if author_id is not UNSET:
            field_dict["author_id"] = author_id
        if note_type is not UNSET:
            field_dict["note_type"] = note_type
        if text_note is not UNSET:
            field_dict["text_note"] = text_note
        if html_note is not UNSET:
            field_dict["html_note"] = html_note

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        context_type = d.pop("context_type", UNSET)

        title = d.pop("title", UNSET)

        _date_entered = d.pop("date_entered", UNSET)
        date_entered: Union[Unset, datetime.datetime]
        if isinstance(_date_entered, Unset):
            date_entered = UNSET
        else:
            date_entered = isoparse(_date_entered)

        author_id = d.pop("author_id", UNSET)

        note_type = d.pop("note_type", UNSET)

        text_note = d.pop("text_note", UNSET)

        html_note = d.pop("html_note", UNSET)

        edit_constituent_note = cls(
            context_type=context_type,
            title=title,
            date_entered=date_entered,
            author_id=author_id,
            note_type=note_type,
            text_note=text_note,
            html_note=html_note,
        )

        return edit_constituent_note
