from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.consumer_identifier_type_enum import ConsumerIdentifierTypeEnum
from ..models.credit_type_enum import CreditTypeEnum
from ..types import UNSET, Unset

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
            minimum_deposit_amount_in_cents (Union[None, Unset, int]): The minimum deposit amount for the credit product (in
                cents).
            maximum_deposit_amount_in_cents (Union[None, Unset, int]): The maximum deposit amount for the credit product (in
                cents).
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
    minimum_deposit_amount_in_cents: Union[None, Unset, int] = UNSET
    maximum_deposit_amount_in_cents: Union[None, Unset, int] = UNSET
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
        if minimum_deposit_amount_in_cents is not UNSET:
            field_dict["minimum_deposit_amount_in_cents"] = minimum_deposit_amount_in_cents
        if maximum_deposit_amount_in_cents is not UNSET:
            field_dict["maximum_deposit_amount_in_cents"] = maximum_deposit_amount_in_cents

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
        if minimum_deposit_amount_in_cents is not UNSET:
            field_dict["minimum_deposit_amount_in_cents"] = minimum_deposit_amount_in_cents
        if maximum_deposit_amount_in_cents is not UNSET:
            field_dict["maximum_deposit_amount_in_cents"] = maximum_deposit_amount_in_cents

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
            minimum_deposit_amount_in_cents=minimum_deposit_amount_in_cents,
            maximum_deposit_amount_in_cents=maximum_deposit_amount_in_cents,
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
