import datetime
from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewConstituentNote")


@_attrs_define
class NewConstituentNote:
    """CreateConstituentNote.

    Example:
        {'constituent_id': 'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE', 'context_type': 0, 'title': 'Merge note',
            'date_entered': '2022-08-24T01:02:47.0000000+00:00', 'author_id': 'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE',
            'note_type': 'Merge', 'text_note': 'Constituent merged 10/12/20', 'html_note': '<!DOCTYPE
            html><html><head></head><body><p>Constituent merged 10/12/20</p></body></html>'}

    Attributes:
        constituent_id (str): The constituent ID.
        date_entered (datetime.datetime): The the date this note was entered. Uses the format YYYY-MM-DDThh:mm:ss. An
            example date: <i>1955-11-05T22:04:00</i>.
        note_type (str): The the user-defined type of this note. This code table can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/codetables/constituentnotetypecode/entries
        context_type (Union[Unset, int]): The context type. Read-only in the SOAP API.
        title (Union[Unset, str]): The the title of this note.
        author_id (Union[Unset, str]): The the author of this note.
        text_note (Union[Unset, str]): The the plain text that comprises this note.
        html_note (Union[Unset, str]): The the html that comprises this note.
    """

    constituent_id: str
    date_entered: datetime.datetime
    note_type: str
    context_type: Union[Unset, int] = UNSET
    title: Union[Unset, str] = UNSET
    author_id: Union[Unset, str] = UNSET
    text_note: Union[Unset, str] = UNSET
    html_note: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        date_entered = self.date_entered.isoformat()

        note_type = self.note_type

        context_type = self.context_type

        title = self.title

        author_id = self.author_id

        text_note = self.text_note

        html_note = self.html_note

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "constituent_id": constituent_id,
                "date_entered": date_entered,
                "note_type": note_type,
            }
        )
        if context_type is not UNSET:
            field_dict["context_type"] = context_type
        if title is not UNSET:
            field_dict["title"] = title
        if author_id is not UNSET:
            field_dict["author_id"] = author_id
        if text_note is not UNSET:
            field_dict["text_note"] = text_note
        if html_note is not UNSET:
            field_dict["html_note"] = html_note

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        constituent_id = d.pop("constituent_id")

        date_entered = isoparse(d.pop("date_entered"))

        note_type = d.pop("note_type")

        context_type = d.pop("context_type", UNSET)

        title = d.pop("title", UNSET)

        author_id = d.pop("author_id", UNSET)

        text_note = d.pop("text_note", UNSET)

        html_note = d.pop("html_note", UNSET)

        new_constituent_note = cls(
            constituent_id=constituent_id,
            date_entered=date_entered,
            note_type=note_type,
            context_type=context_type,
            title=title,
            author_id=author_id,
            text_note=text_note,
            html_note=html_note,
        )

        return new_constituent_note
