import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.consumer_identifier_type_enum import ConsumerIdentifierTypeEnum
from ..models.credit_type_enum import CreditTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreditProductResponse")


@_attrs_define
class CreditProductResponse:
    """A base serializer for response operations (list/retrieve).
    Includes all fields, including server-managed fields.

        Attributes:
            id (int):
            created_at (datetime.datetime): Date and time when the record was created.
            updated_at (datetime.datetime): Date and time when the record was last updated.
            deleted_at (Union[None, datetime.datetime]): Timestamp of when the record was soft deleted.
            name (str): The name of the credit product.
            description (str): A description of the credit product.
            interest_rate (float): The annual interest rate for the credit product.
            credit_type (CreditTypeEnum): * `Mortgages` - Mortgages
                * `Secured credit` - Secured credit
                * `Credit facilities` - Credit facilities
                * `Unsecured credit` - Unsecured credit
                * `Short-term credit` - Short-term credit
                * `Developmental credit` - Developmental credit
                * `Pawn transactions` - Pawn transactions
                * `Incidental credit agreements` - Incidental credit agreements
                * `Educational loans` - Educational loans
                * `Public interest credit agreements` - Public interest credit agreements
            fees (Any): A list of fees associated with the credit product.
            minimum_loan_amount_in_cents (int): The minimum loan amount for the credit product (in cents).
            maximum_loan_amount_in_cents (int): The maximum loan amount for the credit product (in cents).
            minimum_loan_term_in_months (int): The minimum loan term, in months, for the credit product.
            maximum_loan_term_in_months (int): The maximum loan term, in months, for the credit product.
            consumer_identifier_type (ConsumerIdentifierTypeEnum): * `Mortgages` - Mortgages
                * `Secured credit` - Secured credit
                * `Credit facilities` - Credit facilities
                * `Unsecured credit` - Unsecured credit
                * `Short-term credit` - Short-term credit
                * `Developmental credit` - Developmental credit
                * `Pawn transactions` - Pawn transactions
                * `Incidental credit agreements` - Incidental credit agreements
                * `Educational loans` - Educational loans
                * `Public interest credit agreements` - Public interest credit agreements
            metadata (Any): Additional metadata for the credit product.
            created_by (int): User who created the record.
            updated_by (Union[None, int]): User who updated the record.
            deleted_by (Union[None, int]): User who deleted the record.
            tenant (int):
            minimum_deposit_amount_in_cents (Union[None, Unset, int]): The minimum deposit amount for the credit product (in
                cents).
            maximum_deposit_amount_in_cents (Union[None, Unset, int]): The maximum deposit amount for the credit product (in
                cents).
    """

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Union[None, datetime.datetime]
    name: str
    description: str
    interest_rate: float
    credit_type: CreditTypeEnum
    fees: Any
    minimum_loan_amount_in_cents: int
    maximum_loan_amount_in_cents: int
    minimum_loan_term_in_months: int
    maximum_loan_term_in_months: int
    consumer_identifier_type: ConsumerIdentifierTypeEnum
    metadata: Any
    created_by: int
    updated_by: Union[None, int]
    deleted_by: Union[None, int]
    tenant: int
    minimum_deposit_amount_in_cents: Union[None, Unset, int] = UNSET
    maximum_deposit_amount_in_cents: Union[None, Unset, int] = UNSET
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

        description = self.description

        interest_rate = self.interest_rate

        credit_type = self.credit_type.value

        fees = self.fees

        minimum_loan_amount_in_cents = self.minimum_loan_amount_in_cents

        maximum_loan_amount_in_cents = self.maximum_loan_amount_in_cents

        minimum_loan_term_in_months = self.minimum_loan_term_in_months

        maximum_loan_term_in_months = self.maximum_loan_term_in_months

        consumer_identifier_type = self.consumer_identifier_type.value

        metadata = self.metadata

        created_by = self.created_by

        updated_by: Union[None, int]
        updated_by = self.updated_by

        deleted_by: Union[None, int]
        deleted_by = self.deleted_by

        tenant = self.tenant

        minimum_deposit_amount_in_cents: Union[None, Unset, int]
        if isinstance(self.minimum_deposit_amount_in_cents, Unset):
            minimum_deposit_amount_in_cents = UNSET
        else:
            minimum_deposit_amount_in_cents = self.minimum_deposit_amount_in_cents

        maximum_deposit_amount_in_cents: Union[None, Unset, int]
        if isinstance(self.maximum_deposit_amount_in_cents, Unset):
            maximum_deposit_amount_in_cents = UNSET
        else:
            maximum_deposit_amount_in_cents = self.maximum_deposit_amount_in_cents

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "deleted_at": deleted_at,
                "name": name,
                "description": description,
                "interest_rate": interest_rate,
                "credit_type": credit_type,
                "fees": fees,
                "minimum_loan_amount_in_cents": minimum_loan_amount_in_cents,
                "maximum_loan_amount_in_cents": maximum_loan_amount_in_cents,
                "minimum_loan_term_in_months": minimum_loan_term_in_months,
                "maximum_loan_term_in_months": maximum_loan_term_in_months,
                "consumer_identifier_type": consumer_identifier_type,
                "metadata": metadata,
                "created_by": created_by,
                "updated_by": updated_by,
                "deleted_by": deleted_by,
                "tenant": tenant,
            }
        )
        if minimum_deposit_amount_in_cents is not UNSET:
            field_dict["minimum_deposit_amount_in_cents"] = minimum_deposit_amount_in_cents
        if maximum_deposit_amount_in_cents is not UNSET:
            field_dict["maximum_deposit_amount_in_cents"] = maximum_deposit_amount_in_cents

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

        description = d.pop("description")

        interest_rate = d.pop("interest_rate")

        credit_type = CreditTypeEnum(d.pop("credit_type"))

        fees = d.pop("fees")

        minimum_loan_amount_in_cents = d.pop("minimum_loan_amount_in_cents")

        maximum_loan_amount_in_cents = d.pop("maximum_loan_amount_in_cents")

        minimum_loan_term_in_months = d.pop("minimum_loan_term_in_months")

        maximum_loan_term_in_months = d.pop("maximum_loan_term_in_months")

        consumer_identifier_type = ConsumerIdentifierTypeEnum(d.pop("consumer_identifier_type"))

        metadata = d.pop("metadata")

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

        def _parse_minimum_deposit_amount_in_cents(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        minimum_deposit_amount_in_cents = _parse_minimum_deposit_amount_in_cents(
            d.pop("minimum_deposit_amount_in_cents", UNSET)
        )

        def _parse_maximum_deposit_amount_in_cents(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        maximum_deposit_amount_in_cents = _parse_maximum_deposit_amount_in_cents(
            d.pop("maximum_deposit_amount_in_cents", UNSET)
        )

        credit_product_response = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            name=name,
            description=description,
            interest_rate=interest_rate,
            credit_type=credit_type,
            fees=fees,
            minimum_loan_amount_in_cents=minimum_loan_amount_in_cents,
            maximum_loan_amount_in_cents=maximum_loan_amount_in_cents,
            minimum_loan_term_in_months=minimum_loan_term_in_months,
            maximum_loan_term_in_months=maximum_loan_term_in_months,
            consumer_identifier_type=consumer_identifier_type,
            metadata=metadata,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            tenant=tenant,
            minimum_deposit_amount_in_cents=minimum_deposit_amount_in_cents,
            maximum_deposit_amount_in_cents=maximum_deposit_amount_in_cents,
        )

        credit_product_response.additional_properties = d
        return credit_product_response

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
