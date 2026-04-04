from enum import StrEnum


class UserRoles(StrEnum):
    FREE_USER = "free_user"
    PAID_USER = "paid_user"
    SPECIALIST = "specialist"
    ADMIN = "admin"
