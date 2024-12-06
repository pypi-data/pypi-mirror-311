from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstituentDuplicateMatchListSummary")


@_attrs_define
class ConstituentDuplicateMatchListSummary:
    """ListConstituentDuplicateMatches.

    Attributes:
        constituent_id (Union[Unset, str]): The constituent ID.
        match_score (Union[Unset, int]): The match score.
    """

    constituent_id: Union[Unset, str] = UNSET
    match_score: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        constituent_id = self.constituent_id

        match_score = self.match_score

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if constituent_id is not UNSET:
            field_dict["constituent_id"] = constituent_id
        if match_score is not UNSET:
            field_dict["match_score"] = match_score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        constituent_id = d.pop("constituent_id", UNSET)

        match_score = d.pop("match_score", UNSET)

        constituent_duplicate_match_list_summary = cls(
            constituent_id=constituent_id,
            match_score=match_score,
        )

        return constituent_duplicate_match_list_summary
