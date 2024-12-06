"""Module for dynamic serializers using Django REST Framework."""

from copy import deepcopy
from typing import List, Dict, Any, Type
from rest_framework import serializers
from .fields import FIELD_TYPE_MAP, BasicFieldSerializer


class DynamicSerializer(serializers.Serializer):
    """Base class for dynamic serializers."""

    def create(self, *args, **kwargs) -> Any:
        """Create an instance based on validated data."""

    def update(self, *args, **kwargs) -> Any:
        """Update an instance based on validated data."""

    def get_fields_config(self) -> Dict[str, Any]:
        """Return the fields configuration as a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the fields configuration.
        """
        fields_config = {}
        for field_name, field in self.fields.items():
            field_info = {
                "name": field_name,
                "type": field.__class__.__name__,
                "required": getattr(field, "required", None),
                "default": getattr(field, "default", None),
                "validators": [
                    validator.__class__.__name__ for validator in field.validators
                ],
            }
            # Include additional attributes dynamically
            for attr in dir(field):
                if not attr.startswith("_") and attr not in field_info:
                    field_info[attr] = getattr(field, attr)

            fields_config[field_name] = field_info

        return fields_config


def create_dynamic_serializer(
    fields_config: List[Dict[str, Any]],
    base_class: Type[DynamicSerializer] = DynamicSerializer,
    field_type_map: Dict[str, BasicFieldSerializer] = deepcopy(FIELD_TYPE_MAP),
) -> Type[DynamicSerializer]:
    """Create a dynamic serializer class based on field configuration.

    Args:
        field_config (List[Dict[str, Any]]): A list of dictionaries defining the fields.

    Returns:
        Type[DynamicSerializer]: A dynamically created serializer class.
    """
    fields: Dict[str, serializers.Field] = {}

    for field_info in fields_config:
        field_base = field_type_map.get(field_info.get("type", "CharField"))
        allowed_kwargs = {
            k: v
            for k, v in field_info.items()
            if k in field_base.static_args + field_base.extra_args
        }
        field = field_base(**allowed_kwargs)
        field.extra_kwargs = field_info.get("extra_kwargs", {})
        fields[field_info["field_name"]] = field

    return type("DynamicSerializer", (base_class,), fields)
