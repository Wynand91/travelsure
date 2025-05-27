from enum import IntEnum


class PolicyType(IntEnum):
    BASIC = 1
    STANDARD = 2
    PREMIUM = 3


class PolicyStatus(IntEnum):
    PENDING = 1
    ACTIVE = 2
    EXPIRED = 3
    CANCELLED = 4


class Destination(IntEnum):
    EUROPE = 1
    AFRICA = 2
    OCEANIA = 3
    ASIA = 4
    NORTH_AMERICA = 5
    SOUTH_AMERICA = 6
    ANTARCTICA = 7
