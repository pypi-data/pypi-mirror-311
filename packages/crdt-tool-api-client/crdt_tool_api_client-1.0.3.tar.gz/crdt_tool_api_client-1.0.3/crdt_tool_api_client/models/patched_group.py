import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedGroup")


@_attrs_define
class PatchedGroup:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        permissions (Union[Unset, List[int]]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    permissions: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        permissions: Union[Unset, List[int]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = self.id if isinstance(self.id, Unset) else (None, str(self.id).encode(), "text/plain")

        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        permissions: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.permissions, Unset):
            _temp_permissions = self.permissions
            permissions = (None, json.dumps(_temp_permissions).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        permissions = cast(List[int], d.pop("permissions", UNSET))

        patched_group = cls(
            id=id,
            name=name,
            permissions=permissions,
        )

        patched_group.additional_properties = d
        return patched_group

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
