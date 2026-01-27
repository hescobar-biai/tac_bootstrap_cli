"""
TAC Bootstrap Domain Exceptions

Custom exception classes for domain validation and business logic errors.
"""


class TACConfigError(Exception):
    """
    Exception raised for TAC Bootstrap configuration domain errors.

    This exception is used for business logic validation errors that are
    specific to TAC Bootstrap, such as framework-language incompatibility
    or invalid configuration combinations.

    Pydantic ValidationError is used for schema validation, while this
    exception is used for domain-specific business rules.

    Example:
        raise TACConfigError(
            "FastAPI framework is only compatible with Python language"
        )
    """

    pass
