"""Contains all the data models used in inputs/outputs"""

from .consumer_identifier_type_enum import ConsumerIdentifierTypeEnum
from .crdt_user import CrdtUser
from .credit_product import CreditProduct
from .credit_type_enum import CreditTypeEnum
from .customer import Customer
from .group import Group
from .lead import Lead
from .patched_crdt_user import PatchedCrdtUser
from .patched_credit_product import PatchedCreditProduct
from .patched_customer import PatchedCustomer
from .patched_group import PatchedGroup
from .patched_lead import PatchedLead
from .patched_permission import PatchedPermission
from .permission import Permission

__all__ = (
    "ConsumerIdentifierTypeEnum",
    "CrdtUser",
    "CreditProduct",
    "CreditTypeEnum",
    "Customer",
    "Group",
    "Lead",
    "PatchedCrdtUser",
    "PatchedCreditProduct",
    "PatchedCustomer",
    "PatchedGroup",
    "PatchedLead",
    "PatchedPermission",
    "Permission",
)
