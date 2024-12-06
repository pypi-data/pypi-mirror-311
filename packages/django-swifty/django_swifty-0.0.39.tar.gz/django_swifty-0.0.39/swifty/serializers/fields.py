"""Constants"""

from typing import Dict, Tuple, Any
from datetime import date
from rest_framework import serializers


class BasicFieldSerializer:
    """
    _summary_

    Args:
        object (_type_): _description_
    """

    static_args = (
        "read_only",
        "write_only",
        "required",
        "default",
        "initial",
        "source",
        "label",
        "help_text",
        "style",
        "error_messages",
        "validators",
        "allow_null",
    )
    extra_args: Tuple[str, ...] = tuple()
    extra_kwargs: Dict[str, Any] = {}
    empty_value: Any = None
    data = None
    default_empty_html = None
    parent = None


class CharField(BasicFieldSerializer, serializers.CharField):
    """
    A serializer field for handling character (string) data.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
    )
    empty_value: Any = ""


class EmailField(BasicFieldSerializer, serializers.EmailField):
    """
    A serializer field for handling email addresses.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
    )
    empty_value: Any = ""


class URLField(BasicFieldSerializer, serializers.URLField):
    """
    A serializer field for handling URLs.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
    )
    empty_value: Any = ""


class UUIDField(BasicFieldSerializer, serializers.UUIDField):
    """
    A serializer field for handling UUIDs.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_blank",
        "trim_whitespace",
        "max_length",
        "min_length",
        "format",
        "hex_verbose",
    )
    empty_value: Any = ""


class IntegerField(BasicFieldSerializer, serializers.IntegerField):
    """
    A serializer field for handling integers.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("max_value", "min_value")
    empty_value: Any = 0


class FloatField(BasicFieldSerializer, serializers.FloatField):
    """
    A serializer field for handling floats.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("max_value", "min_value")
    empty_value: Any = 0.0


class DecimalField(BasicFieldSerializer, serializers.DecimalField):
    """
    A serializer field for handling decimals.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "max_digits",
        "decimal_places",
        "coerce_to_string",
        "max_value",
        "min_value",
        "normalize_output",
        "localize",
        "rounding",
    )
    empty_value: Any = 0.0


class BooleanField(BasicFieldSerializer, serializers.BooleanField):
    """
    A serializer field for handling booleans.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("allow_null",)
    empty_value: Any = False


class DateField(BasicFieldSerializer, serializers.DateField):
    """
    A serializer field for handling dates.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("format", "input_formats")

    def __init__(self, *args, **kwargs):
        input_formats = ["iso-8601", "%Y-%m-%dT%H:%M:%S.%fZ"]
        self.initial = self.initial if self.initial is not None else date.today()
        super().__init__(*args, input_formats=input_formats, **kwargs)


class DateTimeField(BasicFieldSerializer, serializers.DateTimeField):
    """
    A serializer field for handling date-times.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("format", "input_formats", "default_timezone")


class TimeField(BasicFieldSerializer, serializers.TimeField):
    """
    A serializer field for handling time values.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("format", "input_formats")


class DurationField(BasicFieldSerializer, serializers.DurationField):
    """
    A serializer field for handling duration values.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args = ("max_value", "min_value")


class ListField(BasicFieldSerializer, serializers.ListField):
    """
    A serializer field for handling lists.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("child", "allow_empty", "max_length", "min_length")
    empty_value: Any = []


class DictField(BasicFieldSerializer, serializers.DictField):
    """
    A serializer field for handling dictionaries.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("child", "allow_empty")
    empty_value: Any = {}


class ChoiceField(BasicFieldSerializer, serializers.ChoiceField):
    """
    A serializer field for handling choices.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "choices",
        "html_cutoff",
        "html_cutoff_text",
        "allow_blank",
    )

    def __init__(self, choices=None, **kwargs):
        choices = choices or ()
        super().__init__(choices=choices, **kwargs)


class MultipleChoiceField(BasicFieldSerializer, serializers.MultipleChoiceField):
    """
    A serializer field for handling ultiple choices.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args = (
        "choices",
        "html_cutoff",
        "html_cutoff_text",
        "allow_blank",
        "allow_empty",
    )
    empty_value = []

    def __init__(self, choices=None, **kwargs):
        choices = choices or ()
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return list(super().to_internal_value(data))


class SlugField(BasicFieldSerializer, serializers.SlugField):
    """
    A serializer field for handling slugs.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("allow_unicode",)
    empty_value: Any = ""


class FileField(BasicFieldSerializer, serializers.FileField):
    """
    A serializer field for handling file uploads.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("allow_empty_file", "use_url", "max_length")


class ImageField(BasicFieldSerializer, serializers.ImageField):
    """
    A serializer field for handling image uploads.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "allow_empty_file",
        "use_url",
        "max_length",
        "_DjangoImageField",
    )


class SerializerMethodField(BasicFieldSerializer, serializers.SerializerMethodField):
    """
    A serializer field for handling method-based fields.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("method_name", "source", "read_only")

    def to_internal_value(self, data):
        return data


class HyperlinkedIdentityField(
    BasicFieldSerializer, serializers.HyperlinkedIdentityField
):
    """
    A serializer field for handling hyperlinked identity.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "view_name",
        "lookup_field",
        "lookup_url_kwarg",
        "format",
        "read_only",
        "source",
    )


class HyperlinkedRelatedField(
    BasicFieldSerializer, serializers.HyperlinkedRelatedField
):
    """
    A serializer field for handling hyperlinked relations.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "view_name",
        "lookup_field",
        "lookup_url_kwarg",
        "format",
    )


class PrimaryKeyRelatedField(BasicFieldSerializer, serializers.PrimaryKeyRelatedField):
    """
    A serializer field for handling primary key relations.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "pk_field",
        "queryset",
        "many",
        "read_only",
        "html_cutoff",
        "html_cutoff_text",
    )


class RelatedField(BasicFieldSerializer, serializers.RelatedField):
    """
    A serializer field for handling related objects.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = (
        "queryset",
        "many",
        "read_only",
        "html_cutoff",
        "html_cutoff_text",
    )

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class JSONField(BasicFieldSerializer, serializers.JSONField):
    """
    A serializer field for handling JSON objects.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    extra_args: Tuple[str, ...] = ("binary", "encoder", "decoder")
    empty_value: Any = {}


class ReadOnlyField(BasicFieldSerializer, serializers.ReadOnlyField):
    """
    A serializer field for read-only data.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    def to_internal_value(self, data):
        return data


class HiddenField(BasicFieldSerializer, serializers.HiddenField):
    """
    A serializer field for hidden data.

    Attributes:
        extra_args (Tuple[str, ...]): Extra arguments for the field configuration.
        empty_value (Any): Default value for an empty field.
    """

    def to_representation(self, value):
        return value


FIELD_TYPE_MAP: Dict[str, BasicFieldSerializer] = {
    field_serializer.__name__: field_serializer
    for field_serializer in BasicFieldSerializer.__subclasses__()
}
