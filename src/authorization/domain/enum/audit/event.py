from enum import StrEnum


class AuditEvent(StrEnum):
    REGISTER = "register"
    LOGIN = "login"
