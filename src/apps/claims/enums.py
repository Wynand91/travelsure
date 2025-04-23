from enum import IntEnum


class ClaimStatus(IntEnum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2