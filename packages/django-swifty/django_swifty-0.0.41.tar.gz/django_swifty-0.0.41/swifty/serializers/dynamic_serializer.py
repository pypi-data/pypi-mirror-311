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
            allowed_args = getattr(field, "static_args", ()) + getattr(
                field, "extra_args", ()
            )
            allowed_kwargs = {
                k: v for k, v in field.__dict__.items() if k in allowed_args
            }
            fields_config[field_name] = {
                "field_name": field_name,
                "type": field.__class__.__name__,
                **allowed_kwargs,
                **getattr(field, "extra_kwargs", {}),
            }

        return fields_config


def create_field_kwargs(field_info, field_type_map):
    """_summary_

    Args:
        field_info (_type_): _description_
        field_type_map (_type_): _description_

    Returns:
        _type_: _description_
    """
    field_base = field_type_map.get(field_info.get("type", "CharField"))
    is_swifty_field = issubclass(field_base, BasicFieldSerializer)
    if not is_swifty_field:
        return field_base, field_info

    allowed_args = field_base.static_args + field_base.extra_args
    allowed_kwargs = {}
    extra_kwargs = {}
    for k, v in field_info.items():
        if k in allowed_args:
            allowed_kwargs.update({k: v})
        else:
            extra_kwargs.update({k: v})

    return field_base, {"extra_kwargs": extra_kwargs, **allowed_kwargs}


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
        field_base, field_kwargs = create_field_kwargs(field_info, field_type_map)
        fields[field_info["field_name"]] = field_base(**field_kwargs)

    return type("DynamicSerializer", (base_class,), fields)
