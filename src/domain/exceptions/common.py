class EntityAlreadyExists(Exception):
    entity_name: str

    def __init__(self, unique_columns: dict[str, str]) -> None:
        self.unique_columns = ", ".join(
            [f"{key}={value}" for key, value in unique_columns.items()]
        )

    def __str__(self):
        return f"Entity {self.entity_name} already exists. {self.unique_columns}"


class DatabaseException(Exception):
    pass


class EntityNotFound(Exception):
    entity_name: str

    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id

    def __str__(self):
        return f"{self.entity_name} with id={self.entity_id} not found"


class InvalidEntityReference(Exception):
    """Raised when an entity references doesn't exist"""

    entity_name: str

    def __init__(self, reference_type: str, reference_id: str) -> None:
        self.reference_type = reference_type
        self.reference_id = reference_id

    def __str__(self):
        return f"Invalid {self.entity_name} reference: {self.reference_type} with id={self.reference_id} does not exist"
