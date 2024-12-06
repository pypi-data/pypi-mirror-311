from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.consumer_identifier_type_enum import ConsumerIdentifierTypeEnum
from ..models.credit_type_enum import CreditTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCreditProductRequest")


@_attrs_define
class PatchedCreditProductRequest:
    """A base serializer for request operations (create/update).
    Dynamically excludes server-managed fields.

        Attributes:
            name (Union[Unset, str]): The name of the credit product.
            description (Union[Unset, str]): A description of the credit product.
            interest_rate (Union[Unset, float]): The annual interest rate for the credit product.
            credit_type (Union[Unset, CreditTypeEnum]): * `Mortgages` - Mortgages
                * `Secured credit` - Secured credit
                * `Credit facilities` - Credit facilities
                * `Unsecured credit` - Unsecured credit
                * `Short-term credit` - Short-term credit
                * `Developmental credit` - Developmental credit
                * `Pawn transactions` - Pawn transactions
                * `Incidental credit agreements` - Incidental credit agreements
                * `Educational loans` - Educational loans
                * `Public interest credit agreements` - Public interest credit agreements
            fees (Union[Unset, Any]): A list of fees associated with the credit product.
            minimum_loan_amount_in_cents (Union[Unset, int]): The minimum loan amount for the credit product (in cents).
            maximum_loan_amount_in_cents (Union[Unset, int]): The maximum loan amount for the credit product (in cents).
            minimum_loan_term_in_months (Union[Unset, int]): The minimum loan term, in months, for the credit product.
            maximum_loan_term_in_months (Union[Unset, int]): The maximum loan term, in months, for the credit product.
            minimum_deposit_amount_in_cents (Union[None, Unset, int]): The minimum deposit amount for the credit product (in
                cents).
            maximum_deposit_amount_in_cents (Union[None, Unset, int]): The maximum deposit amount for the credit product (in
                cents).
            consumer_identifier_type (Union[Unset, ConsumerIdentifierTypeEnum]): * `Mortgages` - Mortgages
                * `Secured credit` - Secured credit
                * `Credit facilities` - Credit facilities
                * `Unsecured credit` - Unsecured credit
                * `Short-term credit` - Short-term credit
                * `Developmental credit` - Developmental credit
                * `Pawn transactions` - Pawn transactions
                * `Incidental credit agreements` - Incidental credit agreements
                * `Educational loans` - Educational loans
                * `Public interest credit agreements` - Public interest credit agreements
            metadata (Union[Unset, Any]): Additional metadata for the credit product.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    interest_rate: Union[Unset, float] = UNSET
    credit_type: Union[Unset, CreditTypeEnum] = UNSET
    fees: Union[Unset, Any] = UNSET
    minimum_loan_amount_in_cents: Union[Unset, int] = UNSET
    maximum_loan_amount_in_cents: Union[Unset, int] = UNSET
    minimum_loan_term_in_months: Union[Unset, int] = UNSET
    maximum_loan_term_in_months: Union[Unset, int] = UNSET
    minimum_deposit_amount_in_cents: Union[None, Unset, int] = UNSET
    maximum_deposit_amount_in_cents: Union[None, Unset, int] = UNSET
    consumer_identifier_type: Union[Unset, ConsumerIdentifierTypeEnum] = UNSET
    metadata: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        interest_rate = self.interest_rate

        credit_type: Union[Unset, str] = UNSET
        if not isinstance(self.credit_type, Unset):
            credit_type = self.credit_type.value

        fees = self.fees

        minimum_loan_amount_in_cents = self.minimum_loan_amount_in_cents

        maximum_loan_amount_in_cents = self.maximum_loan_amount_in_cents

        minimum_loan_term_in_months = self.minimum_loan_term_in_months

        maximum_loan_term_in_months = self.maximum_loan_term_in_months

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

        consumer_identifier_type: Union[Unset, str] = UNSET
        if not isinstance(self.consumer_identifier_type, Unset):
            consumer_identifier_type = self.consumer_identifier_type.value

        metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if interest_rate is not UNSET:
            field_dict["interest_rate"] = interest_rate
        if credit_type is not UNSET:
            field_dict["credit_type"] = credit_type
        if fees is not UNSET:
            field_dict["fees"] = fees
        if minimum_loan_amount_in_cents is not UNSET:
            field_dict["minimum_loan_amount_in_cents"] = minimum_loan_amount_in_cents
        if maximum_loan_amount_in_cents is not UNSET:
            field_dict["maximum_loan_amount_in_cents"] = maximum_loan_amount_in_cents
        if minimum_loan_term_in_months is not UNSET:
            field_dict["minimum_loan_term_in_months"] = minimum_loan_term_in_months
        if maximum_loan_term_in_months is not UNSET:
            field_dict["maximum_loan_term_in_months"] = maximum_loan_term_in_months
        if minimum_deposit_amount_in_cents is not UNSET:
            field_dict["minimum_deposit_amount_in_cents"] = minimum_deposit_amount_in_cents
        if maximum_deposit_amount_in_cents is not UNSET:
            field_dict["maximum_deposit_amount_in_cents"] = maximum_deposit_amount_in_cents
        if consumer_identifier_type is not UNSET:
            field_dict["consumer_identifier_type"] = consumer_identifier_type
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        interest_rate = (
            self.interest_rate
            if isinstance(self.interest_rate, Unset)
            else (None, str(self.interest_rate).encode(), "text/plain")
        )

        credit_type: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.credit_type, Unset):
            credit_type = (None, str(self.credit_type.value).encode(), "text/plain")

        fees = self.fees if isinstance(self.fees, Unset) else (None, str(self.fees).encode(), "text/plain")

        minimum_loan_amount_in_cents = (
            self.minimum_loan_amount_in_cents
            if isinstance(self.minimum_loan_amount_in_cents, Unset)
            else (None, str(self.minimum_loan_amount_in_cents).encode(), "text/plain")
        )

        maximum_loan_amount_in_cents = (
            self.maximum_loan_amount_in_cents
            if isinstance(self.maximum_loan_amount_in_cents, Unset)
            else (None, str(self.maximum_loan_amount_in_cents).encode(), "text/plain")
        )

        minimum_loan_term_in_months = (
            self.minimum_loan_term_in_months
            if isinstance(self.minimum_loan_term_in_months, Unset)
            else (None, str(self.minimum_loan_term_in_months).encode(), "text/plain")
        )

        maximum_loan_term_in_months = (
            self.maximum_loan_term_in_months
            if isinstance(self.maximum_loan_term_in_months, Unset)
            else (None, str(self.maximum_loan_term_in_months).encode(), "text/plain")
        )

        minimum_deposit_amount_in_cents: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.minimum_deposit_amount_in_cents, Unset):
            minimum_deposit_amount_in_cents = UNSET
        elif isinstance(self.minimum_deposit_amount_in_cents, int):
            minimum_deposit_amount_in_cents = (None, str(self.minimum_deposit_amount_in_cents).encode(), "text/plain")
        else:
            minimum_deposit_amount_in_cents = (None, str(self.minimum_deposit_amount_in_cents).encode(), "text/plain")

        maximum_deposit_amount_in_cents: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.maximum_deposit_amount_in_cents, Unset):
            maximum_deposit_amount_in_cents = UNSET
        elif isinstance(self.maximum_deposit_amount_in_cents, int):
            maximum_deposit_amount_in_cents = (None, str(self.maximum_deposit_amount_in_cents).encode(), "text/plain")
        else:
            maximum_deposit_amount_in_cents = (None, str(self.maximum_deposit_amount_in_cents).encode(), "text/plain")

        consumer_identifier_type: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.consumer_identifier_type, Unset):
            consumer_identifier_type = (None, str(self.consumer_identifier_type.value).encode(), "text/plain")

        metadata = (
            self.metadata if isinstance(self.metadata, Unset) else (None, str(self.metadata).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if interest_rate is not UNSET:
            field_dict["interest_rate"] = interest_rate
        if credit_type is not UNSET:
            field_dict["credit_type"] = credit_type
        if fees is not UNSET:
            field_dict["fees"] = fees
        if minimum_loan_amount_in_cents is not UNSET:
            field_dict["minimum_loan_amount_in_cents"] = minimum_loan_amount_in_cents
        if maximum_loan_amount_in_cents is not UNSET:
            field_dict["maximum_loan_amount_in_cents"] = maximum_loan_amount_in_cents
        if minimum_loan_term_in_months is not UNSET:
            field_dict["minimum_loan_term_in_months"] = minimum_loan_term_in_months
        if maximum_loan_term_in_months is not UNSET:
            field_dict["maximum_loan_term_in_months"] = maximum_loan_term_in_months
        if minimum_deposit_amount_in_cents is not UNSET:
            field_dict["minimum_deposit_amount_in_cents"] = minimum_deposit_amount_in_cents
        if maximum_deposit_amount_in_cents is not UNSET:
            field_dict["maximum_deposit_amount_in_cents"] = maximum_deposit_amount_in_cents
        if consumer_identifier_type is not UNSET:
            field_dict["consumer_identifier_type"] = consumer_identifier_type
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        interest_rate = d.pop("interest_rate", UNSET)

        _credit_type = d.pop("credit_type", UNSET)
        credit_type: Union[Unset, CreditTypeEnum]
        if isinstance(_credit_type, Unset):
            credit_type = UNSET
        else:
            credit_type = CreditTypeEnum(_credit_type)

        fees = d.pop("fees", UNSET)

        minimum_loan_amount_in_cents = d.pop("minimum_loan_amount_in_cents", UNSET)

        maximum_loan_amount_in_cents = d.pop("maximum_loan_amount_in_cents", UNSET)

        minimum_loan_term_in_months = d.pop("minimum_loan_term_in_months", UNSET)

        maximum_loan_term_in_months = d.pop("maximum_loan_term_in_months", UNSET)

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

        _consumer_identifier_type = d.pop("consumer_identifier_type", UNSET)
        consumer_identifier_type: Union[Unset, ConsumerIdentifierTypeEnum]
        if isinstance(_consumer_identifier_type, Unset):
            consumer_identifier_type = UNSET
        else:
            consumer_identifier_type = ConsumerIdentifierTypeEnum(_consumer_identifier_type)

        metadata = d.pop("metadata", UNSET)

        patched_credit_product_request = cls(
            name=name,
            description=description,
            interest_rate=interest_rate,
            credit_type=credit_type,
            fees=fees,
            minimum_loan_amount_in_cents=minimum_loan_amount_in_cents,
            maximum_loan_amount_in_cents=maximum_loan_amount_in_cents,
            minimum_loan_term_in_months=minimum_loan_term_in_months,
            maximum_loan_term_in_months=maximum_loan_term_in_months,
            minimum_deposit_amount_in_cents=minimum_deposit_amount_in_cents,
            maximum_deposit_amount_in_cents=maximum_deposit_amount_in_cents,
            consumer_identifier_type=consumer_identifier_type,
            metadata=metadata,
        )

        patched_credit_product_request.additional_properties = d
        return patched_credit_product_request

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
