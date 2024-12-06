from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewConstituentMerge")


@_attrs_define
class NewConstituentMerge:
    """CreateMergeTwoConstituents.

    Example:
        {'source_id': '', 'target_id': '', 'config': '', 'delete_source': False, 'constituent_inactivity_reason_code':
            '', 'constituent_inactivity_details': '', 'delete_source_constituent': 'Delete source constituent'}

    Attributes:
        source_id (str): The the constituent whose data will be merged into the target constituent..
        target_id (str): The the constituent record that will represent the consolidated view of the constituent's data
            after the merge has completed..
        config (str): The the merge configuration that will be used to merge the two constituents.. This simple list can
            be queried at https://api.sky.blackbaud.com/crm-adnmg/simplelists/c18b465c-c012-4839-952b-4bb8aae7cb3f.
        delete_source (bool): Indicates whether if true then the source constituent will be deleted after the merge
            operation is complete..
        delete_source_constituent (str): The delete source constituent. Available values are <i>delete source
            constituent</i>, <i>mark source constituent inactive</i>
        constituent_inactivity_reason_code (Union[Unset, str]): The inactive reason. This simple list can be queried at
            https://api.sky.blackbaud.com/crm-adnmg/simplelists/71b29b04-d70f-4d38-bab1-e44a2528d0e8.
        constituent_inactivity_details (Union[Unset, str]): The inactive details.
    """

    source_id: str
    target_id: str
    config: str
    delete_source: bool
    delete_source_constituent: str
    constituent_inactivity_reason_code: Union[Unset, str] = UNSET
    constituent_inactivity_details: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        source_id = self.source_id

        target_id = self.target_id

        config = self.config

        delete_source = self.delete_source

        delete_source_constituent = self.delete_source_constituent

        constituent_inactivity_reason_code = self.constituent_inactivity_reason_code

        constituent_inactivity_details = self.constituent_inactivity_details

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "source_id": source_id,
                "target_id": target_id,
                "config": config,
                "delete_source": delete_source,
                "delete_source_constituent": delete_source_constituent,
            }
        )
        if constituent_inactivity_reason_code is not UNSET:
            field_dict["constituent_inactivity_reason_code"] = constituent_inactivity_reason_code
        if constituent_inactivity_details is not UNSET:
            field_dict["constituent_inactivity_details"] = constituent_inactivity_details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source_id = d.pop("source_id")

        target_id = d.pop("target_id")

        config = d.pop("config")

        delete_source = d.pop("delete_source")

        delete_source_constituent = d.pop("delete_source_constituent")

        constituent_inactivity_reason_code = d.pop("constituent_inactivity_reason_code", UNSET)

        constituent_inactivity_details = d.pop("constituent_inactivity_details", UNSET)

        new_constituent_merge = cls(
            source_id=source_id,
            target_id=target_id,
            config=config,
            delete_source=delete_source,
            delete_source_constituent=delete_source_constituent,
            constituent_inactivity_reason_code=constituent_inactivity_reason_code,
            constituent_inactivity_details=constituent_inactivity_details,
        )

        return new_constituent_merge
