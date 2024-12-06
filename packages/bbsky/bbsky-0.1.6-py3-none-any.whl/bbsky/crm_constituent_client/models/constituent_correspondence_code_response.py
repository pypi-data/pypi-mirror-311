from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.constituent_correspondence_code_response_responses import (
        ConstituentCorrespondenceCodeResponseResponses,
    )


T = TypeVar("T", bound="ConstituentCorrespondenceCodeResponse")


@_attrs_define
class ConstituentCorrespondenceCodeResponse:
    """GetConstituentCorrespondenceCodeResponse.

    Attributes:
        responses (Union[Unset, List['ConstituentCorrespondenceCodeResponseResponses']]): Responses.
    """

    responses: Union[Unset, List["ConstituentCorrespondenceCodeResponseResponses"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        responses: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.responses, Unset):
            responses = []
            for responses_item_data in self.responses:
                responses_item = responses_item_data.to_dict()
                responses.append(responses_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if responses is not UNSET:
            field_dict["responses"] = responses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.constituent_correspondence_code_response_responses import (
            ConstituentCorrespondenceCodeResponseResponses,
        )

        d = src_dict.copy()
        responses = []
        _responses = d.pop("responses", UNSET)
        for responses_item_data in _responses or []:
            responses_item = ConstituentCorrespondenceCodeResponseResponses.from_dict(responses_item_data)

            responses.append(responses_item)

        constituent_correspondence_code_response = cls(
            responses=responses,
        )

        return constituent_correspondence_code_response
