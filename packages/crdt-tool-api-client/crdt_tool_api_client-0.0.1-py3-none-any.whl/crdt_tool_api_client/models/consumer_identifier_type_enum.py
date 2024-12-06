from enum import Enum


class ConsumerIdentifierTypeEnum(str, Enum):
    CREDIT_FACILITIES = "Credit facilities"
    DEVELOPMENTAL_CREDIT = "Developmental credit"
    EDUCATIONAL_LOANS = "Educational loans"
    INCIDENTAL_CREDIT_AGREEMENTS = "Incidental credit agreements"
    MORTGAGES = "Mortgages"
    PAWN_TRANSACTIONS = "Pawn transactions"
    PUBLIC_INTEREST_CREDIT_AGREEMENTS = "Public interest credit agreements"
    SECURED_CREDIT = "Secured credit"
    SHORT_TERM_CREDIT = "Short-term credit"
    UNSECURED_CREDIT = "Unsecured credit"

    def __str__(self) -> str:
        return str(self.value)
