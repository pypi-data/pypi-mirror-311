import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Lead")


@_attrs_define
class Lead:
    """Serializer for the Lead model.

    Attributes:
        id (int):
        created_at (datetime.datetime): Date and time when the record was created.
        updated_at (datetime.datetime): Date and time when the record was last updated.
        deleted_at (Union[None, datetime.datetime]): Timestamp of when the record was soft deleted.
        name (str): The name of the lead.
        surname (str): The surname of the lead.
        email (str): The email address of the lead.
        email_confirmed (bool): Indicates whether the email address has been confirmed.
        phone (str): The phone number of the lead.
        created_by (int): User who created the record.
        updated_by (Union[None, int]): User who updated the record.
        deleted_by (Union[None, int]): User who deleted the record.
        tenant (int):
        source (int): The source from which the lead was acquired.
        metadata (Union[Unset, Any]): JSON field for arbitrary user data.
        phone_confirmed (Union[Unset, bool]): Indicates whether the phone number has been confirmed.
        import_record (Union[None, Unset, int]): The import record associated with the lead, if any.
        qualification_rule (Union[None, Unset, int]): The qualification rule applied to the lead, if any.
        stage (Union[None, Unset, int]): The current stage of the lead in the sales pipeline, if any.
    """

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Union[None, datetime.datetime]
    name: str
    surname: str
    email: str
    email_confirmed: bool
    phone: str
    created_by: int
    updated_by: Union[None, int]
    deleted_by: Union[None, int]
    tenant: int
    source: int
    metadata: Union[Unset, Any] = UNSET
    phone_confirmed: Union[Unset, bool] = UNSET
    import_record: Union[None, Unset, int] = UNSET
    qualification_rule: Union[None, Unset, int] = UNSET
    stage: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        deleted_at: Union[None, str]
        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        name = self.name

        surname = self.surname

        email = self.email

        email_confirmed = self.email_confirmed

        phone = self.phone

        created_by = self.created_by

        updated_by: Union[None, int]
        updated_by = self.updated_by

        deleted_by: Union[None, int]
        deleted_by = self.deleted_by

        tenant = self.tenant

        source = self.source

        metadata = self.metadata

        phone_confirmed = self.phone_confirmed

        import_record: Union[None, Unset, int]
        if isinstance(self.import_record, Unset):
            import_record = UNSET
        else:
            import_record = self.import_record

        qualification_rule: Union[None, Unset, int]
        if isinstance(self.qualification_rule, Unset):
            qualification_rule = UNSET
        else:
            qualification_rule = self.qualification_rule

        stage: Union[None, Unset, int]
        if isinstance(self.stage, Unset):
            stage = UNSET
        else:
            stage = self.stage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "deleted_at": deleted_at,
                "name": name,
                "surname": surname,
                "email": email,
                "email_confirmed": email_confirmed,
                "phone": phone,
                "created_by": created_by,
                "updated_by": updated_by,
                "deleted_by": deleted_by,
                "tenant": tenant,
                "source": source,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if phone_confirmed is not UNSET:
            field_dict["phone_confirmed"] = phone_confirmed
        if import_record is not UNSET:
            field_dict["import_record"] = import_record
        if qualification_rule is not UNSET:
            field_dict["qualification_rule"] = qualification_rule
        if stage is not UNSET:
            field_dict["stage"] = stage

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        created_at = self.created_at.isoformat().encode()

        updated_at = self.updated_at.isoformat().encode()

        deleted_at: Tuple[None, bytes, str]

        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat().encode()
        else:
            deleted_at = (None, str(self.deleted_at).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        surname = (None, str(self.surname).encode(), "text/plain")

        email = (None, str(self.email).encode(), "text/plain")

        email_confirmed = (None, str(self.email_confirmed).encode(), "text/plain")

        phone = (None, str(self.phone).encode(), "text/plain")

        created_by = (None, str(self.created_by).encode(), "text/plain")

        updated_by: Tuple[None, bytes, str]

        if isinstance(self.updated_by, int):
            updated_by = (None, str(self.updated_by).encode(), "text/plain")
        else:
            updated_by = (None, str(self.updated_by).encode(), "text/plain")

        deleted_by: Tuple[None, bytes, str]

        if isinstance(self.deleted_by, int):
            deleted_by = (None, str(self.deleted_by).encode(), "text/plain")
        else:
            deleted_by = (None, str(self.deleted_by).encode(), "text/plain")

        tenant = (None, str(self.tenant).encode(), "text/plain")

        source = (None, str(self.source).encode(), "text/plain")

        metadata = (
            self.metadata if isinstance(self.metadata, Unset) else (None, str(self.metadata).encode(), "text/plain")
        )

        phone_confirmed = (
            self.phone_confirmed
            if isinstance(self.phone_confirmed, Unset)
            else (None, str(self.phone_confirmed).encode(), "text/plain")
        )

        import_record: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.import_record, Unset):
            import_record = UNSET
        elif isinstance(self.import_record, int):
            import_record = (None, str(self.import_record).encode(), "text/plain")
        else:
            import_record = (None, str(self.import_record).encode(), "text/plain")

        qualification_rule: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.qualification_rule, Unset):
            qualification_rule = UNSET
        elif isinstance(self.qualification_rule, int):
            qualification_rule = (None, str(self.qualification_rule).encode(), "text/plain")
        else:
            qualification_rule = (None, str(self.qualification_rule).encode(), "text/plain")

        stage: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.stage, Unset):
            stage = UNSET
        elif isinstance(self.stage, int):
            stage = (None, str(self.stage).encode(), "text/plain")
        else:
            stage = (None, str(self.stage).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "deleted_at": deleted_at,
                "name": name,
                "surname": surname,
                "email": email,
                "email_confirmed": email_confirmed,
                "phone": phone,
                "created_by": created_by,
                "updated_by": updated_by,
                "deleted_by": deleted_by,
                "tenant": tenant,
                "source": source,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if phone_confirmed is not UNSET:
            field_dict["phone_confirmed"] = phone_confirmed
        if import_record is not UNSET:
            field_dict["import_record"] = import_record
        if qualification_rule is not UNSET:
            field_dict["qualification_rule"] = qualification_rule
        if stage is not UNSET:
            field_dict["stage"] = stage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_deleted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at"))

        name = d.pop("name")

        surname = d.pop("surname")

        email = d.pop("email")

        email_confirmed = d.pop("email_confirmed")

        phone = d.pop("phone")

        created_by = d.pop("created_by")

        def _parse_updated_by(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        updated_by = _parse_updated_by(d.pop("updated_by"))

        def _parse_deleted_by(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        deleted_by = _parse_deleted_by(d.pop("deleted_by"))

        tenant = d.pop("tenant")

        source = d.pop("source")

        metadata = d.pop("metadata", UNSET)

        phone_confirmed = d.pop("phone_confirmed", UNSET)

        def _parse_import_record(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        import_record = _parse_import_record(d.pop("import_record", UNSET))

        def _parse_qualification_rule(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        qualification_rule = _parse_qualification_rule(d.pop("qualification_rule", UNSET))

        def _parse_stage(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stage = _parse_stage(d.pop("stage", UNSET))

        lead = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            name=name,
            surname=surname,
            email=email,
            email_confirmed=email_confirmed,
            phone=phone,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            tenant=tenant,
            source=source,
            metadata=metadata,
            phone_confirmed=phone_confirmed,
            import_record=import_record,
            qualification_rule=qualification_rule,
            stage=stage,
        )

        lead.additional_properties = d
        return lead

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
