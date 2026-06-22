class ScientistNotFound(Exception):
    """Raised when a scientist id does not mathch any known scientist."""

    def __init__(self, scientist_id: str):
        self.scientist_id=scientist_id
        super().__init__(f"Scientist with id: '{scientist_id}' not found.")