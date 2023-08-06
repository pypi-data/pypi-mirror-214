import uuid


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Parameters:
    * uuid_to_test: str - The string to test as a UUID.
    * version: int - UUID version (default is 4).

    Returns:
    * `True` if uuid_to_test is a valid UUID; otherwise `False`.
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
