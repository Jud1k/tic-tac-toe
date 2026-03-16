from typing import Any


def generate_updated_fields(update_data: dict[str, Any]) -> list[str]:
    fields = [f"{key} = ${i + 1}" for i, key in enumerate(update_data)]
    return fields
