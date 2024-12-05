import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.method_ad_method_type_id import MethodADMethodTypeId
from ..models.method_status_enum import MethodStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file import File


T = TypeVar("T", bound="MethodAD")


@_attrs_define
class MethodAD:
    """
    Attributes:
        method_id (UUID):
        name (str):
        location_id (UUID):
        method_status_id (MethodStatusEnum): (
            PLANNED=1,
            READY=2,
            CONDUCTED=3,
            VOIDED=4,
            APPROVED=5,
            )
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        remarks (Union[None, Unset, str]):
        method_type_id (Union[Unset, MethodADMethodTypeId]):  Default: MethodADMethodTypeId.VALUE_17.
        created_by (Union[None, Unset, str]):
        updated_by (Union[None, Unset, str]):
        conducted_at (Union[None, Unset, datetime.datetime]):
        conducted_by (Union[None, Unset, str]):
        files (Union[Unset, List['File']]):
        self_ (Union[None, Unset, str]):
    """

    method_id: UUID
    name: str
    location_id: UUID
    method_status_id: MethodStatusEnum
    created_at: datetime.datetime
    updated_at: datetime.datetime
    remarks: Union[None, Unset, str] = UNSET
    method_type_id: Union[Unset, MethodADMethodTypeId] = MethodADMethodTypeId.VALUE_17
    created_by: Union[None, Unset, str] = UNSET
    updated_by: Union[None, Unset, str] = UNSET
    conducted_at: Union[None, Unset, datetime.datetime] = UNSET
    conducted_by: Union[None, Unset, str] = UNSET
    files: Union[Unset, List["File"]] = UNSET
    self_: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        method_id = str(self.method_id)

        name = self.name

        location_id = str(self.location_id)

        method_status_id = self.method_status_id.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        remarks: Union[None, Unset, str]
        if isinstance(self.remarks, Unset):
            remarks = UNSET
        else:
            remarks = self.remarks

        method_type_id: Union[Unset, int] = UNSET
        if not isinstance(self.method_type_id, Unset):
            method_type_id = self.method_type_id.value

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        updated_by: Union[None, Unset, str]
        if isinstance(self.updated_by, Unset):
            updated_by = UNSET
        else:
            updated_by = self.updated_by

        conducted_at: Union[None, Unset, str]
        if isinstance(self.conducted_at, Unset):
            conducted_at = UNSET
        elif isinstance(self.conducted_at, datetime.datetime):
            conducted_at = self.conducted_at.isoformat()
        else:
            conducted_at = self.conducted_at

        conducted_by: Union[None, Unset, str]
        if isinstance(self.conducted_by, Unset):
            conducted_by = UNSET
        else:
            conducted_by = self.conducted_by

        files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        self_: Union[None, Unset, str]
        if isinstance(self.self_, Unset):
            self_ = UNSET
        else:
            self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method_id": method_id,
                "name": name,
                "location_id": location_id,
                "method_status_id": method_status_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if remarks is not UNSET:
            field_dict["remarks"] = remarks
        if method_type_id is not UNSET:
            field_dict["method_type_id"] = method_type_id
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if conducted_at is not UNSET:
            field_dict["conducted_at"] = conducted_at
        if conducted_by is not UNSET:
            field_dict["conducted_by"] = conducted_by
        if files is not UNSET:
            field_dict["files"] = files
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file import File

        d = src_dict.copy()
        method_id = UUID(d.pop("method_id"))

        name = d.pop("name")

        location_id = UUID(d.pop("location_id"))

        method_status_id = MethodStatusEnum(d.pop("method_status_id"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_remarks(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remarks = _parse_remarks(d.pop("remarks", UNSET))

        _method_type_id = d.pop("method_type_id", UNSET)
        method_type_id: Union[Unset, MethodADMethodTypeId]
        if isinstance(_method_type_id, Unset):
            method_type_id = UNSET
        else:
            method_type_id = MethodADMethodTypeId(_method_type_id)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_updated_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        updated_by = _parse_updated_by(d.pop("updated_by", UNSET))

        def _parse_conducted_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                conducted_at_type_0 = isoparse(data)

                return conducted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        conducted_at = _parse_conducted_at(d.pop("conducted_at", UNSET))

        def _parse_conducted_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        conducted_by = _parse_conducted_by(d.pop("conducted_by", UNSET))

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = File.from_dict(files_item_data)

            files.append(files_item)

        def _parse_self_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        self_ = _parse_self_(d.pop("self", UNSET))

        method_ad = cls(
            method_id=method_id,
            name=name,
            location_id=location_id,
            method_status_id=method_status_id,
            created_at=created_at,
            updated_at=updated_at,
            remarks=remarks,
            method_type_id=method_type_id,
            created_by=created_by,
            updated_by=updated_by,
            conducted_at=conducted_at,
            conducted_by=conducted_by,
            files=files,
            self_=self_,
        )

        method_ad.additional_properties = d
        return method_ad

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
