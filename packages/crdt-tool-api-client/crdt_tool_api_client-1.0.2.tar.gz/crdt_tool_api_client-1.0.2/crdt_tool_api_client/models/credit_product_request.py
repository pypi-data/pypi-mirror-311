from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.consumer_identifier_type_enum import ConsumerIdentifierTypeEnum
from ..models.credit_type_enum import CreditTypeEnum

T = TypeVar("T", bound="CreditProductRequest")


@_attrs_define
class CreditProductRequest:
    """A base serializer for request operations (create/update).
    Dynamically excludes server-managed fields.

        Attributes:
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
    """

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
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
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        description = (None, str(self.description).encode(), "text/plain")

        interest_rate = (None, str(self.interest_rate).encode(), "text/plain")

        credit_type = (None, str(self.credit_type.value).encode(), "text/plain")

        fees = (None, str(self.fees).encode(), "text/plain")

        minimum_loan_amount_in_cents = (None, str(self.minimum_loan_amount_in_cents).encode(), "text/plain")

        maximum_loan_amount_in_cents = (None, str(self.maximum_loan_amount_in_cents).encode(), "text/plain")

        minimum_loan_term_in_months = (None, str(self.minimum_loan_term_in_months).encode(), "text/plain")

        maximum_loan_term_in_months = (None, str(self.maximum_loan_term_in_months).encode(), "text/plain")

        consumer_identifier_type = (None, str(self.consumer_identifier_type.value).encode(), "text/plain")

        metadata = (None, str(self.metadata).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
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
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
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

        credit_product_request = cls(
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
        )

        credit_product_request.additional_properties = d
        return credit_product_request

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
